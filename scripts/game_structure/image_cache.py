import pygame
from scripts.file_loader import image_load

_images = {}
def load_image(path):
    """
    If not in the cache already, loads the image from path as a surface.
    Otherwise, the image is retrieved from the cache.
    """
    if path not in _images:
        _images[path] = image_load(path)
    return _images[path]

def clear_cache():
    """Clears the image cache."""
    _images.clear()