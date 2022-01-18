import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
import validators
from pytube import YouTube
import os
from urllib.parse import urlparse
import pytube, aiogram
import time
API_TOKEN = "{Personal Telgram Bot API Key from Bot Father}"

# Configure Logging
logging.basicConfig(level=logging.INFO)

def Try(link: str):
    import requests
    x = requests.get(link)
    if x.text.count("This video isn't available anymore") == 1:
        return 1
    else:
        return link

# Button Inline
button1 = InlineKeyboardButton(text="📮Help & Support",callback_data="returned_text_button1")
button2 = InlineKeyboardButton(text="📥 Report",callback_data="returned_text_button2")
keyboard_inline = InlineKeyboardMarkup().add(button1,button2)

button = KeyboardButton("📮Help & Support")
buton = KeyboardButton("📥 Report")
keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True).add(button).add(buton)
# Configure Bot and Dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Simple Command >>> Start <<<
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` command
    """
    # video = InputFile(r'Video/vDHtypVwbHQ.f136.mp4')

    # await bot.send_photo(message.from_user.id, 'https://tinypng.com/images/social/website.jpg', caption="Sekil")
    await message.reply(f"""By using this bot you agree to our Terms Of Use and Copyright Claims.

Terms Of Use - https://telegra.ph/Terms-Of-Use-01-13
Copyright Claims - https://telegra.ph/Copyright-Claims-01-13""")
    await bot.send_video(message.from_user.id, 'http://birainy.com/Kesh/vDHtypVwbHQ.f136.mp4', caption="Video")
    user = types.User.get_current()
    import sqlite3
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    count = 0
    listu = []
    names = []
    for row in cur.execute('SELECT * FROM link_user'):
        listu.append(row[0])
        names.append(row[3])

    if names.count(str(message.from_user.username)) == 1:
        print("continue")
    else:
        print("else")
        cur.execute(f"INSERT INTO link_user VALUES ({listu[-1]+1},'{message.chat.id}','{message.from_user.full_name}','{message.from_user.username}')")
        con.commit()
    con.close()
    await message.reply(f"Salam {user.first_name} Video Yukleme Botuna Xos gelmisiniz!", reply_markup=keyboard1)
# Simple Command >>> End <<<


# All Message Answer >>> Start <<<
@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    print(message.text)
    if validators.url(message.text):
        domain = urlparse(message.text).netloc
        print(domain)
        response = Try(message.text)
        if response != 1:
            if domain == "www.youtube.com" or "www.m.youtube.com":
                try:
                    await message.answer("Zehmet Olmazsa Gozleyin!")
                    import sqlite3
                    con = sqlite3.connect('db.sqlite3')
                    cur = con.cursor()
                    listu = []
                    for row in cur.execute('SELECT * FROM link_link'):
                        listu.append(row[0])
                    cur.execute(
                        f"INSERT INTO link_link VALUES ({listu[-1]+1},'{message.text}')")
                    con.commit()
                    # url input from user
                    yt = YouTube(str(message.text))
                    # extract only audio
                    video = yt.streams.filter(only_audio=True).first()
                    # check for destination to save file
                    destination = '.'
                    # download the file
                    out_file = video.download(output_path=destination)
                    await message.answer("Yuklenir!", reply_markup=keyboard1)
                    # save the file
                    base, ext = os.path.splitext(out_file)
                    new_file = base + '.mp3'
                    os.rename(out_file, new_file)
                    print("new_file: ",out_file)
                    file_name = new_file.split('/')[-1]
                    os.system(f"mv '{file_name}' Files/")
                    await bot.send_audio(message.from_user.id, 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3', caption="@tMusiqiBot", reply_markup=keyboard1)
                    os.system(f"rm -r Files/'{file_name}'")
                except pytube.exceptions.RegexMatchError:
                    await message.answer("Link Tapilmadi!", reply_markup=keyboard1)
            else:
                await message.answer("Link Tapilmadi!", reply_markup=keyboard1)
        else:
            await message.answer("Link Tapilmadi!", reply_markup=keyboard1)

        # Video Download Link
        # sample_url = "https://da.gd/s?url={}".format(message.text)
        # url = requests.get(sample_url).text
        # ydl_opts_start = {
        #     'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # This Method Need ffmpeg
        #     'outtmpl': f'localhoct/%(id)s.%(ext)s',
        #     'no_warnings': True,
        #     'ignoreerrors': True,
        #     'noplaylist': True,
        #     'http_chunk_size': 20097152,
        #     'writethumbnail': True
        #
        # }
        # with youtube_dl.YoutubeDL(ydl_opts_start) as ydl:
        #     result = ydl.extract_info("{}".format(url))
        #     title = ydl.prepare_filename(result)
        #     ydl.download([url])
        # print("Title: ", title)
        # import os
        # directory = os.getcwd()
        # file_name = "1O0yazhqaxs.f137.mp4".split('.')[0]
        # for name in glob.glob(f'{directory}/localhoct/{file_name}*'):
        #     os.system(f"mv {name} {directory}/httpserver/Files")
        # await bot.send_video(message.from_user.id, 'http://birainy.com/Kesh/vDHtypVwbHQ.f136.mp4', caption="Video")
    elif message.text.lower() == "Salam".lower():
        await message.answer("Aleykum Salam. Youtube Linki At!", reply_markup=keyboard1)

    elif message.text == "📮Help & Support":
        await message.answer("""Bot istifadəsi: https://t.me/tMusiqi/2
    Support:  @OnTechSupBot""", reply_markup=keyboard1)

    elif message.text == "📥 Report":
        await message.answer("""Terms of use:
    https://telegra.ph/Terms-Of-Use-01-13
    Copyright claims:
    https://telegra.ph/Copyright-Claims-01-13


    If SaveYoutubeBot’s or/and YouTubaBot's material infringes your rights, please report: @OnTechSupBot 
    Allow 3-5 business days for a response to your request. We will try to respond to your request as soon as possible.""",
                             reply_markup=keyboard1)
    elif str(message.chat.id) == "2136890049":  # 2136890049   1317516217
        split = message.text.split(" ")
        if message.text == "/stats":
            import sqlite3
            con = sqlite3.connect('db.sqlite3')
            cur = con.cursor()
            say = 0
            for row in cur.execute('SELECT * FROM link_user'):
                say+=1
            count = 0
            for row in cur.execute('SELECT * FROM link_link'):
                count += 1
            await message.answer(f"""User Sayı: {say}
Link Sayı: {count}""", reply_markup=keyboard1)
        elif message.text == "/backup":
            # await bot.send_(file="db.sqlite3",file_type="multipart/form-data",method="GET",payload="payload")
            await message.answer(f"Bacup Script ve Db", reply_markup=keyboard1)
        elif split[0] == "/message":
            import sqlite3
            con = sqlite3.connect('db.sqlite3')
            cur = con.cursor()
            mesaj = message.text.split("/message")
            print(mesaj)
            start = time.time()
            blocked_user = 0
            for row in cur.execute('SELECT * FROM link_user'):
                try:
                    await bot.send_message(row[1], mesaj[1])
                except aiogram.utils.exceptions.BotBlocked:
                    blocked_user +=1
                    time.sleep(1)
            end = time.time()
            await message.answer(f"""Mesaj Gonderme Zamani: {str(end-start).split(".")[0]}
Bloked User Say: {blocked_user}""", reply_markup=keyboard1)
    else:
        if message.text == "📮Help & Support":
                await message.answer("""Bot istifadəsi: https://t.me/tMusiqi/2\nSupport:  @OnTechSupBot""", reply_markup=keyboard1)
        elif message.text == "📥 Report":
                await message.answer("""Terms of use:
        https://telegra.ph/Terms-Of-Use-01-13
        Copyright claims:
        https://telegra.ph/Copyright-Claims-01-13


        If SaveYoutubeBot’s or/and YouTubaBot's material infringes your rights, please report: @OnTechSupBot 
        Allow 3-5 business days for a response to your request. We will try to respond to your request as soon as possible.""",
                                          reply_markup=keyboard1)

        # Inline Buttons >>> End <<<
        else:
            await message.answer("Youtube Linki At!")
# All Message Answer >>> End <<<


# Inline Buttons >>> Start <<<
@dp.callback_query_handler(text=["returned_text_button1","returned_text_button2"])
async def function(call: types.CallbackQuery):
    if call.data == "returned_text_button1":
        await call.message.answer("""Bot istifadəsi: https://t.me/tMusiqi/2
Support:  @OnTechSupBot""", reply_markup=keyboard1)
    else:
        await call.message.answer("""Terms of use:
https://telegra.ph/Terms-Of-Use-01-13
Copyright claims:
https://telegra.ph/Copyright-Claims-01-13


If SaveYoutubeBot’s or/and YouTubaBot's material infringes your rights, please report: @OnTechSupBot 
Allow 3-5 business days for a response to your request. We will try to respond to your request as soon as possible.""", reply_markup=keyboard1)
# Inline Buttons >>> End <<<



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
