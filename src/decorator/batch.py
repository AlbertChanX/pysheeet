import six
import types


def skip(func):
    func.__func_skip__ = True
    return func


def batch_decorate(decorator_func):
    def inner_meta(in_class):
        def collect_attrib(key, value, new_attrs):
            if hasattr(value, '__func_skip__'):
                new_attrs[key] = value
                return
            if hasattr(value, '__func__') or isinstance(value, types.FunctionType):
                if isinstance(value, staticmethod):
                    new_attrs[key] = staticmethod(decorator_func(value.__func__))
                    return
                elif isinstance(value, classmethod):
                    new_attrs[key] = classmethod(decorator_func(value.__func__))
                    return
                elif not key.startswith('__'):
                    new_attrs[key] = decorator_func(value)
                    return
            else:
                if isinstance(value, property):
                    # 当对property类进行重组的时候，我们强制装饰了property类的fget fset和fdel方法。
                    # 但是，不是每个propery都有这三个方法，有些是None，强制装饰会报错，所以我们这里要考虑提前返回None
                    propertyWrapper = property(fget=decorator_func(value.fget) if value.fget else None,
                                               fset=decorator_func(value.fset) if value.fset else None,
                                               fdel=decorator_func(value.fdel) if value.fdel else None,
                                               doc=value.__doc__)
                    new_attrs[key] = propertyWrapper
                    return
            new_attrs[key] = value

        class Meta(type):
            @classmethod
            def options(cls, bases, attrs):
                new_attrs = {}
                for key, value in attrs.items():
                    collect_attrib(key, value, new_attrs)
                for base in bases:
                    for mbase in base.mro():
                        for key, value in mbase.__dict__.items():
                            if key not in new_attrs:
                                collect_attrib(key, value, new_attrs)
                return new_attrs

            def __new__(cls, name, bases, attrs):
                new_attrs = cls.options(bases, attrs)
                return super(Meta, cls).__new__(cls, name, bases, new_attrs)

        return six.add_metaclass(Meta)(in_class)

    return inner_meta
