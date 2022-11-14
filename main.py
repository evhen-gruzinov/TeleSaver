import telebot
import data
import requests
import os.path
from datetime import datetime

bot = telebot.TeleBot(data.bot_token)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Who are you, if you don't know me?")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(content_types=['photo', 'video', 'animation'])
def save_media(message):
    is_admin = False
    chat_id = message.chat.id

    for admin_id in data.admins_id:
        if message.from_user.id == admin_id:
            is_admin = True

    if is_admin == False:
        return bot.send_message(chat_id, "Bip-bip")
    else:

        if message.photo != None:
            raw_photos_arr = message.photo
            max_size = {"file_size": 0, "file_id": ""}

            for photo in raw_photos_arr:
                if photo.file_size > max_size['file_size']:
                    max_size['file_size'] = photo.file_size
                    max_size['file_id'] = photo.file_id

            file_path = bot.get_file(max_size["file_id"]).file_path
            url = "https://api.telegram.org/file/bot" + data.bot_token + "/" + file_path

            r = requests.get(url, allow_redirects=True)

            file_name = 'photos/' + datetime.today().strftime("%Y-%m-%d %H.%M.%S")

            counter = 1

            new_file_name = file_name
            while os.path.isfile(new_file_name+".jpg"):
                new_file_name = file_name + "_" + str(counter+1)

            open(new_file_name + '.jpg', 'wb').write(r.content)



        if message.video != None:
            if message.video.mime_type == 'video/mp4':
                file_id = message.video.file_id
                file_path = bot.get_file(file_id).file_path
                url = "https://api.telegram.org/file/bot" + data.bot_token + "/" + file_path
                r = requests.get(url, allow_redirects=True)
                file_name = 'videos/' + datetime.today().strftime("%Y-%m-%d %H.%M.%S")
                counter = 1
                new_file_name = file_name

                while os.path.isfile(new_file_name + ".mp4"):
                    new_file_name = file_name + "_" + str(counter + 1)

                open(new_file_name + '.mp4', 'wb').write(r.content)

            else:
                print(message)
                return bot.reply_to(message, "I dont know that video type")


        if message.animation != None:
            if message.animation.mime_type == 'video/mp4':
                file_id = message.animation.file_id
                file_path = bot.get_file(file_id).file_path
                url = "https://api.telegram.org/file/bot" + data.bot_token + "/" + file_path
                r = requests.get(url, allow_redirects=True)
                file_name = 'videos/to_gif/' + datetime.today().strftime("%Y-%m-%d %H.%M.%S")
                counter = 1
                new_file_name = file_name

                while os.path.isfile(new_file_name + ".mp4"):
                    new_file_name = file_name + "_" + str(counter + 1)

                open(new_file_name + '.mp4', 'wb').write(r.content)

            elif message.animation.mime_type == 'image/gif':
                file_id = message.animation.file_id
                file_path = bot.get_file(file_id).file_path
                url = "https://api.telegram.org/file/bot" + data.bot_token + "/" + file_path
                r = requests.get(url, allow_redirects=True)
                file_name = 'gifs/' + datetime.today().strftime("%Y-%m-%d %H.%M.  %S")
                counter = 1
                new_file_name = file_name

                while os.path.isfile(new_file_name + ".mp4"):
                    new_file_name = file_name + "_" + str(counter + 1)

                open(new_file_name + '.gif', 'wb').write(r.content)


            else:
                print(message)
                return bot.reply_to(message, "I dont know that animation type")



        return bot.reply_to(message, "Saved")

bot.infinity_polling()