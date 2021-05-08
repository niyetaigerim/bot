import telebot
from telebot import types
import requests, feedparser
from get_chefkoch import chefkoch
import random

bot = telebot.TeleBot('1785162747:AAE0tN5e3yY6OG771g8MJ_S1_hnNwnfTG3s')

user_height = ''
user_weight = ''
user_age = ''
user_gender = ''
user_lifestyle = ''
user_result = None

c=chefkoch()
recipe = c.daily_recipe()


# start
@bot.message_handler(commands=['start'])
def keyboard(message):
    key = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    itembtn1 = types.KeyboardButton("күнделікті калория мөлшері")
    itembtn2 = types.KeyboardButton("рецепттер")
    itembtn3 = types.KeyboardButton("дәрумендер")
    itembtn4 = types.KeyboardButton("ораза кестесі")

    key.add(itembtn1, itembtn2, itembtn3, itembtn4)
    msg = bot.send_message(message.chat.id, "Сәлеметсіз бе! \nМенің атым Gera's bot. \nСізбен танысқаныма қуаныштымын."
                           "\nСіз кез-келген сұрақ бойынша /help теруіңізге болады",
                           reply_markup=key)
    bot.register_next_step_handler(msg, process_switch_step)


# help
@bot.message_handler(commands=['help'])
def help_section(message):
    bot.send_message(message.chat.id, "Хей, мен сізге көмектесу үшін келдім."
                     " \nЕгер сіз өзіңіздің күнделікті калория мөлшерің білгіңіз келсе, 'күнделікті калория мөлшері' батырмасын басыңыз."
                     "\nЕгер сіз бүгінгі астың рецептін білгіңіз келсе, 'рецепттер' батырмасын басыңыз."
                     "\nҚандай өнімде белгілі бір витамин бар екенін білгіңіз келсе, 'дәрумендер' батырмасын басыңыз."
                     "\nЕгер сіз ауыз бекіту және ауыз ашу уақытың білгіңіз келсе, 'ораза кестесі' батырмасын басыңыз.")


# buttons with functions
@bot.message_handler(content_types=["text"])
def process_switch_step(message):
    if message.text == "күнделікті калория мөлшері":
        get_calc(message)

    elif message.text == "рецепттер":
        get_recipe(message)

    elif message.text == "дәрумендер":
        get_vitamins(message)

    elif message.text == "ораза кестесі":
        get_time(message)


# calories calculator
def get_calc(message):
    msg = bot.send_message(message.chat.id, "Мен сіздің бойыңызды біле аламын ба?")
    bot.register_next_step_handler(msg, get_height)


# height
def get_height(message):
    try:
        global user_height
        user_height = int(message.text)
        msg = bot.send_message(message.chat.id, "Мен сіздің салмағыңызды біле аламын ба?")
        bot.register_next_step_handler(msg, get_weight)
    except Exception as e:
        bot.reply_to(message, 'Бір жерде қате бар, қайталап тексеріңіз')

# weight
def get_weight(message):
    try:
        global user_weight
        user_weight = int(message.text)
        msg = bot.send_message(message.chat.id, "Мен сіздің жасыңызды біле аламын ба?")
        bot.register_next_step_handler(msg, get_age)
    except Exception as e:
        bot.reply_to(message, 'Бір жерде қате бар, қайталап тексеріңіз')


# age
def get_age(message):
    try:
        global user_age
        user_age = int(message.text)
        key = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        itembtn1 = types.KeyboardButton('ЕРКЕК')
        itembtn2 = types.KeyboardButton('ӘЙЕЛ')

        key.add(itembtn1, itembtn2)

        msg = bot.send_message(message.chat.id, "Мен сіздің жынысыңызды біле аламын ба?",
                           reply_markup=key)
        bot.register_next_step_handler(msg, process_gender)
    except Exception as e:
        bot.reply_to(message, 'Бір жерде қате бар, қайталап тексеріңіз')


# gender
def process_gender(message):
    try:
        global user_gender
        if message.text == "ЕРКЕК":
            user_gender = 5
        elif message.text == "ӘЙЕЛ":
            user_gender = -161
        key = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        itembtn1 = types.KeyboardButton('Физикалық белсенділік жоқ немесе өте аз')
        itembtn2 = types.KeyboardButton('Орташа күш жаттығулары аптасына 3 рет')
        itembtn3 = types.KeyboardButton('Орташа күш жаттығулары аптасына 5 рет')
        itembtn4 = types.KeyboardButton('Аптасына 5 рет қарқынды жаттығулар')
        itembtn5 = types.KeyboardButton('Күн сайын жаттығу')
        itembtn6 = types.KeyboardButton('Күн сайын қарқынды жаттығулар немесе күніне 2 рет')
        itembtn7 = types.KeyboardButton('Күнделікті дене белсенділігі + физикалық жұмыс')

        key.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7)

        msg = bot.send_message(message.chat.id,
                           "Мен сіздің белсенділігіңізді біле аламын ба?",
                           reply_markup=key)
        bot.register_next_step_handler(msg, process_lifestyle)    

    except Exception as e:
        bot.reply_to(message, 'Бір жерде қате бар, қайталап тексеріңіз')


# lifestyle
def process_lifestyle(message):
    try:
        global user_lifestyle
        if message.text == "Физикалық белсенділік жоқ немесе өте аз":
            user_lifestyle = 1.2
        elif message.text == "Орташа күш жаттығулары аптасына 3 рет":
            user_lifestyle = 1.38
        elif message.text == "Орташа күш жаттығулары аптасына 5 рет":
            user_lifestyle = 1.46
        elif message.text == "Аптасына 5 рет қарқынды жаттығулар":
            user_lifestyle = 1.55
        elif message.text == "Күн сайын жаттығу":
            user_lifestyle = 1.64
        elif message.text == "Күн сайын қарқынды жаттығулар немесе күніне 2 рет":
            user_lifestyle = 1.73
        elif message.text == "Күнделікті дене белсенділігі + физикалық жұмыс":
            user_lifestyle = 1.9
        key = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        itembtn1 = types.KeyboardButton("ИӘ")
        itembtn2 = types.KeyboardButton("ЖОҚ")

        key.add(itembtn1, itembtn2)
        msg = bot.send_message(message.chat.id, "Сіз есептеулердің нәтижесін көруге дайынсыз ба?",
                           reply_markup=key)
        bot.register_next_step_handler(msg, process_calc)
    except Exception as e:
        bot.reply_to(message, 'Бір жерде қате бар, қайталап тексеріңіз')


# result1
def process_calc(message):
        if message.text == "ИӘ":
            calc()
            markup = types.ReplyKeyboardRemove(selective=False)
            bot.send_message(message.chat.id, calcResultPrint(), reply_markup=markup)
        elif message.text == "ЖОҚ":
            print("Ok")
            

# result2
def calcResultPrint():
    global user_height, user_weight, user_age, user_gender, user_lifestyle, user_result
    return "Міне, сіздің нәтижеңіз: " + str(user_result)


# calculations
def calc():
    global user_height, user_weight, user_age, user_gender, user_lifestyle, user_result

    user_result = (10 * (user_weight) + 6.25 * (user_height) - 5 * (user_age) + (user_gender)) * (user_lifestyle)

    return user_result

#recipe
def get_recipe(message):
    bot.send_message(message.chat.id, recipe.category)
    bot.send_message(message.chat.id, recipe.name)
    bot.send_message(message.chat.id, recipe.ingredients)
    bot.send_message(message.chat.id, recipe.description)

#vitamins1
def give_random(filename):
    with open(filename, encoding="utf8") as f:
        lines = f.readlines()
        current = (random.choice(lines))
    return current

def get_vitamins(message):
    key = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=7)
    itembtn1 = types.KeyboardButton('A')
    itembtn2 = types.KeyboardButton('B')
    itembtn3 = types.KeyboardButton('C')
    itembtn4 = types.KeyboardButton('D')
    itembtn5 = types.KeyboardButton('E')

    key.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)

    msg = bot.send_message(message.chat.id, "Дәруменді таңдаңыз (A, B, C, D, E):",
                           reply_markup=key)
    bot.register_next_step_handler(msg, process_vitamins)


#vitamins2
def process_vitamins(message):
    #vitamin_type = str(input(message.text))

    vitamin = give_random("vitamins/vitamin_" + message.text.lower() + ".txt").title()
    bot.send_message(message.chat.id, vitamin)

    
#time1
def get_time(message):
    key = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    itembtn1 = types.KeyboardButton('Нұр-Сұлтан')
    itembtn2 = types.KeyboardButton('Алматы')
    itembtn3 = types.KeyboardButton('Шымкент')
    itembtn4 = types.KeyboardButton('Ақтөбе')
    itembtn5 = types.KeyboardButton('Ақтау')
    itembtn6 = types.KeyboardButton('Атырау')
    itembtn7 = types.KeyboardButton('Көкшетау')
    itembtn8 = types.KeyboardButton('Тараз')
    itembtn9 = types.KeyboardButton('Қарағанды')
    itembtn10 = types.KeyboardButton('Қызылорда')
    itembtn11 = types.KeyboardButton('Қостанай')
    itembtn12 = types.KeyboardButton('Павлодар')
    itembtn13 = types.KeyboardButton('Петропавл')
    itembtn14 = types.KeyboardButton('Түркістан')
    itembtn15 = types.KeyboardButton('Өскемен')
    itembtn16 = types.KeyboardButton('Семей')
    itembtn17 = types.KeyboardButton('Талдықорған')
    
    key.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7, itembtn8, itembtn9, itembtn10, itembtn11, itembtn12, itembtn13, itembtn14, itembtn15, itembtn16, itembtn17)

    msg = bot.send_message(message.chat.id, "Сіздің қалаңыз?",
                           reply_markup=key)
    bot.register_next_step_handler(msg, process_time)


#time2
def process_time(message):
    if message.text == 'Нұр-Сұлтан':
        bot.send_message(message.chat.id, 'https://baribar.kz/wp-content/uploads/2021/04/b6b81dac8212aa959a7d9d5de37967c1-977x1536.png', parse_mode='html')
        
    elif message.text == 'Алматы':
        bot.send_message(message.chat.id, 'https://baribar.kz/wp-content/uploads/2021/04/d11ed41ff76f6c78424ff9d4106fcd66-977x1536.png', parse_mode='html')

    elif message.text == 'Шымкент':
        bot.send_message(message.chat.id, 'https://baribar.kz/wp-content/uploads/2021/04/b47996875a73c023ec9b2c16004464a1-977x1536.png', parse_mode='html')

    elif message.text == 'Ақтөбе':
        bot.send_message(message.chat.id, 'https://baribar.kz/wp-content/uploads/2021/04/965f88a192c3f100606b4e051c7f53fb-977x1536.png', parse_mode='html')

    elif message.text == 'Ақтау':
        bot.send_message(message.chat.id, 'https://baribar.kz/wp-content/uploads/2021/04/f87db46669d04d95376dbd4f293ec85f-977x1536.png', parse_mode='html')

    elif message.text == 'Атырау':
        bot.send_message(message.chat.id, 'https://baribar.kz/wp-content/uploads/2021/04/77542474001f4fbcbc34990e64c5429f-977x1536.png', parse_mode='html')

    elif message.text == 'Көкшетау':
        bot.send_message(message.chat.id, 'https://baribar.kz/wp-content/uploads/2021/04/63eb82334ecc8f810c9d62fa9434b261-977x1536.png', parse_mode='html')

    elif message.text == 'Тараз':
        bot.send_message(message.chat.id, 'https://baribar.kz/wp-content/uploads/2021/04/bcdf169accad00ca9ebac30d44165ce3-977x1536.png', parse_mode='html')

    elif message.text == 'Қарағанды':
        bot.send_message(message.chat.id, 'https://baribar.kz/wp-content/uploads/2021/04/a07432ee3894594e329fcb22da8a62de-977x1536.png', parse_mode='html')

    elif message.text == 'Қызылорда':
        bot.send_message(message.chat.id, 'https://baribar.kz/wp-content/uploads/2021/04/8d14743df0ee8035696c6e596948e939-977x1536.png', parse_mode='html')

    elif message.text == 'Қостанай':
        bot.send_message(message.chat.id, 'https://baribar.kz/wp-content/uploads/2021/04/53c6dd61f7f2b72f294660e04cd07cc9-977x1536.png', parse_mode='html')

    elif message.text == 'Павлодар':
        bot.send_message(message.chat.id, 'https://baribar.kz/wp-content/uploads/2021/04/5e0a94e67647f5d4ba98a13ea42a6d70-977x1536.png', parse_mode='html')

    elif message.text == 'Петропавл':
        bot.send_message(message.chat.id, 'https://baribar.kz/wp-content/uploads/2021/04/66b720f54faa803d84c09c65569c86db-977x1536.png', parse_mode='html')

    elif message.text == 'Түркістан':
        bot.send_message(message.chat.id, 'https://baribar.kz/wp-content/uploads/2021/04/ef9e9a914832db364ffd50fac73137a3-977x1536.png', parse_mode='html')

    elif message.text == 'Өскемен':
        bot.send_message(message.chat.id, 'https://baribar.kz/wp-content/uploads/2021/04/d1e0ba00eca9f5a34705ed28bd1e4392-977x1536.png', parse_mode='html')

    elif message.text == 'Семей':
        bot.send_message(message.chat.id, 'https://baribar.kz/wp-content/uploads/2021/04/02099ca130e2d74c48b8f49df58814cd-977x1536.png', parse_mode='html')

    elif message.text == 'Талдықорған':
        bot.send_message(message.chat.id, 'https://baribar.kz/wp-content/uploads/2021/04/c66ce7843306a3509f131ad864d5285b-977x1536.png', parse_mode='html')

        
bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
