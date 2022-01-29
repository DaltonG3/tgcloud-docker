from telethon import TelegramClient, events, sync

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
api_id = 955988
api_hash = 'e952e7758184a420da64724e670d585e'
client = TelegramClient('backup', api_id, api_hash)
client.start()
async def main():
    async for dialog in client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id)
with client:
    client.loop.run_until_complete(main())







    # Getting information about yourself
    #me = await client.get_me()

    # "me" is an User object. You can pretty-print
    # any Telegram object with the "stringify" method:
    #print(me.stringify())

    # When you print something, you see a representation of it.
    # You can access all attributes of Telegram objects with
    # the dot operator. For example, to get the username:
    #username = me.username
    #print(username)
    #print(me.phone)

    # You can print all the dialogs/conversations that you are part of:
    #async for dialog in client.iter_dialogs():
    #    print(dialog.name, 'has ID', dialog.id)

    # You can send messages to yourself...

    # ...to some chat ID
    #await client.send_message(-100123456, 'Hello, group!')
    # ...to your contacts
    #await client.send_message('+34600123123', 'Hello, friend!')
    # ...or even to any username
    #await client.send_message('TelethonChat', 'Hello, Telethon!')

    # You can, of course, use markdown in your messages:
    #message = await client.send_message(
    #    'me',
    #    'This message has **bold**, `code`, __italics__ and '
    #    'a [nice website](https://lonamiwebs.github.io)!',
    #    link_preview=False
    #)

    # Sending a message returns the sent message object, which you can use
    #print(message.raw_text)

    # You can reply to messages directly if you have a message object
    #await message.reply('Cool!')

    # Or send files, songs, documents, albums...

    # You can print the message history of any chat:



        # You can download media from messages, too!
        # The method will return the path where the file was saved.
