def test_import():
    from trame_flow.widgets.flow import CustomWidget  # noqa: F401

    # For components only, the CustomWidget is also importable via trame
    from trame.widgets.trame_flow import CustomWidget  # noqa: F401,F811
