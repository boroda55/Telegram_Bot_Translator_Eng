import random
import configparser
import psycopg2
import re
from telebot import types, TeleBot, custom_filters
from telebot.storage import StateMemoryStorage
from telebot.handler_backends import State, StatesGroup



config =configparser.ConfigParser()
config.read('setting.ini')
print('Start telegram bot...')

state_storage = StateMemoryStorage()
token_bot = config['Token']['tg_token']
database = config['SQL']['database']
user = config['SQL']['user']
password = config['SQL']['password']
bot = TeleBot(token_bot, state_storage=state_storage)
conn = psycopg2.connect(database=database, user=user, password=password)
# проверка русского слова
def is_rus_word(word):
    pattern = r'^[а-яА-ЯёЁ]+$'
    return bool(re.match(pattern, word))
# проверка английского слова
def is_eng_word(word):
    pattern = r'^[a-zA-Z]+$'
    return bool(re.match(pattern, word))

def add_user_sql(name, name_id):
    with conn.cursor() as cur:
        cur.execute('insert into users(name, number_user) values (%s, %s) RETURNING userid;', (name, name_id))
        user_id = cur.fetchone()[0]
        for x in range(1,11):
            cur.execute('insert into studied_users(userid, wordid) values (%s, %s)', (user_id, x))
        conn.commit()
    conn.close()

def search_word_sql(name_id,limited, no_word=''):
    word_eng = list()
    word_rus = list()
    with conn.cursor() as cur:
        query = '''SELECT word_eng, word_rus
                    FROM words w 
                    inner join studied_users su on w.wordid=su.wordid
                    inner join users u on su.userid=u.userid
                    where  u.number_user = %s and w.word_eng != %s
                    ORDER BY RANDOM()
                    LIMIT %s;'''
        cur.execute(query, (name_id, no_word, limited))
        for row in cur.fetchall():
            word_eng.append(row[0])
            word_rus.append(row[1])
        cur.close()
    if limited == 1:
        r_word_eng = word_eng[0]
        r_word_rus = word_rus[0]
        return r_word_eng, r_word_rus
    elif limited > 1:
        return word_eng

def add_known_users_sql():
    known_users = list()
    with conn.cursor() as cur:
        query = 'select number_user  from users;'
        cur.execute(query)
        known_users = [x[0] for x in cur.fetchall()]
        cur.close()
    return known_users

def add_word_sql(name_id):
    with conn.cursor() as cur:
        query = '''insert into studied_users (
                    SELECT u.userid, w.wordid FROM users u
                    CROSS JOIN Words w WHERE u.number_user = %s
                    AND NOT EXISTS (SELECT 1 FROM studied_users su
                    WHERE su.userid = u.userid AND su.wordid = w.wordid)
                    ORDER BY RANDOM()LIMIT 1);'''
        cur.execute(query, (name_id,))
        conn.commit()
    conn.close()



known_users = add_known_users_sql()
userStep = {}
buttons = []



def show_hint(*lines):
    return '\n'.join(lines)


def show_target(data):
    return f"{data['target_word']} -> {data['translate_word']}"


class Command:
    ADD_WORD = 'Добавить слово ➕'
    DELETE_WORD = 'Удалить слово🔙'
    NEXT = 'Дальше ⏭'


class MyStates(StatesGroup):
    target_word = State()
    translate_word = State()
    another_words = State()



def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        known_users.append(uid)
        userStep[uid] = 0
        print("New user detected, who hasn't used \"/start\" yet")
        return 0


@bot.message_handler(commands=['cards', 'start'])
def create_cards(message):
    cid = message.chat.id
    if cid not in known_users:
        add_user_sql(message.chat.first_name,cid)
        known_users.append(cid)
        userStep[cid] = 0
        bot.send_message(cid, "Hello, stranger, let study English...")
    markup = types.ReplyKeyboardMarkup(row_width=2)

    global buttons
    buttons = []
    target_word, translate = search_word_sql(cid, 1)
    # target_word = 'Peace'  # брать из БД
    # translate = 'Мир'  # брать из БД
    target_word_btn = types.KeyboardButton(target_word)
    buttons.append(target_word_btn)
    others = search_word_sql(cid, 3, target_word)
    # others = ['Green', 'White', 'Hello', 'Car']  # брать из БД
    other_words_btns = [types.KeyboardButton(word) for word in others]
    buttons.extend(other_words_btns)
    random.shuffle(buttons)
    next_btn = types.KeyboardButton(Command.NEXT)
    add_word_btn = types.KeyboardButton(Command.ADD_WORD)
    delete_word_btn = types.KeyboardButton(Command.DELETE_WORD)
    buttons.extend([next_btn, add_word_btn, delete_word_btn])

    markup.add(*buttons)

    greeting = f"Выбери перевод слова:\n🇷🇺 {translate}"
    bot.send_message(message.chat.id, greeting, reply_markup=markup)
    bot.set_state(message.from_user.id, MyStates.target_word, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['target_word'] = target_word
        data['translate_word'] = translate
        data['other_words'] = others


@bot.message_handler(func=lambda message: message.text == Command.NEXT)
def next_cards(message):
    create_cards(message)

# сделать
@bot.message_handler(func=lambda message: message.text == Command.DELETE_WORD)
def delete_word(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        print(data['target_word'])  # удалить из БД


@bot.message_handler(func=lambda message: message.text == Command.ADD_WORD)
def add_word(message):
    cid = message.chat.id
    userStep[cid] = 1
    add_word_sql(cid)
    print(message.text, message.chat.first_name)  # сохранить в БД


@bot.message_handler(func=lambda message: True, content_types=['text'])
def message_reply(message):
    text = message.text
    markup = types.ReplyKeyboardMarkup(row_width=2)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        target_word = data['target_word']
        if text == target_word:
            hint = show_target(data)
            hint_text = ["Отлично!❤", hint]
            # next_btn = types.KeyboardButton(Command.NEXT)
            # add_word_btn = types.KeyboardButton(Command.ADD_WORD)
            # delete_word_btn = types.KeyboardButton(Command.DELETE_WORD)
            # buttons.extend([next_btn, add_word_btn, delete_word_btn])
            hint = show_hint(*hint_text)
        else:
            for btn in buttons:
                if btn.text == text:
                    btn.text = text + '❌'
                    break
            hint = show_hint("Допущена ошибка!",
                             f"Попробуй ещё раз вспомнить слово 🇷🇺{data['translate_word']}")
    markup.add(*buttons)
    bot.send_message(message.chat.id, hint, reply_markup=markup)


bot.add_custom_filter(custom_filters.StateFilter(bot))

bot.infinity_polling(skip_pending=True)
