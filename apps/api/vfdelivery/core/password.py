from pwdlib import PasswordHash

passwordHash = PasswordHash.recommended()


class SecurePassword:
    @staticmethod
    def hash(*, password: str) -> str:
        return passwordHash.hash(password)

    @staticmethod
    def verify(*, plain: str, hash: str) -> bool:
        return passwordHash.verify(plain, hash)
