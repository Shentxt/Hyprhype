import os
from gi.repository import GdkPixbuf, GLib, Gdk
from fabric.notifications import (
    Notification,
    NotificationAction,
    NotificationCloseReason,
    Notifications,
)
from loguru import logger
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.image import Image
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.label import Label
from fabric.widgets.revealer import Revealer
from fabric.widgets.wayland import WaylandWindow as Window
from utils import CustomImage
import utils.icons as icons


class ActionButton(Button):
    def __init__(
        self, action: NotificationAction, index: int, total: int, notification_box
    ):
        super().__init__(
            name="action-button",
            h_expand=True,
            on_clicked=self.on_clicked,
            child=Label(name="button-label", label=action.label),
        )
        self.action = action
        self.notification_box = notification_box
        style_class = (
            "start-action"
            if index == 0
            else "end-action"
            if index == total - 1
            else "middle-action"
        )
        self.add_style_class(style_class)
        self.connect(
            "enter-notify-event", lambda *_: notification_box.hover_button(self)
        )
        self.connect(
            "leave-notify-event", lambda *_: notification_box.unhover_button(self)
        )

    def on_clicked(self, *_):
        self.action.invoke()
        self.action.parent.close("dismissed-by-user")


class NotificationWidget(Box):
    def __init__(self, notification: Notification, timeout_ms=5000, **kwargs):
        bubble_container = Box(
           name="notification-bubble", 
           orientation="v",
        )
        bubble_container.set_vexpand(True)
        bubble_container.set_style(
            "background-image: url('/home/shen/.config/Modus/assets/Icon/buble.png');"
            "background-repeat: no-repeat;"
            "background-position: center;"
            "background-size: cover;" 
        )
        bubble_container.add(self.create_header(notification))
        bubble_container.add(self.create_content_text(notification))
        bubble_container.add(self.create_action_buttons(notification))

        notification_image = Box(
            name="notification-image",
            children=CustomImage(
                pixbuf=notification.image_pixbuf.scale_simple(
                    70, 70, GdkPixbuf.InterpType.BILINEAR
                )
                if notification.image_pixbuf
                else self.get_pixbuf(notification.app_icon, 70, 70)
            ),
        )

        super().__init__(
            name="notification-box",
            orientation="h",
            h_align="fill",
            h_expand=True,
            children=[
                notification_image,
                bubble_container,
            ],
        )

        self.notification = notification
        self.timeout_ms = timeout_ms
        self._timeout_id = None
        self.start_timeout()

    def create_header(self, notification):
        app_icon = (
            Image(
                name="notification-icon",
                image_file=notification.app_icon[7:],
                size=24,
            )
            if "file://" in notification.app_icon
            else Image(
                name="notification-icon",
                icon_name="dialog-information-symbolic" or notification.app_icon,
                icon_size=24,
            )
        )

        return CenterBox(
            name="notification-title",
            start_children=[
                #Box(
                #    spacing=0,
                #    children=[
                #        app_icon,
                #        Label(
                #            notification.app_name,
                #            name="notification-app-name",
                #            h_align="start",
                #        ),
                #    ],
                #)
            ],
            end_children=[self.create_close_button()],
        ) 

    def create_content_text(self, notification):
        return Box(
            name="notification-text",
            orientation="v",
            v_align="center",
            h_expand=False,
            spacing=0,
            children=[
                Box(
                    name="notification-summary-box",
                    orientation="h",
                    children=[
                        Label(
                            name="notification-summary",
                            markup=notification.summary.replace("\n", " "),
                            h_align="start",
                            ellipsization="end",
                        ),
                        Label(
                            name="notification-app-name",
                            markup=" | " + notification.app_name, 
                            h_align="start",
                            ellipsization="end",
                        ),
                    ],
                ),
                Label(
                    name="notification-body",
                    markup=notification.body.replace("\n", " "),
                    h_align="start",   
                    ellipsization="end", 
                )
                if notification.body
                else Box(),
            ],
        )

    def get_pixbuf(self, icon_path, width, height):
        if icon_path.startswith("file://"):
            icon_path = icon_path[7:]

        if not os.path.exists(icon_path):
            logger.warning(f"Icon path does not exist: {icon_path}")
            return None

        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(icon_path)
            return pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
        except Exception as e:
            logger.error(f"Failed to load or scale icon: {e}")
            return None

    def create_action_buttons(self, notification):
        return Box(
            name="notification-action-buttons",
            spacing=0,
            h_expand=True,
            children=[
                ActionButton(action, i, len(notification.actions), self)
                for i, action in enumerate(notification.actions)
            ],
        )

    def create_close_button(self):
        close_button = Button(
            name="notif-close-button",
            child=Label(name="notif-close-label", markup=icons.cancel),
            on_clicked=lambda *_: self.notification.close("dismissed-by-user"),
        )
        close_button.connect(
            "enter-notify-event", lambda *_: self.hover_button(close_button)
        )
        close_button.connect(
            "leave-notify-event", lambda *_: self.unhover_button(close_button)
        )
        return close_button

    def start_timeout(self):
        self.stop_timeout()
        self._timeout_id = GLib.timeout_add(self.timeout_ms, self.close_notification)

    def stop_timeout(self):
        if self._timeout_id is not None:
            GLib.source_remove(self._timeout_id)
            self._timeout_id = None

    def close_notification(self):
        self.notification.close("expired")
        self.stop_timeout()
        return False

    def pause_timeout(self):
        self.stop_timeout()

    def resume_timeout(self):
        self.start_timeout()

    def destroy(self):
        self.stop_timeout()
        super().destroy()

    # @staticmethod
    def set_pointer_cursor(self, widget, cursor_name):
        window = widget.get_window()
        if window:
            cursor = Gdk.Cursor.new_from_name(widget.get_display(), cursor_name)
            window.set_cursor(cursor)

    def hover_button(self, button):
        self.pause_timeout()
        self.set_pointer_cursor(button, "hand2")

    def unhover_button(self, button):
        self.resume_timeout()
        self.set_pointer_cursor(button, "arrow")


class NotificationRevealer(Revealer):
    def __init__(self, notification: Notification, **kwargs):
        self.notif_box = NotificationWidget(notification)
        self._notification = notification
        super().__init__(
            child=Box(
                children=[self.notif_box],
            ),
            transition_duration=250,
            transition_type="slide-down",
        )

        self.connect(
            "notify::child-revealed",
            lambda *_: self.destroy() if not self.get_child_revealed() else None,
        )

        self._notification.connect("closed", self.on_resolved)

    def on_resolved(
        self,
        notification: Notification,
        reason: NotificationCloseReason,
    ):
        self.set_reveal_child(False)


class NotificationPopup(Window):
    def __init__(self):
        self._server = Notifications()
        self.notifications = Box(
            v_expand=True,
            h_expand=True,
            style="margin: 1px 0px 1px 1px;",
            orientation="v",
            spacing=5,
        )
        self._server.connect("notification-added", self.on_new_notification)

        super().__init__(
            anchor="top right",
            child=self.notifications,
            layer="overlay",
            all_visible=True,
            visible=True,
            exclusive=False,
        )

    def on_new_notification(self, fabric_notif, id):
        new_box = NotificationRevealer(fabric_notif.get_notification_from_id(id))
        self.notifications.add(new_box)
        new_box.set_reveal_child(True)
