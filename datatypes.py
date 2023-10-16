from dataclasses import dataclass


@dataclass
class SessionData:
    session_username: str
    api_hash: str
    api_id: int


class SubStatus:
    ACTUAL = 2
    EXPIRED = -2
    EXPIRED_SOON = -1
