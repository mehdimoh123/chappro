# ذخیره اطلاعات موقت کاربران در حین ثبت‌نام
user_data_collection = {}

def get_user_data(user_id):
    """اگر کاربر قبلاً داده‌ای وارد نکرده باشد، یک ورودی جدید برای او ایجاد می‌کند"""
    if user_id not in user_data_collection:
        user_data_collection[user_id] = {}
    return user_data_collection[user_id]

def update_user_data(user_id, field, value):
    """ بروزرسانی مقدار فیلد وارد شده توسط کاربر """
    if user_id not in user_data_collection:
        user_data_collection[user_id] = {}
    
    user_data_collection[user_id][field] = value
    
def clear_user_data(user_id):
    """حذف اطلاعات کاربر پس از ثبت نهایی"""
    if user_id in user_data_collection:
        del user_data_collection[user_id]
