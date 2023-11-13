from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext
from moviepy.editor import VideoFileClip
import os

def start(update, context):
    update.message.reply_text("Привіт! Відправте мені відео, і я витягну аудіо у голосовому форматі. Ігорю привет")

def process_video(update, context):
    chat_id = update.message.chat_id
    video_message = update.message.video

    # Зберігаємо відео-повідомлення на локальний сервер
    video_file = context.bot.get_file(video_message.file_id)
    video_file.download('input_video.mp4')

    # Витягуємо аудіо з відео
    audio_file = 'output_audio.ogg'
    clip = VideoFileClip('input_video.mp4')
    clip.audio.write_audiofile(audio_file)

    # Надсилаємо аудіо у голосовому повідомленні
    context.bot.send_voice(chat_id, voice=open(audio_file, 'rb'))

    # Видаляємо тимчасові файли
    os.remove('input_video.mp4')
    os.remove(audio_file)

def main():
    updater = Updater("6439114775:AAEDsVXRMBiZ6GlIA4VgjIgi2kAuOc5zt_E", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.video & ~Filters.command, process_video))

    updater.start_polling()
    updater.idle()

if name == 'main':
    main()