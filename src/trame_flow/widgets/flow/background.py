from trame_flow.widgets.flow.common import HtmlElement

__all__ = [
    "Background",
]


class Background(HtmlElement):
    """Background for `NodeEditor`."""

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__("Background", **kwargs)

        self._attr_names += [
            "variant",
            "gap",
            "size",
            ("pattern_color", "patternColor"),
            ("bg_color", "bgColor"),
            "height",
            "width",
            "x",
            "y",
        ]
