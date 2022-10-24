from typing import Any, Dict, List

from pydantic import BaseModel, Extra


class HTTPErrorResponse(BaseModel, extra=Extra.allow):
    detail: Any


def generate_responses(*status_codes: List[int]) -> Dict[str, Any]:
    return {status_code: {'model': HTTPErrorResponse} for status_code in status_codes}
