"""Errors for the screenutils module"""

class ScreenNotFoundError(Exception):
    """raised when the screen does not exists"""
    def __init__(self, message, screen_name):
        message += " Screen \"{0}\" not found".format(screen_name)
        self.screen_name = screen_name
        super(ScreenNotFoundError, self).__init__(message)
