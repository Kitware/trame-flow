from trame.app import TrameApp
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets.html import H4, P
from trame.widgets.vuetify3 import (
    VBtn,
    VIcon,
    VSelect,
)
from trame_flow.module.core import Node, create_node
from trame_flow.widgets.flow import (
    Background,
    Controls,
    CustomNode,
    Handle,
    NodeEditor,
    NodeResizer,
    NodeToolbar,
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
                x=(self.next_node_id % 10) * 100,
                y=(self.next_node_id // 10) * 100,
                type=self.state.node_type,
                label=f"Node {self.next_node_id}",
                data={"subtitle": "subtitle"},
            )
        )
        self.next_node_id += 1

    def remove_node(self):
        if self.state.nodes:
            node_to_remove: Node = self.state.nodes[self.next_node_id - 1]
            self.vueflow.remove_node(node_to_remove["id"])
            self.next_node_id -= 1

    def build_ui(self):
        with SinglePageLayout(self.server) as layout:
            layout.title.set_text("trame-flow example")
            with layout.toolbar:
                VSelect(
                    label="Node type",
                    items=(
                        "['default', 'input', 'output', 'text', 'title', 'toolbar']",
                    ),
                    v_model=("node_type", "default"),
                    density="compact",
                    hide_details="true",
                    max_width="120px",
                )
                with VBtn(
                    "Add a node",
                    click=self.add_node,
                ):
                    VIcon("mdi-plus")
                with VBtn(
                    "Remove a node",
                    click=self.remove_node,
                ):
                    VIcon("mdi-minus")

            with NodeEditor() as self.vueflow:
                Background(gap=10, size=1, pattern_color="#81818a")
                Controls()
                with CustomNode("title"):
                    Handle(type="target", position="top")
                    H4("{{props.data.label}}")
                    P("{{props.data.subtitle}}")
                with CustomNode("text", var_name="nodeProps"):
                    NodeResizer()
                    P("{{nodeProps.data.label}}")
                with CustomNode("toolbar"):
                    with NodeToolbar(
                        is_visible=True,
                        style="background: darkgray; padding: 4px; font-size: 1.2em; border-radius: 4px",
                    ):
                        P("This is a toolbar")
                    P("{{props.data.label}}")

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
