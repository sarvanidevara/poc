from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Convert Plain password to Hashed Password
def hash(password: str):
    return pwd_context.hash(password)

# Verify Plain password Match Hashed Password
def verify(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)