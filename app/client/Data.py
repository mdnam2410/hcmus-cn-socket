class Data(object):
    def __init__(self) -> None:
        super().__init__()
        self.mac_addr = None
        self.ip_addr = None
        self.port = None
        self.process = []
        self.app = []
        self.image = None
        self.path = ['']
        self.listF = [[]]
        self.currentF = None