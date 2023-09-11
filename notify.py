import datetime
from settings import ID
from avito import parse
from sqlite3 import connect


def notify(bot):
    print(datetime.datetime.now())
    print('INTO NOTIFY!')
    links = parse()
    print('PARSED!')

    con = connect("avito.sqlite3")
    cur = con.cursor()
    table_exists = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='links';").fetchone()
    if not table_exists:
        cur.execute("CREATE TABLE links(link);")
        cur.executemany("INSERT INTO links VALUES (?)", list(map(lambda x: (x, ), links)))
        for link in links:
            bot.send_message(ID, link)
            pass
    else:
        links_exist = list(map(lambda x: x[0], cur.execute("SELECT link FROM links").fetchall()))
        for link in links:
            if link not in links_exist:
                cur.execute(f"INSERT INTO links VALUES ('{link}')")
                bot.send_message(ID, link)
                print('MESSAGE SENT!')
    print('-' * 32)
    con.commit()