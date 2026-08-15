from vfdelivery.security.password import create_hash, verify


def test_create_hash():
    password = 'secret'
    hash = create_hash(password)

    assert password != hash


def test_verify():
    password = 'secret'
    hash = create_hash(password)

    assert verify(password, hash)
