def test_import_strategies():
    import strategies
    assert hasattr(strategies, "rsi")
