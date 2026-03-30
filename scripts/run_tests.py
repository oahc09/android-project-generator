#!/usr/bin/env python3
"""
测试运行脚本

运行测试并生成 HTML 报告
"""

import subprocess
import sys
import webbrowser
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SUMMARY_REPORT_PATH = PROJECT_ROOT / "reports" / "test-results.json"
REPORT_HTML_PATH = PROJECT_ROOT / "reports" / "test-report.html"


def format_command_message(cmd) -> str:
    """返回控制台安全的命令提示文本。"""
    return f"[CMD] Running: {' '.join(cmd)}"


def format_display_path(path: Path) -> str:
    """尽量输出相对于项目根目录的路径，避免控制台显示绝对路径。"""
    try:
        return str(Path(path).resolve().relative_to(PROJECT_ROOT)).replace("\\", "/")
    except Exception:
        return str(path).replace("\\", "/")


def run_tests():
    """运行测试"""
    from generate_report import run_tests_and_generate_report

    print("=" * 60)
    print("[TEST] Android Project Generator - Test Runner")
    print("=" * 60)
    print()

    cmd = [
        sys.executable, "-m", "pytest",
        "tests",
        "-v",
        "--tb=short",
        "--cov=scripts",
        "--cov-report=term-missing",
        "--cov-report=html:reports/htmlcov",
        "-p", "tests.conftest"
    ]
    print(format_command_message(cmd))
    print()

    result = run_tests_and_generate_report(
        "tests",
        extra_args=[
            "--cov=scripts",
            "--cov-report=term-missing",
            "--cov-report=html:reports/htmlcov",
            "-p", "tests.conftest",
        ],
    )

    report_path = REPORT_HTML_PATH
    
    if report_path.exists():
        print()
        print("=" * 60)
        print(f"[OK] Test report generated: {format_display_path(report_path)}")
        print("=" * 60)
        
        # 询问是否打开报告
        response = input("\n是否打开 HTML 报告？(y/n): ").strip().lower()
        if response == 'y':
            webbrowser.open(f'file:///{report_path.absolute()}')
    else:
        print()
        print("[WARN] Test report was not generated")
    
    return result.returncode


def run_unit_tests():
    """只运行单元测试"""
    print("=" * 60)
    print("[TEST] Run unit tests")
    print("=" * 60)
    
    tests_dir = PROJECT_ROOT / "tests" / "unit"
    
    cmd = [
        sys.executable, "-m", "pytest",
        str(tests_dir),
        "-v",
        "--tb=short",
        "-p", "tests.conftest"
    ]
    
    return subprocess.run(cmd, cwd=PROJECT_ROOT).returncode


def run_integration_tests():
    """只运行集成测试"""
    print("=" * 60)
    print("[TEST] Run integration tests")
    print("=" * 60)
    
    tests_dir = PROJECT_ROOT / "tests" / "integration"
    
    cmd = [
        sys.executable, "-m", "pytest",
        str(tests_dir),
        "-v",
        "--tb=short",
        "-p", "tests.conftest"
    ]
    
    return subprocess.run(cmd, cwd=PROJECT_ROOT).returncode


def generate_report_only():
    """只生成报告（从现有 JSON）"""
    tests_path = PROJECT_ROOT / "tests"
    if str(tests_path) not in sys.path:
        sys.path.insert(0, str(tests_path))

    from report_generator import parse_summary_report

    if not SUMMARY_REPORT_PATH.exists():
        print(f"[ERROR] Missing summary report: {format_display_path(SUMMARY_REPORT_PATH)}")
        print("Run tests first to generate the summary report.")
        return 1

    generator = parse_summary_report(str(SUMMARY_REPORT_PATH))
    generator.output_path = REPORT_HTML_PATH
    generator.save()

    return 0


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="测试运行器")
    parser.add_argument(
        "--unit",
        action="store_true",
        help="只运行单元测试"
    )
    parser.add_argument(
        "--integration",
        action="store_true",
        help="只运行集成测试"
    )
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="只生成报告（从现有 JSON）"
    )
    
    args = parser.parse_args()
    
    if args.unit:
        sys.exit(run_unit_tests())
    elif args.integration:
        sys.exit(run_integration_tests())
    elif args.report_only:
        sys.exit(generate_report_only())
    else:
        sys.exit(run_tests())
