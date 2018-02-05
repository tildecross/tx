from sandbox import Sandbox

#####
#
# Framework for modular design and message passing
#
#####

class Core:
    def __init__(self, debug=False):
        self.modules = dict()
        self.extensions = dict()
        self.sandbox = Sandbox(self)
        self.debug = debug
        
    # Add extension (callable object or function) to Core
    def extend(self, name, fn):
        if name not in self.extensions:
            self.extensions[name] = fn
        else:
            if self.debug:
                print("Error: '%s' already exists in extensions" % name)
        
    # Accessor function for extensions
    def get_extension(self, extension):
        return self.extensions.get(extension, None)
    
    # Register module to Core
    def register(self, name, fn):
        if name not in self.modules:
            self.modules[name] = {
                "fn": fn,
                "instance": None
            }
            return self.modules[name]
        else:
            if self.debug:
                print("Error: '%s' already exists in modules" % name)
            return None
    
    # Start module under name
    def start(self, name, deps=None, args=None):
        module = self.modules.get(name, None)
        if module is not None:
            if deps is not None and isinstance(deps, list):
                for dep in deps:
                    dep()
            module["instance"] = module["fn"](self.sandbox)
            if "create" in dir(module["instance"]):
                if args is not None:
                    return module["instance"].create(*args)
                return module["instance"].create()
            return module["instance"]
        else:
            if self.debug:
                print("Error: '%s' does not exist in modules" % name)
        return None
        
    # Stop module under name
    def stop(self, name):
        module = self.modules.get(name, None)
        if module is not None:
            instance = module.get("instance", None)
            if instance is not None:
                if "remove" in dir(instance):
                    module["instance"].remove()
                    module["instance"] = None
        else:
            if self.debug:
                print("Error: '%s' does not exist in modules" % name)
