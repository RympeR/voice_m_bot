import telebot
import speech_recognition as sr
import requests
from telebot import types
from telebot.types import Message
from pydub import AudioSegment
import os
from config import SRC, DST, BOT_TOKEN, languages

os.sys.path.append(os.getcwd())

AudioSegment.converter = os.path.join(os.getcwd(), 'ffmpeg')

AUDIO_FILE = 'voice.wav'
wav_path = ''

bot = telebot.TeleBot(BOT_TOKEN)

LANGUAGE = {

}


@bot.message_handler(content_types=['voice'])
def repeat_messages(message: Message):
    file_info = bot.get_file(message.voice.file_id)
    file = requests.get(
        'https://api.telegram.org/file/bot{0}/{1}'.format(BOT_TOKEN, file_info.file_path))

    with open('voice.ogg', 'wb') as f:
        f.write(file.content)

    sound = AudioSegment.from_ogg(SRC)
    sound.export(DST, format="wav")

    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        # r.adjust_for_ambient_noise(source)
        audio = r.record(source)

        try:
            bot.send_message(message.chat.id, r.recognize_google(
                audio, language=LANGUAGE[message.chat.id]))
        except sr.UnknownValueError:
            bot.send_message(message.chat.id, "Повтори внятно")
        except sr.RequestError as e:
            bot.send_message(
                message.chat.id, "Чет сервак упал, напиши в личку, пофиксим\n @rymperit")


@bot.message_handler(commands=['start', 'settings'], content_types=['text'])
def language_selector(message: Message):
    print(message.chat.id)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    btns = [types.KeyboardButton(lang) for lang in languages]
    for i in range(1, 2):
        markup.row(*btns[i * 2 - 2:i * 2])
    bot.send_message(message.chat.id, "Choose action:", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def set_language(message: Message):
    if message.text in languages:
        LANGUAGE[message.chat.id] = message.text


if __name__ == '__main__':
    bot.polling(none_stop=True)
