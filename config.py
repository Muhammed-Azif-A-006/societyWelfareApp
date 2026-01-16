"""Application configuration defaults."""

from __future__ import annotations

import os
from pathlib import Path

DEFAULT_DB_NAME = "society_welfare.db"

DB_FILE = os.getenv("WELFARE_DB_FILE", DEFAULT_DB_NAME)
SOCIETY_NAME = os.getenv("SOCIETY_NAME", "Society Welfare Fund")
SOCIETY_VPA = os.getenv("SOCIETY_VPA", "society@upi")

DB_PATH = Path(DB_FILE)
