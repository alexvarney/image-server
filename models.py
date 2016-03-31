import datetime

class ImageModel:
    def __init__(self, file_url, display_url, shortcode, timestamp=0):
        self.file_url = file_url
        self.display_url = display_url
        self.shortcode = shortcode
        self.timestamp = timestamp

    def get_readable_timestamp(self):
        return datetime.datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M')