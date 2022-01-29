import platform, os
os_name = platform.system()
print(os_name)
chatid = -123456789 # es. 
maxsize = 2047 # in MB
api_id = '123456' #
api_hash = 'e123e1231231a123ee123123e123d123e'
debug = 1 # mettere a 1 per visualizzare i log a CLI
hidden_files = 1 # will hidden files be ignored? 1 = yes 0 = no
# il programma non considera la variazione di sistema operativo, se il backup è su linux il restore deve essere su linux, stessa cosa per windows
if os_name == "Windows":
    dirName = 'C:\\Users\\utente\\Desktop\\tg-python\\input'
    cache = 'C:\\Users\\utente\\Desktop\\tg-python\\cache'
elif os_name == "Linux":
    dirName = '/source' #senza slash finale!!
    cache = '/cache/musica'
    if not os.path.exists(cache):                  # caller handles errors
        os.mkdir(cache)                            # make dir, read/write parts
    else:
        for fname in os.listdir(cache):            # delete any existing files
            os.remove(os.path.join(cache, fname))
#optional
step = 2 # ogni quanto si vuole aggiornare il database remoto
#don't change...
from telethon import TelegramClient, events, sync
client = TelegramClient('backup', api_id, api_hash)

