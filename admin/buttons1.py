from telebot.types import ReplyKeyboardMarkup, KeyboardButton  # ✅ اینو اضافه کن!
                    #کیبورد رو می‌سازه و دکمه‌ها رو داخلش قرار می‌ده
                          #این دکمه‌ را می‌سازه
from config import ADMIN_ID
from bot_instance import bot
import sqlite3
import telebot
bot = telebot.TeleBot("7572843939:AAEf8hWjpGI5dKxFDDe7f_pgrpiBduf4aKc")


def admin_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    price_btn = KeyboardButton("💰 قیمت")
    fac_btn = KeyboardButton("🧾 فاکتور")
    reset_fac_btn = KeyboardButton("🔄 ریست فاکتور")
    list_mosh_btn = KeyboardButton ("📋 لیست مشتری‌های دوره‌ای")
    keyboard.add(price_btn,fac_btn, reset_fac_btn,list_mosh_btn )
    return keyboard

# 📌 حذف تمام اطلاعات دیتابیس
def reset_database():
    connection = sqlite3.connect('user.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users")
    connection.commit()
    connection.close()
    bot.send_message(ADMIN_ID, "✅ تمام اطلاعات کاربران حذف شد.")

# 📌 هندل کردن دستور ریست فاکتور
@bot.message_handler(func=lambda message: message.text == "🔄 ریست فاکتور")
def handle_reset_fac(message):
    if message.from_user.id == ADMIN_ID:  # اطمینان از اینکه فقط ادمین‌ها این کار را انجام دهند
        reset_database()
    else:
        bot.send_message(message.chat.id, "⛔ شما اجازه این کار را ندارید!")
