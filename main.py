from loader import dp
from data_base.base import conn
from aiogram.utils import executor


async def on_startup(_):
    print("Бот вышел в онлайн")
    try:
        ans = conn.query("MATCH (n) RETURN n", db='neo4j')
        # for i in list(ans):
        #     print(i)
        print("База подключена")
    except:
        print("База НЕ подключена")


from handlers import client, admin, other

client.register_client_handler(dp)
admin.register_admin_handler(dp)
other.register_other_handler(dp)

executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
