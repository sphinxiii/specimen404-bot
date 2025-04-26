# main.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

TOKEN = 'ICI_TON_TOKEN_TELEGRAM'

user_data = {}

choices = [
    {"text": "Aider une créature", "karma": +1},
    {"text": "Ignorer un appel de détresse", "karma": -1},
    {"text": "Offrir une technologie", "karma": +2},
    {"text": "Voler une ressource", "karma": -2},
    {"text": "Soigner un être vivant", "karma": +1},
    {"text": "Déclencher une tempête", "karma": -1},
    {"text": "Partager des connaissances", "karma": +2}
]

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_data[user_id] = {"karma": 0, "tokens": 0}
    update.message.reply_text("Bienvenue sur Specimen404 Tap-To-Earn ! 👽\nClique sur ton alien pour commencer !")
    send_choices(update.message.reply_text)

def send_choices(send_func):
    keyboard = [[InlineKeyboardButton(choice["text"], callback_data=str(i))] for i, choice in enumerate(choices)]
    reply_markup = InlineKeyboardMarkup(keyboard)
    send_func("Fais ton choix du jour :", reply_markup=reply_markup)

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user_id = query.from_user.id

    index = int(query.data)
    impact = choices[index]["karma"]
    user = user_data.setdefault(user_id, {"karma": 0, "tokens": 0})
    user["karma"] += impact
    user["tokens"] += 1

    karma = user["karma"]
    tokens = user["tokens"]

    if karma >= 5:
        evolution = "✨ Alien Divin ✨"
    elif karma <= -5:
        evolution = "💀 Alien Sombre 💀"
    else:
        evolution = "👽 Alien Normal 👽"

    response = (
        f"{choices[index]['text']}\n\n"
        f"Ton évolution actuelle : {evolution}\n"
        f"Tokens gagnés : {tokens} 🪙"
    )
    query.edit_message_text(text=response)
    send_choices(lambda text, reply_markup=None: context.bot.send_message(chat_id=query.message.chat_id, text=text, reply_markup=reply_markup))

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
