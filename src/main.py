import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw

from window.athan_window import AthanWindow

class AthanApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = AthanWindow(application=app)
        self.win.present()

def main():
    app = AthanApp(application_id="com.example.athan")
    return app.run(None)

if __name__ == "__main__":
    main()
