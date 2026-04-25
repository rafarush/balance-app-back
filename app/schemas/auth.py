from pydantic import BaseModel

from app.core.config import get_settings

settings = get_settings()


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    access_token_life: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    refresh_token_life: int = settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60


class TokenPayload(BaseModel):
    sub: str
    role: str
    exp: int
