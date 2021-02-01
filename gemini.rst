Example Usage of Gemini API
===========================
Gemini has a public API where you can make requests without any authorization keys and 
a private API where each request needs authroization codes.

Create account API keys
^^^^^^^^^^^^^^^^^^^^^^^
Gemini uses two API keys, one called the api key and one called the secret key. In order to use the Gemini
private API to place orders, view account activity, etc. you will need to generate these keys on the website.
Below are pictures on how to do that. You will also need to call the login function before you can call
any of the functions that use the private API. If you are not logged in, any function that requires your
API keys will raise an exception. 

.. image:: docs/source/_static/pics/gemini/market.png

.. image:: docs/source/_static/pics/gemini/settings.png

.. image:: docs/source/_static/pics/gemini/create.png

.. image:: docs/source/_static/pics/gemini/primary.png

.. image:: docs/source/_static/pics/gemini/final.png

Logging in
^^^^^^^^^^
Loggin in is very simple. Just type

>>> import robin_stocks.gemini as g
>>> g.login("account-apigoeshere", "secret-api-goes-here")

Be aware that only functions that are decorated with @login_required need you to be logged in.
The rest can be called without you having to login.