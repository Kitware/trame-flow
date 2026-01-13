from ast import literal_eval
from typing import Callable, Literal, Optional, Union

from trame_client.widgets.core import AbstractElement, Template
from typing_extensions import NotRequired, TypedDict

from .. import module


class HtmlElement(AbstractElement):
    def __init__(self, _elem_name, children=None, **kwargs):
        super().__init__(_elem_name, children, **kwargs)
        if self.server:
            self.server.enable_module(module)


__all__ = [
    "DEFAULT_EXTENT",
    "CustomNode",
    "Dimensions",
    "Edge",
    "EdgeMarkerType",
    "EdgeType",
    "Extent",
    "Graph",
    "HandlePosition",
    "Node",
    "NodeEditor",
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


class CustomNode(Template):
    def __init__(self, type: str, var_name: str = "props", **kwargs):
        """Shortcut to define a custom node's HTML.
        This is equivalent to `Template(raw_attrs=["v-slot:node-myType=myProps"])`

        :param type: Name of the custom node type.
        :type type: str
        :param var_name: Name of the node properties variable. (Default = "props")
        :type var_name:  str
        """
        super().__init__(raw_attrs=[f"v-slot:node-{type}={var_name}"], **kwargs)


class NodeEditor(HtmlElement):
    """
    Node Editor based on VueFlow.

    Args:
        background_pattern_color (html color string):
            Color of the pattern in the background.
        background_pattern_gap (number):
            Size of the gaps for the pattern in the background.
        background_pattern_size (number):
            Size of the pattern in the background.
        background_pattern_variant ("dots" or "lines"):
            Pattern type in the background.
        show_controls (boolean):
            Show the controls panel (zoom in, zoom out, fit view, lock graph).
            Enabled by default.
        show_mini_map (boolean):
            Show the nodes mini map.
            Enabled by default.
    """

    _next_id = 0

    def __init__(self, **kwargs):
        super().__init__(
            "node-editor",
            **kwargs,
        )

        self._attr_names += [
            ("background_pattern_color", "backgroundPatternColor"),
            ("background_pattern_gap", "backgroundPatternGap"),
            ("background_pattern_size", "backgroundPatternSize"),
            ("background_pattern_variant", "backgroundPatternVariant"),
            ("show_controls", "showControls"),
            ("show_mini_map", "showMiniMap"),
        ]
        self._event_names += [
            ("click_connect_end", "clickConnectEnd"),
            ("click_connect_start", "clickConnectStart"),
            "connect",
            ("connect_end", "connectEnd"),
            ("connect_start", "connectStart"),
            ("edge_click", "edgeClick"),
            ("edge_context_menu", "edgeContextMenu"),
            ("edge_double_click", "edgeDoubleClick"),
            ("edge_mouse_enter", "edgeMouseEnter"),
            ("edge_mouse_leave", "edgeMouseLeave"),
            ("edge_mouse_move", "edgeMouseMove"),
            ("edges_change", "edgesChange"),
            ("edge_update", "edgeUpdate"),
            ("edge_update_end", "edgeUpdateEnd"),
            ("edge_update_start", "edgeUpdateStart"),
            "error",
            "init",
            ("mini_map_node_click", "miniMapNodeClick"),
            ("mini_map_node_double_click", "miniMapNodeDoubleClick"),
            ("mini_map_node_mouse_enter", "miniMapNodeMouseEnter"),
            ("mini_map_node_mouse_leave", "miniMapNodeMouseLeave"),
            ("mini_map_node_mouse_move", "miniMapNodeMouseMove"),
            "move",
            ("move_end", "moveEnd"),
            ("move_start", "moveStart"),
            ("node_click", "nodeClick"),
            ("node_context_menu", "nodeContextMenu"),
            ("node_double_click", "nodeDoubleClick"),
            ("node_drag", "nodeDrag"),
            ("node_drag_start", "nodeDragStart"),
            ("node_drag_stop", "nodeDragStop"),
            ("node_mouse_enter", "nodeMouseEnter"),
            ("node_mouse_leave", "nodeMouseLeave"),
            ("node_mouse_move", "nodeMouseMove"),
            ("nodes_change", "nodesChange"),
            ("nodes_initialized", "nodesInitialized"),
            ("pane_click", "paneClick"),
            ("pane_context_menu", "paneContextMenu"),
            ("pane_mouse_enter", "paneMouseEnter"),
            ("pane_mouse_leave", "paneMouseLeave"),
            ("pane_mouse_move", "paneMouseMove"),
            ("pane_scroll", "paneScroll"),
            ("selection_context_menu", "selectionContextMenu"),
            ("selection_drag", "selectionDrag"),
            ("selection_drag_start", "selectionDragStart"),
            ("selection_drag_stop", "selectionDragStop"),
            ("selection_end", "selectionEnd"),
            ("selection_start", "selectionStart"),
            ("update_node_internals", "updateNodeInternals"),
            ("viewport_change", "viewportChange"),
            ("viewport_change_end", "viewportChangeEnd"),
            ("viewport_change_start", "viewportChangeStart"),
        ]

        self._nodes: list[Node] = []
        self._edges: list[Edge] = []

        self.__ref = kwargs.get("ref")
        if self.__ref is None:
            NodeEditor._next_id += 1
            self.__ref = f"_node_editor_{NodeEditor._next_id}"
        self._attributes["ref"] = f'ref="{self.__ref}"'

        self.nodes_change = (lambda events: self.on_nodes_change(events), "[$event]")
        self.edges_change = (lambda events: self.on_edges_change(events), "[$event]")
        self.node_drag_stop = (lambda event: self.on_node_drag_stop(event), "[$event]")
        self.init = lambda: self._sync()

        self.connect = (lambda event: self.on_connect(event), "[$event]")

        self.graph_change: Callable[[list[Node], list[Edge]], None] = lambda *_: None

    def on_connect(self, event):
        if not self.get_edge(source=event["source"], target=event["target"]):
            self.add_edge(
                Edge(
                    source=event["source"],
                    target=event["target"],
                    id=f"{event['source']}->{event['target']}",
                    type="default",
                    animated=False,
                )
            )

    def on_nodes_change(self, events):
        need_sync = False
        for event in events:
            if event["type"] == "remove":
                node = self.get_node(event["id"])
                if node:
                    self._nodes.remove(node)
                    need_sync = True
        if need_sync:
            self._sync()

    def on_edges_change(self, events):
        need_sync = False
        for event in events:
            if event["type"] == "remove":
                edge = self.get_edge(event["source"], event["target"])
                if edge:
                    self._edges.remove(edge)
                    need_sync = True
        if need_sync:
            self._sync()

    def on_node_drag_stop(self, events):
        need_sync = False
        for node in events["nodes"]:
            for i in range(len(self._nodes)):
                if self._nodes[i]["id"] == node["id"]:
                    self._nodes[i]["position"] = node["position"]
                    self.server.js_call(
                        self.__ref,
                        "updateNode",
                        node["id"],
                        {"position": node["position"]},
                    )
                    need_sync = True
        if need_sync:
            self._sync()

    def _sync(self):
        """Synchronise VueFlow graph with this widget's internal state."""
        self.server.js_call(self.__ref, "setNodes", self._nodes)
        self.server.js_call(self.__ref, "setEdges", self._edges)
        self.graph_change(self._nodes, self._edges)

    def add_node(self, node: Node):
        """Add a Node to the graph."""
        self._nodes.append(node)
        self.server.js_call(self.__ref, "addNodes", node)
        self.graph_change(self._nodes, self._edges)

    def add_edge(self, edge: Edge):
        """Add an Edge to the graph."""
        self._edges.append(edge)
        self.server.js_call(self.__ref, "addEdges", edge)
        self.graph_change(self._nodes, self._edges)

    def get_node(self, id: str):
        """Get a Node from its id. Returns None if not found."""
        for node in self._nodes:
            if node["id"] == id:
                return node
        return None

    def get_edge(self, source: str, target: str):
        """Get an Edge from its source and target. Returns None if not found."""
        for edge in self._edges:
            if edge["source"] == source and edge["target"] == target:
                return edge
        return None

    def remove_node(self, node_id: str):
        """Remove a Node from the graph. Does nothing if no node has id=`node_id`"""
        node = self.get_node(node_id)
        if node is not None:
            self.server.js_call(self.__ref, "removeNodes", node_id)
            self._nodes.remove(node)
            self.graph_change(self._nodes, self._edges)

    def remove_edge(self, source: str, target: str):
        """Remove an Edge from the graph. Does nothing if there is no edge from `source` to `target`."""
        edge = self.get_edge(source, target)
        if edge is not None:
            self.server.js_call(self.__ref, "removeEdges", edge["id"])
            self._edges.remove(edge)
            self.graph_change(self._nodes, self._edges)

    @property
    def graph(self) -> Graph:
        return Graph(nodes=self._nodes, edges=self._edges)

    def serialize_graph(self) -> str:
        """Returns graph as a string representing a `Graph` object."""
        return str(self.graph)

    def deserialize_graph(self, graph_str: str) -> bool:
        """
        Deserialize graph from a string representing a `Graph` object.

        Returns False if deserialization produced any error, else True.
        """
        try:
            graph = literal_eval(graph_str)
            self._nodes = graph["nodes"]
            self._edges = graph["edges"]
            self._sync()
        except Exception:
            return False
        return True

    def update_node(self, node_id: str, **kwargs):
        """Update a node's property."""
        for node in self._nodes:
            if node["id"] == node_id:
                node.update(**kwargs)
                self._sync()
                break

    def update_edge(self, source: str, target: str, **kwargs):
        """Update an edge's property."""
        for edge in self._edges:
            if edge["source"] == source and edge["target"] == target:
                edge.update(**kwargs)
                self._sync()
                break

    def fit_view(self):
        """Fit VueFlow's view to show the entire graph (excluding hidden nodes)"""
        self.server.js_call(self.__ref, "fitView")
