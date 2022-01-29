from posixpath import dirname
from telethon import TelegramClient, events, sync, utils, functions
from telethon.tl import types
from FastTelethon import download_file, upload_file
from config import *
import os, hashlib, re, time, shutil, datetime
from scripts import *
print("Select an option:")
print("")
print("1 - Restore at last backup state (rewrite existing files)")
print("2 - Restore EVERITHING (you sure?)(rewrite existing files)")
print("3 - Restore at last backup state (leave existing files)")
print("4 - Restore EVERITHING (you sure?)(leave existing files)")
print("5 - Just one file... ()search")
initial_choice = input()
async def main():
    await download_datastore()
    print("ottengo la lista dei file presenti...")
    listOfFiles = getListOfFiles(dirName) # Get the list of all files in directory tree at given path
    listOfFiles = list() # Get the list of all files in directory tree at given path
    list_of_files=get_files_from_datastore()
    if initial_choice == "5":
        print("inserire il testo da cercare...")
        search = input()
        search_list = search_in_datastore(search)
        for element in search_list:
            if ">>digest_cache<<" not in element:
                is_local, md5, path, timestamp , epoch = get_file_data(element,list_of_files)
                epoch_date = datetime.datetime.fromtimestamp(int(epoch)).strftime('%Y-%m-%d %H:%M:%S')
                if path == "":
                    print("no data found!")
                else:
                    print("md5 ==", md5)
                    msg_id = await search_msg_id(md5)
                    if msg_id is None:
                        msg_id = await search_msg_id_cache(md5)
                    print (msg_id,"||",path,"||",epoch_date)
                    print("")
                    time.sleep (1)
                    print("digitare l'id del messaggio da scaricare")
                    id_da_scaricare = input()
                    message = await client.get_messages(chatid, ids=int(id_da_scaricare))
                    print("message.text ==", message.text)
                    if ">>digest_cache<<" in message.text:
                        digest = get_digest_cache(message.text)
                    else:
                        digest = message.text
                    temp_list = search_in_datastore(digest)
                    print(temp_list)
                    for temp_elem in temp_list:
                        if ">>digest_cache<<" not in temp_elem:
                            path_composto = get_path(temp_elem)
                    esiste = check_if_exists(dirName+path_composto)
                    if esiste == 1:
                        print("file esistente, vuoi sovrascriverlo? ( y | n )")
                        decision = input()
                        if decision == "y" or decision == "Y":
                            await download(md5)
                            esiste = check_if_exists(dirName+path_composto)
                            print("esiste2 ?",dirName+path_composto,esiste)
                            if esiste == 1:
                                break
                    else:
                        await download(md5)
                        esiste = check_if_exists(dirName+path_composto)
                        print("esiste 3?",dirName+path_composto)
                        if esiste == 1:
                            break
                        
                        
    else:
        async for message in client.iter_messages(chatid,reverse=1,limit=None):
            if message.media is not None:
                if "d41d8cd98f00b204e9800998ecf8427e" not in message.text:
                    is_local, md5, path, timestamp , epoch = get_file_data(message.text,list_of_files)
                    esiste = check_if_exists(dirName+path)
                    if esiste == 1:
                        print ("file esistente!!!", dirName+path)
                        epoch_localfile,dirpath_without_root,nomefile, dimension = obtain_info(dirName+path)
                        if epoch != str(epoch_localfile) and initial_choice == "1" and is_local == "yes":
                            await download(md5)
                        elif epoch != str(epoch_localfile) and initial_choice == "2" and is_local == "no":
                            await download(md5)
                        elif epoch != str(epoch_localfile) and initial_choice == "3" and is_local == "yes":
                            print("is local but initial choice was to leave the file")
                        elif epoch != str(epoch_localfile) and initial_choice == "4" and is_local == "no":
                            print("is not local but initial choice was to leave the file")
                    else:
                        if is_local == "yes":
                            await download(md5)
                        if is_local == "no" and initial_choice == "2":
                            await download(md5)
                        if is_local == "no" and initial_choice == "4":
                            await download(md5)
with client:
    client.loop.run_until_complete(main())