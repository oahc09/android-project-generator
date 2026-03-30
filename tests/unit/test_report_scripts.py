#!/usr/bin/env python3
"""
报告与测试入口脚本回归测试
"""

import sys
import subprocess
from pathlib import Path

scripts_path = Path(__file__).parent.parent.parent / "scripts"
tests_path = Path(__file__).parent.parent
sys.path.insert(0, str(scripts_path))
sys.path.insert(0, str(tests_path))

from generate_report import parse_test_output, save_summary_report, REPORT_HTML_PATH, CACHE_ROOT
from run_tests import format_command_message, format_display_path
from report_generator import parse_summary_report

PROJECT_ROOT = Path(__file__).parent.parent.parent


class TestGenerateReportParsing:
    """generate_report.py 行为测试"""

    def test_parse_test_output_handles_windows_paths(self):
        output = """
tests\\unit\\test_detect_env.py::TestRunCommand::test_run_command_success PASSED [ 10%]
tests\\unit\\test_detect_env.py::TestRunCommand::test_run_command_timeout FAILED [ 20%]
tests\\integration\\test_project_structure.py::test_structure SKIPPED [ 30%]
======================== 1 failed, 1 passed, 1 skipped in 0.12s ========================
"""
        result = parse_test_output(output)

        assert result["total"] == 3
        assert result["passed"] == 1
        assert result["failed"] == 1
        assert result["skipped"] == 1
        assert len(result["suite_details"]) == 2
        assert any(item["file"] == "tests\\unit\\test_detect_env.py" for item in result["suite_details"])

    def test_save_and_parse_summary_report(self, temp_dir):
        stats = {
            "passed": 3,
            "failed": 1,
            "skipped": 0,
            "total": 4,
            "pass_rate": 75.0,
            "suite_details": [
                {
                    "name": "Detect Env",
                    "file": "tests\\unit\\test_detect_env.py",
                    "passed": 3,
                    "failed": 1,
                    "skipped": 0,
                    "total": 4,
                    "pass_rate": 75.0,
                    "tests": [
                        {"name": "test_one", "status": "passed"},
                        {"name": "test_two", "status": "failed"},
                    ],
                }
            ],
        }

        summary_path = temp_dir / "summary.json"
        save_summary_report(stats, summary_path)
        generator = parse_summary_report(str(summary_path))

        calculated = generator.calculate_stats()
        assert calculated["total"] == 4
        assert calculated["passed"] == 3
        assert calculated["failed"] == 1

    def test_parsed_summary_can_render_html(self, temp_dir):
        stats = {
            "passed": 1,
            "failed": 1,
            "skipped": 0,
            "total": 2,
            "pass_rate": 50.0,
            "suite_details": [
                {
                    "name": "Detect Env",
                    "file": "tests\\unit\\test_detect_env.py",
                    "passed": 1,
                    "failed": 1,
                    "skipped": 0,
                    "total": 2,
                    "pass_rate": 50.0,
                    "tests": [{"name": "test_one", "status": "passed"}],
                }
            ],
        }

        summary_path = temp_dir / "summary.json"
        output_path = temp_dir / "report.html"
        save_summary_report(stats, summary_path)
        generator = parse_summary_report(str(summary_path))
        generator.output_path = output_path
        generator.save()

        assert output_path.exists()
        html = output_path.read_text(encoding="utf-8")
        assert '<html lang="en">' in html
        assert "Test Report" in html
        assert "https://esm.run/@material/web" in html
        assert 'class="lang-btn active"' in html
        assert 'id="lang-en"' in html
        assert 'id="lang-zh"' in html
        assert 'addEventListener("click"' in html
        assert "const translations =" in html
        assert ".lang-btn:hover" in html
        assert ".lang-btn.active" in html
        assert "<md-elevated-card" in html
        assert "<md-divider" in html

    def test_report_output_path_is_under_reports_root(self):
        assert REPORT_HTML_PATH.name == "test-report.html"
        assert REPORT_HTML_PATH.parent.name == "reports"

    def test_cache_root_is_unified_under_cache_directory(self):
        assert CACHE_ROOT.name == "cache"


class TestRunTestsFormatting:
    """run_tests.py 行为测试"""

    def test_format_command_message_is_console_safe_ascii(self):
        message = format_command_message(["python", "-m", "pytest", "tests"])

        assert message == "[CMD] Running: python -m pytest tests"
        assert all(ord(ch) < 128 for ch in message)

    def test_format_display_path_returns_relative_path(self):
        relative = format_display_path(Path("D:/AI/Github/android-project-generator/reports/test-report.html"))
        assert relative == "reports/test-report.html"

    def test_running_report_only_does_not_create_scripts_pycache(self):
        scripts_pycache = PROJECT_ROOT / "scripts" / "__pycache__"
        if scripts_pycache.exists():
            import shutil
            shutil.rmtree(scripts_pycache, ignore_errors=True)

        summary_path = PROJECT_ROOT / "reports" / "test-results.json"
        save_summary_report(
            {
                "passed": 1,
                "failed": 0,
                "skipped": 0,
                "total": 1,
                "pass_rate": 100.0,
                "suite_details": [],
            },
            summary_path,
        )

        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "scripts" / "run_tests.py"), "--report-only"],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, result.stderr
        assert not scripts_pycache.exists()
