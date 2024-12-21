import threading
from ignis.utils import Utils

class UpdateService:
    _instance = None

    @classmethod
    def get_default(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.updates_count = 0
        self._listeners = []
        self._stop_event = threading.Event()
        self._interval = 1  
        self.update_updates_count()
        self._start_periodic_update()

    def update_updates_count(self):
        Utils.exec_sh_async(
            "~/.config/hypr/scripts/get_updates.sh --get-updates",
            self._on_updates_result,
        )

    def _on_updates_result(self, result):
        try:
            updates = int(result.stdout.strip())
            if updates != self.updates_count:
                self.updates_count = updates
                self._update_number_only()
        except ValueError:
            self.updates_count = 0

    def _update_number_only(self):
        self._notify_listeners()

    def _notify_listeners(self):
        for callback in self._listeners:
            callback(self.updates_count)

    def bind(self, callback):
        self._listeners.append(callback)

    def emit_event(self):
        self._notify_listeners()

    def get_updates(self):
        return self.updates_count

    def _start_periodic_update(self):
        def periodic_update():
            while not self._stop_event.is_set():
                self.update_updates_count()
                self._stop_event.wait(self._interval)

        threading.Thread(target=periodic_update, daemon=True).start()

    def stop_periodic_update(self):
        self._stop_event.set()
