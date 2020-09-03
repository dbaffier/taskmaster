Supervisor
==========

Supervisor is a client/server system that allows its users to
control a number of processes on UNIX-like operating systems.

Running Supervisor
==================

You should have python3 ready to go.
``` python3 server.py <config_file> ```

Adding a Program
----------------

Before :program:`taskmasterd` will do anything useful for you, you'll
need to add at least one ``program`` section to its configuration.
The ``program`` section will define a program that is run and managed
when you invoke the :command:`taskmasterd` command.

One of the simplest possible programs to run is the UNIX
:program:`cat` program.  A ``program`` section that will run ``cat``
when the :program:`supervisord` process starts up is shown below.

.. code-block:: ini

   [program:foo]
   command=/bin/cat
