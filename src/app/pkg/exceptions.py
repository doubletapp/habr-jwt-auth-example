from dataclasses import dataclass


@dataclass
class JsonHTTPException(Exception):
    content: dict
    status_code: int = 400
