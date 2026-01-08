from trame.app import TrameApp
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets.vuetify3 import (
    VCol,
    VContainer,
    VRow,
    VTextarea,
)
from trame_flow.widgets.flow import Node, NodeEditor

DEFAULT_GRAPH = """{
    "nodes": [
        {
            "id": "0",
            "type": "input",
            "data": {"label": "My input node"},
            "position": {"x": 9.5, "y": 49.5},
            "draggable": True,
            "expandParent": False,
            "width": "auto",
            "height": "auto",
            "extent": "parent",
            "style": {
                "background": "linear-gradient(40deg, lightgreen, blue)",
            },
        },
        {
            "id": "1",
            "type": "output",
            "data": {"label": "My output node"},
            "position": {"x": 0, "y": 350},
            "draggable": True,
            "expandParent": False,
            "width": "auto",
            "height": "auto",
            "extent": "parent",
            "style": {
                "border": "2px green dotted",
            },
        },
        {
            "id": "2",
            "type": "default",
            "data": {"label": "My parent node"},
            "position": {"x": -43.5, "y": 205.51916885375977},
            "draggable": True,
            "width": 200,
            "height": 100,
        },
        {
            "id": "3",
            "type": "default",
            "data": {"label": "My child node"},
            "position": {"x": 50, "y": 50},
            "draggable": True,
            "width": "auto",
            "height": "auto",
            "parentNode": "2",
            "extent": "parent",
        },
    ],
    "edges": [
        {
            "source": "0",
            "target": "2",
            "id": "0->2",
            "type": "default",
            "animated": False,
            "markerEnd": {
                "type": "arrowclosed",
                "width": 50,
                "height": 50,
                "color": "red",
            },
            "style": {
                "stroke": "orange",
            },
        },
        {
            "source": "2",
            "target": "1",
            "id": "2->1",
            "type": "default",
            "animated": True,
            "markerEnd": {
                "type": "arrow",
                "width": 20,
                "height": 20,
                "color": "magenta",
            },
            "style": {
                "stroke": "purple",
            },
        },
    ],
}"""


class Example(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self.ui = self.build_ui()
        self.next_node_id = 0

        @self.state.change("serialized_graph")
        def _on_serialized_graph_change(serialized_graph, **_):
            self.state.serialization_error = not self.vueflow.deserialize_graph(
                serialized_graph
            )
            self.vueflow.fit_view()

    @property
    def state(self):
        return self.server.state

    def build_ui(self):
        with SinglePageLayout(self.server) as layout:
            layout.title.set_text("trame-flow example")

            with (
                layout.content,
                VContainer(fluid=True, classes="h-100"),
                VRow(classes="h-100"),
            ):
                with VCol():
                    self.vueflow = NodeEditor()
                with VCol():
                    VTextarea(
                        density="compact",
                        label="Serialized graph",
                        v_model=("serialized_graph", DEFAULT_GRAPH),
                        classes="h-100",
                        error=("serialization_error", False),
                    )

            def on_graph_change(*_):
                with self.state:
                    graph_str = self.vueflow.serialize_graph()
                    if graph_str != self.state.serialized_graph:
                        self.state.serialized_graph = graph_str

            self.vueflow.graph_change = on_graph_change

            def on_node_click(node: Node):
                print(f'Clicked on node "{node["data"]["label"]}" (id={node["id"]})')  # noqa: T201

            self.vueflow.node_click = (on_node_click, "[$event.node]")


# Main

if __name__ == "__main__":
    app = Example()
    app.server.start()
