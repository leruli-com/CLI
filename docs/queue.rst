==========
Leruli-Queue
==========

API access
########

Every group of users (e.g. a research group or a division within a company) has a *group token*, which is meant to be shared within the group, but not outside thereof. Every user within the group has an API secret, which is only to be known by that one user and must not be shared with other users (within or outside the group). These tokens serve different purposes: while the group token allows to see group activity (read access), the API secret is required to create new (chargable) tasks or calculations (write access).

There are two kinds to users:

- Regular users: They can see group activity, start new jobs, cancel their own jobs, delete their own data.
- Admin users: Everything a regular user can do plus adding new users (also admin users), and canceling other user's jobs as well as deleting their data (pruning), rotating the compute secret. We suggest to work as regular users on a daily basis.

Storage is provided as S3 object storage, for which the server address, the access token and the secret token need to be available. If own S3 storage is used in the context of Leruli Queue / Leruli Compute, these tokens do *not* need to be available to Leruli, i.e. we do not have read or write access to your data.

In total, the following environment variables should be defined for every user wishing to interact with the paid features of leruli via our command line applications: LERULI_API_SECRET, LERULI_S3_ACCESS, LERULI_S3_SECRET, LERULI_S3_SERVER. If you prefer to implement your own client tools, you can either use our python module *leruli* or interface the API directly via https://api.leruli.com

Set-Up and Security
########

See Leruli Compute: Set-Up and Security.

Additionally, there is the *compute secret*. Everybody who has that compute secret, can provide additional compute resources over which the jobs of the group will be distributed. Should somebody with access to the compute secret leave the group, we suggest to rotate that token, as otherwise the compute secret could be used to produce failed jobs. Since the S3 object storage is not accessible for the user who left the group, both input and output data are protected even without rotation of the secret. This compute secret together with the group token enters the configuration file on each compute node you wish to add.

Setting a compute secret and rotating it is identical:

.. code-block:: bash

    curl -X POST ... example here

Take that token and place it in the configuration file for the client.

When setting up storage, make sure the S3 object storage does not allow listing all buckets, since the security model of input and output data is designed around unguessable bucket names. Depending on your threat model, it might be acceptable to share S3 credentials within one group, as accessing other user's data requires knowledge of the corresponding bucket.

User management
########

To create a new user (i.e. API token), use

.. code-block:: bash

    curl -X POST ... example here

where name should be the identifier allowing you to revoke an API secret in the future, e.g. if a machine gets stolen or a user leave the group. Note that you cannot retrieve the API token again except for the first call.

To disable access for a user, use

.. code-block:: bash

    curl -X POST ... example here

which will be effective immediately. Their corresponding jobs and data will be kept (and executed if still queueing). Any admin user has access to them. Note that you cannot delete the last admin user token.


Adding a Node
########

Docker
**********

The containerized solution of the Leruli-Queue is enabled through rootless Docker.

.. caution:: In order for rootless Docker to work, any rootful Docker solution on the system has to be uninstalled.


Additionally, check whether any other rootless Docker deamon is running with

.. code-block:: bash

    ps -u $USER | grep docker

Stop the Docker deamon via

.. code-block:: bash

    systemctl --user stop docker

You are now ready to set up the compute node!

Creating a Compute User (as root)
********************

To have a homogenous setup across different nodes, the easiest
is to add a new user under which all computations will be executed.

.. important:: You need sudo rights in order to add a new user to your system. Before you start with the process, login as root via `sudo su -`

You can add a new user via the `useradd` command:

.. code-block:: bash

    sudo useradd -m -s /bin/bash -u 2013 leruli

This automatically creates a home directory for the new user `leruli` which is required for a succesful installation.

.. hint:: Don't forget to add a password to the new user via `sudo passwd leruli`

Next, a directory in which all computations will be executed is required.
Create such a directory via:

.. code-block:: bash

    sudo mkdir -p /data/leruli/nomad

.. hint:: Don't forget to change the ownership to the user leruli via `sudo chown leruli:leruli /data/leruli/ -R`

Finally, add the following two lines to the `.bashrc` of the user leruli in `/home/leruli/.bashrc`:

.. code-block:: bash

    export XDG_RUNTIME_DIR="/run/user/$UID"
    export DBUS_SESSION_BUS_ADDRESS="unix:path=${XDG_RUNTIME_DIR}/bus"


With the compute user `leruli` set up, we are now ready to finally connect the node to the scheduler.

Software Setup (as user leruli)
******************

First, login as the new compute user `leruli`


.. code-block:: bash

    su - leruli


Next, download and unpack the provided setup package via:

.. code-block:: bash

    # Copy package from workstation Carbon (user: leruli, pw:leruli)
    scp c:/tmp/leruli/nomadrun.tar .
    tar -xf nomadrun.tar

This setup package contains all required config files that are needed in order to
connect the node to the scheduler.

Run the `get-started.sh` script to download `nomad`, `rootless docker` and `minio`. In the last step, the script
will start the docker deamon.

Check whether Docker is actually running via

.. code-block:: bash

    ps -u $USER | grep docker

.. caution:: If you experience any issues with starting Docker via systemctl, please either freshly login or create a new ssh connection of the new `leruli` user.  A simple `su - leruli` might lead to problems.


Connecting the Node (as root)
******************

In order to connect the node, switch to `root` via

.. code-block:: bash

     sudo su -

To allow the scheduler-node communications to run in the background, we start a new screen session via:

.. code-block:: bash

     screen -S node

.. hint:: `Screen` is a terminal multiplexer which allows us to run commands in a virtual console. If you don't have `screen` installed you can do so via `sudo apt install screen`.

To connect the node, run our `run.sh` script contained in the setup package via:

.. code-block:: bash

     bash run.sh

The console should now show some logs in which the node communicates with the scheduler.
If the connection was not succesful, you will see the command line prompt again. If that is not the case, the connection was succesful and you can disconnect from the screen session by pressing `control+a+d`.

Congratulations! Your node is now connected to the scheduler.

Software management
########

All software is run from containers. You can prepare a new container with a local docker environment on your machine (rootless docker is sufficient). Docker containers provide a reproducible way of packaging software in a manner that does not interfere with the host operating system. This allows you to package software even if we do not have access to the source. A docker container is defined by a Dockerfile, which is similar in spirit to a bash script setting up the environment. There are numerous resources how to build a docker container, e.g. TUTORIALS HERE. Note that we do not provide support for writing Dockerfiles, except for cases once a Dockerfile you prepared that runs on your computer does not work via Leruli, we will help.

The requirements of Dockerfiles suitable for Leruli are:

* Tagged with name:version. We use this information internally to select the correct image to run from.
* Working directory is `/rundir` within the container, i.e. the input files and output files are expected to be in that folder. This means that all docker containers are considered to be executed in a directory with your input files. The input files are then made available via a mount into the container. For testing purposes, you can get the same behavior on your machine with

.. code-block:: bash

    docker -v $(pwd):/rundir


* You can rely on `OMP_NUM_THREADS` and similar variables being set to respect the core limits upon job submission.
* You may not use the following filenames for input or output files as they have special meaning: *run.sh*, *joblog.txt*, *joberr.txt*

We provide a number of preconfigured software packages already prepared for use with Leruli:

* crest:2.11.2
* Psi4:1.5

We will make them available for you during onboarding.

Job Submission
########


- command line stuff
- submit
- status
- get
- purge


Support
########

Please file any issues you observe by sending an email to info@leruli.com quoting any involved job ids. Never share your API secret or other credentials with us or colleagues.
