from dataclasses import dataclass
from pathlib import Path

@dataclass
class Config:
    stationAltitude: int
    deviceTimeout: int
    deviceConnectionRetryDelay: int
    uploadFrequency: int
    uploadLocalPort: int
    logDir: Path
    outputDir: Path
    logBackupCount: int