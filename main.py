from utils import getch, clear
from threading import Thread
from game import Game


class PyroDaemonThread(Thread):
    def __init__(self, engine):
        Thread.__init__(self)
        self.pyroserver=remote.GameServer(engine)
        self.pyrodaemon=Pyro4.Daemon()
        self.ns=Pyro4.locateNS()
        self.setDaemon(True)
        
    def run(self):
        with self.pyrodaemon:
            with self.ns:
                uri=self.pyrodaemon.register(self.pyroserver)
                self.ns.register("example.robotserver", uri)
                print("Pyro server registered on %s" % self.pyrodaemon.locationStr)
                self.pyrodaemon.requestLoop()


if __name__ == '__main__':
    z = Game()
    inp = Input(lambda c: z.move(c))
    out = Output(lambda: z.get())
    try:
        PyroDaemonThread(z).start()
    except Pyro4.errors.NamingError:
        print("Can't find the Pyro Nameserver. Running without remote connections.")

    out.start()
    inp.start()

    # maze = Maze(5, 5)
    # for _ in range(5):
    #     clear()
    #     print maze
    #     # char = getch()
    #     # print (char,)
