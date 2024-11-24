import keyboard
import pygetwindow


class KeyHandler:

    # When you start the program you are in terminal so pass in that name. BIG BRAIN MOMENT!
    def __init__(self, terminal_name: str) -> None:
        self.terminal_name = terminal_name
        self.key = ""
        keyboard.on_press(self.on_press, suppress=True)
        keyboard.on_release_key("ctrl", self.on_release)
        keyboard.on_release_key("c", self.on_release)
        self.hooked = True
        # FOR KEYBOARD INTERRUPT
        self.ctrl_and_c_dict = {
            "c": False,
            "ctrl": False,
        }

    def on_press(self, event: keyboard.KeyboardEvent) -> None:
        if event.name in self.ctrl_and_c_dict:
            self.ctrl_and_c_dict[event.name] = True

        self.key = event.name

    def on_release(self, event: keyboard.KeyboardEvent) -> None:
        self.ctrl_and_c_dict[event.name] = False

    def window_is_terminal(self) -> bool:
        return pygetwindow.getActiveWindowTitle() == self.terminal_name

    def getch(self) -> str | None:
        if self.window_is_terminal():
            if not self.hooked:
                keyboard.on_press(self.on_press, suppress=True)
                keyboard.on_release_key("ctrl", self.on_release)
                keyboard.on_release_key("c", self.on_release)
                self.hooked = True
        else:
            if self.hooked:
                keyboard.unhook_all()
                self.hooked = False

        if self.ctrl_and_c_dict["c"] and self.ctrl_and_c_dict["ctrl"]:
            raise KeyboardInterrupt

        key, self.key = self.key, ""
        return key

    def close(self):
        keyboard.unhook_all()
