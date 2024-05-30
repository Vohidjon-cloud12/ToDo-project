
from db import cur, conn
from models import User, UserStatus, Todo, UserRole
from session import Session
from hashlib import sha256

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def sign_up():
    try:
        username = input('Foydalanuvchi nomini kiriting: ')
        password = input('Parolni kiriting: ')
        hashed_password = hash_password(password)

        select_one_user = """SELECT * FROM users WHERE username = %s;"""
        cur.execute(select_one_user, (username,))
        user_data = cur.fetchone()

        if user_data:
            print("Bu foydalanuvchi nomi allaqachon mavjud. Iltimos, qayta urinib ko'ring.")
        else:
            insert_user = """INSERT INTO users (username, password, role, status, login_try_count)
                             VALUES (%s, %s, %s, %s, %s);"""
            cur.execute(insert_user, (username, hashed_password, 'USER', 'ACTIVE', 0))
            conn.commit()
            print("Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi!")
            session = Session()
            new_user = User(username=username, password=hashed_password, role=UserRole.USER, status=UserStatus.ACTIVE)
            session.add_session(new_user)
            todo_menu()  # Muvaffaqiyatli ro'yxatdan o'tgandan keyin todo menyusini ko'rsatish
    except Exception as e:
        conn.rollback()
        print(f"Foydalanuvchini ro'yxatdan o'tkazishda xatolik: {e}")

def sign_in():
    for attempt in range(3):
        try:
            username = input('Foydalanuvchi nomini kiriting: ')
            password = input('Parolni kiriting: ')
            hashed_password = hash_password(password)

            select_one_user = """SELECT * FROM users WHERE username = %s;"""
            cur.execute(select_one_user, (username,))
            user_data = cur.fetchone()

            if user_data:
                user = User(
                    username=user_data[1],
                    password=user_data[2],
                    user_id=user_data[0],
                    role=UserRole[user_data[3]],
                    status=UserStatus[user_data[4]],
                    login_try_count=user_data[5]
                )

                if user.status == UserStatus.BLOCKED.value:
                    print("Sizning hisobingiz bloklangan.")
                    return False

                if user.password == hashed_password:
                    print("Kirish muvaffaqiyatli!")
                    user.login_try_count = 0
                    update_login_try_count(user)
                    session = Session()
                    session.add_session(user)
                    todo_menu()
                    return True
                else:
                    user.login_try_count += 1
                    update_login_try_count(user)
                    if user.login_try_count >= 3:
                        user.status = UserStatus.BLOCKED.value
                        update_user_status(user)
                        print("Urinishlar limiti oshdi. Siz bloklandingiz.")
                        return False
                    else:
                        print(f"Noto'g'ri parol. {user.login_try_count} urinishdan {3} qoldi.")
            else:
                print("Foydalanuvchi topilmadi.")
        except Exception as e:
            conn.rollback()
            print(f"Kirishda xatolik: {e}")
    return False

def update_login_try_count(user):
    try:
        update_query = """UPDATE users SET login_try_count = %s WHERE id = %s;"""
        cur.execute(update_query, (user.login_try_count, user.id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Login urinishlar sonini yangilashda xatolik: {e}")

def update_user_status(user):
    try:
        update_query = """UPDATE users SET status = %s WHERE id = %s;"""
        cur.execute(update_query, (user.status, user.id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Foydalanuvchi holatini yangilashda xatolik: {e}")
def create_todo():
    try:
        title = input('Todo sarlavhasini kiriting: ')
        todo_type = input('Todo turini kiriting (optional/personal/shopping): ')
        session = Session()
        user = session.get_session()

        insert_todo = """INSERT INTO todos (title, todo_type, user_id)
                         VALUES (%s, %s, %s);"""
        cur.execute(insert_todo, (title, todo_type, user.id))
        conn.commit()
        print("Todo muvaffaqiyatli yaratildi!")
    except Exception as e:
        conn.rollback()
        print(f"Todo yaratishda xatolik: {e}")

def read_todos():
    try:
        session = Session()
        user = session.get_session()

        select_todos = """SELECT * FROM todos WHERE user_id = %s;"""
        cur.execute(select_todos, (user.id,))
        todos = cur.fetchall()

        for todo in todos:
            print(f"ID: {todo[0]}, Sarlavha: {todo[1]}, Turi: {todo[2]}")
    except Exception as e:
        print(f"Todolarni o'qishda xatolik: {e}")

def update_todo():
    try:
        todo_id = int(input('Yangilash uchun todo ID ni kiriting: '))
        new_title = input('Yangi sarlavhani kiriting: ')
        new_todo_type = input('Yangi todo turini kiriting (optional/personal/shopping): ')

        update_todo = """UPDATE todos SET title = %s, todo_type = %s WHERE id = %s;"""
        cur.execute(update_todo, (new_title, new_todo_type, todo_id))
        conn.commit()
        print("Todo muvaffaqiyatli yangilandi!")
    except Exception as e:
        conn.rollback()
        print(f"Todo yangilashda xatolik: {e}")

def delete_todo():
    try:
        todo_id = int(input('Oʻchirish uchun todo ID ni kiriting: '))

        delete_todo = """DELETE FROM todos WHERE id = %s;"""
        cur.execute(delete_todo, (todo_id,))
        conn.commit()
        print("Todo muvaffaqiyatli o'chirildi!")
    except Exception as e:
        conn.rollback()
        print(f"Todo o'chirishda xatolik: {e}")

def todo_menu():
    while True:
        print("\nTodo Menyu:")
        print("1: Todo yaratish")
        print("2: Todolarni o'qish")
        print("3: Todo yangilash")
        print("4: Todo o'chirish")
        print("5: Chiqish")

        choice = input("Tanlovingizni kiriting: ")

        if choice == '1':
            create_todo()
        elif choice == '2':
            read_todos()
        elif choice == '3':
            update_todo()
        elif choice == '4':
            delete_todo()
        elif choice == '5':
            print("Chiqish...")
            break
        else:
            print("Noto'g'ri tanlov. Iltimos, qayta urinib ko'ring.")

def main_menu():
    while True:
        print("\nAsosiy Menyu:")
        print("1: Kirish")
        print("2: Ro'yxatdan o'tish")

        choice = input("Tanlovingizni kiriting: ")

        if choice == '1':
            if sign_in():
                break
        elif choice == '2':
            sign_up()
        else:
            print("Noto'g'ri tanlov. Iltimos, qayta urinib ko'ring.")