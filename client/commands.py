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

    def __init__(self, logger, queue):
        super(Commands, self).__init__()
        self.logger = logger
        self.queue = queue

    def do_h(self, line):
        self.logger.setLevel('WARNING')

    def do_s(self, line):
        self.logger.setLevel('INFO')

    def do_exit(self, line):
        sys.exit()

    def do_controller_coeff(self, line):
        available_names = ['A', 'B', 'C', 'D', 'K', 'L']
        [name, value] = line.split(';')
        if name in available_names:
            self.queue.put(['set_matrix', name, value])
        else:
            logger.warning("Incorrect matrix name")
