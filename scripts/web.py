import sys
import platform
import builtins

is_web: bool = sys.platform == 'emscripten'
# is_web = True # testing

def _import(name, *args, **kwargs):
    if name == "ujson" and is_web:
        name = "json"
    return builtin_import(name, *args, **kwargs)

def print(*args, **kwargs):
    excludes = [
        "pygame_gui/ui_manager.py",
        "Trying to pre-load font id"
    ]
    if any([str(args).__contains__(exclude) for exclude in excludes]): return 
    if is_web:
        platform.window.console.log(str(object=args))
    return builtin_print(*args, **kwargs)

builtin_print = builtins.print
builtins.print = print

builtin_import = builtins.__import__
builtins.__import__ = _import

def mean(data):
    """Return the sample arithmetic mean of data."""
    n = len(data)
    if n < 1:
        raise ValueError('mean requires at least one data point')
    return sum(data)/n

def median(data):
    """Return the median of the data."""
    data = sorted(data)
    n = len(data)
    if n == 0:
        raise ValueError('median requires at least one data point')
    if n % 2 == 1:
        return data[n//2]
    else:
        i = n//2
        return (data[i - 1] + data[i])/2
    