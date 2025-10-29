from trame.app import get_server
from trame.decorators import TrameApp
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets.vuetify3 import (
    VBtn,
    VCheckbox,
    VCol,
    VContainer,
    VNumberInput,
    VRow,
    VSelect,
    VTextarea,
    VTextField,
)
from trame_flow.widgets.flow import Node, NodeEditor, create_node

example_graph_state = """{
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
        self.server = get_server(server, client_type="vue3")
        self.ui = self.build_ui()
        self.state.new_node_name = ""
        self.next_node_id = 0

        @self.state.change("selected_resize_node_id")
        def _on_selected_resize_node_id_change(selected_resize_node_id, **_):
            node = self.vueflow.get_node(selected_resize_node_id)
            if node:
                self.state.resize_node_width = node["width"]
                self.state.resize_node_height = node["height"]

        @self.state.change("resize_node_width", "resize_node_height")
        def _on_resize(resize_node_width, resize_node_height, **_):
            self.vueflow.update_node(
                self.state.selected_resize_node_id,
                width=resize_node_width,
                height=resize_node_height,
            )

    @property
    def state(self):
        return self.server.state

    def add_node(self):
        self.vueflow.add_node(
            create_node(
                id=str(self.next_node_id),
                x=0,
                y=0,
                type="default",
                label=self.state.new_node_name,
                parent_id=self.state.selected_parent_node_id,
                extent="parent" if self.state.new_node_force_inside else None,
                expand_parent=self.state.new_node_expand_parent,
            )
        )
        self.next_node_id += 1
        self.state.new_node_name = ""

    def remove_node(self):
        self.vueflow.remove_node(self.state.selected_node_id)

    def export_graph(self):
        with self.state:
            self.state.exported_graph = self.vueflow.serialize_graph()

    def import_graph(self):
        with self.state:
            self.vueflow.deserialize_graph(self.state.imported_graph)

    def build_ui(self):
        with SinglePageLayout(self.server) as layout:
            layout.title.set_text("trame-flow example")
            with layout.toolbar:
                VBtn(
                    "Show Example",
                    click=lambda: self.vueflow.deserialize_graph(example_graph_state),
                )

            with layout.content, VContainer(), VRow():
                with VCol():
                    VTextField(
                        label="Node name",
                        v_model=("new_node_name", ""),
                    )
                    VSelect(
                        label="Parent",
                        items=("nodes", []),
                        item_title="data.label",
                        item_value="id",
                        v_model=("selected_parent_node_id", None),
                        clearable=True,
                    )
                    VCheckbox(
                        label="Expand parent",
                        v_model=("new_node_expand_parent", False),
                    )
                    VCheckbox(
                        label="Force inside parent",
                        v_model=("new_node_force_inside", True),
                    )
                    VBtn("Add Node", click=self.add_node)
                with VCol():
                    VSelect(
                        label="Node",
                        items=("nodes", []),
                        item_title="data.label",
                        item_value="id",
                        v_model=("selected_resize_node_id", None),
                    )
                    VNumberInput(
                        label="Width",
                        v_model=("resize_node_width", 0),
                        min=0,
                    )
                    VNumberInput(
                        label="Height",
                        v_model=("resize_node_height", 0),
                        min=0,
                    )
                with VCol():
                    VSelect(
                        label="Node",
                        items=("nodes", []),
                        item_title="data.label",
                        item_value="id",
                        v_model=("selected_node_id", None),
                    )
                    VBtn("Remove Node", click=self.remove_node)
                with VCol():
                    VTextarea(
                        density="compact",
                        label="Exported graph here",
                        readonly=True,
                        v_model=("exported_graph", ""),
                    )
                    VBtn("Export Graph", click=self.export_graph)
                with VCol():
                    VTextarea(
                        density="compact",
                        label="Paste graph here",
                        v_model=("imported_graph", ""),
                    )
                    VBtn("Import Graph", click=self.import_graph)

            self.vueflow = NodeEditor()

            def on_graph_change(nodes, edges):
                with self.state:
                    self.state.nodes = nodes
                    self.state.edges = edges
                    self.state.selected_node_id = None
                self.state.dirty("nodes")
                self.state.dirty("edges")

            self.vueflow.graph_change = on_graph_change

            def on_node_click(node: Node):
                print(f'Clicked on node "{node["data"]["label"]}" (id={node["id"]})')  # noqa: T201

            self.vueflow.node_click = (on_node_click, "[$event.node]")


# Main

if __name__ == "__main__":
    app = Example()
    app.server.start()
