import json
import time
import requests
def bot_resp(user_message):
    if is_bad_word(user_message):
        animation, response = upset_animations.pop()
        return animation, response
    elif "joke" in user_message:
        return 'giggling', joke_generator()
    elif 'time' in user_message or 'date' in user_message:
        return time_resp(user_message)[0], time_resp(user_message)[1]
    elif 'day' in user_message:
        return 'money', 'Seize the day; time is money, bebe'
    elif is_greeting(user_message):
        return is_greeting(user_message)[0], is_greeting(user_message)[1]
    elif is_question(user_message):
        return 'confused', "I'm not sure how to answer that. May I suggest Googling your question? That might be more fruitful."
    elif ("weather" in user_message.lower()) or ("forcast" in user_message.lower()) or ("temperature" in user_message.lower()):
        return weather_fetch(user_message)[0], weather_fetch(user_message)[1]
    elif is_name(user_message)[0]:
        return 'excited', 'Hello ' + is_name(user_message)[1]
    else:
        return "laughing", "I'm not sure what you're getting at, so I'm just going to laugh and hope you go away"

upset_animations = {("no", "That language is not tolerated here"), ('heartbroken', "Please don't speak to me like that."), ('crying',"It hurts my feelings when you use bad words.")}
bad_word_set = set(line.strip() for line in open('bad_words.txt'))

def is_bad_word(s):
    for i in s.lower().split():
        if i in bad_word_set:
            return True

def time_resp(s):
    if is_question(s):
        if 'date' in s.lower():
           return 'takeoff', time.ctime()[:10] + ', ' + time.ctime()[20:]
        if 'time' in s.lower():
            return 'takeoff', time.ctime()[10:20]
    else:
        return 'dancing', "Time is a social construct. Be in the present."

name_set = set(line.strip().strip(',\n') for line in open('names.txt'))

def is_name(s):
    if 'name' in s.split():
        return True, s.split()[s.split().index('name')+2]
    for i in range(len(s.split())):
        if s.split()[i] in name_set:
            return True, s.split()[i]
    return False, ""

def make_greeting_set():
    greeting_set = set()
    with open('greetings.json', 'r') as greetings_JSON:
        data = json.load(greetings_JSON)
        for p in data['greetings']:
            greeting_set.add(p['phrase'].lower())
    return greeting_set
greeting_set = make_greeting_set()

def is_greeting(s):
    if (s.lower() in greeting_set) or (s.lower()[:-1] in greeting_set):
        if is_question(s):
            return 'dog', "I don't care or experience emotion, but I do like dogs! What can I do for you?"
        else:
            return 'bored', s


def is_question(s):
    if "?" in s:
        return True

jokes_set = set()

def joke_generator():
    with open('jokes.json', 'r') as jokes_JSON:
        data = json.load(jokes_JSON)
        for j in range(len(data)):
            jokes_set.add(data[j]['body'])
    return jokes_set.pop()

city_set = set(line.strip().split(',',1)[0].lower() for line in open('cities.txt'))

def weather_fetch(s):
    understood_city = True
    if "in" in s:
        if s.split('in ', 1)[1].lower() in city_set:
            location = s.split('in ', 1)[1].lower().replace(' ','+')
        elif s.split('in ', 1)[1][:-1].lower() in city_set:
            location = s.split('in ', 1)[1][:-1].lower().replace(' ','+')
        else:
            understood_city = False
            location = 'Tel+Aviv'
    else:
        location = 'Tel+Aviv'
    print(location)
    r = requests.get('http://api.openweathermap.org/data/2.5/forecast?q='+ location +'&APPID=33de9d56e3cf768116eab8aebe3cf7b9')
    if location.replace('+', ' ') == "paris":
        returned_animation = 'inlove'
    elif (int(r.json()['list'][0]['main']['temp']) - 273 < -3) or (int(r.json()['list'][0]['main']['temp']) - 273 > 30):
        print(int(r.json()['list'][0]['main']['temp']) - 273 < -3)
        print(int(r.json()['list'][0]['main']['temp']) - 273 > 30)
        returned_animation = 'afraid'
    else:
        returned_animation = 'ok'
    if understood_city:
        return returned_animation, "It is " + str(int(r.json()['list'][0]['main']['temp']) - 273) + " degrees Celcius in " + location.replace('+', ' ').capitalize()
    else:
        return 'ok', "I'm not sure which city you're looking for, but the current temperature is " + str(int(r.json()['list'][0]['main']['temp']) - 273) + " degrees Celcius in Tel Aviv."
