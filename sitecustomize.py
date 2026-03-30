#!/usr/bin/env python3
"""
Repository-wide Python startup customization.

Ensures Python bytecode caches are redirected into the repo cache directory
before normal module imports occur.
"""

import os
import sys
import tempfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
CACHE_ROOT = PROJECT_ROOT / "cache"
PYCACHE_ROOT = CACHE_ROOT / "pycache"
TMP_ROOT = CACHE_ROOT / "tmp" / "python"

CACHE_ROOT.mkdir(parents=True, exist_ok=True)
PYCACHE_ROOT.mkdir(parents=True, exist_ok=True)
TMP_ROOT.mkdir(parents=True, exist_ok=True)

sys.pycache_prefix = str(PYCACHE_ROOT)
os.environ["PYTHONPYCACHEPREFIX"] = str(PYCACHE_ROOT)
tempfile.tempdir = str(TMP_ROOT)
