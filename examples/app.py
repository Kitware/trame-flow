from trame.app import get_server
from trame.decorators import TrameApp
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets.flow import NodeEditor
from trame.widgets.vuetify3 import (
    VBtn,
    VCol,
    VContainer,
    VRow,
    VSelect,
    VTextarea,
    VTextField,
)


class Example(TrameApp):
    def __init__(self, server=None):
        self.server = get_server(server, client_type="vue3")
        self.ui = self.build_ui()
        self.state.new_node_name = ""
        self.next_node_id = 0

    @property
    def state(self):
        return self.server.state

    def add_node(self):
        self.vueflow.add_node(
            id=str(self.next_node_id),
            x=0,
            y=0,
            type="default",
            label=self.state.new_node_name,
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
                pass

            with layout.content, VContainer(), VRow():
                with VCol():
                    VTextField(
                        label="Node name",
                        v_model=("new_node_name", ""),
                    )
                    VBtn("Add Node", click=self.add_node)
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


# Main

if __name__ == "__main__":
    app = Example()
    app.server.start()
