from typing import Callable
from threading import Thread
import json
import dotenv
from dotenv import load_dotenv
import os
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from ..util import valid_youtube_url

load_dotenv()


class TelegramBot:
    def __init__(self, on_back: Callable = None, on_pause: Callable = None,
                 on_play: Callable = None, on_skip: Callable = None,
                 on_yt: Callable = None):
        self.on_back = on_back
        self.on_pause = on_pause
        self.on_play = on_play
        self.on_skip = on_skip
        self.on_yt = on_yt
        self.api_key = os.getenv('API_KEY')
        self.approved_chat_ids = set(
            map(int, json.loads(os.getenv('APPROVED_CHAT_IDS'))))
        self.super_chat_id = int(os.getenv('SUPER_CHAT_ID'))
        self.updater = Updater(self.api_key)
        self.updater.dispatcher.add_handler(
            CommandHandler('approved_ids', self.cmd_approved_ids))
        self.updater.dispatcher.add_handler(
            CommandHandler('whitelist', self.cmd_whitelist))
        self.updater.dispatcher.add_handler(
            CommandHandler('blacklist', self.cmd_blacklist))
        self.updater.dispatcher.add_handler(
            CommandHandler('start', self.cmd_start))
        self.updater.dispatcher.add_handler(
            CommandHandler('help', self.cmd_help))
        self.updater.dispatcher.add_handler(
            CommandHandler('show_id', self.cmd_show_id))
        self.updater.dispatcher.add_handler(
            CommandHandler('back', self.cmd_back))
        self.updater.dispatcher.add_handler(
            CommandHandler('pause', self.cmd_pause))
        self.updater.dispatcher.add_handler(
            CommandHandler('play', self.cmd_play))
        self.updater.dispatcher.add_handler(
            CommandHandler('skip', self.cmd_skip))
        self.updater.dispatcher.add_handler(
            CommandHandler('yt', self.cmd_yt))
        self.updater.dispatcher.add_handler(
            MessageHandler(Filters.text, self.unknown))
        self.updater.dispatcher.add_handler(
            MessageHandler(Filters.command, self.unknown))
        self.updater.dispatcher.add_handler(
            MessageHandler(Filters.text, self.unknown_text))

    def approved_user(func: Callable):
        def wrapper(self, update: Update, context: CallbackContext, *args,
                  **kwargs):
            chat_id = update.effective_user.id
            if chat_id not in self.approved_chat_ids:
                return
            return func(self, update, context, *args, **kwargs)
        return wrapper

    def super_user(func: Callable):
        def wrapper(self, update: Update, context: CallbackContext, *args,
                  **kwargs):
            chat_id = update.effective_user.id
            if chat_id != self.super_chat_id:
                return
            return func(self, update, context, *args, **kwargs)
        return wrapper

    def run(self):
        """
        Run telegram bot
        :return:
        """
        Thread(target=self.updater.start_polling, daemon=True).start()

    def save_approved_chat_ids(self):
        #approved_chat_ids = ','.join(
        #    sorted(list(map(str, self.approved_chat_ids))))
        approved_chat_ids = json.dumps(sorted(list(self.approved_chat_ids)))
        os.environ['APPROVED_CHAT_IDS'] = approved_chat_ids
        dotenv_file = dotenv.find_dotenv()
        dotenv.set_key(dotenv_file, 'APPROVED_CHAT_IDS', approved_chat_ids)

    def cmd_show_id(self, update: Update, context: CallbackContext):
        chat_id = update.effective_user.id
        update.message.reply_text(f'Your ID: {chat_id}')

    @super_user
    def cmd_approved_ids(self, update: Update, context: CallbackContext):
        update.message.reply_text(f'Approved IDs: {self.approved_chat_ids}')

    @super_user
    def cmd_whitelist(self, update: Update, context: CallbackContext):
        chat_ids = set(map(int, update.message.text.split(' ')[1:]))
        self.approved_chat_ids.update(chat_ids)
        # Store changes to dotenv file
        self.save_approved_chat_ids()
        update.message.reply_text('IDs have been whitelisted!')

    @super_user
    def cmd_blacklist(self, update: Update, context: CallbackContext):
        chat_ids = set(map(int, update.message.text.split(' ')[1:]))
        self.approved_chat_ids -= chat_ids
        # Store changes to dotenv file
        self.save_approved_chat_ids()
        update.message.reply_text('IDs have been removed from whitelist')

    def cmd_start(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            'Thanks for using YouPlayer\nUse /help to get more info')

    def cmd_help(self, update: Update, context: CallbackContext):
        chat_id = update.effective_user.id
        msg = '''## Common ##
/help : Show this help message
/show_id : Show your chat ID'''
        if chat_id in self.approved_chat_ids:
            msg += '''
## Music ##
/back : Play previous song in music player
/pause : Pause playback in music player
/play : Start or continue playback in music player
/skip : Play next song in music player
/yt youtube_url[, youtube_url[, ...]] : Add one or more songs'''
        if chat_id == self.super_chat_id:
            msg += '''
## Administrative (Superuser) ##
/approved_ids: Show list of approved IDs
/whitelist chat_id[, chat_id[, chat_id]] : Whitelist a chat ID
/blacklist chat_id[, chat_id[, chat_id]] : Blacklist a chat ID'''
        update.message.reply_text(msg)

    @approved_user
    def cmd_back(self, update: Update, context: CallbackContext):
        if not self.on_back:
            update.message.reply_text('No on_back() callback set!')
            return
        self.on_back()
        update.message.reply_text('Backtracked')

    @approved_user
    def cmd_pause(self, update: Update, context: CallbackContext):
        if not self.on_pause:
            update.message.reply_text('No on_pause() callback set!')
            return
        self.on_pause()
        update.message.reply_text('Paused')

    @approved_user
    def cmd_play(self, update: Update, context: CallbackContext):
        if not self.on_play:
            update.message.reply_text('No on_play() callback set!')
            return
        self.on_play()
        update.message.reply_text('Playing')

    @approved_user
    def cmd_skip(self, update: Update, context: CallbackContext):
        if not self.on_skip:
            update.message.reply_text('No on_skip() callback set!')
            return
        self.on_skip()
        update.message.reply_text('Skipped')

    @approved_user
    def cmd_yt(self, update: Update, context: CallbackContext):
        urls = update.message.text.split(' ')[1:]
        if not self.on_yt:
            update.message.reply_text('No on_yt() callback set!')
            return
        for url in urls:
            if not valid_youtube_url(url):
                continue
            self.on_yt(url)
        update.message.reply_text(f'Added!')

    def unknown_text(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            f'Sorry, I don\'t recognize {update.message.text}')

    def unknown(self, update: Update, context: CallbackContext):
        # Check if valid YouTube URL
        update.message.reply_text('I don\'t know what that\'s about')
