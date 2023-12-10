import telebot
import random
from random import choice
import emoji
from glob import glob

from telebot import types
bot = telebot.TeleBot("TOKEN")

#Symbols and board settings
gameGround = [" "] * 9
playerSymbol = emoji.emojize(":growing_heart:")
botSymbol = emoji.emojize(":strawberry:")
gameIsStart = False

#Settings for the board
def display_board(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=3)
    buttons = []

    for i in range(9):
        button = types.InlineKeyboardButton(gameGround[i], callback_data=str(i))
        buttons.append(button)

    markup.add(*buttons)
    bot.send_message(chat_id, "Choose a cell:", reply_markup=markup)

#Display greeting pic
def hi_pic(chat_id):
   lists = glob('Hi/*')
   pic = choice(lists)
   bot.send_photo(chat_id, photo=open(pic, "rb"))

#Display winner pic
def win_pic(chat_id):
   lists = glob('Win/*')
   pic = choice(lists)
   bot.send_photo(chat_id, photo=open(pic, "rb"))

#Display loser pic
def lose_pic(chat_id):
   lists = glob('Loose/*')
   pic = choice(lists)
   bot.send_photo(chat_id, photo=open(pic, "rb"))

#Display tie pic
def tie_pic(chat_id):
   lists = glob('Tie/*')
   pic = choice(lists)
   bot.send_photo(chat_id, photo=open(pic, "rb"))

#Display mad pic
def mad_pic(chat_id):
   lists = glob('Mad/*')
   pic = choice(lists)
   bot.send_photo(chat_id, photo=open(pic, "rb"))


#Win and lose conditions:
def check_winner(symbol):
    # Check rows
    for i in range(0, 9, 3):
        if gameGround[i] == gameGround[i + 1] == gameGround[i + 2] == symbol:
            return True

    #Check columns
    for i in range(3):
        if gameGround[i] == gameGround[i + 3] == gameGround[i + 6] == symbol:
            return True

    #Check diagonals
    if gameGround[0] == gameGround[4] == gameGround[8] == symbol or \
       gameGround[2] == gameGround[4] == gameGround[6] == symbol:
        return True

    return False


#Start button and greetings
@bot.message_handler(commands=['start'])
def welcome(message):
    item = {}
    # Button
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item[1] = types.KeyboardButton("Start ૮ ˶ᵔ ᵕ ᵔ˶ ა")
    markup.add(item[1])

    #Greetings
    if message.text == "/start":
        bot.send_message(message.chat.id, "Hello, {0.first_name}!".format(message.from_user, bot.get_me()),
                         parse_mode='html', reply_markup=markup)
        hi_pic(message.chat.id)
        bot.send_message(message.chat.id, "Press 'Start' to start the game <3")


#Displaying the board for the 1st time
@bot.message_handler(content_types=['text'])
def mess(message):
    global turn
    if message.chat.type == 'private' and message.text == "Start ૮ ˶ᵔ ᵕ ᵔ˶ ა":
        gameIsStart = True
        if gameIsStart == True:
            global gameGround
            bot.send_message(message.chat.id, 'You go first!')
            gameGround = [" "] * 9
            display_board(message.chat.id)


#The game itself
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global gameGround
    global gameIsStart
    gameIsStart = True

    if call.message:

        # Player's turn
        selected_cell = int(call.data)

        #If the cells is free the game continues
        if gameGround[selected_cell] == " ":
            gameGround[selected_cell] = playerSymbol
            display_board(call.message.chat.id)
        #If the player press the occupied button the game crashes
        elif gameGround[selected_cell] != " ":
            bot.send_message(call.message.chat.id, "YOU RUINED EVERYTHING!")
            bot.send_message(call.message.chat.id, "USE THE EMPTY ONES ONLY!!")
            mad_pic(call.message.chat.id)
            bot.send_message(call.message.chat.id, "Type '/start' to start the game again!")
            call.message = False

        #Win/lose/tie situations check
        if check_winner(playerSymbol):
            bot.send_message(call.message.chat.id, "You win!")
            win_pic(call.message.chat.id)
            bot.send_message(call.message.chat.id, "Press 'Start' to start the game again!")
            gameIsStart = False
        elif check_winner(botSymbol):
            bot.send_message(call.message.chat.id, "You lose!")
            lose_pic(call.message.chat.id)
            bot.send_message(call.message.chat.id, "Press 'Start' to start the game again!")
            gameIsStart = False
        elif " " not in gameGround:
            bot.send_message(call.message.chat.id, "Tie!")
            tie_pic(call.message.chat.id)
            bot.send_message(call.message.chat.id, "Press 'Start' to start the game again!")
            gameIsStart = False

        # Continue the game if no win/lose
        else:
            # Bot's turn
            selected_cell = random.choice([i for i, cell in enumerate(gameGround) if cell == " "])
            gameGround[selected_cell] = botSymbol
            display_board(call.message.chat.id)

            # Win/lose/tie situations check
            if check_winner(playerSymbol):
                bot.send_message(call.message.chat.id, "You win!")
                win_pic(call.message.chat.id)
                bot.send_message(call.message.chat.id, "Press 'Start' to start the game again!")
                gameIsStart = False
            elif check_winner(botSymbol):
                bot.send_message(call.message.chat.id, "You lose!")
                lose_pic(call.message.chat.id)
                bot.send_message(call.message.chat.id, "Press 'Start' to start the game again!")
                gameIsStart = False
            elif " " not in gameGround:
                bot.send_message(call.message.chat.id, "Tie!")
                tie_pic(call.message.chat.id)
                bot.send_message(call.message.chat.id, "Press 'Start' to start the game again!")
                gameIsStart = False

bot.polling(none_stop=True)