|queuelogo| Leruli Queue
========================

.. note:: Please feel free to `✎ improve this page <https://github.com/leruli-com/CLI/edit/master/docs/queue.rst>`_ or to `🕮 ask questions about this page <https://github.com/leruli-com/CLI/discussions>`_.

.. |queuelogo| image:: _static/images/boxes-stacked-solid.png
  :width: 30
  :alt: queue logo

Leruli Queue conceptually is an alternative to job schedulers like SLURM. The main difference is the focus on scalibility and intake of tens of thousands of jobs at once. Whatever you can run under Linux, you likely can run via Leruli Queue on hundreds of machines in parallel. 


Getting Started
###############

To make the best use of our software, we suggest the following workflow: any individual calulation with all input and (later) output files is a single folder. Since the input files need to be distributed to the compute nodes, it is required to only store actually needed input files in this folder at time of submission. In the following, we run a psi4 calculation via Leruli Queue.

First, we need the `leruli` command line tool:

.. code-block:: bash

    pip install -U leruli

Since the calculations will consume resources, we need to authenticate. This is achieved by adding the following lines to your `~/.bashrc` file:

.. code-block:: bash

    export LERULI_API_SECRET=<your API secret>
    export LERULI_S3_SERVER=<your S3 server>
    export LERULI_S3_ACCESS=<your S3 access>
    export LERULI_S3_SECRET=<your S3 secret>

You should have been provided with the credentials by the point-of-contact in your group. If you are new to Leruli, please get in touch via info@leruli.com to obtain an API secret. Now we set up the actual calculation. Create a new folder and define a psi4 input file within that folder:

.. code-block:: bash

    make test
    cd test
    echo "molecule{
    o
    h 1 roh
    h 1 roh 2 ahoh

    roh = 0.957
    ahoh = 104.5
    }

    set basis cc-pVDZ
    set ccenergy print 3
    set scf print 1
    energy('ccsd')" > input.dat

Normally, you would run `psi4` as follows (if it were installed on your machine):

.. code-block:: bash

    psi4 input.dat

Now to run it in the cloud on Leruli, instead you run

.. code-block:: bash

    leruli task-submit psi4 1.5 psi4 input.dat

This tells leruli to run the command `psi4 input.dat` with the data from the current directory using the code `psi4` in version 1.5. If you run the command, new files are created in your directory: `leruli.job` contains the job id, a unique identifier of the submission. It is guaranteed to be unique across all submissions from all users. The other file is `leruli.bucket` which contains the folder in a distributed storage system where your input files have been copied to and where the compute node will download them. You can monitor the progress of the calculation by running

.. code-block:: bash

    leruli task-status

Which will print "received" (the calculation has been accepted but is too far down the queue), "submitted" (the calculation is towards the head of the queue and is likely to start soon), "running" (some node is working on it right now), or "completed" (the job is done and the results have been uploaded to the distributed storage). Which result you are shown depends on how quickly you ran `leruli status` after submission. Once the output is `completed`, you can download the results from the distributed storage to your computer. This is done with

.. code-block:: bash

    leruli task-get

If you check the directory contents now, you will find all the output files as if you had run `psi4` directly in this directory on your computer. Please note that the results are still available on the distributed storage system in case you want to downlaod them again, e.g. to share them with colleagues. To clean them up, run

.. code-block:: bash

    leruli task-purge

This step is not reversible: once deleted from the distributed storage, the results and input files are not available for download and cannot be reconstructed. Purging the task does not affect your downloaded copy of the data.

It is important that you run all these commands in the same directory, as the `leruli.job` file is used to figure out which job this is about. While advanced usage allows you to access jobs from other directories and other tricks, this goes beyond the initial getting started. Please refer to the detailed documentation of the Leruli CLI for all options.

API access
##########

Every group of users (e.g. a research group or a division within a company) has a *group token*, which is meant to be shared within the group, but not outside thereof. Every user within the group has an API secret, which is only to be known by that one user and must not be shared with other users (within or outside the group). These tokens serve different purposes: while the group token allows to see group activity (read access), the API secret is required to create new (chargable) tasks or calculations (write access).

There are two kinds to users:

- Regular users: They can see group activity, start new jobs, cancel their own jobs, delete their own data.
- Admin users: Everything a regular user can do plus adding new users (also admin users), and canceling other user's jobs as well as deleting their data (pruning), rotating the compute secret. We suggest to work as regular users on a daily basis.

Storage is provided as S3 object storage, for which the server address, the access token and the secret token need to be available. If own S3 storage is used in the context of Leruli Queue / Leruli Compute, these tokens do *not* need to be available to Leruli, i.e. we do not have read or write access to your data.

In total, the following environment variables should be defined for every user wishing to interact with the paid features of leruli via our command line applications: LERULI_API_SECRET, LERULI_S3_ACCESS, LERULI_S3_SECRET, LERULI_S3_SERVER. If you prefer to implement your own client tools, you can either use our python module *leruli* or interface the API directly via https://api.leruli.com

Set-Up and Security
###################

See Leruli Compute: Set-Up and Security.

Additionally, there is the *compute secret*. Everybody who has that compute secret, can provide additional compute resources over which the jobs of the group will be distributed. Should somebody with access to the compute secret leave the group, we suggest to rotate that token, as otherwise the compute secret could be used to produce failed jobs. Since the S3 object storage is not accessible for the user who left the group, both input and output data are protected even without rotation of the secret. This compute secret together with the group token enters the configuration file on each compute node you wish to add.

Setting a compute secret and rotating it is identical:

.. code-block:: bash

    curl -X POST "https://api.leruli.com/v22_1/group-rotate-compute-secret" \
         -H "Accept: application/json" -H "Content-Type: application/json" \
         -d '{"adminsecret":"ADMINSECRETHERE"}'

where `ADMINSECRETHERE` is your admin secret. Take that token and place it in the configuration file for the client.

When setting up storage, make sure the S3 object storage does not allow listing all buckets, since the security model of input and output data is designed around unguessable bucket names. Depending on your threat model, it might be acceptable to share S3 credentials within one group, as accessing other user's data requires knowledge of the corresponding bucket.

User management
###############

To create a new user (i.e. API token), use

.. code-block:: bash

    curl -X POST "https://api.leruli.com/v22_1/group-create-user" \
         -H "Accept: application/json" -H "Content-Type: application/json" \
         -d '{"adminsecret":"ADMINSECRETHERE","name":"USERNAME","admin":false}' 

where name should be the identifier allowing you to revoke an API secret in the future, e.g. if a machine gets stolen or a user leave the group. Note that you cannot retrieve the API token again except for the first call.

To disable access for a user, use

.. code-block:: bash

    curl -X POST "https://api.leruli.com/v22_1/group-revoke-user" \
         -H "Accept: application/json" -H "Content-Type: application/json" \
         -d '{"adminsecret":"string","name":"string"}' 

which will be effective immediately. Their corresponding jobs and data will be kept (and executed if still queueing). Any admin user has access to them. Note that you cannot delete the last admin user token.


Adding a Node
#############

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
**********************************

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

Now, add the following two lines to the `.bashrc` of the user leruli in `/home/leruli/.bashrc`:

.. code-block:: bash

    export XDG_RUNTIME_DIR="/run/user/$UID"
    export DBUS_SESSION_BUS_ADDRESS="unix:path=${XDG_RUNTIME_DIR}/bus"

Finally, enable user lingering for the user `leruli` to enable the startup of the rootless docker daemon later in the procedure.

.. code-block:: bash

    sudo loginctl enable-linger leruli

With the compute user `leruli` set up, we are now ready to finally connect the node to the scheduler.

Software Setup (as user leruli)
*******************************

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
*****************************

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
####################

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
##############


- command line stuff
- submit
- status
- get
- purge


Support
########

Please file any issues you observe by sending an email to info@leruli.com quoting any involved job ids. Never share your API secret or other credentials with us or colleagues.
