Example Usage of TD Ameritrade API
===========================
TD Ameritrade take a little work to get up and running, but once you set it up the first time,
you should be able to log in automatically every time after that.

Loggin in to API
^^^^^^^^^^^^^^^^
The first thing you need to do is create an encryption passcode. Robin-Stocks stores your confidential
API information in a pickle file on your computer, but encrypts it using a password for your own safety.
To generate this passcode, execute the following code.

>>> import robin_stocks.tda as tda
>>> passcode = tda.generate_encryption_passcode()
>>> print("my secret passcode is ", passcode)

Write this passcode down and store it in a safe place. You can store the passcode in a .env file as 
shown in .test.env. In this example, the passcode is stored as tda_encryption_passcode and if you
wanted to get the value in your personal scripts you would execute the following code.

>>> import os
>>> from dotenv import load_dotenv
>>> load_dotenv()
>>> my_secret_passcode = os.environ["tda_encryption_passcode"]

Now you are free to use my_secret_passcode variable to log in to the TD Ameritrade API. To log in to
the API, you will need three things: your encryption passcode, an authentication token that is generated
on the TD Ameritrade API website, and a refresh token that is also generated on the TD Ameritrade API website.
To log in for the first time execute the following code.

>>> import robin_stocks.tda as tda
>>> tda.login_first_time("my-encryption-passcode", "my-authroization-token", "my-refresh-token") # ONLY CALL ME ONCE. EVER.

Please be sure to note, that you do not use login_first_time every time you run a script. You run it only once, 
and then you should delete the code from your python file. A better solution would be to enter the python interpreter 
in Terminal or Windows Command Prompt and to execute the login_first_time function from there. login_first_time will save 
the authentication and refresh token to a pickle file in your home directory. Authorization tokens expire every 30 minutes, 
and the refresh token is used by robin_stocks to get you a new authentication token.

So, as the start of every TD Ameritrade script or program you write, you should execute the following code.

>>> import robin_stocks.tda as tda
>>> tda.login("my-encryption-passcode") # make sure you have called login_first_time as some point.

The login function will use your encryption passcode to decrypt your pickle file, generate a new authorization token 
if it needs to, and then save your authorization to the session information. 

There is an example log in script in the examples folder.