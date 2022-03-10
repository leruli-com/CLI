|computelogo| Leruli Compute
============================

.. hint:: Please feel free to `✎ improve this page <https://github.com/leruli-com/CLI/edit/master/docs/compute.rst>`_ or to `🕮 ask questions about this page <https://github.com/leruli-com/CLI/discussions>`_.

.. |computelogo| image:: _static/images/server-solid.png
  :width: 30
  :alt: compute logo


API Access
##########


See Leruli Queue: API Access.

Set-Up and Security
####################


You will be provided with a group token, and an admin API secret. If you opted to use Leruli storage, you will also receive a S3 access token, a S3 secret and a S3 server URL; otherwise please consult with your provider of S3 storage to obtain these tokens. To get started, add the following to your '~/.bashrc' (or similar):


.. code-block:: bash

    export LERULI_API_SECRET="<your API secret>"
    export LERULI_S3_ACCESS="<your S3 access token>"
    export LERULI_S3_SECRET="<your S3 secret>"
    export LERULI_S3_SERVER="<your S3 server name"


When setting up storage, make sure the S3 object storage does not allow listing all buckets, since the security model of input and output data is designed around unguessable bucket names. Depending on your threat model, it might be acceptable to share S3 credentials within one group, as accessing other user's data requires knowledge of the corresponding bucket. This is the assumption if you obtain S3 storage from Leruli.

User management
###############


See Leruli Queue: User management

Software management
###################

See Leruli Queue: Software management

Support
########


Please file any issues you observe by sending an email to info@leruli.com quoting any involved job ids. Never share your API secret or other credentials with us or colleagues.
