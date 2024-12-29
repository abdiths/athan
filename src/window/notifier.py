import os

class Notifier:
    def show_notification(self, message):
        os.system(f'notify-send "Athan" "{message}"')
