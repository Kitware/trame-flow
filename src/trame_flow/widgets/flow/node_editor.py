from ast import literal_eval
from typing import Callable, Literal

from trame_client.widgets.core import Template

from trame_flow.module.core import (
    Edge,
    Graph,
    HandlePosition,
    Node,
)
from trame_flow.widgets.flow.common import HtmlElement

__all__ = [
    "CustomNode",
    "Handle",
    "NodeEditor",
]


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


class Handle(HtmlElement):
    def __init__(
        self,
        position: HandlePosition,
        type: Literal["source", "target"],
        **kwargs,
    ):
        """Handle used to connect a node to other nodes. Use it inside a `CustomNode`.

        :param position: Position of the handle.
        :param type: Type of the handle.
        :param connectable: (Optional) Boolean, integer for maximum connection number or function that returns a boolean.
        :param id: (Optional) ID of the handle. Useful when using multiple source handles or target handles.
        :param connection_mode: (Optional) Defines if a handle can be connected to another handle with the same type. "loose" (default) or "strict".
        """
        super().__init__("Handle", position=position, type=type, **kwargs)

        self._attr_names += [
            "connectable",
            ("connection_mode", "connection-mode"),
            "id",
            "position",
            "type",
        ]


class NodeEditor(HtmlElement):
    """Node Editor based on VueFlow."""

    _next_id = 0

    def __init__(self, **kwargs):
        super().__init__(
            "node-editor",
            **kwargs,
        )

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
