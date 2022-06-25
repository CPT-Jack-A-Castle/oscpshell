import json


def persist_to_file(file_name):
    # https://stackoverflow.com/questions/16463582/memoize-to-disk-python-persistent-memoization
    def decorator(original_func):
        try:
            cache = json.load(open(file_name, 'r'))
        except (IOError, ValueError):
            cache = {}

        def new_func(param):
            if param not in cache:
                cache[param] = original_func(param)
                json.dump(cache, open(file_name, 'w'))
            return cache[param]

        return new_func

    return decorator


class Memoize:
    # https://python-course.eu/advanced-python/memoization-decorators.php
    def __init__(self, fn):
        self.fn = fn
        self.memo = {}

    def __call__(self, *args):
        if args not in self.memo:
            self.memo[args] = self.fn(*args)
        return self.memo[args]
