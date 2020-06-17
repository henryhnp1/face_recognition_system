import types
import os
import os.path
import imp

class PluginMeta(type):
    def __new__(cls, name, bases, dct):
        modules = [imp.load_source(filename, os.path.join(dct['plugindir'], filename))
                    for filename in os.listdir(dct['plugindir']) if filename.endswith('.py')]
        for module in modules:
            for name in dir(module):
                function = getattr(module, name)
                if isinstance(function, types.FunctionType):
                    dct[function.__name__] = function
        return type.__new__(cls, name, bases, dct)
