
Quick Start
============

----

.. image:: _static/pics/robinyell.jpg

Importing and Logging In
------------------------

The first thing you will need to do is to import Robin Stocks by typing:

>>> import robin_stocks

robin_stocks will need to added as a preface to every function call in the form of ``robin_stocks.function``.
If you don't want to have to type robin_stocks at the beginning of every call,
then import Robin Stocks by typing

>>> from robin_stocks import *

Keep in mind that this method is not considered good practice as it obfuscates the distinction between Robin Stocks'
functions and other functions. For the rest of the documentation, I will assume that Robin Stocks was imported as ``import robin_stocks``.

Once you have imported Robin Stocks, you will need to login in order to store an authentication token using

>>> robin_stocks.login(<username>,<password>)

Not all functions require authentication, but its good practice to log in to Robinhood at the beginning of your script.


Building Profile and User Data
------------------------------

The two most useful functions are ``build_holdings`` and ``build_user_profile``. These condense information from several
functions into a single dictionary. If you wanted to view all your holdings then type:

>>> my_stocks = robin_stocks.build_holdings()
>>> for key,value in my_stocks.items():
>>>     print(key,value)
