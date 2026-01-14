from trame.app import TrameApp
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets.html import Label
from trame.widgets.vuetify3 import (
    VCol,
    VColorPicker,
    VContainer,
    VRow,
    VSlider,
)
from trame_flow.module.core import create_node
from trame_flow.widgets.flow import NodeEditor


class Example(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self.ui = self.build_ui()

        @self.state.change("width", "height")
        def _on_size_change(width, height, **_):
            self.vueflow.update_node("0", width=width, height=height)
            self.vueflow.fit_view()

        @self.state.change("node_color", "node_background", "node_font_size")
        def _on_style_change(node_color, node_background, node_font_size, **_):
            self.vueflow.update_node(
                "0",
                style={
                    "color": node_color,
                    "background": node_background,
                    "font-size": str(node_font_size) + "px",
                },
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
                    self.vueflow = NodeEditor(show_mini_map=False, show_controls=False)
                    self.vueflow.add_node(
                        create_node(id="0", type="default", x=0, y=0, label="My node")
                    )
                    self.vueflow.graph_change = lambda *_: self.vueflow.fit_view()
                with VCol():
                    VSlider(
                        label="Width",
                        v_model=("width", 150),
                        min=20,
                        max=400,
                    )
                    VSlider(
                        label="Height",
                        v_model=("height", 40),
                        min=10,
                        max=100,
                    )
                    VSlider(
                        label="Font Size",
                        v_model=("node_font_size", 12),
                        min=1,
                        max=30,
                    )
                    with VContainer(fluid=True), VRow(justify="space-around"):
                        with VCol(
                            classes="text-center d-flex flex-column flex-wrap align-content-center"
                        ):
                            Label("Color")
                            VColorPicker(
                                v_model=("node_color", "#000"),
                                classes="ma-2",
                            )
                        with VCol(
                            classes="text-center d-flex flex-column flex-wrap align-content-center"
                        ):
                            Label("Background")
                            VColorPicker(
                                v_model=("node_background", "#fff"),
                                classes="ma-2",
                            )


# Main

if __name__ == "__main__":
    app = Example()
    app.server.start()
