#####
#
# Sandbox is designed to be passed around by Core for communication
#
#####

class Sandbox:
    def __init__(self, core):
        self.core = core
        self.modules = dict()
        
    # Add function to modules to listen to under listener
    def listen(self, listener, fn):
        if listener not in self.modules:
            self.modules[listener] = []
        self.modules[listener].append(fn)
        
    # Remove listener from module under listener
    def silence(self, listener):
        module = self.modules.get(listener, None)
        if module is not None:
            for i in range(len(module)):
                if module[i] == fn:
                    del module[i]
                    break
                    
    # Pass data from notif into listening functions in module under name
    def notify(self, notif):
        name = notif["name"]
        data = notif["data"]
        module = self.modules.get(name, None)
        if module is not None:
            for fn in module:
                fn(data)
                
    # Call extensions from inside modules
    def use(self, extension):
        return self.core.get_extension(extension)
