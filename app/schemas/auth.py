from pydantic import BaseModel

from app.core.config import get_settings

settings = get_settings()


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60


class TokenPayload(BaseModel):
    sub: str
    role: str
    exp: int
