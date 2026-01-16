import json
from datetime import datetime, timedelta
from typing import Any, Dict

from models.scrape_task import ScrapeRequest
from models.flight import FlightRoute, Flight

def datetime_to_json(d: datetime) -> str:
    return d.isoformat()

def json_to_datetime(s: str) -> datetime:
    return datetime.fromisoformat(s)

def _encode_value(value: Any):
    """Make values JSON-serializable (handle datetime recursively)."""
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, list):
        return [_encode_value(v) for v in value]
    if isinstance(value, dict):
        return {k: _encode_value(v) for k, v in value.items()}
    return value


def _decode_value(value: Any):
    """Restore values (convert ISO strings back to datetime if possible)."""
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return value
    if isinstance(value, list):
        return [_decode_value(v) for v in value]
    if isinstance(value, dict):
        return {k: _decode_value(v) for k, v in value.items()}
    return value

def scrape_request_to_json(req: ScrapeRequest) -> Dict:
    return req.model_dump(mode="json")

def scrape_request_from_json(data: Dict) -> ScrapeRequest:
    return ScrapeRequest.model_validate(data)
