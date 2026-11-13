from dataclasses import dataclass
from typing import Any 
@dataclass(frozen=True)
class ReadingInfo:
    real_read_data: dict[str, Any]
    read_data: dict[str, bool]
    errors: dict[str, dict[str]]