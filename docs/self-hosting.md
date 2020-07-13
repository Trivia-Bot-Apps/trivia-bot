## Self Hosting

Note: Make sure to use python 3.5 or 3.7 **OTHER VERSIONS WILL NOT WORK**

* You will need all the packages in requirements.txt. You can do this by ```pip install -r requirements.txt```.

* Get a discord token. Get the token ready for input. (If you want the token to be inputed automatically, put the token in the env var ```bottoken```)

* Setup a [REDIS](https://redislabs.com/) database with a key ```data``` with value ```"{}"```. Get the URL ready for imput. (If you want the URL to be inputed automatically, put the URL in the env var ```REDIS_URL```)

* Type ```python3 bot.py```
