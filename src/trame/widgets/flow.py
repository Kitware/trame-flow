from trame_flow.widgets.flow import *  # noqa: F403


def initialize(server):
    from trame_flow import module

    server.enable_module(module)
