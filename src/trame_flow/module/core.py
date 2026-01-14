from typing import Literal, Optional, Union

from typing_extensions import NotRequired, TypedDict

__all__ = [
    "DEFAULT_EXTENT",
    "Dimensions",
    "Edge",
    "EdgeMarkerType",
    "EdgeType",
    "Extent",
    "Graph",
    "HandlePosition",
    "Node",
    "NodeType",
    "Position",
    "create_edge",
    "create_node",
]


class Position(TypedDict):
    x: float
    y: float


HandlePosition = Literal["top", "bottom", "left", "right"]


class Dimensions(TypedDict):
    height: float
    width: float


# "parent" or [[x-from, y-from], [x-to, y-to]]
Extent = Union[Literal["parent"], list[list[float]]]
DEFAULT_EXTENT = [[float("-inf"), float("-inf")], [float("+inf"), float("+inf")]]

NodeType = Literal["default", "input", "output"] | str


Node = TypedDict(
    "Node",
    {
        "ariaLabel": NotRequired[str],
        "class": NotRequired[str],
        "connectable": NotRequired[bool],
        "data": NotRequired[dict],
        "deletable": NotRequired[bool],
        "draggable": NotRequired[bool],
        "expandParent": NotRequired[bool],
        "extent": NotRequired[Extent],
        "focusable": NotRequired[bool],
        "height": Union[int, str],
        "hidden": NotRequired[bool],
        "id": str,
        "parentNode": NotRequired[str],
        "position": Position,
        "selectable": NotRequired[bool],
        "sourcePosition": NotRequired[HandlePosition],
        "style": NotRequired[dict],
        "targetPosition": NotRequired[HandlePosition],
        "type": NodeType,
        "width": Union[int, str],
        "zIndex": NotRequired[int],
    },
)


def create_node(
    id: str,
    type: NodeType,
    x: float,
    y: float,
    label: str,
    parent_id: Optional[str] = None,
    expand_parent: bool = False,
    extent: Optional[Extent] = None,
    width: Union[int, str] = "auto",
    height: Union[int, str] = "auto",
    style: Optional[dict] = None,
    data: Optional[dict] = None,
) -> Node:
    """Helper function to build a Node."""
    node = Node(
        id=id,
        type=type,
        data={"label": label},
        position=Position(x=x, y=y),
        expandParent=expand_parent,
        width=width,
        height=height,
    )
    if extent:
        node["extent"] = extent
    if extent == "parent" and parent_id is None:
        parent_id = ""
    if parent_id:
        node["parentNode"] = parent_id
    if style:
        node["style"] = style
    if data:
        node["data"] = node["data"] | data
    # set default node style for custom node
    if type not in ["default", "input", "output"]:
        node["class"] = "vue-flow__node-default"
    return node


EdgeType = Literal["default", "step", "smoothstep", "straight"]

EdgeMarkerType = Literal["arrow", "arrowclosed"]


class EdgeMarker(TypedDict):
    color: NotRequired[str]
    height: NotRequired[float]
    id: NotRequired[str]
    markerUnits: NotRequired[str]
    orient: NotRequired[str]
    strokeWidth: NotRequired[float]
    type: EdgeMarkerType
    width: NotRequired[float]


Edge = TypedDict(
    "Edge",
    {
        "animated": NotRequired[bool],
        "ariaLabel": NotRequired[str],
        "class": NotRequired[str],
        "data": NotRequired[dict],
        "deletable": NotRequired[bool],
        "focusable": NotRequired[bool],
        "hidden": NotRequired[bool],
        "id": str,
        "interactionWidth": NotRequired[float],
        "label": NotRequired[str],
        "labelBgBorderRadius": NotRequired[float],
        "labelBgPadding": NotRequired[tuple[float, float]],
        "labelBgStyle": NotRequired[dict],
        "labelShowBg": NotRequired[bool],
        "labelStyle": NotRequired[dict],
        "markerEnd": NotRequired[Union[EdgeMarkerType, EdgeMarker]],
        "markerStart": NotRequired[Union[EdgeMarkerType, EdgeMarker]],
        "selectable": NotRequired[bool],
        "source": str,
        "style": NotRequired[dict],
        "target": str,
        "type": EdgeType,
        "zIndex": NotRequired[int],
    },
)


def create_edge(
    source_id: str,
    target_id: str,
    type: EdgeType = "default",
    label: Optional[str] = None,
    animated: bool = False,
    marker_start: Optional[Union[EdgeMarkerType, EdgeMarker]] = None,
    marker_end: Optional[Union[EdgeMarkerType, EdgeMarker]] = None,
    style: Optional[dict] = None,
):
    """Helper function to build an edge."""
    edge = Edge(
        id=f"{source_id}->{target_id}",
        source=source_id,
        target=target_id,
        type=type,
        animated=animated,
    )
    if label:
        edge["label"] = label
    if marker_start:
        edge["markerStart"] = marker_start
    if marker_end:
        edge["markerEnd"] = marker_end
    if style:
        edge["style"] = style
    return edge


class Graph(TypedDict):
    nodes: list[Node]
    edges: list[Edge]
