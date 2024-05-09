import sqlite3 as sq
from aiogram import html


async def db_start():
    global db, cur

    db = sq.connect('wishes.db')
    cur = db.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS wishes(wish_id TEXT PRIMARY KEY, author TEXT, name TEXT, description TEXT, giver TEXT)")

    db.commit()


async def create_wish(wish_id, author, name, description, giver):
    cur.execute("INSERT INTO wishes VALUES(?, ?, ?, ?, ?)", (wish_id, author, name, description, giver))
    db.commit()


async def delete_wish(wish_id, user):
    cur.execute("SELECT author FROM wishes WHERE wish_id = ?", (wish_id,))
    author = cur.fetchone()[0]
    if author != user:
        return "Вы не можете удалить не свою хотлеку"
    cur.execute("DELETE FROM wishes WHERE wish_id = ?", (wish_id,))
    db.commit()
    return "Хотелка удалена"


async def look_wishes(author, check_myself: bool):
    cur.execute("SELECT * FROM wishes WHERE author = ?", (author,))
    result = f"Ваши хотелки:\n" if check_myself else f"Хотелки {author}:\n"
    rows = cur.fetchall()
    for row in rows:
        result += f"\n{html.bold('id хотелки:')}\n"
        result += f"{row[0]}\n"
        result += f"{html.bold('название хотелки:')}\n"
        result += f"{row[2]}\n"
        result += f"{html.bold('описание хотелки:')}\n"
        result += f"{row[3]}\n"
        if not check_myself:
            result += f"{html.bold('тот, кто забронировал хотелку:')}\n"
            result += f"{row[4]}\n"
        result += f"\n"
    if len(rows) == 0:
        result = "У вас нет хотелок\n" if check_myself else "У пользователя нет хотелок\n"
    return result


async def rent_wish(wish_id, user):
    cur.execute("SELECT author FROM wishes WHERE wish_id = ?", (wish_id,))
    author = cur.fetchone()[0]
    if author == user:
        return "Вы не можете забронировать свою собственную хотелку"
    cur.execute("UPDATE wishes SET giver = ? WHERE wish_id = ?", (user, wish_id))
    db.commit()
    return "Хотелка забронированна"


async def stop_rent(wish_id, user):
    cur.execute("SELECT giver FROM wishes WHERE wish_id = ?", (wish_id,))
    giver = cur.fetchone()[0]
    if (giver != user):
        return "Вы и так не бронировали эту хотелку"
    cur.execute("UPDATE wishes SET giver = ? WHERE wish_id = ?", ("no_one", wish_id))
    return "Вы больше не дарите эту хотелку"
