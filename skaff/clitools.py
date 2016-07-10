#!/usr/bin/env python3

"""
A suite of command line based tools.
"""
# --------------------------------- MODULES -----------------------------------
import errno
import fcntl
import os
import signal
import sys
import termios

from functools import wraps
# --------------------------------- MODULES -----------------------------------


class ANSIColor:
    RED = "\x1b[31m"
    GREEN = "\x1b[32m"
    YELLOW = "\x1b[33m"
    KHAKI = "\x1b[1;33m"
    BLUE = "\x1b[34m"
    MAGENTA = "\x1b[35m"
    PURPLE = "\x1b[1;35m"
    CYAN = "\x1b[36m"
    BOLD = "\x1b[1m"
    RESET = "\x1b[0m"


class TimeOutError(Exception):
    pass


def timeout(seconds, error_message=os.strerror(errno.ETIME)):
    """Sets a timer on a function; should be used as a decorator.

    Raises 'TimeOutError' upon expiration.
    """
    # Borrowed from stackoverflow:
    # /questions/2281850/timeout-function-if-it-takes-too-long-to-finish
    def decorator(func):
        def _timeout_handle(signum, frame):
            raise TimeOutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _timeout_handle)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator


def getkey():
    """Waits for a single keypress on stdin.

    This is a silly function to call if you need to do it a lot because it has
    to store stdin's current setup, setup stdin for reading single keystrokes
    then read the single keystroke then revert stdin back after reading the
    keystroke.

    Returns the character of the key that was pressed (zero on
    KeyboardInterrupt which can happen when a signal gets handled)

    """
    # Borrowed from stackoverflow:
    # /questions/983354/how-do-i-make-python-to-wait-for-a-pressed-key
    # Windows support is added but not tested.

    if "nt" == os.name:
        import msvcrt
        try:
            ret = msvcrt.getch()
        except KeyboardInterrupt:
            ret = 0
        return ret

    fd = sys.stdin.fileno()
    # save old state
    flags_save = fcntl.fcntl(fd, fcntl.F_GETFL)
    attrs_save = termios.tcgetattr(fd)
    # make raw - the way to do this comes from the termios(3) man page.
    attrs = list(attrs_save)  # copy the stored version to update
    # iflag
    attrs[0] &= ~(termios.IGNBRK | termios.BRKINT | termios.PARMRK
                  | termios.ISTRIP | termios.INLCR | termios. IGNCR
                  | termios.ICRNL | termios.IXON)
    # oflag
    attrs[1] &= ~termios.OPOST
    # cflag
    attrs[2] &= ~(termios.CSIZE | termios. PARENB)
    attrs[2] |= termios.CS8
    # lflag
    attrs[3] &= ~(termios.ECHONL | termios.ECHO | termios.ICANON
                  | termios.ISIG | termios.IEXTEN)
    termios.tcsetattr(fd, termios.TCSANOW, attrs)
    # turn off non-blocking
    fcntl.fcntl(fd, fcntl.F_SETFL, flags_save & ~os.O_NONBLOCK)
    # read a single keystroke
    try:
        ret = sys.stdin.read(1)  # returns a single character
    except KeyboardInterrupt:
        ret = 0
    finally:
        # restore old state
        termios.tcsetattr(fd, termios.TCSAFLUSH, attrs_save)
        fcntl.fcntl(fd, fcntl.F_SETFL, flags_save)
    return ret
