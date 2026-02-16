import telebot
from database.database import *

API_TOKEN = ""

db = myDB("database/db.db")
bot = telebot.TeleBot(API_TOKEN)
tickets = {}

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, """\
Hello there and welcome.
I'm the register bot. Type /register to start the registration process""")
    
@bot.message_handler(commands=["register"])
def start_registration_process(message):
    bot.reply_to(message, """
Let's begin the registration process then.
Enter your bio first: """)
    bot.register_next_step_handler(message, step1)
    
def step1(message):
    bot.reply_to(message, """
Great!
Now enter your phone number so we could contact you later:""")
    ticket = Ticket()
    ticket.set_bio(message.text)
    tickets[message.chat.id] = ticket
    bot.register_next_step_handler(message, step2)

def step2(message):
    bot.reply_to(message, """
Wonderful!
So now let's figure out the time you want to come.
Enter the prefered date in YYYY-MM-DD format. (We don't work on weekends)""")
    ticket = tickets.get(message.chat.id)
    if ticket is not None:
        ticket.set_phone_number(message.text)
        tickets[message.chat.id] = ticket
    bot.register_next_step_handler(message, step3)

def step3(message):
    bot.reply_to(message, """
Alright. So now let's figure out the time. Our work hours are 
10:00 - 16:00 UTC +3
""")
    ticket = tickets.get(message.chat.id)
    if ticket is not None:
        ticket.set_date(message.text)
        tickets[message.chat.id] = ticket
    bot.register_next_step_handler(message, step4)

def step4(message):
    bot.reply_to(message, """
So now take your time and write your reason to use our service and that would be the final step.
""")
    ticket = tickets.get(message.chat.id)
    if ticket is not None:
        ticket.set_time(message.text)
        tickets[message.chat.id] = ticket
    bot.register_next_step_handler(message, step5)

def step5(message):
    ticket = tickets.get(message.chat.id)
    bio = ""
    phone_number = ""
    date = ""
    time = ""
    reason = ""
    if ticket is not None:
        date = ticket.get_date()
        time = ticket.get_time()
        ticket.set_reason(message.text)
        tickets[message.chat.id] = ticket
        bio = ticket.get_bio()
        print(bio)
        phone_number = ticket.get_phone_number()
        print(phone_number)
        date = ticket.get_date()
        print(date)
        time = ticket.get_time()
        print(time)
        reason = ticket.get_reason()
        print(reason)
    bot.reply_to(message, """
And done! Thanks for using our service and don't forget to show up at {0} on {1}
Additionally, you can contact us using this phone number:  
""".format(time, date))
    # db.cursor.execute("INSERT INTO appointments ({0}, {1}, {2}, {3}, {4})".format(bio, phone_number, time, reason, date))
    try:
        db.cursor.execute(
            "INSERT INTO appointments (full_name, phone_number, start_time, reason, date) VALUES (?, ?, ?, ?, ?)",
            (bio, phone_number, time, reason, date)
        )
        db.conn.commit()
        print("Data inserted successfully!")
        
    except Exception as e:
        print(f"Database error: {e}")
        bot.reply_to(message, "There was an error saving your registration. Please try again.")
        return

@bot.message_handler(commands=["stop"])
def stop(message):
    bot.stop_polling()


bot.infinity_polling()
