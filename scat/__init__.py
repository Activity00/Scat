

class ScatObjectSingleton:
    def __init__(self):
        self.root = None
        self.web_root = None
        self.remote = {}
        self.net = None

        self.remote_map = {}  # for master mapping remote

ScatObject = ScatObjectSingleton()
