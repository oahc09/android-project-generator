# android-project-generator
When generating an Android project from scratch, it can be compiled successfully in one go.

## Python Environment

- Python 3.10+ recommended
- Install test dependencies before running scripts that call pytest:

```bash
python -m pip install -r tests/requirements.txt
```

## Directory Layout

```text
android-project-generator/
├── SKILL.md                    # skill entrypoint
├── README.md
├── LICENSE
├── docs/                       # one human-facing guide: reporting
├── cache/                      # python / pytest / coverage caches
├── references/                 # version matrix and config templates
├── scripts/                    # executable helpers
│   ├── run_tests.py            # test runner entrypoint
│   └── generate_report.py      # report generator
├── tests/                      # unit / integration / e2e tests
└── reports/                    # generated reports (ignored)
```

## Features

- AGP / Gradle / JDK / Kotlin compatibility profiles
- Local environment detection
- Complete Android project templates
- Real Gradle Wrapper validation
- `assembleDebug` build verification
- APK output confirmation
- JNI / NDK / CMake native project setup
- Build-state reporting: scaffolding_only, build_failed, compiled, runnable

## Roadmap

- Expand Android template coverage
- Add Compose template support
- Add CI matrix for AGP / Gradle / JDK combinations
- Add more JNI / NDK / CMake examples
- Improve China mirror support
- Add GitHub Action for generated project verification
