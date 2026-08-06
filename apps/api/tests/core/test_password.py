from vfdelivery.core.password import SecurePassword


def test_hash():
    password: str = 'plain_password'
    hashed: str = SecurePassword.hash(password=password)

    assert password != hashed


def test_verify():
    password: str = 'plain_password'
    hashed: str = SecurePassword.hash(password=password)

    assert SecurePassword.verify(plain=password, hash=hashed)
