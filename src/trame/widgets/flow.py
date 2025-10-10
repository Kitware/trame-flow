from trame_flow.widgets.flow import *


def initialize(server):
    from trame_flow import module

    server.enable_module(module)
