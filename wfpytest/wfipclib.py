from typing import Any
import socket
import json as js

def get_msg_template():
    # Create generic message template
    message = {}
    message["data"] = {}
    return message

class WayfireIPCClient:
    def __init__(self, socket_name: str):
        self.client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.client.connect(socket_name)

    def send_json(self, msg):
        data = js.dumps(msg).encode('utf8')
        header = len(data).to_bytes(4, byteorder="little")
        self.client.send(header)
        self.client.send(data)

        response = self.client.recv(1024)
        rlen = int.from_bytes(response[:4], byteorder="little")
        rps = js.loads(response[4:(rlen+4)])
        return rps

    def ping(self):
        message = get_msg_template()
        message["method"] = "core/ping"
        response = self.send_json(message)
        return ("result", "ok") in response.items()

    def create_wayland_output(self):
        message = get_msg_template()
        message["method"] = "core/create_wayland_output"
        self.send_json(message)

    def list_views(self):
        message = get_msg_template()
        message["method"] = "core/list_views"
        return self.send_json(message)

    def get_view_info(self, app_id: str) -> Any:
        views = self.list_views()
        for v in views:
            if v['app-id'] == app_id:
                return v
        return None

    def run(self, cmd):
        message = get_msg_template()
        message["method"] = "core/run"
        message["data"]["cmd"] = cmd
        return self.send_json(message)

    def move_cursor(self, x: int, y: int):
        message = get_msg_template()
        message["method"] = "core/move_cursor"
        message["data"]["x"] = x
        message["data"]["y"] = y
        return self.send_json(message)

    def click_button(self, btn_with_mod: str, mode: str):
        """
        btn_with_mod can be S-BTN_LEFT/BTN_RIGHT/etc. or just BTN_LEFT/...
        If S-BTN..., then the super modifier will be pressed as well.
        mode is full, press or release
        """
        message = get_msg_template()
        message["method"] = "core/feed_button"
        message["data"]["mode"] = mode
        message["data"]["combo"] = btn_with_mod
        return self.send_json(message)


# Helper functions
def check_geometry(x: int, y: int, width: int, height: int, obj) -> bool:
    if obj['x'] == x and obj['y'] == y and \
        obj['width'] == width and obj['height'] == height:
        return True
    return False
