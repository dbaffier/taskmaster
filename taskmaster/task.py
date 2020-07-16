

class Task:
    def __init__(self):
        self.jobs = dict()
        self.process = dict()
        self.queue = dict()
        self.lst_pid = list()
        self.old_fd = list()
        self.fds = list()
        self.prg_fds = dict()