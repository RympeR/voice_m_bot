import random
import telebot
from telebot import types
from telebot.types import Message
import sqlite3
import datetime

BASE_PART = "B02FEFWEFE"
BASE_PART_BACKUP = "B02FEFWEFE"
# TOKEN = '1131446027:AAGbB-qxxkj_oEpFHFjNkTHfQcsfsCLCy9I'
TOKEN_TEST = '999933605:AAFTTx0UhKuJ7tjIf9AB5NNVo3Bcx3EpVqc'
bot = telebot.TeleBot(TOKEN_TEST)

STICKER_ID = 'CAACAgIAAxkBAAIBQV6EoqXqh4E3Vyv9UpRyUE-FF7cBAAIJAAPz8o4_PQHMda6J_OUYBA'
con = sqlite3.connect('user_bots.db')
cur = con.cursor()
SUPERUSERS = {
    'Rymperit' : '502220139',
}
USER = {
    'Rymperit' : ['502220139','',''],
}


def sql_create():
    cur.execute('CREATE DATABASE IF NOT EXISTS users')
    cur.execute("""CREATE TABLE IF NOT EXISTS user(
                username TEXT PRIMARY KEY NOT NULL,
                token TEXT);""")
    con.commit()


def is_token_valid(username):
    if datetime.datetime.time() - USER[username][2] <= 1:
        return True
    else:
        del USER[username][2]
        return False


def generate_token(id_user):
    return datetime.datetime.time() + '_' + BASE_PART + '_' + id_user


@bot.message_handler(commands=['start', 'options'])
def command_handler(message: Message):
    if message.chat.id == 502220139:
        # print(message.text.split(' ')[1])
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        btn_add = types.KeyboardButton('/add')
        btn_rem = types.KeyboardButton('/remove')
        btn_check = types.KeyboardButton('/check')
        btn_base = types.KeyboardButton('/change_base')
        markup.row(btn_add, btn_rem)
        markup.row(btn_check, btn_base)
        bot.send_message(message.chat.id, "Choose action:", reply_markup=markup)
    else:
        if message.chat.username in USER.keys():
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            btn_add = types.KeyboardButton('/get_token')
            btn_rem = types.KeyboardButton('/is_valid')
            markup.row(btn_add, btn_rem)
            bot.send_message(message.chat.id, "Do you want to get token? or check how long it will exists:",
                             reply_markup=markup)

#change base part

@bot.edited_message_handler(content_types=['text'])
@bot.message_handler(commands=['change_base'], content_types=['text'])
def change_base_token_part(message: Message):
    if message.text in ('change_base', '/change_base'):
        msg = bot.reply_to(message, f"Current base part: {BASE_PART}, want to choose new?")
        bot.register_next_step_handler(msg, change_base_token_step_1)


def change_base_token_step_1(message: Message):
    if message.text.lower() in ('y', 'yes', 'да', 'д', '+'):
        msg = bot.reply_to(message, f'Enter your new BASE_PART')
        bot.register_next_step_handler(msg, change_base_token_step_2)
    else:
        pass


def change_base_token_step_2(message: Message):
    global BASE_PART_BACKUP
    BASE_PART_BACKUP = message.text
    msg = bot.reply_to(message, f"This will be new BASE_PART, {BASE_PART_BACKUP} all correct?")
    bot.register_next_step_handler(msg, change_base_token_validation)


def change_base_token_validation(message: Message):
    global BASE_PART
    global BASE_PART_BACKUP
    if message.text.lower() in ('y', 'yes', 'да', 'д', '+'):
        BASE_PART = BASE_PART_BACKUP
        bot.send_message(message.chat.id,f'This is new base_part: {BASE_PART}')
    else:
        pass


@bot.edited_message_handler(content_types=['text'])
@bot.message_handler(commands=['check'], content_types=['text'])
def add_profile(message: Message):
    result = ""
    if message.text.split(' ')[0] in ("check", "/check"):
        if message.chat.username in SUPERUSERS.keys():
            if len(message.text.split(' ')) > 1:
                for profile in range(len(message.text.split(' '))):
                    if message.text.split(' ')[profile] not in USER.keys():
                        USER[message.text.split(' ')[profile]] = ''
                        bot.send_message(message.chat.id, f"user {message.text} added to list")
                    else:
                        bot.send_message(message.chat.id, f"user {message.text} already in list")
            else:

                for profile, data in USER.items():
                    result += f"{profile} INFO: CHAT_ID : {data[0]}  TOKEN : {data[1]}  VALIDATION_TERM : {data[2]} \n"
                bot.send_message(message.chat.id, result)

        elif message.chat.usarname in USER.keys():
            if USER[message.chat.username][2]:
                bot.send_message(message.chat.id, f"token {USER[message.chat.username][1]}\
                 valid: {is_token_valid(USER[message.chat.username])}\
                  final term {USER[message.chat.username][2]}")
            else:
                bot.send_message(message.chat.id, "You haven't token")

        else:
            bot.send_message(message.chat.id, 'You are not in registered list')


def users_username():
    pass


@bot.edited_message_handler(content_types=['text'])
@bot.message_handler(commands=['add'], content_types=['text'])
def add_profile(message: Message):
    users_not_in_list = ""
    users_in_list = ""
    global USER
    global SUPERUSERS
    if message.text.split(' ')[0] in ("add", '/add'):
        if message.chat.username in SUPERUSERS.keys():
            if len(message.text.split(' ')) > 1:
                for profile in range(len(message.text.split(' '))):
                    if message.text.split(' ')[profile] not in USER.keys():
                        USER[message.text.split(' ')[profile]] = ['', '', '']
                        users_in_list += f"{message.text.split()[profile]}\n"
                    else:
                        users_not_in_list += f"{message.text.split()[profile]}\n"
                bot.send_message(message.chat.id,
                                 f"Users added to list: {users_in_list} where in  list: {users_not_in_list}")
            else:
                msg = bot.reply_to(message, f"input user profiles in format [name] [name] ...")
                bot.register_next_step_handler(msg, add_user)


def add_user(message: Message):
    users_not_in_list = ""
    users_in_list = ""
    global USER
    for profile in range(len(message.text.split(' '))):
        if message.text.split(' ')[profile] not in USER.keys():
            USER[message.text.split(' ')[profile]] = ['', '', '']
            users_in_list += f"{message.text.split()[profile]}\n"
        else:
            users_not_in_list += f"{message.text.split()[profile]}\n"
    bot.send_message(message.chat.id, f"Users added to list: {users_in_list} where in  list: {users_not_in_list}")


@bot.edited_message_handler(content_types=['text'])
@bot.message_handler(commands=['del'], content_types=['text'])
def add_profile(message: Message):
    users_not_in_list = ""
    users_in_list = ""
    global USER
    global SUPERUSERS
    if message.text.split(' ')[0] in ("del", '/del'):
        if message.chat.username in SUPERUSERS.keys():
            if len(message.text.split(' ')) > 1:
                for profile in range(len(message.text.split(' '))):
                    if message.text.split(' ')[profile] in USER.keys():
                        del USER[message.text.split(' ')[profile]]
                        users_in_list += f"{message.text.split()[profile]}\n"
                    else:
                        users_not_in_list += f"{message.text.split()[profile]}\n"
                bot.send_message(message.chat.id,
                                 f"Users deleted from list: {users_in_list} where in  list: {users_not_in_list}")
            else:
                msg = bot.reply_to(message, f"input user profiles in format [name] [name] ...")
                bot.register_next_step_handler(msg, del_user)


def del_user(message: Message):
    users_not_in_list = ""
    users_in_list = ""
    global USER
    for profile in range(len(message.text.split(' '))):
        if message.text.split(' ')[profile] in USER.keys():
            del USER[message.text.split(' ')[profile]]
            users_in_list += f"{message.text.split()[profile]}\n"
        else:
            users_not_in_list += f"{message.text.split()[profile]}\n"
    bot.send_message(message.chat.id, f"Users deleted from list: {users_in_list} where in  list: {users_not_in_list}")




    """
    generate_token(message.chat.id)
    'chat': {'id': 502220139
    'username': 'Rymperit'}
    'date': 1585765661
    """


@bot.message_handler(commands=['add_token'])
def give_token(message: Message):
    # generate_token()
    print(message)
    bot.send_message(message.chat.id, message)


@bot.message_handler(content_types=['sticker'])
def sticker_handler(message: Message):
    bot.send_sticker(message.chat.id, STICKER_ID)


if __name__ == "__main__":
    try:
        sql_create()
    except Exception as e:
        pass
    finally:
        bot.polling(none_stop=True)
