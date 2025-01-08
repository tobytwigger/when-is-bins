from playhouse.shortcuts import model_to_dict, dict_to_model
from peewee import Model

class ValueChangeNotifier:
    def __init__(self, value=None, refresh=None):
        self._value = value
        self._refresh = refresh
        self._has_changed = False
        self._observers = []

    @property            # first decorate the getter method
    def value(self): # This getter method name is *the* name
        return self._value

    @value.setter
    def value(self, v):
        if not self._is_equal(v):
            self._value = v
            self._has_changed = True
            self.notify()

    def _is_equal(self, v):
        if isinstance(self._value, list) and isinstance(v, list):
            if all(isinstance(x, Model) for x in self._value) and all(isinstance(y, Model) for y in v):
                return all(model_to_dict(x) == model_to_dict(y) for x, y in zip(self._value, v)) and len(self._value) == len(v)
            return all(x == y for x, y in zip(self._value, v)) and len(self._value) == len(v)
        return self._value == v

    def handle_change(self):
        if self._has_changed:
            self.mark_handled()
            return True

        return False

    def has_changed(self):
        return self._has_changed

    def on_change(self, observer):
        self._observers.append(observer)

    def mark_handled(self):
        self._has_changed = False

    def notify(self):
        for observer in self._observers:
            observer()

    def refresh(self):
        if self._refresh:
            self.value = self._refresh()
