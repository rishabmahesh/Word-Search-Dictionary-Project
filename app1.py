"""
    References: 
    Code inspired from the Oxford Dictionary API Documentation which can be found at: https://developer.oxforddictionaries.com/documentation/

    About: 
    This is a mini python project which uses a JSON database to get the meaning of words, and find similar words if a word is not found. 
    It also uses the Oxford Dictionary API to get meanings, and examples of words. 

    Author: Rishab Maheshwari
"""
import os
import json
import requests
from difflib import get_close_matches

#oxfordDefinition(word:str, action:str):(list, str)
def oxfordDefinition(word: str, action: str) -> (list, str):
    app_id = "17716a22"
    app_key = "4b9c14b519cb8a415ed3a97ab10b6122"

    language = 'en-gb'
    word_id = word
    fields = action
    strictMatch = 'false'

    url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/' + language + '/' + word_id.lower() + '?fields=' + fields + '&strictMatch=' + strictMatch
    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
    closeMatchUsed = False

    if r.status_code == 502:
        return "Bad gateway. Try again later :/", "ERROR"
    elif r.status_code == 504:
        return "Gateway timeout. Try again later :/", "ERROR"
    elif r.status_code == 404:
        try:
            closestWordChoice = input("%s wasn't found. Would you like to use the closest match: %s? Y/N:" %(word, closeMatch[0]))
        except:
            return "Exception occurred", "ERROR"
        if closestWordChoice.upper() == "Y":
            closeMatchUsed = True
            return oxfordDefinition(closeMatch[0], action)
        else:
            return "Word not found :'(", word
    elif r.status_code == 200:
        jsonData = json.loads(json.dumps(r.json()))
        requestedData = jsonData["results"][0]["lexicalEntries"][0]["entries"][0]["senses"]
        if closeMatchUsed == True:
            return requestedData, closeMatch[0]
        else:
            return requestedData, word    
    else:
        return "Unknown error occured", "ERROR"

#definition(word:str):(list, str)
def definition(word:str) -> (list, str):
    global closeMatch 
    try:
        closeMatch = get_close_matches(word, data.keys())
    except:
        return "Exception occurred", "ERROR"

    if word in data:
        return data[word], word

    elif word.lower() in data:
        return data[word], word
    
    elif word.title() in data:
        return data[word.title()], word

    elif word.upper() in data:
        return data[word.upper()], word

    elif len(closeMatch) != 0:
        print("%s wasn't found in the database" %word)
        yesOrNo = input("Did you mean %s instead? Y for yes, N for no: " %closeMatch[0])

        if yesOrNo.lower() == 'y':
            return definition(closeMatch[0])
        
        else:
            return "Word not found :'(", word
    
    else:
        return "Word not found :'(", word


#MAIN
scriptpath=os.path.dirname(__file__)
filename=os.path.join(scriptpath, 'data.json')
data = json.load(open(filename))

word = input("Enter word: ")

#Gives the definition from a database
print()
print("Definition from database: -")
returnDef = definition(word)
if type(returnDef[0]) == list:
    for definition in returnDef[0]:
        print(returnDef[1] + ": " + definition)
else:
    print(returnDef[1] + ": " + returnDef[0])
print()

#Gives the definition from the Oxford Dictionary API
print("Definition from API: -")
returnVal = oxfordDefinition(word, "definitions")
if type(returnVal[0]) == list:
    for defOfWord in returnVal[0]:
        print(returnVal[1] + ": " + defOfWord["definitions"][0])
else:
    print(returnVal[1] + ": " + returnVal[0])
print()

#Prints examples which use the searched word
exampleRequest = input("Would you like an example using this word? Y/N :")
print()
if exampleRequest.upper() == 'Y':
    examples = oxfordDefinition(word, "examples")
    if type(examples[0]) == list:
        for example in examples[0]:
            try:
                print(examples[1] + ": " + example["examples"][0]["text"])
            except:
                try:
                    print(examples[1] + ": " + example["subsenses"][0]["examples"][0]["text"])
                except:
                    print("Exception occurred")
    else:
        print(examples[1] + ": " + examples[0]) 
print()