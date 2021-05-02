
import telebot, bs4, requests
from telebot import types

bot = telebot.TeleBot('1785162747:AAE0tN5e3yY6OG771g8MJ_S1_hnNwnfTG3s')

user_height = ''
user_weight = ''
user_age = ''
user_gender = ''
user_lifestyle = ''
user_result = None

# /start, /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardRemove(selective=False)

    msg = bot.send_message(message.chat.id, "Hi " + message.from_user.first_name + ", I'm bot with calculations and recipes\nMay I ask you about your height?", reply_markup=markup)
    bot.register_next_step_handler(msg, get_height)

# height
def get_height(message, user_result = None):
    try:
       global user_height
       if user_result == None:
          user_height = int(message.text)
       msg = bot.send_message(message.chat.id, "May I ask you about your weight?", reply_markup=markup)
       bot.register_next_step_handler(msg, get_weight)
    except Exception as e:
       bot.reply_to(message, 'Error')

# weight
def get_weight(message):
    try:
       global user_weight
       user_weight = int(message.text)
       msg = bot.send_message(message.chat.id, "May I ask you about your age?", reply_markup=markup)
       bot.register_next_step_handler(msg, get_age)
    except Exception as e:
       bot.reply_to(message, 'Error')

# age
def get_age(message):
    try:
       global user_age
       user_age = int(message.text)
       msg = bot.send_message(message.chat.id, "May I ask you about your gender?", reply_markup=markup)
       bot.register_next_step_handler(msg, get_gender)
    except Exception as e:
       bot.reply_to(message, 'Error')

# показать результат или продолжить операцию
def process_alternative_step(message):
    try:
       # calculations
       calc()
    except Exception as e:
       bot.reply_to(message, 'Error')

# result
def calcResultPrint():
    global user_height, user_weight, user_age, user_result
    return "Result: " + str(user_result)

# calculations
def calc():
    global user_height, user_weight, user_age, user_result

    user_result = eval(str(user_height))

    return user_result

bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)

def getrecipe():
    z=''
    s=requests.get('https://www.russianfood.com/recipes/bytype/?fid=3')
    b=bs4.BeautifulSoup(s.text, "html.parser")
    p=b.select('recipe_1 in_seen v2')
    for x in p:        
        s=(x.getText().strip())
        z=z+s+'\n\n'
    return s

@bot.message_handler(content_types=["text"])

def handle_text(message):
    msg=message.text
    msg=msg.lower()

    if (u'recipe' in msg):
        try:
            bot.send_message(message.from_user.id, getrecipe())
        except:
            pass
    elif (u'no' in msg):
        try:
            bot.send_message(message.from_user.id, "Bye)")
        except:
            pass
    elif (u'yes' in msg):
        try:
            bot.send_message(message.from_user.id, getrecip())
        except:
            pass
    else:
        bot.send_message(message.from_user.id, u'Do you want to get a recipe?')

bot.polling(none_stop=True, timeout=123)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.from_user.id, u'Text me recipe')

bot.polling(none_stop=True, interval=0)
       
