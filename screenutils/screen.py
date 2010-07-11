# -*- coding:utf-8 -*-
#
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the GNU Public License 2 or upper.
# Please ask if you wish a more permissive license.

from commands import getoutput
from threading import Thread
from os import system
from time import sleep

from errors import ScreenNotFoundError

def list_screens():
    """List all the existing screens and build a Screen instance for each
    """
    return [Screen(".".join(l.split(".")[1:]).split("\t")[0])
                for l in getoutput("screen -ls | grep -P '\t'").split('\n')]


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
        # The screen -ls | grep name returns something like that:
        #  "	28062.G.Terminal	(Detached)"
        lines = getoutput("screen -ls | grep " + self.name).split('\n')
        return self.name in [".".join(l.split(".")[1:]).split("\t")[0]
                             for l in lines]

    def initialize(self):
        """initialize a screen, if does not exists yet"""
        if not self.exists:
            # Detach the screen once attached, on a new tread.
            Thread(target=self._delayed_detach).start()
            # support Unicode (-U),
            # attach to a new/existing named screen (-R).
            system('screen -UR ' + self.name)

    def interrupt(self):
        """Insert CTRL+C in the screen session"""
        self._check_exists()
        system("screen -x " + self.name + " -X eval \"stuff \\003\"")

    def kill(self):
        """Kill the screen applications then close the screen"""
        self._check_exists()
        system('screen -x ' + self.name + ' -X quit')

    def detach(self):
        """detach the screen"""
        self._check_exists()
        system("screen -d " + self.name)

    def _delayed_detach(self):
        sleep(0.5)
        self.detach()

    def send_commands(self, *commands):
        """send commands to the active gnu-screen"""
        self._check_exists()
        for command in commands:
            sleep(0.02)
            system('screen -x ' + self.name + ' -X stuff "' + command + '" ')
            sleep(0.02)
            system('screen -x ' + self.name + ' -X eval "stuff \\015" ')

    def _check_exists(self, message="Error code: 404"):
        """check whereas the screen exist. if not, raise an exception"""
        if not self.exists:
            raise ScreenNotFoundError(message)

    def _set_screen_infos(self):
        """set the screen information related parameters"""
        if self.exists:
            infos = getoutput("screen -ls | grep %s" % self.name).split('\t')[1:]
            self._id = infos[0].split('.')[0]
            self._date = infos[1][1:-1]
            self._status = infos[2][1:-1]

    def __repr__(self):
        return "<%s '%s'>" % (self.__class__.__name__, self.name)

