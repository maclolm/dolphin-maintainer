from dataclasses import dataclass


@dataclass
class Config:
    session_username: str
    token: str
    api_hash: str
    api_id: int
    db_file: str
