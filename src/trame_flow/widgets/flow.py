from ast import literal_eval
from typing import Callable, Literal, Optional, TypedDict, Union

from trame_client.widgets.core import AbstractElement

from .. import module


class HtmlElement(AbstractElement):
    def __init__(self, _elem_name, children=None, **kwargs):
        super().__init__(_elem_name, children, **kwargs)
        if self.server:
            self.server.enable_module(module)


__all__ = [
    "DEFAULT_EXTENT",
    "Dimensions",
    "Edge",
    "EdgeType",
    "Extent",
    "Graph",
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


class Dimensions(TypedDict):
    height: float
    width: float


# "parent" or [[x-from, y-from], [x-to, y-to]]
Extent = Union[Literal["parent"], list[list[float]]]
DEFAULT_EXTENT = [[float("-inf"), float("-inf")], [float("+inf"), float("+inf")]]

NodeType = Literal["default", "input", "output"]


class NodeData(TypedDict):
    label: str


class Node(TypedDict):
    id: str
    type: NodeType
    data: NodeData
    position: Position
    draggable: bool
    parentNode: Optional[str]
    expandParent: Optional[bool]
    extent: Extent
    width: int
    height: int
    style: Optional[dict]


def create_node(
    id: str,
    type: NodeType,
    x: float,
    y: float,
    label: str,
    parent_id: Optional[str] = None,
    expand_parent: bool = False,
    extent: Extent = DEFAULT_EXTENT,
    width: int = 150,
    height: int = 40,
    style: Optional[dict] = None,
) -> Node:
    node = Node(
        id=id,
        type=type,
        data=NodeData(label=label),
        position=Position(x=x, y=y),
        draggable=True,
        parentNode=parent_id,
        expandParent=expand_parent,
        extent=extent,
        width=width,
        height=height,
        style=style,
    )
    if extent == "parent" and parent_id is None:
        parent_id = ""
    return node


EdgeType = Literal["default", "step", "smoothstep", "straight"]


class Edge(TypedDict):
    id: str
    source: str
    target: str
    type: EdgeType
    label: Optional[str]
    animated: bool


def create_edge(
    source_id: str,
    target_id: str,
    type: EdgeType = "default",
    label: Optional[str] = None,
    animated: bool = False,
):
    return Edge(
        id=f"{source_id}->{target_id}",
        source=source_id,
        target=target_id,
        type=type,
        label=label,
        animated=animated,
    )


class Graph(TypedDict):
    nodes: list[Node]
    edges: list[Edge]


class NodeEditor(HtmlElement):
    """
    Node Editor based on VueFlow

    Args:
        background_pattern_variant ("dots" or "lines"):
            Pattern type in the background
        background_pattern_color (html color string):
            Color of the pattern in the background
        background_pattern_size (number):
            Size of the pattern in the background
        background_pattern_gap (number):
            Size of the gaps for the pattern in the background
    """

    _next_id = 0

    def __init__(self, auto_connect=True, **kwargs):
        super().__init__(
            "node-editor",
            **kwargs,
        )

        self._attr_names += [
            ("background_pattern_variant", "backgroundPatternVariant"),
            ("background_pattern_color", "backgroundPatternColor"),
            ("background_pattern_size", "backgroundPatternSize"),
            ("background_pattern_gap", "backgroundPatternGap"),
        ]
        self._event_names += [
            ("node_click", "nodeClick"),
            ("edge_click", "edgeClick"),
            "connect",
            ("nodes_change", "nodesChange"),
            ("edges_change", "edgesChange"),
            "init",
            ("node_drag_stop", "nodeDragStop"),
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

        if auto_connect:
            self.connect = (lambda event: self.on_connect(event), "[$event]")

        self.graph_change: Callable[[list[Node], list[Edge]], None] = lambda *_: None

    def on_connect(self, event):
        if not self.get_edge(event["source"], event["target"]) and not self.get_edge(
            event["target"], event["source"]
        ):
            self.add_edge(
                Edge(
                    source=event["source"],
                    target=event["target"],
                    id=f"{event['source']}->{event['target']}",
                    type="default",
                    animated=False,
                    label="",
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
        self.server.js_call(self.__ref, "setNodes", self._nodes)
        self.server.js_call(self.__ref, "setEdges", self._edges)
        self.graph_change(self._nodes, self._edges)

    def add_node(self, node: Node):
        self._nodes.append(node)
        self.server.js_call(self.__ref, "addNodes", node)
        self.graph_change(self._nodes, self._edges)

    def add_edge(self, edge: Edge):
        self._edges.append(edge)
        self.server.js_call(self.__ref, "addEdges", edge)
        self.graph_change(self._nodes, self._edges)

    def get_node(self, id: str):
        for node in self._nodes:
            if node["id"] == id:
                return node
        return None

    def get_edge(self, source: str, target: str):
        for edge in self._edges:
            if edge["source"] == source and edge["target"] == target:
                return edge
        return None

    def remove_node(self, node_id: str):
        node = self.get_node(node_id)
        if node:
            self.server.js_call(self.__ref, "removeNodes", node_id)
            self._nodes.remove(node)
            self.graph_change(self._nodes, self._edges)

    def remove_edge(self, edge: Edge):
        self.server.js_call(self.__ref, "removeEdges", edge["id"])
        self._edges.remove(edge)

    def serialize_graph(self) -> str:
        return str(
            {
                "nodes": self._nodes,
                "edges": self._edges,
            }
        )

    def deserialize_graph(self, graph_str: str):
        graph = literal_eval(graph_str)
        self._nodes = graph["nodes"]
        self._edges = graph["edges"]
        self._sync()

    def update_node(self, node_id: str, **kwargs):
        for node in self._nodes:
            if node["id"] == node_id:
                node.update(kwargs)
                self._sync()
                break
