# -*- coding:utf-8 -*-
#
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the GNU Public License 2 or upper.
# Please ask if you wish a more permissive license.

from screenutils.errors import ScreenNotFoundError

try:
    from commands import getoutput
except:
    from subprocess import getoutput
from threading import Thread
from os import system
from os.path import getsize
from time import sleep


def tailf(file_):
    """Each value is content added to the log file since last value return"""
    last_size = getsize(file_)
    while True:
        cur_size = getsize(file_)
        if (cur_size != last_size):
            f = open(file_, 'r')
            f.seek(last_size if cur_size > last_size else 0)
            text = f.read()
            f.close()
            last_size = cur_size
            yield text
        else:
            yield ""


def list_screens():
    """List all the existing screens and build a Screen instance for each
    """
    list_cmd = "screen -ls"
    return [
                Screen(".".join(l.split(".")[1:]).split("\t")[0])
                for l in getoutput(list_cmd).split('\n')
                if "\t" in l and ".".join(l.split(".")[1:]).split("\t")[0]
            ]


class Screen(object):
    """Represents a gnu-screen object::

        >>> s=Screen("screenName", initialize=True)
        >>> s.name
        'screenName'
        >>> s.exists
        True
        >>> s.state
        >>> s.send_commands("man -k keyboard")
        >>> s.kill()
        >>> s.exists
        False
    """

    def __init__(self, name, initialize=False):
        self.name = name
        self._id = None
        self._status = None
        self.logs = None
        self._logfilename = None
        if initialize:
            self.initialize()

    @property
    def id(self):
        """return the identifier of the screen as string"""
        if not self._id:
            self._set_screen_infos()
        return self._id

    @property
    def status(self):
        """return the status of the screen as string"""
        self._set_screen_infos()
        return self._status

    @property
    def exists(self):
        """Tell if the screen session exists or not."""
        # Parse the screen -ls call, to find if the screen exists or not.
        #  "	28062.G.Terminal	(Detached)"
        lines = getoutput("screen -ls").split('\n')
        return self.name in [".".join(l.split(".")[1:]).split("\t")[0]
                             for l in lines if self.name in l]

    def enable_logs(self, filename=None):
        if filename is None:
            filename = self.name
        self._screen_commands("logfile " + filename, "log on")
        self._logfilename = filename
        open(filename, 'w+')
        self.logs = tailf(filename)

    def disable_logs(self, remove_logfile=False):
        self._screen_commands("log off")
        if remove_logfile:
            system('rm ' + self._logfilename)
        self.logs = None

    def initialize(self):
        """initialize a screen, if does not exists yet"""
        if not self.exists:
            self._id = None
            # Detach the screen once attached, on a new tread.
            Thread(target=self._delayed_detach).start()
            # support Unicode (-U),
            # attach to a new/existing named screen (-R).
            system('screen -UR ' + self.name)

    def interrupt(self):
        """Insert CTRL+C in the screen session"""
        self._screen_commands("eval \"stuff \\003\"")

    def kill(self):
        """Kill the screen applications then close the screen"""
        self._screen_commands('quit')

    def detach(self):
        """detach the screen"""
        self._check_exists()
        system("screen -d " + self.id)

    def send_commands(self, *commands):
        """send commands to the active gnu-screen"""
        self._check_exists()
        for command in commands:
            self._screen_commands('stuff "' + command + '" ',
                                  'eval "stuff \\015"')

    def add_user_access(self, unix_user_name):
        """allow to share your session with an other unix user"""
        self._screen_commands('multiuser on', 'acladd ' + unix_user_name)

    def _screen_commands(self, *commands):
        """allow to insert generic screen specific commands
        a glossary of the existing screen command in `man screen`"""
        self._check_exists()
        for command in commands:
            system('screen -x ' + self.id + ' -X ' + command)
            sleep(0.02)

    def _check_exists(self, message="Error code: 404."):
        """check whereas the screen exist. if not, raise an exception"""
        if not self.exists:
            raise ScreenNotFoundError(message, self.name)

    def _set_screen_infos(self):
        """set the screen information related parameters"""
        if self.exists:
            line = ""
            for l in getoutput("screen -ls").split("\n"):
                if (
                        self.name in l and
                        self.name == ".".join(
                            l.split('\t')[1].split('.')[1:]) in l):
                    line = l
            if not line:
                raise ScreenNotFoundError("While getting info.", self.name)
            infos = line.split('\t')[1:]
            self._id = infos[0].split('.')[0]
            if len(infos) == 3:
                self._date = infos[1][1:-1]
                self._status = infos[2][1:-1]
            else:
                self._status = infos[1][1:-1]

    def _delayed_detach(self):
        sleep(0.5)
        self.detach()

    def __repr__(self):
        return "<%s '%s'>" % (self.__class__.__name__, self.name)
