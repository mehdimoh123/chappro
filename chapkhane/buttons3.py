from telebot.types import ReplyKeyboardMarkup, KeyboardButton  # ✅ اینو اضافه کن!
                    #کیبورد رو می‌سازه و دکمه‌ها رو داخلش قرار می‌ده
                          #این دکمه‌ را می‌سازه


def chapkhane_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    fac_chapkhane_btn = KeyboardButton("🧾 فاکتور")
    list_moshtari_btn = KeyboardButton ("📋 لیست مشتری‌های دوره‌ای")
    keyboard.add(fac_chapkhane_btn, list_moshtari_btn )
    return keyboard
