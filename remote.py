import Pyro4

ids = [0]

@Pyro4.expose
class RemoteClient(object):
    def __init__(self):
        self.id = ids[0]
        ids[0] += 1
        self.x, self.y = 0, 0
        self.listeners = []

    def change_direction(self, direction):
        print(direction)
        self.x, self.y = direction

    def send_msg(self, frm, msg):
        print("msg to:", self.id)
        print("msg from:", frm)
        print("msg text:", text)

    def append_listener(self, listener_uri):
        self.listeners.append(listener_uri)

    def start(self):
        print('Started')
        for listener in self.listeners:
            Pyro4.Proxy(listener).send_msg(self.id, "hey, i miss you")
