from trame_flow.widgets.flow.common import HtmlElement

__all__ = [
    "NodeResizer",
]


class NodeResizer(HtmlElement):
    """NodeResizer for `CustomNode`."""

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__("NodeResizer", **kwargs)

        self._attr_names += [
            ("node_id", "nodeId"),
            "color",
            ("handle_class_name", "handleClassName"),
            ("handle_style", "handleStyle"),
            ("line_class_name", "lineClassName"),
            ("line_style", "lineStyle"),
            ("is_visible", "isVisible"),
            ("min_width", "minWidth"),
            ("min_height", "minHeight"),
        ]

        self._event_names += [
            ("resize_start", "resizeStart"),
            "resize",
            ("resize_end", "resizeEnd"),
        ]
