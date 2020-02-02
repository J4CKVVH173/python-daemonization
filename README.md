# Daemon python process

Class `Daemon` allow to run python script like a daemon process.

To run a process as a daemon you must inherit from `Daemon`. `Daemon` has abstractmethod `daemon`. The code to run in
the background must be placed in the `daemon` method.

The `Daemon` class constructor contains the required parameter `pid_file` which is the path to the storage location of
the file with the daemon's pid. Also the constructor also has parameters for determining the path for the `stdout` and
`stderr` files.

`start` method used to run daemon.
`stop` method used to stop daemon.
`restart` method used to restart daemon.



## Process to background (note)
Calling setsid is usually one of the steps a process goes through when becoming a so called daemon process. (We are talking about Linux/Unix OS).
With setsid the association with the controlling terminal breaks. This means that the process will be NOT affected by a logout.
There are other way how to survive a logout, but the purpose of this 'daemonizing' process is to create a background process as independent from the outside world as possible.
That's why all inherited descriptors are closed; cwd is set to an appropriate directory, often the root directory; and the process leaves the session it was started from.
A double fork approach is generally recommended. At each fork the parent exits and the child continues. Actually nothing changes except the PID, but that's exactly what is needed here.
First fork before the setsid makes sure the process is not a process group leader. That is required for a succesfull setsid.
The second fork after the setsid makes sure that a new association with a controlling terminal won't be started merely by opening a terminal device.

Source [stackoverflow](https://stackoverflow.com/questions/45911705/why-use-os-setsid-in-python)

Краткая суть в том что необходимо создать копию процесса через fork, сделать его максимально независимым от внешнего
мира и создание еще одной копии процесса через fork, это делается для смена PID.