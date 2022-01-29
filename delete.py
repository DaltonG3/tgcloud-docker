from telethon import TelegramClient, events, sync
from config import *
import os
client = TelegramClient('delete', api_id, api_hash)
client.start()
async def main():
    async for message in client.iter_messages(chatid):
        await message.delete()
print("are you ABSOLUTELY sure? This will erase EVERITHING in the chat specified!   (yes | no)")
choice = input()
if choice == "yes":
    with client:
        client.loop.run_until_complete(main())
