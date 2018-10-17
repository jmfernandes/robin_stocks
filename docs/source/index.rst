.. robin_stocks documentation master file, created by
   sphinx-quickstart on Tue Oct 16 18:34:53 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to robin_stocks's documentation!
========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

This library aims to create simple to use functions to interact with the
Robinhood API. This is a pure python interface and it requires Python3. The purpose
of this library is to allow people to make their own robo-investors or to view
stock information in real time.

Sending Requests to API
-----------------------

.. automodule:: robin_stocks.helper
   :members: request_get,request_post,request_delete

Logging In and Out
------------------

.. automodule:: robin_stocks.authentication
   :members:

Loading Profiles
------------------

.. automodule:: robin_stocks.profiles
   :members:

Getting Stock Information
-------------------------

.. automodule:: robin_stocks.stocks
   :members:

Getting Option Information
--------------------------

.. automodule:: robin_stocks.options
   :members:

Getting Market Information
--------------------------

.. automodule:: robin_stocks.markets
   :members:

Getting Positions and Account Information
-----------------------------------------

.. automodule:: robin_stocks.account
   :members:

Placing and Cancelling Orders
-----------------------------

.. automodule:: robin_stocks.orders
   :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
