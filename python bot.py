import telebot
from telebot import types
import requests, feedparser
from get_chefkoch import chefkoch

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
    itembtn1 = types.KeyboardButton("DAILY CALORIC")
    itembtn2 = types.KeyboardButton("RECIPES")

    key.add(itembtn1, itembtn2)
    msg = bot.send_message(message.chat.id, "Hi, I'm a healthy bot. I'm so glad to meet you!\n"
                           "I have two options and I think you will like it)\nIf you have any "
                           "problem, you may text me \n/help and I will be here for you",
                           reply_markup=key)
    bot.register_next_step_handler(msg, process_switch_step)


# help
@bot.message_handler(commands=['help'])
def help_section(message):
    bot.send_message(message.chat.id, "Hey, I'm here to help you.\nIf you want to calculate the calorie goals, "
                     "\nthen press the DAILY CALORIC.\nIf you don't know what to cook, \nthen press the RECIPES.")


# buttons with functions
@bot.message_handler(content_types=["text"])
def process_switch_step(message):
    if message.text == "DAILY CALORIC":
        get_calc(message)

    elif message.text == "RECIPES":
        get_recipe(message)


# calories calculator
def get_calc(message):
    msg = bot.send_message(message.chat.id, "May I ask you about your height?")
    bot.register_next_step_handler(msg, get_height)


# height
def get_height(message):
    try:
        global user_height
        user_height = int(message.text)
        msg = bot.send_message(message.chat.id, "May I ask you about your weight?")
        bot.register_next_step_handler(msg, get_weight)
    except Exception as e:
        bot.reply_to(message, 'Error')

# weight
def get_weight(message):
    try:
        global user_weight
        user_weight = int(message.text)
        msg = bot.send_message(message.chat.id, "May I ask you about your age?")
        bot.register_next_step_handler(msg, get_age)
    except Exception as e:
        bot.reply_to(message, 'Error')


# age
def get_age(message):
    try:
        global user_age
        user_age = int(message.text)
        key = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        itembtn1 = types.KeyboardButton('MALE')
        itembtn2 = types.KeyboardButton('FEMALE')

        key.add(itembtn1, itembtn2)

        msg = bot.send_message(message.chat.id, "May I ask you about your gender?",
                           reply_markup=key)
        bot.register_next_step_handler(msg, process_gender)
    except Exception as e:
        bot.reply_to(message, 'Error')


# gender
def process_gender(message):
    try:
        global user_gender
        if message.text == "MALE":
            user_gender = 5
        elif message.text == "FEMALE":
            user_gender = -161
        key = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        itembtn1 = types.KeyboardButton('No or minimal physical activity')
        itembtn2 = types.KeyboardButton('Moderate weight training 3 times a week')
        itembtn3 = types.KeyboardButton('Moderate weight training 5 times a week')
        itembtn4 = types.KeyboardButton('Intensive training 5 times a week')
        itembtn5 = types.KeyboardButton('Training every day')
        itembtn6 = types.KeyboardButton('Intense workouts every day or 2 times a day')
        itembtn7 = types.KeyboardButton('Daily physical activity + physical work')

        key.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7)

        msg = bot.send_message(message.chat.id,
                           "May I ask you about your lifestyle?",
                           reply_markup=key)
        bot.register_next_step_handler(msg, process_lifestyle)    

    except Exception as e:
        bot.reply_to(message, 'Error')


# lifestyle
def process_lifestyle(message):
    try:
        global user_lifestyle
        if message.text == "No or minimal physical activity":
            user_lifestyle = 1.2
        elif message.text == "Moderate weight training 3 times a week":
            user_lifestyle = 1.38
        elif message.text == "Moderate weight training 5 times a week":
            user_lifestyle = 1.46
        elif message.text == "Intensive training 5 times a week":
            user_lifestyle = 1.55
        elif message.text == "Training every day":
            user_lifestyle = 1.64
        elif message.text == "Intense workouts every day or 2 times a day":
            user_lifestyle = 1.73
        elif message.text == "Daily physical activity + physical work":
            user_lifestyle = 1.9
        key = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        itembtn1 = types.KeyboardButton("YES")
        itembtn2 = types.KeyboardButton("NO")

        key.add(itembtn1, itembtn2)
        msg = bot.send_message(message.chat.id, "Are you ready for result?",
                           reply_markup=key)
        bot.register_next_step_handler(msg, process_calc)
    except Exception as e:
        bot.reply_to(message, 'Error')


# result1
def process_calc(message):
        if message.text == "YES":
            calc()
            markup = types.ReplyKeyboardRemove(selective=False)
            bot.send_message(message.chat.id, calcResultPrint(), reply_markup=markup)
        elif message.text == "NO":
            print("Ok")
            

# result2
def calcResultPrint():
    global user_height, user_weight, user_age, user_gender, user_lifestyle, user_result
    return "Your daily caloric: " + str(user_result)


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


bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
