from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.button import Button
from fabric.utils.helpers import exec_shell_command_async
import utils.icons as icons


class PowerMenu(Box):
    def __init__(self, **kwargs):
        super().__init__(
            name="power-menu",
            orientation="v",         
            spacing=10,
            v_align="center",        
            h_align="end",           
            v_expand=False,
            h_expand=False,
            visible=True,
            **kwargs,
        )

        self.launcher = kwargs["launcher"]

        self.btn_suspend = Button(
            name="power-menu-button",
            child=Label(name="button-label", markup=icons.suspend),
            on_clicked=self.suspend,
        )

        self.btn_logout = Button(
            name="power-menu-button",
            child=Label(name="button-label", markup=icons.logout),
            on_clicked=self.logout,
        )

        self.btn_reboot = Button(
            name="power-menu-button",
            child=Label(name="button-label", markup=icons.reboot),
            on_clicked=self.reboot,
        )

        self.btn_shutdown = Button(
            name="power-menu-button",
            child=Label(name="button-label", markup=icons.shutdown),
            on_clicked=self.poweroff,
        )

        self.buttons = [
            self.btn_suspend,
            self.btn_logout,
            self.btn_reboot,
            self.btn_shutdown,
        ]

        for button in self.buttons:
            self.add(button)

        self.show_all()

    def close_menu(self):
        self.launcher.close()

    def suspend(self, *args):
        exec_shell_command_async("systemctl suspend")
        self.close_menu()

    def logout(self, *args):
        exec_shell_command_async("hyprctl dispatch exit")
        self.close_menu()

    def reboot(self, *args):
        exec_shell_command_async("systemctl reboot")
        self.close_menu()

    def poweroff(self, *args):
        exec_shell_command_async("systemctl poweroff")
        self.close_menu()
