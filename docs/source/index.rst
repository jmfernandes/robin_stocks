.. robin_stocks documentation master file, created by
   sphinx-quickstart on Tue Oct 16 18:34:53 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Robin Stocks: Python Trading on Wall St.
=========================================

-----

.. image:: _static/pics/robin.jpg

This library aims to create simple to use functions to interact with the
Robinhood API. This is a pure python interface and it requires Python 3. The purpose
of this library is to allow people to make their own robo-investors or to view
stock information in real time.

.. note::

  These functions make real time calls to your Robinhood account. Unlike in the app, there are
  no warnings when you are about to buy, sell, or cancel an order. It is up to **YOU** to use
  these commands responsibly.

User Guide
==========

Below is the table of contents for Robin Stocks. Use it to find example code or
to scroll through the list of all the callable functions.

.. toctree::
   :maxdepth: 3

   intro
   install
   quickstart
   advanced
   robinhood
   tda
   gemini
   example

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
