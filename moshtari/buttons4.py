from telebot.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
import telebot
from moshtari.user_session import get_user_data, update_user_data, clear_user_data
from moshtari.user_data import register_user

bot = telebot.TeleBot("7572843939:AAEf8hWjpGI5dKxFDDe7f_pgrpiBduf4aKc")

# 📌 ایجاد منوی اصلی مشتری
def moshtari_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    ptint_btn = KeyboardButton("🖨️ ثبت سفارش پرینت")
    profile_btn = KeyboardButton("👤 حساب کاربری")
    keyboard.add(ptint_btn, profile_btn)
    return keyboard

# منویی که هنگام زدن روی حساب کاربری می‌بینید
def moshtari_submenu_profile_btn():
    keybord = ReplyKeyboardMarkup(resize_keyboard=True)
    backtomoshtri_menu = KeyboardButton("🔙 بازگشت")
    keybord.add(backtomoshtri_menu)
    return keybord

@bot.message_handler(func=lambda message: True)
def handle_text_messages(message):
    text = message.text
    user_id = message.from_user.id

    if text == "👤 حساب کاربری":
        bot.send_message(user_id, "👤 اطلاعات حساب کاربری شما:", reply_markup=moshtari_submenu_profile_btn())

    elif text == "🔙 بازگشت":
        bot.send_message(user_id, "چه کاری میتونم برات انجام بدم؟", reply_markup=moshtari_menu())






# 📌 ایجاد منوی اینلاین برای دریافت اطلاعات مشتری جدید
def moshtari_new_menu(user_id):
    user_data = get_user_data(user_id)  # دریافت اطلاعات کاربر از session

    inlin_kybord_new_moshtari = InlineKeyboardMarkup(row_width=2)

    # 🆔 آیدی کاربر
    user_id_matn = InlineKeyboardButton(text="🆔 آیدی شما:", callback_data="ignore")
    user_idd = InlineKeyboardButton(text=f"{user_id}", callback_data="ignore")

    # 👤 نام کاربر
    first_name_matn = InlineKeyboardButton(text=" :نام👤 ", callback_data="ignore")
    first_name = InlineKeyboardButton(
        text=user_data.get("first_name", "؟"), callback_data="set_first_name"
    )

    # 👥 نام خانوادگی کاربر
    last_name_matn = InlineKeyboardButton(text=" :نام خانودگی👥", callback_data="ignore")
    last_name = InlineKeyboardButton(
        text=user_data.get("last_name", "؟"), callback_data="set_last_name"
    )

    # 🏫 دانشگاه کاربر
    uni_matn = InlineKeyboardButton(text=" :دانشگاه🏫 ", callback_data="ignore")
    uni = InlineKeyboardButton(
        text=user_data.get("uni_name", "؟"), callback_data="set_uni_name"
    )

    # 🏢 دانشکده کاربر
    unit_matn = InlineKeyboardButton(text=" :دانشکده🏢", callback_data="ignore")
    unit = InlineKeyboardButton(
        text=user_data.get("unit_name", "؟"), callback_data="set_unit_name"
    )

    # 📞 شماره تلفن کاربر
    phon_number_matn = InlineKeyboardButton(text=" :شماره تماس📞", callback_data="ignore")
    phon_number = InlineKeyboardButton(
        text=user_data.get("phone_number", "؟"), callback_data="set_phone_number"
    )

    # ✅ دکمه تأیید اطلاعات
    sabt = InlineKeyboardButton(text="✅ تأیید نهایی", callback_data="confirm_registration")

    # 📌 اضافه کردن دکمه‌ها به منو
    inlin_kybord_new_moshtari.add(
        user_id_matn, user_idd,
        first_name_matn, first_name,
        last_name_matn, last_name,
        uni_matn, uni,
        unit_matn, unit,
        phon_number_matn, phon_number,
        sabt
    )
    return inlin_kybord_new_moshtari

@bot.callback_query_handler(func=lambda call: True)
def check_button(call):
    user_id = call.from_user.id

    field_map = {
        "set_first_name": ("first_name", "نام خود را وارد کنید:"),
        "set_last_name": ("last_name", "نام خانوادگی خود را وارد کنید:"),
        "set_uni_name": ("uni_name", "نام دانشگاه خود را وارد کنید:"),
        "set_unit_name": ("unit_name", "نام دانشکده خود را وارد کنید:"),
        "set_phone_number": ("phone_number", "شماره تماس خود را وارد کنید:"),
    }

    if call.data in field_map:
        field_name, message_text = field_map[call.data]
        bot.answer_callback_query(call.id, "✏ لطفاً مقدار جدید را وارد کنید.")
        bot.send_message(user_id, f"✏ {message_text}")
        bot.register_next_step_handler_by_chat_id(user_id, save_user_input, field_name)

    elif call.data == "confirm_registration":
        save_user_to_db(user_id)

    elif call.data == "btn_sabt":  # اضافه کن این رو!
        save_user_to_db(user_id)

    elif call.data == "ignore":
        bot.answer_callback_query(call.id, "این گزینه فقط نمایشی است.", show_alert=True)


# 📌 ذخیره مقدار جدیدی که کاربر وارد می‌کند
def save_user_input(message, field_name):
    user_id = message.from_user.id
    user_input = message.text.strip()  # حذف فاصله‌های اضافی

    update_user_data(user_id, field_name, user_input)  # ذخیره در session

    bot.send_message(user_id, " ✅ ثبت شد لطفا فیلد بعدی را وارد نمایید      برای ویراش روی دکمه مورد نظر کلیک کنید")
    bot.send_message(user_id, "🔄 به‌روزرسانی فرم...", reply_markup=moshtari_new_menu(user_id))

# 📌 ذخیره اطلاعات کاربر در دیتابیس بعد از تأیید نهایی
def save_user_to_db(user_id):
    user_data = get_user_data(user_id)  # دریافت اطلاعات کاربر از session

    if all(user_data.values()):  # بررسی پر بودن تمام فیلدها
        register_user(
            user_id,
            user_data["first_name"],
            user_data["last_name"],
            user_data["uni_name"],
            user_data["unit_name"],
            user_data["phone_number"]
        )

        bot.send_message(user_id, """✅ اطلاعات شما در سیستم ذخیره شد.""")
        
       
        clear_user_data(user_id)  # پاک کردن اطلاعات موقت بعد از ثبت در دیتابیس
       
        bot.send_message(user_id, "🔄برای راه اندازی مجدد ربات /start کلیک کنید")
        
    else:
        bot.send_message(user_id, "❌ لطفاً تمام فیلدها را تکمیل کنید.")
