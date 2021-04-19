class Store:
    def __init__(self):
        self.values = {}
        self.hooks = {}
    def set_value(self, key, value):
        if not key in self.hooks:
            self.hooks[key] = []
        self.values[key] = value
        for callback in self.hooks[key]:
            callback(value)
    def get_value(self, key):
        if key in self.values:
            return self.values[key]
    def add_hook_for_key(self, key, callback):
        self.hooks[key].append(callback)
store = Store()
