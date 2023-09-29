from calendar import timegm
from datetime import datetime
from hashlib import sha256


def convert_to_timestamp(datetime: datetime) -> int:
    return timegm(datetime.utctimetuple())


def get_sha256_hash(line: str) -> str:
    return sha256(str.encode(line)).hexdigest()
