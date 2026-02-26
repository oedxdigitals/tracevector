from dataclasses import dataclass, asdict
from typing import List, Dict, Any


@dataclass
class ScanResult:
    target: str
    type: str
    metadata: Dict[str, Any]
    risk_flags: List[str]
    confidence: float

    def to_dict(self):
        return asdict(self)
