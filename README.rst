screenutils
===========

screenutils is a set of classes that should help handling gnu-screen windows.

Feel free to report any modification you made, the whole code source is
available under the terms of the GPLv2.

Example usage
-------------

Example in a python console::

   >>> from screenutils import list_screens, Screen
   >>> list_screens()
   []
   >>> s= Screen("session1",True)
   >>> # funky prompts could reduce log visibility. Use sh or bash for best results
   >>> s.send_commands('bash')
   >>> s.enable_logs()
   >>> s.send_commands("df")
   >>> print next(s.logs)
   df
   Filesystem           1K-blocks      Used Available Use% Mounted on
   /dev/sda6             20161172   8084052  11052980  43% /
   none                   1505916       304   1505612   1% /dev
   none                   1512676       936   1511740   1% /dev/shm
   none                   1512676       380   1512296   1% /var/run
   none                   1512676         0   1512676   0% /var/lock
   none                   1512676         0   1512676   0% /lib/init/rw
   none                  20161172   8084052  11052980  43% /var/lib/ureadahead/debugfs
   /dev/sda7            403567768 196284216 186783420  52% /home
   popi@popi-laptop:~/Dev/github/screenutils$
   >>> s.disable_logs()
   >>> s = None
   >>> s = Screen("session1")
   >>> s.exists
   True
   >>> s2 = Screen("session2")
   >>> s2.exists
   False
   >>> s2.initialize()
   >>> s2.exists
   True
   >>> list_screens()
   [<Screen 'session2'>, <Screen 'session1'>]
   >>>


Installation
-------------

You could install screenutils from github, by doing the following::

    $ pip install git+http://github.com/Christophe31/screenutils.git

Or by just using the packages published on Pypi, for instance with pip::

    $ pip install screenutils

Features
---------

* screens listing
* screen session creation
* screen session closing
* screen code insertion
* screen monitoring/logging
* screen session sharing with unix users (see below)

Core Documentation
------------------

**Screen class**:

* ``Screen(name, initialize=False)`` Create a new screen.

  - ``name`` (required): The name associated with the screen.

  - ``initialize``: If True, creates a screen session if it does not exists.

* ``screen.id`` (property) the id of the screen as a string.
* ``screen.status`` (property) the status of the screen as a string.
* ``screen.exists`` (property) True if the screen exists (has been initialized)

  - NOTE: ``.id``, ``.status``, ``.exists`` are all based off of the output of ``screen -ls``

* ``screen.initialize`` Initialize a screen if does not exists yet. Equivalent to running ``screen -UR screen_name``
* ``screen.enable_logs()`` turns Screen's logging on. The Logfile's name is automatically set to that of the ``Screen`` object.
* ``screen.log`` A generator that acts like ``tailF`` on the logfile.
* ``screen.disable_logs()`` turns logging off.
* ``screen.kill()`` Quit the screen. Equivalent to running ``screen -x screen_name -X quit``
* ``screen.detach()`` Detach from the screen.
* ``screen.send_commands(*commands)`` send bash commands to the screen.

  - ``*commands`` the command(s) to run (as a string).

* ``screen.add_user_access(unix_user_name)`` Allow another user to access the screen.

  - ``unix_user_name`` (required): the unix name of the user to add.

  - \*NOTE: to allow this feature, you will **need** to change some unix rights:

    + ``sudo chmod +s /usr/bin/screen``

    + ``sudo chmod 755 /var/run/screen``

**Functions** :

* ``list_screens()`` list screens. Returns a list of ``Screen`` instances.

**Exceptions** :

* ``ScreenNotFoundError``: Raised when a screen wasn't found.

Known issues
-------------

This may not work properly with bpython.

Roadmap
--------

* multi windows screen support
