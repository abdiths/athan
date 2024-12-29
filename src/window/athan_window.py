import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, GLib, Adw
import datetime

from api.prayer_time_fetcher import PrayerTimeFetcher
from window.settings_manager import SettingsManager
from window.notifier import Notifier

class AthanWindow(Adw.ApplicationWindow):
    def __init__(self, application, *args, **kwargs):
        super().__init__(application=application, *args, **kwargs)

        # Window properties
        self.set_title("Athan Prayer Times")
        self.set_default_size(400, 200)
        
        # Main box layout
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.main_box.set_margin_top(12)
        self.main_box.set_margin_bottom(12)
        self.main_box.set_margin_start(12)
        self.main_box.set_margin_end(12)

        # Header label
        header = Gtk.Label()
        header.set_markup("<span size='x-large'>Prayer Times</span>")
        self.main_box.append(header)

        # Prayer times box
        self.prayer_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.main_box.append(self.prayer_box)

        # Set the content of the window
        self.set_content(self.main_box)
        
        settings_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        
        # Location entry
        self.location_entry = Gtk.Entry()
        self.location_entry.set_placeholder_text("Enter city name")
        settings_box.append(self.location_entry)
        
        update_button = Gtk.Button(label="Update")
        update_button.connect("clicked", self.update_prayer_times)
        settings_box.append(update_button)
        
        self.main_box.append(settings_box)
        
        # Initialize components
        self.prayer_labels = {}
        self.settings_manager = SettingsManager()
        self.prayer_fetcher = PrayerTimeFetcher()
        self.notifier = Notifier()
        
        self.settings_manager.load_config(self.location_entry)
        self.update_prayer_times()
        
        # Set up periodic updates
        GLib.timeout_add_seconds(60, self.check_prayer_times)
    
    def update_prayer_times(self, *args):
        child = self.prayer_box.get_first_child()
        while child is not None:
            next_child = child.get_next_sibling()  
            self.prayer_box.remove(child)        
            child = next_child
        
        city = self.location_entry.get_text()
        if not city:
            return
        
        # Save the location
        self.settings_manager.save_config(city)
        
        # Get prayer times from API
        try:
            timings, error = self.prayer_fetcher.get_prayer_times(city)
            if error:
                error_label = Gtk.Label(label=f"Error: Could not fetch prayer times\n{str(error)}")
                self.prayer_box.append(error_label)
            else:
                prayer_names = {
                    'Fajr': 'Fajr',
                    'Dhuhr': 'Dhuhr',
                    'Asr': 'Asr',
                    'Maghrib': 'Maghrib',
                    'Isha': 'Isha'
                }
                
                for prayer, display_name in prayer_names.items():
                    time = timings[prayer]
                    label = Gtk.Label()
                    label.set_markup(f"<b>{display_name}:</b> {time}")
                    label.set_xalign(0)
                    self.prayer_box.append(label)
                    self.prayer_labels[prayer] = label
    
        except Exception as e:
            error_label = Gtk.Label(label=f"Error: Could not fetch prayer times\n{str(e)}")
            self.prayer_box.append(error_label)
    
    def check_prayer_times(self):
        current_time = datetime.datetime.now().strftime("%H:%M")
        for prayer, label in self.prayer_labels.items():
            prayer_time = label.get_text().split(": ")[1]
            if current_time == prayer_time:
                self.notifier.show_notification(f"Time for {prayer} prayer")
        return True 
