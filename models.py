import datetime
from typing import Sequence

class Image:
    def __init__(self, file_url, display_url, shortcode, timestamp=0):
        self.file_url = file_url
        self.display_url = display_url
        self.shortcode = shortcode
        self.timestamp = timestamp

    def get_readable_timestamp(self):
        return datetime.datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M')

class TemplateDisplayImage:
    def __init__(self, app_url: str, image_url: str):
        self.app_url = app_url
        self.image_url = image_url

class TemplateListImage:
    def __init__(self, app_url: str, images: Sequence[Image]):
        self.app_url = app_url
        self.images = images