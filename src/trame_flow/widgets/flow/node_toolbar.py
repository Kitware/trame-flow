from trame_flow.widgets.flow.common import HtmlElement

__all__ = [
    "NodeToolbar",
]


class NodeToolbar(HtmlElement):
    """NodeToolbar for `NodeEditor`."""

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__("NodeToolbar", **kwargs)

        self._attr_names += [
            ("node_id", "nodeId"),
            ("is_visible", "isVisible"),
            "position",
            "offset",
        ]
