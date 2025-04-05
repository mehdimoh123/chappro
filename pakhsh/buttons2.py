from telebot.types import ReplyKeyboardMarkup, KeyboardButton  # ✅ اینو اضافه کن!
                    #کیبورد رو می‌سازه و دکمه‌ها رو داخلش قرار می‌ده
                          #این دکمه‌ را می‌سازه


def pakhsh_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    daramad_btn = KeyboardButton("💰 درامد این دوره")
    list_mosh_btn2 = KeyboardButton ("📋 لیست مشتری‌های دوره‌ای")
    keyboard.add(daramad_btn,list_mosh_btn2 )
    return keyboard
