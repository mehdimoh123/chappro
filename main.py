
import telebot


from config import ADMIN_ID, CHAPKHANE_ID, PAKHSH_ID, WELCOME_MESSAGE

# منوها
from admin.buttons1 import admin_menu
from pakhsh.buttons2 import pakhsh_menu
from chapkhane.buttons3 import chapkhane_menu
from moshtari.buttons4 import moshtari_menu, moshtari_new_menu
from moshtari import buttons4

# مدیریت دیتابیس و داده‌های موقت
from moshtari.user_data import is_user_registered, register_user, get_registered_user
from moshtari.user_session import get_user_data, clear_user_data

bot = telebot.TeleBot("7572843939:AAEf8hWjpGI5dKxFDDe7f_pgrpiBduf4aKc")




# لیست آیدی‌هایی که اطلاعاتشان نباید ذخیره شود
EXCLUDED_USERS = {ADMIN_ID, CHAPKHANE_ID, PAKHSH_ID}


# واکنش به استارت اولیه
@bot.message_handler(commands=["start"])
def send_welcome(message):
    user_id = message.from_user.id  # دریافت آیدی عددی کاربر
   
   
    if user_id == ADMIN_ID:
        bot.reply_to(message, "سلام ادمین عزیز، خوش آمدید! 😊", reply_markup=admin_menu())

    elif user_id == CHAPKHANE_ID:
        bot.reply_to(message, "سلام وقتتون بخیر\n شما با حساب چاپ‌خانه وارد شدید.", reply_markup=chapkhane_menu())

    elif user_id == PAKHSH_ID:
        bot.reply_to(message, "سلام وقتتون بخیر\n شما با حساب کاربری پخش جزوه وارد شده‌اید.", reply_markup=pakhsh_menu())

    elif user_id not in EXCLUDED_USERS and not is_user_registered(user_id):
        user_data = get_user_data(user_id)  # دریافت اطلاعات موقت کاربر

        if not user_data:
            bot.reply_to(message, WELCOME_MESSAGE, reply_markup=moshtari_new_menu(user_id))
        else:
            bot.reply_to(message, "⏳ شما در حال تکمیل اطلاعات هستید.", reply_markup=moshtari_new_menu(user_id))
    else:
        first_name = get_registered_user(user_id, "first_name")
        print(f"first_name از دیتابیس گرفته شد: {first_name}")

        if first_name:
            bot.reply_to(message, f"{first_name} عزیز، خوش آمدید 😊", reply_markup=moshtari_menu())
        else:
            bot.reply_to(message, "⚠️ اطلاعات شما در دیتابیس پیدا نشد. لطفاً دوباره ثبت‌نام کنید.")







if __name__ == "__main__":
    while True:
        try:
            bot.polling(non_stop=True, timeout=60)
        except Exception as e:
            print(f"❌ خطا در اجرای بات: {e}")
