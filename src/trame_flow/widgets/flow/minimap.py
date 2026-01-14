from trame_flow.module.core import Dimensions, Position
from trame_flow.widgets.flow.common import HtmlElement

__all__ = [
    "MiniMap",
    "MiniMapNode",
]


class MiniMap(HtmlElement):
    """MiniMap for `NodeEditor`."""

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__("MiniMap", **kwargs)

        self._attr_names += [
            ("node_color", "nodeColor"),
            ("node_stroke_color", "nodeStrokeColor"),
            ("node_class_name", "nodeClassName"),
            ("node_border_radius", "nodeBorderRadius"),
            ("node_stroke_width", "nodeStrokeWidth"),
            ("mask_color", "maskColor"),
            "pannable",
            "zoomable",
        ]


class MiniMapNode(HtmlElement):
    """MiniMapNode for `MiniMap`."""

    def __init__(
        self,
        id: str,
        position: Position,
        dimensions: Dimensions,
        **kwargs,
    ):
        super().__init__(
            "MiniMapNode",
            id=id,
            position=position,
            dimensions=dimensions,
            **kwargs,
        )

        self._attr_names += [
            "id",
            ("parent_node", "parentNode"),
            "selected",
            "dragging",
            "position",
            "dimensions",
            ("border_radius", "borderRadius"),
            "color",
            ("shape_rendering", "shapeRendering"),
            ("stroke_color", "strokeColor"),
            ("stroke_width", "strokeWidth"),
        ]
