def test_import():
    from trame.widgets.flow import (
        Background,
        Controls,
        ControlsButton,
        CustomNode,
        Handle,
        MiniMap,
        MiniMapNode,
        NodeEditor,
        NodeResizer,
        NodeToolbar,
    )
    from trame_flow.widgets.flow import (  # noqa: F401,F811
        Background,
        Controls,
        ControlsButton,
        CustomNode,
        Handle,
        MiniMap,
        MiniMapNode,
        NodeEditor,
        NodeResizer,
        NodeToolbar,
    )
