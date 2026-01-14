from trame_flow.widgets.flow.common import HtmlElement

__all__ = [
    "Controls",
    "ControlsButton",
]


class Controls(HtmlElement):
    """Controls for `NodeEditor`."""

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__("Controls", **kwargs)

        self._attr_names += [
            ("show_fit_view", "showFitView"),
            ("show_interactive", "showInteractive"),
            ("show_zoom", "showZoom"),
            ("fit_view_params", "fitViewParams"),
        ]

        self._event_names += [
            ("zoom_in", "zoom-in"),
            ("zoom_out", "zoom-out"),
            ("fit_view", "fit-view"),
            ("interaction_change", "interaction-change"),
        ]


class ControlsButton(HtmlElement):
    """ControlsButton for `Controls`."""

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__("ControlsButton", **kwargs)
