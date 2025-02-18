from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(non_hashed_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(secret=non_hashed_password, hash=hashed_password)

