class device:
    def __init__(self):
        self.meth = dict() #public methods (interface)
        self.set_vars()
        self.report = "object created"

    def set_vars(self):
        self.type = "Generic Device"
        self.report = "vars created"
        pass

    def do(self, method):
        if method in self.meth:
            self.meth[method]()
        else:
            self.report = "no such method '"+str(method)+"'"

    def get_type(self):
        return self.type

    def get_methods(self):
        self.report = "methods returned"
        return self.meth.keys()

    def add_method(self, method, function):
        self.meth[method] = function
        self.report = str(len(self.meth)) + " method(s) written"

class test(device):
    def set_vars(self):
        self.type = "Generic Test"
        self.add_method("extend",self.retract)
        self.add_method("retract",self.shrink)
        self.add_method("get data",self.getval)
        self.retracted = False
    def retract(self):
        self.retracted = True
        self.report = "Length 1 m"
    def getval(self):
        return self.retracted
    def shrink(self):
        self.retracted = False
        self.report = "Length 0 m"

class door(device):
    def set_vars(self):
        self.type = "Door"
        self.add_method("Open",self.open)
        self.add_method("Close",self.close)
        self.add_method("Check",self.is_open)
        self.state = True
    def open(self):
        self.state = True
        self.report = "Door was opened"
    def close(self):
        self.state = False
        self.report = "Door was closed"
    def is_open(self):
        if self.state:
            self.report = "Door is opened"
        else:
            self.report = "Door is closed"
        return self.state

class antenna(device):
    def set_vars(self):
        self.type = "Antenna"
        self.add_method("Receive",self.get_data)
        self.add_method("Send",self.send_data)
        self.add_method("Activate",self.turn_on)
        self.add_method("Dectivate",self.turn_off)
        self.state = False
    def send_data(self):
        if self.state:
            self.report = "Sended data"
        else:
            self.report = "No power"
    def get_data(self):
        if self.state:
            self.report = "Received data"
        else:
            self.report = "No power"
    def turn_on(self):
        self.state = True
        self.report = "Power on"
    def turn_off(self):
        self.state = False
        self.report = "Power off"

dev_class = ["Don't add device", "Door", "Test", "Antenna"]
def make(dev_name):
    k = None
    if dev_name == "Door":
        k = door()
    elif dev_name == "Test":
        k = test()
    elif dev_name == "Antenna":
        k = antenna()
    return k
