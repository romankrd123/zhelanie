import telebot, sqlite3, random
from telebot import types



bot = telebot.TeleBot('5985154835:AAG53szPQnpzqsik1TPlN7VtXLlmcrtlRLw')

def ispol(message):
    #MAX(`id`)
    db = sqlite3.connect('db.db')
    cursor = db.cursor()
    n = 0
    cursor.execute("SELECT * FROM 'table'")
    for x in cursor:
        x = str(x)
        x = x.split('(')
        x = x[1]
        x = x.split(')')
        x = x[0]
        x = x.split(',')
        x = x[-1]
        x = x.strip()
        print(x)
        n = int(x)
    #print(str(cursor.execute("SELECT MAX(`ID`) FROM 'table'"))
    num = random.randint(7, n)
    text = cursor.execute(f"SELECT text FROM 'table' WHERE id = '{num}'")

    
    markup_inline = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton(text="другое", callback_data="ispol")
    item2 = types.InlineKeyboardButton(text="исполнить", callback_data="ispolzhel")
    markup_inline.add(item1, item2)
    bot.send_message(message.chat.id, text, reply_markup = markup_inline)




@bot.message_handler(commands=['start'])
def welcome(message):
    markup_inline = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton("Исполнить желание", callback_data = "ispol")
    item2 = types.InlineKeyboardButton("Загадать желание", callback_data = "zagzhel")
    markup_inline.add(item1, item2)
    bot.send_message(message.chat.id, "Привет, тут можешь загадать или исполнить чьё-то желание", reply_markup=markup_inline)




def regzhel(message):
    db = sqlite3.connect('db.db')
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO 'table' (text) VALUES('{message.text}')")
    db.commit()
    db.close()

@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if "желание" in message.text.lower():
            db = sqlite3.connect('db.db')
            cursor = db.cursor()
            query = f" INSERT INTO 'table' (text) VALUES('{message.text}') "
            cursor.execute(query)
            db.commit()
            db.close()
            bot.send_message(call.message.chat.id,'Ваше желание добавленно, ждите исполнителя!!!')
@bot.callback_query_handler(func = lambda call: True)
def answer(call):
    if call.data == "ispol":
        ispol(call.message)
    elif call.data == "zagzhel":
        bot.send_message(call.message.chat.id, 'Введите своё желание в формате:\nЖелание: \nАдрес(страна, город, улица, дом): ')
        bot.send_message(call.message.chat.id, 'После того как напишите желание оно добавится в список\nОбъязательно введите слово "желание"')
    elif call.data == "ispolzhel":
        markup_inline = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton("Хочу исполнить", callback_data = "podver")
        item2 = types.InlineKeyboardButton("Отмена", callback_data = "back")
        markup_inline.add(item1, item2)
        bot.send_message(call.message.chat.id, 'Вы решили исполнитьь чьё-то желание, если это было случайно нажмите "отмена"\nсли вы действительно хотите исполнить чьё-то желание, то нажмите "хочу исполнить"', reply_markup=markup_inline)
    elif call.data == "back":
        bot.send_message(call.message.chat.id, "Вы отменили испонение желания")
    elif call.data == "podver":
        msg = bot.send_message(call.message.chat.id, "Вы подтвердили что хотите исполнить желание другого человека\nПросьба добросовестно исполнить желание другого человека\nА неисполнение желание - бан на вечно\nЧеловек может посмотреть есть-ли его желание в списках невыполненых, если его там нет и с момента удаления желания(исполнителем) проходит более 2 месяцев, то человек(исполнитель) отправляется в бан")
        bot.register_next_step_handler(msg, regzhel(call.message))
bot.polling(none_stop=True)
