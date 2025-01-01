import os
import shutil
from ignis.services.options import OptionsService

options = OptionsService.get_default()

def replace_face_with_avatar(gfile):
    face_path = os.path.expanduser("~/.face")
    
    try:
        shutil.copy(gfile.get_path(), face_path)
    except Exception as e:
       pass

user_opt_group = options.create_group("user", exists_ok=True)
avatar_opt = user_opt_group.create_option(
    "avatar",
    default=f"{os.path.expanduser('~')}/.face",
    exists_ok=True,
)

settings_opt_group = options.create_group("settings", exists_ok=True)
settings_last_page = settings_opt_group.create_option(
    "last_page",
    default=0,
    exists_ok=True,
)
