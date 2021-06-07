from pytube import YouTube
from pytube.exceptions import RegexMatchError
from tempfile import gettempdir
from dotenv import load_dotenv
from telegram import Update
from telegram.constants import MESSAGEENTITY_URL, MESSAGEENTITY_TEXT_LINK
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler
import os

load_dotenv()
try:
	bot = Updater(os.environ['TOKEN'])
except KeyError:
	exit(1)


def getVideo(update: Update, context: CallbackContext) -> None:
	def sendCompliteMsg(stream, file):
		with open(file, 'rb') as fd:
			update.message.reply_video(fd, timeout=60)
		os.unlink(file)

	update.message.reply_text('Чекай')
	try:
		a = YouTube(update.message.text, on_complete_callback=sendCompliteMsg).streams.filter(progressive=True)
		a.first().download(gettempdir())
	except RegexMatchError:
		update.message.reply_text('Я тебе не зрозумів')


def getInfo(update: Update, context: CallbackContext) -> None:
	update.message.reply_text('Кинь мені посилання на видиво з ютуба і я скачаю тобі його')


bot.dispatcher.add_handler(MessageHandler(
	(Filters.text & (Filters.entity(MESSAGEENTITY_URL) | Filters.entity(MESSAGEENTITY_TEXT_LINK))),
	getVideo
	))
bot.dispatcher.add_handler(CommandHandler(['start', 'help'], getInfo))


print('Starting...')
bot.start_polling(1)
bot.idle()