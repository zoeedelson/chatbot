

def bot_resp(user_message):
    if is_bad_word(user_message):
        return "Please don't speak to me like that"
    if 'name' in user_message.split():
        print(user_message.split())
        return 'Hello, '+ user_message.split()[user_message.split().index('name')+2]
    if len(user_message.split()) <= 4:
        print(user_message.split()[0])
        for i in range(3):
            if user_message.split()[i][0].isupper() and user_message.split()[i].find("'") == -1 and len(user_message.split()[i]) >= 2:
                return 'Hello, ' + user_message.split()[i]


bad_word_set = set(line.strip() for line in open('bad_words.txt'))

def is_bad_word(s):
    for i in s.lower().split():
        if i in bad_word_set:
            return True

