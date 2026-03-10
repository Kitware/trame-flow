from trame.app import TrameApp
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets.html import Span
from trame.widgets.vuetify3 import (
    VBtn,
    VIcon,
    VSelect,
)
from trame_flow.module.core import create_node
from trame_flow.widgets.flow import (
    Background,
    Controls,
    CustomNode,
    Handle,
    NodeEditor,
)


class Example(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self.ui = self.build_ui()
        self.next_node_id = 0

    @property
    def state(self):
        return self.server.state

    def add_node(self):
        self.vueflow.add_node(
            create_node(
                id=str(self.next_node_id),
                x=0,
                y=0,
                type=self.state.node_type,
                label=f"Node {self.next_node_id}",
                data={"subtitle": "subtitle"},
            )
        )
        self.next_node_id += 1

    def build_ui(self):
        with SinglePageLayout(self.server) as layout:
            layout.title.set_text("trame-flow example")
            with layout.toolbar:
                VSelect(
                    label="Node type",
                    items=("['solver1', 'solver2', 'solver3', 'solver4']",),
                    v_model=("node_type", "solver1"),
                    density="compact",
                    hide_details="true",
                    max_width="120px",
                )
                with VBtn(
                    "Add a node",
                    click=self.add_node,
                ):
                    VIcon("mdi-plus")

            with NodeEditor() as self.vueflow:
                Background(gap=10, size=1, pattern_color="#81818a")
                Controls()
                with CustomNode("solver1"):
                    Handle(
                        type="source", position="right", id="out1", style="top: 10px"
                    )
                    Handle(
                        type="source", position="right", id="out2", style="top: 20px"
                    )
                    Handle(
                        type="source", position="right", id="out3", style="top: 30px"
                    )
                    Span("Solver 1")

                with CustomNode("solver2"):
                    Handle(type="source", position="right")
                    Handle(type="target", position="left", id="in1", style="top: 10px")
                    Handle(type="target", position="left", id="in2", style="top: 20px")
                    Span("Solver 2")

                with CustomNode("solver3"):
                    Handle(type="source", position="right")
                    Handle(type="target", position="left")
                    Span("Solver 3")

                with CustomNode("solver4"):
                    Handle(type="target", position="left", id="in1", style="top: 10px")
                    Handle(type="target", position="left", id="in2", style="top: 20px")
                    Span("Solver 4")

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
