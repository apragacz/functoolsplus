def new_singleton(cls):
    if not hasattr(cls, '__instance__'):
        cls.__instance__ = object.__new__(cls)
    return cls.__instance__


class MissingType(object):

    def __new__(cls):
        return new_singleton(cls)


Missing = MissingType()
