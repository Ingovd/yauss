def test_consume(yauss_key):
    key = yauss_key.keys.consume()
    assert len(key) == 8
    assert yauss_key.keys.consume(key) is None
    # Has a 1 in 2^48 chance of failing
    assert yauss_key.keys.consume('abcdefgh') is 'abcdefgh' 


def test_approve(yauss_key):
    key = yauss_key.keys.consume()
    approved = yauss_key.keys._approve_key(key)
    assert not approved