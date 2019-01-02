from collections import namedtuple

class _Entry(namedtuple('_Entry', 'value next')):
    def _repr_assist(self, postfix):
        r = repr(self.value) + postfix
        if self.next is not None:
            return self.next._repr_assist(', ' + r)
        return r

class Stack(object):
    def __init__(self):
        self.top = None
    def push(self, value):
        self.top = _Entry(value, self.top)
    def pop(self):
        if self.top is None:
            raise ValueError("Can't pop from an empty stack")
        res, self.top = self.top.value, self.top.next
        return res
    def __repr__(self):
        if self.top is None: return '[]'
        return '[' + self.top._repr_assist(']')