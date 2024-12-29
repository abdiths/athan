import requests

class PrayerTimeFetcher:
    def get_prayer_times(self, city):
        try:
            response = requests.get(f'http://api.aladhan.com/v1/timingsByCity',
                                    params={'city': city, 'country': '', 'method': 2})
            data = response.json()
            timings = data['data']['timings']
            return timings, None
        except Exception as e:
            return None, e
