.. You should enable this project on travis-ci.org and coveralls.io to make
   these badges work. The necessary Travis and Coverage config files have been
   generated for you.

.. image:: https://travis-ci.org/pdekraker-epa/ckanext-relationshipdisplay.svg?branch=master
    :target: https://travis-ci.org/pdekraker-epa/ckanext-relationshipdisplay

.. image:: https://coveralls.io/repos/pdekraker-epa/ckanext-relationshipdisplay/badge.svg
  :target: https://coveralls.io/r/pdekraker-epa/ckanext-relationshipdisplay

=============
ckanext-relationshipdisplay
=============

.. Put a description of your extension here:
   What does it do? What features does it have?
   Consider including some screenshots or embedding a video!


------------
Requirements
------------

For example, you might want to mention here which versions of CKAN this
extension works with.


------------
Installation
------------

.. Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

To install ckanext-relationshipdisplay:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-relationshipdisplay Python package into your virtual environment::

     pip install ckanext-relationshipdisplay

3. Add ``relationshipdisplay`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


---------------
Config Settings
---------------

Document any optional config settings here. For example::

    # The minimum number of hours to wait before re-checking a resource
    # (optional, default: 24).
    ckanext.relationshipdisplay.some_setting = some_default_value


------------------------
Development Installation
------------------------

To install ckanext-relationshipdisplay for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/pdekraker-epa/ckanext-relationshipdisplay.git
    cd ckanext-relationshipdisplay
    python setup.py develop
    pip install -r dev-requirements.txt


-----------------
Running the Tests
-----------------

To run the tests, do::

    nosetests --nologcapture --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.relationshipdisplay --cover-inclusive --cover-erase --cover-tests
