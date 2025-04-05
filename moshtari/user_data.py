import sqlite3

# ایجاد دیتابیس و جدول در صورت عدم وجود
def init_db():
    connection = sqlite3.connect('user.db')
    cursor = connection.cursor()

    create_table_query = """
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            uni_name TEXT NOT NULL,
            unit_name TEXT NOT NULL,
            phone_number TEXT NOT NULL
        );
    """

    cursor.execute(create_table_query)
    connection.commit()
    connection.close()

# بررسی اینکه آیا کاربر قبلاً ثبت شده است
def is_user_registered(user_id):
    connection = sqlite3.connect('user.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    connection.close()
    return user is not None

# ثبت اطلاعات کاربر جدید
def register_user(user_id, first_name, last_name, uni_name, unit_name, phone_number):
    connection = sqlite3.connect('user.db')
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO users (user_id, first_name, last_name, uni_name, unit_name, phone_number)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, first_name, last_name, uni_name, unit_name, phone_number))
        connection.commit()
    except sqlite3.IntegrityError:
        print(f"خطا: کاربری با آیدی {user_id} قبلاً ثبت شده است!")
    finally:
        connection.close()

# اجرای تابع init_db هنگام ایمپورت فایل
init_db()




# برای گرفتن اطلاعات از دیتابیس
def get_registered_user(user_id, columns="*"):
   
   
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()

    # اجرای کوئری با ستون‌های دلخواه
    query = f"SELECT {columns} FROM users WHERE user_id = ?"
    cursor.execute(query, (user_id,))
    row = cursor.fetchone()

    conn.close()

    if row:
        if columns.strip() == "*":
            # اگر همه ستون‌ها خواسته شده، تبدیل به دیکشنری کنیم
            return {
                "user_id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "uni_name": row[3],
                "unit_name": row[4],
                "phone_number": row[5],
            }
        elif "," in columns:
            # چند ستون خاص خواسته شده
            column_list = [col.strip() for col in columns.split(",")]
            return {col: val for col, val in zip(column_list, row)}
        else:
            # فقط یک ستون خاص خواسته شده
            return row[0]

    return None
