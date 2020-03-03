import telebot
from telebot import types
import mysql.connector

TOKEN = "<My token>"
bot = telebot.TeleBot(TOKEN)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1234",
    port="3307",
    database="1234"
)

cursor = db.cursor()


class User:
    def __init__(self, first_name):
        self.first_name = first_name
        self.last_name = ''


user_data = {}

# Buttons
registration_main = types.InlineKeyboardButton(text='Регистрация', callback_data="Registration")
search_main = types.InlineKeyboardButton(text='Поиск информации', callback_data="Search")
mainMenu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data="mainmenu")


@bot.message_handler(commands=["start"])
def main(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    but_main = types.KeyboardButton('/Main_Menu')
    markup.add(but_main)
    bot.send_message(message.chat.id, "Welcome text",
                     reply_markup=markup)


@bot.message_handler(commands=["Main_Menu"])
def inline(message):
    key = types.InlineKeyboardMarkup()
    but_reg = registration_main
    but_search = search_main
    key.add(but_reg)
    key.add(but_search)
    bot.send_message(message.chat.id, "Зарегистрируйтесь или начните поиск необходимой информации:",
                     reply_markup=key)


@bot.message_handler(content_types=["text"])
def registration_firstname(message):
    try:
        user_id = message.from_user.id
        user_data[user_id] = User(message.text)

        msg = bot.send_message(message.chat.id, "Введите фамилию")
        bot.register_next_step_handler(msg, registration_lastname)
    except Exception as e:
        bot.reply_to(message, 'Error')


def registration_lastname(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.last_name = message.text

        sql = "INSERT INTO users (first_name, last_name, user_id) \
                                          VALUES (%s, %s, %s)"
        val = (user.first_name, user.last_name, user_id)
        cursor.execute(sql, val)
        db.commit()

        bot.send_message(message.chat.id, "Вы успешно зарегистрированны!")
    except Exception as e:
        bot.reply_to(message, 'Error')


########################################################################################################
def search_info(message):

# Вот здесь не знаю как правильно написать функцию для поиска
# информации из базы данных (в моем случае это MeSQL),
# пользователь тг бота вводит имя или фамилию для поиска контакта и
# и в тг из базы данных отправляется: имя, фамилия и номер телефона.


# Есть вот такой код, и не знаю, как можно его адаптировать под свои нужды, т.к. в этом коде
# поиск производится по команде /kino, хотя у меня задача, это ввод от пользователя:

# @bot.message_handler(commands=['kino'])
# def films(message):
#     # Подключаемся к БД, которая прописана в отдельном файле constants и приравнена к database_name_films
#     conn = sqlite3.connect(constants.database_name_films)
#     c = conn.cursor()
#     # Запрос данных в БД
#     c.execute('SELECT * FROM webafisha')
#     # Делаем слияние строк в один текстовый блок
#     text = '\n\n'.join([', '.join(map(str, x)) for x in c])
#     # Закрываем подключение к БД
#     c.close()
#     conn.close()
#     # Определяем параметры пользовательской клавиатуры в боте
#     user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
#     # Отрисовываем клавиатуру - тут рисуете свои кнопки (в моем проекте задействованы такие)
#     user_markup.row('/ugadaiki', '/sticker', '/kino')
#     # Отправка сообщения пользователю по конкретному from_user.id, который получаете из Message
#     bot.send_message(message.from_user.id, text, reply_markup=user_markup)

########################################################################################################

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "mainmenu":
        keymain = types.InlineKeyboardMarkup()
        but_reg = registration_main
        but_search = search_main
        keymain.add(but_reg)
        keymain.add(but_search)
        bot.send_message(chat_id=call.message.chat.id, text="Главное меню",
                         reply_markup=keymain)

    if call.data == "Registration":
        keyreg = types.InlineKeyboardMarkup()
        but_main_menu = mainMenu  # главное меню
        keyreg.add(but_main_menu)
        msg = bot.send_message(chat_id=call.message.chat.id, text="Введите Ваше имя: ",
                               reply_markup=keyreg)
        bot.register_next_step_handler(msg, registration_firstname)

    if call.data == "Search":
        key = types.InlineKeyboardMarkup()
        but_1 = types.InlineKeyboardButton(text="Button1")
        but_2 = types.InlineKeyboardButton(text="Button2")
        but_main_menu = mainMenu
        key.add(but_1)
        key.add(but_2)
        key.add(but_main_menu)
        msg = bot.send_message(chat_id=call.message.chat.id, text="Введите имя или фамилию для поиска контакта:",
                         reply_markup=key)
        bot.register_next_step_handler(msg, search_info)
