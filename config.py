from dataclasses import dataclass


@dataclass
class SessionData:
    session_username: str
    api_hash: str
    api_id: int
