def test_deliberately_broken():
    expected = 2
    actual = 1
    assert actual == expected, "Deliberate failure to verify CI blocks merging"
