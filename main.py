import telebot
import speech_recognition as sr
import requests
from telebot import types
from telebot.types import Message
import threading
from pydub import AudioSegment
import os
os.sys.path.append(os.getcwd())

AudioSegment.converter = os.path.join(os.getcwd(), 'ffmpeg')
SRC = "voice.ogg"
DST = "voice.wav"

BOT_TOKEN = '1289493438:AAFEKtVsPq9xBNmrfYIuKkSHdGFWFmuJPa0'
AUDIO_FILE = 'voice.wav'
wav_path = ''

bot = telebot.TeleBot(BOT_TOKEN)

write_f_t = threading.Thread()
recognize_speech_t = threading.Thread()

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
            bot.send_message(message.chat.id, r.recognize_google(audio, language = "ru-RU"))
        except sr.UnknownValueError:
            bot.send_message(message.chat.id, "Повтори внятно")
        except sr.RequestError as e:
            bot.send_message(message.chat.id, "Чет сервак упал, напиши в личку, поифксим @rymperit")


if __name__ == '__main__':
    bot.polling(none_stop=True)
