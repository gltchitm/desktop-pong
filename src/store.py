class Store:
    def __init__(self):
        self.values = {}
        self.hooks = {}
    def __setitem__(self, key, value):
        if key == 'hooks':
            raise KeyError('cannot set key "hooks"')

        if not key in self.hooks:
            self.hooks[key] = []

        self.values[key] = value
        for callback in self.hooks[key]:
            callback(value)
    def __getitem__(self, key):
        if key == 'hooks':
            class Hooks:
                def __setitem__(_, key, callback):
                    self.hooks[key].append(callback)

            return Hooks()
        elif key in self.values:
            return self.values[key]

store = Store()
