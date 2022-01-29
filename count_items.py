import os, hashlib, calendar, time, shutil
from telethon import TelegramClient, events, sync, utils
from telethon.tl import types
from FastTelethon import download_file, upload_file
from config import *
from scripts import *
from config import *

async def main():
    messages=0
    total=0
    async for message in client.iter_messages(chatid,reverse=1,limit=None):
        if message.media is not None:
            msg=message.text
            size = message.file.size
            total = total + size
            messages += 1
            print ("total ==", total)
            print ("messages ==",messages)
            in_MB = total / 1024000
            print ("size in MB ==",in_MB)
            in_GB = in_MB / 1024
            print ("size in GB == ", in_GB)
            #print ("size ==",size)
            #print ("msg == "+msg)
            #path = msg.split(">>path<<",1)[1] # ottengo la stringa dopo il pattern specificato
            # print(message.id,message.text+">>name<<"+message.file.name)
            '''
            msg_id=message.id
            digest = re.search('>>md5<<(.*)>>timestamp<<', msg)
            md5 = digest.group(1)
            timestamp_tmp = re.search('>>timestamp<<(.*)>>path<<', msg)
            timestamp = timestamp_tmp.group(1)
            path = msg.split(">>path<<",1)[1]
            filename=message.file.name
            print("msg_id == "+str(msg_id))
            print("md5 == "+md5)
            print("timestamp == "+timestamp)
            print("path  == "+path)
            print("filename == ",filename)
            path_file = path+"/"+filename # preparo la variabile di download unendo il percorso e il nome del file
            #print("scarico in path_file"+path_file)
            print("cerco ",md5,"in ",files_present)
            '''
with client:
    client.loop.run_until_complete(main())