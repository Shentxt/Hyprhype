import os
from ignis.services.options import OptionsService

options = OptionsService.get_default()

icons_opt_group = options.create_group("icons", exists_ok=True)

def create_icon_option(icon_name, file_path):
    return icons_opt_group.create_option(
        icon_name,
        default=os.path.join(os.path.expanduser("~/.config/ignis/assets"), file_path),
        exists_ok=True,
    )

imgs_opt_group = options.create_group("icons", exists_ok=True)

def create_img_option(img_name, file_path):
    return imgs_opt_group.create_option(
        img_name,
        default=os.path.join(os.path.expanduser("~/.config/hypr/assets/icons/persona"), file_path),
        exists_ok=True,
    )

icon_options = {
    "hypr": create_icon_option("hypr", "hypr-symbolic.svg"),
    "ann": create_img_option("ann", "ann.png"),
}

