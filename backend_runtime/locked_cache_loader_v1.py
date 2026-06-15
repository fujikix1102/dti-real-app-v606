import hashlib
import json
from pathlib import Path
from typing import Any, Dict

from contract_constants_v1 import CACHE_PAYLOAD_SHA256

class CacheIntegrityError(RuntimeError):
    pass

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load_locked_cache(cache_path: str | Path) -> Dict[str, Any]:
    path = Path(cache_path)
    if not path.exists():
        raise CacheIntegrityError(f"cache file missing: {path}")
    actual = sha256_file(path)
    if actual != CACHE_PAYLOAD_SHA256:
        raise CacheIntegrityError(f"cache sha mismatch: {actual}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload
