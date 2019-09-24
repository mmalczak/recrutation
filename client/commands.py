import threading
import cmd
import sys


class CommandsThread(threading.Thread):

    def __init__(self, cmd):
        threading.Thread.__init__(self)
        self.cmd = cmd

    def run(self):
        self.cmd.cmdloop()


class Commands(cmd.Cmd):

    def __init__(self, logger):
        super(Commands, self).__init__()
        self.logger = logger

    def do_bleble(self, line):
        print("bleblebla")

    def do_h(self, line):
        print("dupa")
        self.logger.setLevel('WARNING')

    def do_s(self, line):
        self.logger.setLevel('INFO')

    def do_exit(self, line):
        sys.exit()
