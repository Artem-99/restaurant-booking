from datetime import datetime, timedelta
from jose import jwt, JWTError
from ninja.security import HttpBearer
from django.conf import settings


def create_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


class AuthBearer(HttpBearer):
    def authenticate(self, request, token: str):
        from restaurant.models import User
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
            return User.objects.get(id=int(payload["sub"]))
        except (JWTError, Exception):
            return None


auth = AuthBearer()
