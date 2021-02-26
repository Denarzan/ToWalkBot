import telebot
import mysql.connector

token = '1662333710:AAGThQhn53n16CqBHF3kK9byaJwxK0avCr0'
bot = telebot.TeleBot(token)


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="010701",
    database='mydatabase'
)
mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE newdatabase")
mycursor.execute("CREATE TABLE users (user_id VARCHAR(255), name VARCHAR(255), "
                 "description VARCHAR (255), location VARCHAR (255))")

mycursor.execute("USE mydatabase;")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hello! I can add some places you want to visit later. Write /add to add new "
                                      "place, /list to see your 10 last places and /reset to delete all your places! ")


@bot.message_handler(commands=['add'])
def handle_name(message):
    def get_confirmation(message, name, description, full_location_data):
        if 'yes' in message.text.lower():
            bot.send_message(message.from_user.id, 'Added')
            sql = "INSERT INTO users (user_id, description, photo, location) VALUES (%s, %s, %s, %s)"
            val = (message.chat.id, name, description, full_location_data)
            mycursor.execute(sql, val)

            mydb.commit()
        elif 'no' in message.text.lower():
            bot.send_message(message.from_user.id, 'Not added')
        else:
            bot.register_next_step_handler(message, lambda message:
            get_confirmation(message, name, description, full_location_data))

    def get_location(message, name, description):
        location = message.location
        if location == '/list':
            show_places(message)
        elif location == '/reset':
            delete_places(message)
        else:
            lat, lon = location.latitude, location.longitude
            full_location_data = f'{message.chat.id}&#124;{lat}&#124;{lon}'
            bot.send_message(message.from_user.id, "Do you wanna add this? Write 'yes' or 'no'.")
            bot.register_next_step_handler(message, lambda message:
            get_confirmation(message, name, description, full_location_data))

    def get_description(message, name):
        description = message.text
        if description == '/list':
            show_places(message)
        elif description == '/reset':
            delete_places(message)
        else:
            bot.send_message(message.from_user.id, 'Send a location')
            bot.register_next_step_handler(message, lambda message: get_location(message, name, description))

    def get_name(message):
        name = message.text
        if name == '/list':
            show_places(message)
        elif name == '/reset':
            delete_places(message)
        else:
            bot.send_message(message.from_user.id, 'Send a description of your place')
            bot.register_next_step_handler(message, lambda message: get_description(message, name))

    bot.send_message(message.from_user.id, "What is the name of your establishment?")
    bot.register_next_step_handler(message, get_name)


@bot.message_handler(commands=['list'])
def show_places(message):
    try:
        bot.send_message(message.from_user.id, "Your last places:")
        mycursor.execute(
            "SELECT description, photo, location FROM users WHERE user_id={} LIMIT 10".format(message.from_user.id))
        result = mycursor.fetchall()
        print(result)
        if not result:
            bot.send_message(message.from_user.id, 'No any places')
        for x in result:
            title, lat, lon = str(x[2]).split(';')
            bot.send_message(message.from_user.id, text=f"""
Name: {x[0]}.
Description: {x[1]}.
Location:
                """)
            bot.send_location(message.from_user.id, lat, lon)
    except NameError:
        bot.send_message(message.from_user.id, 'No any places.')


@bot.message_handler(commands=['reset'])
def delete_places(message):
    sql = "DELETE FROM users WHERE user_id={}".format(message.chat.id)
    mycursor.execute(sql)
    mydb.commit()
    bot.send_message(message.from_user.id, "All your places has been deleted.")


bot.polling()
