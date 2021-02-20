TD Ameritrade Functions
=======================

----

.. note::

  Even though the functions are written as ``robin_stocks.module.function``, the module
  name is unimportant when calling a function. Simply use ``robin_stocks.function`` for all functions.

Sending Requests to API
-----------------------

----

.. automodule:: robin_stocks.tda.helper
   :members: request_get,request_post

Logging In and Authentication
-----------------------------

----

.. automodule:: robin_stocks.tda.authentication
   :members: login_first_time, login, generate_encryption_passcode, 

Getting Stock Information
--------------------------

----

.. automodule:: robin_stocks.tda.stocks
   :members:

Placing and Cancelling Orders
-----------------------------

----

.. automodule:: robin_stocks.tda.orders
   :members:


Getting Account Information
---------------------------

----

.. automodule:: robin_stocks.tda.accounts
   :members:


Getting Market Information
--------------------------

----

.. automodule:: robin_stocks.tda.markets
   :members: