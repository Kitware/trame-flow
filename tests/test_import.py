def test_import():
    # For components only, the CustomWidget is also importable via trame
    from trame.widgets.trame_flow import NodeEditor

    from trame_flow.widgets.flow import NodeEditor  # noqa: F401,F811
