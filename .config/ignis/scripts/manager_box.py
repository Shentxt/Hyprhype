class BoxStateManager:
    def __init__(self):
        self.state = {
            "visible_box": "box1",
            "icons": {
                "box1": "",
                "box2": "",
            },
        }

    def update_state(self, box_to_show: str):
        if box_to_show in self.state["icons"]:
            self.state["visible_box"] = box_to_show
        else:
            raise ValueError(f"Box '{box_to_show}' no está definida.")

    def get_state(self):
        return {
            "box_visible": self.state["visible_box"],
            "icon": self.state["icons"][self.state["visible_box"]],
        }

manager = BoxStateManager()

def update_state(box_to_show: str):
    manager.update_state(box_to_show)

def get_state():
    return manager.get_state()

