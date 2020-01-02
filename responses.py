import json
import time
def bot_resp(user_message):
    if is_bad_word(user_message):
        return "no", "Please don't speak to me like that"
    if 'day' in user_message:
        return 'money', 'Time is money, bebe'
    if ('time' or 'date') in user_message:
        return 'takeoff', time_resp(user_message)
    if is_greeting(user_message):
        return is_greeting(user_message)[0], is_greeting(user_message)[1]
    if is_name(user_message)[0]:
        return 'excited', 'Hello ' + is_name(user_message)[1]



bad_word_set = set(line.strip() for line in open('bad_words.txt'))

def is_bad_word(s):
    for i in s.lower().split():
        if i in bad_word_set:
            return True

def time_resp(s):
    if is_question(s):
        if 'date' and 'time' in s.lower():
            return time.ctime()
        if 'date' in s.lower():
           return time.ctime()[:10] + ', ' + time.ctime()[20:]
        if 'time' in s.lower():
            return time.ctime()[10:20]
    else:
        return "Time is a social construct. Be in the present."

name_set = set(line.strip().strip(',\n') for line in open('names.txt'))

def is_name(s):
    if (('name' in s.split()) and ((s.split()[s.split().index('name')+1] or s.split()[s.split().index('name')+2]) in name_set)):
        return True, s.split()[s.split().index('name')+2]
    if len(s.split()) <= 4:
        print(name_set)
        for i in range(4):
            if s.split()[i] in name_set:
                return True, s.split()[i]


def is_greeting(s):
    greeting_set = set()
    with open('greetings.json', 'r') as greetings_JSON:
        data = json.load(greetings_JSON)
        for p in data['greetings']:
            greeting_set.add(p['phrase'].lower())
    if s.lower() in greeting_set:
        if is_question(s):
            return 'dog', "I don't care or experience emotion, but I do like dogs! What can I do for you?"
        else:
            return 'bored', s

def is_question(s):
    if "?" in s:
        return True


