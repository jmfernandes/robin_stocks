''' The most basic way to interact with the public api.
'''
import robin_stocks.gemini as g

response, error = g.get_pubticker("cheese")

if error:
    print("there was an error!")
    print("the response status code is ", response.status_code)
    print("the reponse json is ", response.json())

print("let's try that again")

response, error = g.get_pubticker("btcusd")

if not error:
    print("it worked this time!")
    print(response)
    print(response.json())

print("i don't care about raw response anymore, let's get json by default! This will apply to all functions from now on.")

g.set_default_json_flag(True)

response, error = g.get_pubticker("btcusd")

print("reponse is the json format now!")
print(response)

print("you can also set whether you want the json format directly for each function by passing in jsonify")

response, error = g.get_pubticker("btcusd", jsonify=False)

print("this function is back to raw response")
print(response)
