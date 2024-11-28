state = {
    "box1_visible": True,
    "box2_visible": False,
    "icon1": "",
    "icon2": "",
}

def update_state(box_to_show: str):
    if box_to_show == "box1":
        state["box1_visible"] = True
        state["box2_visible"] = False
        state["icon1"] = ""
        state["icon2"] = ""
    elif box_to_show == "box2":
        state["box1_visible"] = False
        state["box2_visible"] = True
        state["icon1"] = ""
        state["icon2"] = ""

def get_state():
    return state
