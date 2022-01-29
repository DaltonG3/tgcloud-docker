import os, hashlib, calendar, time, shutil, scripts,re, sys, fileinput,math, stat
from telethon import TelegramClient, events, sync, utils
from telethon.tl import types
from FastTelethon import download_file, upload_file
from config import *
import telethon
from tempfile import mkstemp
from shutil import move
from os import remove
local_md5 = []
kilobytes = 1024
megabytes = kilobytes * 1000
chunksize = int(maxsize * megabytes)
fname = "d41d8cd98f00b204e9800998ecf8427e"
if os.path.isfile(fname) is False:
    print("datastore non presente lo creo")
    f= open("d41d8cd98f00b204e9800998ecf8427e","w+")
    f.close()
def writelog(testo):
    if debug == 1:
        with open("log.txt", "a") as logfile:
            ora =  time.strftime('%d %b %p%H:%M %Y')
            print(ora, testo, file = logfile)
def upload_datastore_func():
    async def upload_datastore():        
        db_digest = get_md5("d41d8cd98f00b204e9800998ecf8427e")
        if db_digest != "d41d8cd98f00b204e9800998ecf8427e":
            msg_id = 1
            async for message in client.iter_messages(chatid,search="d41d8cd98f00b204e9800998ecf8427e"):
                msg_id=message.id
            message = await client.get_messages(chatid, ids=msg_id)
            if msg_id != 1:
                await message.delete()
            #time.sleep(3)
            await client.send_file(chatid,"d41d8cd98f00b204e9800998ecf8427e",caption="d41d8cd98f00b204e9800998ecf8427e")
        else: 
            print ("attenzione file datastore vuoto!")
            with open("d41d8cd98f00b204e9800998ecf8427e") as search:
                for line in search:
                    print (line)
                    if line == "":
                        print("---",file=open("d41d8cd98f00b204e9800998ecf8427e", "a"))
    with client:
        client.loop.run_until_complete(upload_datastore())

def check_if_exists(elem):
    if os.path.isfile(elem) is True:
        return 1
    else:
        return 0


async def main_remote_md5(): #ottengo tutti gli md5 in remoto
    md5_is_present=[]
    message = await client.get_messages(chatid)
    print(message)
    async for message in client.iter_messages(chatid):
        if message.text is not None:
            if ">>digest_cache<<" in message.text:
                md5_tmp = re.search('>>md5<<(.*)>>digest_cache<<', message.text)
                md5 = md5_tmp.group(1)
                md5_is_present.append(md5)
            else:    
                md5_is_present.append(message.text)
    print(md5_is_present)
    testo = "in main_remote_md5 md5_is_present == " + str(md5_is_present)
    writelog(testo)
    return md5_is_present
with client:
    md5_in_remote=client.loop.run_until_complete(main_remote_md5())

def obtain_info(elem):
    epoch_localfile = get_last_time_modified(elem) #ottengo i dati dell'ultima modifica del file
    dirpath_without_root = get_elem_without_root(elem)  #ne rimuovo il percorso base, lascio solo la sottocartella
    nomefile = get_nomefile(elem) #ottengo il nome del file
    dimension = os.path.getsize(elem)
    #is_file_present = search_in_array(dirpath_without_root,files_in_datastore) #conto il numero di elementi con nome dirpath_without_root
    return epoch_localfile,dirpath_without_root,nomefile, dimension#,is_file_present

def get_files_from_datastore():
    list_of_files=[]
    with open("d41d8cd98f00b204e9800998ecf8427e") as search:
        for line in search:
            list_of_files.append(line)
    return list_of_files



def get_file_data(message,list_of_files):
    msg=message
    if msg is not None:
        if ">>digest_cache<<" not in msg:
            var =  [s for s in list_of_files if msg in s]
            if not var :
                is_local = md5 = path = timestamp = epoch = ""
                return is_local, md5, path, timestamp, epoch
            else:
                for line in var:
                    path_tmp = re.search('>>file<<(.*)>>timestamp<<', line)
                    path = path_tmp.group(1)
                    digest = re.search('>>md5<<(.*)>>file<<', line)
                    md5 = digest.group(1)
                    is_local_tmp = re.search('>>is_local<<(.*)>>md5<<', line)
                    is_local = is_local_tmp.group(1)
                    filename=os.path.split(path)[1]
                    timestamp_tmp = re.search('>>timestamp<<(.*)>>epoch<<', line)
                    timestamp = timestamp_tmp.group(1)
                    epoch_tmp = re.search('>>epoch<<(.*)>>end_of_line<<', line)
                    epoch = epoch_tmp.group(1)
                    return is_local, md5, path, timestamp, epoch
        else:
            md5 = get_digest_cache(msg)
            print("get_gigest_cache == ", md5)
            list_tmp = search_in_datastore(md5)
            print("list_tmp ==", list_tmp)
            for line_tmp in list_tmp:
                if ">>digest_cache<<" not in line_tmp:
                    print("line_tmp== ",line_tmp)
                    path_tmp = re.search('>>file<<(.*)>>timestamp<<', line_tmp)
                    path = path_tmp.group(1)
                    is_local_tmp = re.search('>>is_local<<(.*)>>md5<<', line_tmp)
                    is_local = is_local_tmp.group(1)
                    filename=os.path.split(path)[1]
                    timestamp_tmp = re.search('>>timestamp<<(.*)>>epoch<<', line_tmp)
                    timestamp = timestamp_tmp.group(1)
                    epoch_tmp = re.search('>>epoch<<(.*)>>end_of_line<<', line_tmp)
                    epoch = epoch_tmp.group(1)
                    print("data obtained in else for digest_cache presetne",is_local, md5, path, timestamp, epoch)
                    return is_local, md5, path, timestamp, epoch
    else:
        is_local = md5 = path = timestamp = epoch = ""
        return is_local, md5, path, timestamp, epoch

def replace(file,searchExp,replaceExp):
    for line in fileinput.input(file, inplace=1):
        if searchExp in line:
            print("found "+line)
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)

def update_is_local(md5, is_local):
    testo = "md5 ==" + md5
    writelog(testo)
    if is_local == "no":
        testo = "update_is_local == no"
        writelog(testo)
        with open("d41d8cd98f00b204e9800998ecf8427e") as search:
            for line in search:
                line = line.rstrip()  # remove '\n' at end of line
                if md5 in line:
                    replace("d41d8cd98f00b204e9800998ecf8427e",">>is_local<<yes"+">>md5<<"+md5,">>is_local<<no"+">>md5<<"+md5)
    if is_local == "yes":
        testo = "update_is_local == yes"
        writelog(testo)
        with open("d41d8cd98f00b204e9800998ecf8427e") as search:
            for line in search:
                line = line.rstrip()  # remove '\n' at end of line
                if md5 in line:
                    print("replace (>>is_local<<no"+">>md5<<"+md5,">>is_local<<yes"+">>md5<<"+md5)
                    replace("d41d8cd98f00b204e9800998ecf8427e",">>is_local<<no"+">>md5<<"+md5,">>is_local<<yes"+">>md5<<"+md5)

def update_epoch(digest, dirpath_without_root, epoch_localfile):
    with open("d41d8cd98f00b204e9800998ecf8427e") as search:
        for line in search:
            line = line.rstrip()  # remove '\n' at end of line
            if digest in line and "digest_cache" not in line:
                path = get_path(line)
                replace_path(digest,dirpath_without_root)
                epoch = get_epoch(line)
                replace("d41d8cd98f00b204e9800998ecf8427e",">>epoch<<"+epoch,">>epoch<<"+epoch_localfile)
                time.sleep(1)

async def search_msg_id(md5):
    async for message in client.iter_messages(chatid,search=md5):
        if message.text is not None:
            if ">>digest_cache<<" not in message.text:
                msg_id = message.id
                return msg_id

async def search_msg_id_cache(md5):
    async for message in client.iter_messages(chatid,search=md5):
        if message.text is not None:
            if ">>digest_cache<<" in message.text:
                msg_id = message.id
                return msg_id


def upload(elem, dimension, nomefile,digest,timestamp,epoch_localfile,dirpath_without_root, n_file_current, n_file_total):
    try:
        if dimension > int(maxsize * 1024 * 1000): #se la dimensione sumepera la massima consentita
            print("file maggiore della dimensione specificata, procedo alla divisione...")
            split(elem, cache, nomefile, digest, timestamp, dimension , epoch_localfile , chunksize)
            was_uploaded = 0
            while was_uploaded != 1:
                was_uploaded = check_after_upload_cache(cache, digest, timestamp,dirpath_without_root,dimension)
                if was_uploaded == 1:
                    print(">>is_local<<"+"yes"+">>md5<<"+digest+">>file<<"+dirpath_without_root+">>timestamp<<"+str(timestamp)+">>epoch<<"+str(epoch_localfile)+">>end_of_line<<",file=open("d41d8cd98f00b204e9800998ecf8427e", "a"))
                    time.sleep(1)
            #upload_cache(cache, digest, timestamp,dirpath_without_root,dimension,epoch_localfile)
            print("")
        else: # se la dimensione NON supera la massima consentita
            was_uploaded = 0
            while was_uploaded != 1:
                upload_normal(elem,digest,dirpath_without_root,nomefile,epoch_localfile)
                print("")
                was_uploaded = check_after_upload(digest)
                testo = "was_uploaded == ", was_uploaded # attenzione ritorna un integer!!!
                writelog(testo)
                if was_uploaded == 1: #se il caricamento è stato positivo
                    print ("file uploaded successfully")
                    print("")
                    print(">>is_local<<"+"yes"+">>md5<<"+digest+">>file<<"+dirpath_without_root+">>timestamp<<"+str(timestamp)+">>epoch<<"+str(epoch_localfile)+">>end_of_line<<",file=open("d41d8cd98f00b204e9800998ecf8427e", "a"))
                    time.sleep(1)
                else: #se il caricamento non è stato positivo
                    print("< maxsize I file non sono stati caricati correttamente, procedo all'eliminazione e li ricarco...")
                    check_after_upload(dimension, digest, dirpath_without_root, nomefile)
        md5_in_remote.append(digest) #aggiungo l'md5 agli md5 remoti
    except Exception as e:
        ora =  time.strftime('%d %b %p%H:%M %Y')
        with open("log.txt", "a") as logfile:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno, file = logfile)
            print(ora,"Errore! == "+str(e), file = logfile)
        pass

def upload_normal(elem,digest,dirpath, nomefile,epoch_localfile): #upload files < 2GB
    client.start()
    async def main():
        result = await upload_file(client, out, nomefile, progress_callback=callback(nomefile))
        attributes, mime_type = utils.get_attributes(elem,)
        #print("attributes==",attributes)
        #time.sleep(10)
        media = types.InputMediaUploadedDocument(
            file=result,
            mime_type=mime_type,
            attributes=attributes,
            # not needed for most files, thumb=thumb,
            force_file=False
        )
        await client.send_file(chatid, caption=digest, file=result)
    with open(elem, "rb") as out:
        client.loop.run_until_complete(main())

def has_hidden_attribute(filepath):
    return bool(os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)

character_sets=["#","@","."]
def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName) # create a list of file and sub directories
    allFiles = list() #names in the given directory
    for entry in listOfFile: # Iterate over all the entries
        fullPath = os.path.join(dirName, entry) # Create full path
        if os.path.isdir(fullPath): # If entry is a directory then get the list of files in this directory
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            if os_name == "Windows":
                has_attribute = has_hidden_attribute(fullPath)
                testo = "has_attribute = " + has_attribute
                writelog(testo)
                if has_attribute == True and hidden_files == 1:
                    pass
                else:
                    allFiles.append(fullPath)
            if os_name == "Linux":
                non_aggiungere = 0
                var = fullPath.split("/")
                for elem in var:
                    if elem != "":
                        if elem[0] in character_sets:
                            non_aggiungere = 1
                if non_aggiungere == 1:
                    pass
                else:
                    allFiles.append(fullPath)
    return allFiles

async def download_datastore():
    async for message in client.iter_messages(chatid,search="d41d8cd98f00b204e9800998ecf8427e"):
        esiste = check_if_exists("d41d8cd98f00b204e9800998ecf8427e")
        if esiste == 1:
            print("sostituire il file datastore? ( Y | N )")
            choice= input()
            if choice == "Y" or choice == "y":
                await message.download_media(file="d41d8cd98f00b204e9800998ecf8427e", progress_callback=callback)
        else:
             await message.download_media(file="d41d8cd98f00b204e9800998ecf8427e", progress_callback=callback)

async def download(md5):
    md5_already_found=""
    async for message in client.iter_messages(chatid,search= md5):
        msg = message.text
        if message.media is not None:
            if "digest_cache" not in msg:
                files = search_in_datastore(md5)
                for file in files:
                    if "digest_cache" not in file:
                        path = get_path(file)
                        await message.download_media(file=dirName+path, progress_callback=callback)
                        esiste = check_if_exists(dirName+path)
                        epoch = get_epoch(file)
                        if esiste == 1:
                            update_epoch_localfile(dirName+path, epoch)
            else:
                if md5_already_found != md5:
                    asd_list_of_files = search_in_datastore(md5)
                    testo = "asd_listOfFiles" + str(asd_list_of_files)
                    writelog (testo)
                    for file in asd_list_of_files:
                        if "digest_cache" in file:
                            md5 = get_digest_cache(file)
                            is_local, digest, path, data_backup = get_file_data_cache(file)
                            print("path =="+cache+path,"path_file=="+dirName+path)
                            path_file = cache+"/"+path
                            epoch = get_epoch(file)
                            msg_id = await search_msg_id_cache(digest)
                            print("digest to search ==", digest)
                            print("msg:_id found ==", msg_id)
                            async for message in client.iter_messages(chatid,search= digest):
                                await message.download_media(file=cache+"/"+path, progress_callback=callback)
                            #await message.download_media(file=path_file, progress_callback=callback)
                            print("message.download_media(file="+path_file+", progress_callback=callback)")
                    files_in_datastore = search_in_datastore(md5)
                    epoch = ""
                    for file_in_datastore in files_in_datastore:
                        if file_in_datastore is not None:
                            if ">>digest_cache<<" not in file_in_datastore:
                                path = get_path(file_in_datastore)
                                epoch = get_epoch(file_in_datastore)
                    print("path =="+path)
                    path_file = dirName + path
                    join(cache, path_file)
                    print("join cache",cache,"path_file",path_file)
                    esiste = check_if_exists(path_file)
                    if esiste == 1:
                        delete_folder(cache)
                        update_is_local(md5, is_local)
                        update_epoch_localfile(path_file, epoch)
                        md5_already_found=md5
                else:
                    print("md5_already found", md5_already_found)

def get_file_data_cache(message):
    msg=message
    md5_tmp = re.search('>>md5<<(.*)>>digest_cache<<', msg)
    md5 = md5_tmp.group(1)
    md5_cache_tmp = re.search('>>digest_cache<<(.*)>>file<<', msg)
    digest = md5_cache_tmp.group(1)
    cache_list = search_in_datastore(digest)
    for cache_element in cache_list:
        is_local = get_is_file_present(cache_element)
        path = get_path(cache_element)
        data_backup = get_timestamp(cache_element)
        return is_local, digest, path, data_backup



def update_epoch_localfile(path_file, epoch):
    os.utime(path_file, (int(epoch) - 100, int(epoch)))

def join(fromdir, tofile): #ricomponi file splittato problema della cartella inesisttente
    path_tmp=os.path.split(tofile)[0]
    if not os.path.exists(path_tmp):                  # caller handles errors
        print("os.mkdir",path_tmp)
        os.makedirs(path_tmp)
    print("fromdir "+fromdir,"tofile",tofile)
    output = open(tofile, 'wb')
    parts  = os.listdir(fromdir)
    print("parts ==", parts)
    parts.sort(  )
    for filename in parts:
        filepath = os.path.join(fromdir, filename)
        fileobj  = open(filepath, 'rb')
        while 1:
            filebytes = fileobj.read(maxsize)
            if not filebytes: break
            output.write(filebytes)
        fileobj.close(  )
    output.close(  )


def split(elem, cache, nomefile, md5, timestamp, dimension, epoch_localfile,chunksize=chunksize): #divido i file in base alle impostazioni
    #print ("cache ==", cache)
    #time.sleep(10)
    if not os.path.exists(cache):                  # caller handles errors
        os.mkdir(cache)                            # make dir, read/write parts
    else:
        for fname in os.listdir(cache):            # delete any existing files
            os.remove(os.path.join(cache, fname)) 
    partnum = 0
    input = open(elem, 'rb')                   # use binary mode on Windows
    while 1:                                       # eof=empty string from read
        chunk = input.read(chunksize)              # get next part <= chunksize
        if not chunk: break
        partnum  = partnum+1
        filename = os.path.join(cache, (nomefile+'.part%02d' % partnum))
        fileobj  = open(filename, 'wb')
        fileobj.write(chunk)
        fileobj.close()
        upload_cache(cache,md5,timestamp, filename, dimension,epoch_localfile)
        os.remove(filename)
    input.close(  )
    assert partnum <= 9999                         # join sort fails if 5 digits
    return partnum


def upload_cache(cache,digest,timestamp,dirpath_without_root,dimension,epoch_localfile):
    client.start()
    listOfFiles = getListOfFiles(cache) # Get the list of all files in directory tree at given path
    listOfFiles = list() # Get the list of all files in directory tree at given path    
    for (dirpath, dirnames, filenames) in os.walk(cache):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]    
    for elem_cache in listOfFiles:  # Print the files 
        print ("Parte Trattata == ", elem_cache)
        print("")
        nomefile_cache = elem_cache[elem_cache.rindex('/')+1:]
        dirpath_without_root_cache = elem_cache.split(cache,1)[1] #ottengo il perscorso togliendo tutto cio che è dopo la root
        digest_cache=get_md5(elem_cache)
        async def main_cache():
            result = await upload_file(client, out, nomefile_cache, progress_callback=callback)
            attributes, mime_type = utils.get_attributes(
                elem_cache,
            )
            media = types.InputMediaUploadedDocument(
                file=result,
                mime_type=mime_type,
                attributes=attributes,
                # not needed for most files, thumb=thumb,
                force_file=False
            )
            await client.send_file(chatid, caption=">>md5<<"+digest+">>digest_cache<<"+digest_cache+">>end_of_line<<", file=result)
            was_uploaded = 0
            #print("setto la variabile was_uploaded == 0")
            while was_uploaded != 1:
                is_present = []
                message = await client.get_messages(chatid)
                async for message in client.iter_messages(chatid,search=digest_cache):
                    is_present.append(message.id)
                number_of_items = len(is_present)
                #print("number_of_items (remote) ==", number_of_items)
                if number_of_items < 1:
                    was_uploaded = 0
                else:
                    was_uploaded = 1
                if was_uploaded == 1:
                    print (elem_cache+" uploaded successfully")
                    print(">>is_local<<"+"yes"+">>md5<<"+digest+">>digest_cache<<"+digest_cache+">>file<<"+nomefile_cache+">>timestamp<<"+str(timestamp)+">>epoch<<"+str(epoch_localfile)+">>end_of_line<<",file=open("d41d8cd98f00b204e9800998ecf8427e", "a"))
                else:
                    main_cache()
        with open(elem_cache, "rb") as out:
            client.loop.run_until_complete(main_cache())
            
def delete_folder(folder): # mi cancella la cache
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def callback(nomefile,current, total): # def per visionare la percentuale
    print(nomefile,' Transferred', current, 'out of', total,'bytes: {:.1%}'.format(current / total), end="\r")

def get_list_of_files_present(): #ottengo la lista degli md5 locali, e aggiungo li aggiungo ad un array
    files_present = []
    listOfFiles = getListOfFiles(dirName) # Get the list of all files in directory tree at given path
    listOfFiles = list() # Get the list of all files in directory tree at given path    
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]   
    for elem in listOfFiles:  # Print the files
        writelog(elem)
        digest = get_md5(elem)
        files_present.append(digest)
        nomefile = elem[elem.rindex('/')+1:]
        testo = "digest "+digest+" è stato aggiunto alla lista dei file presenti"
        writelog (testo)
    return files_present

def get_md5(elem):
    with open(elem, "rb") as f:
        file_hash = hashlib.md5()
        chunk = f.read(1024000)
        while chunk:
            file_hash.update(chunk)
            chunk = f.read(1024000)
        #print("file hash ==",file_hash.hexdigest())
        digest = file_hash.hexdigest()
    return digest

def check_after_upload_cache(cache, digest, timestamp,dirpath_without_root,dimension):
    client.start()
    is_present = []
    async def main():
        message = await client.get_messages(chatid)
        async for message in client.iter_messages(chatid,search=digest):
            is_present.append(message.id)
    with client:
        client.loop.run_until_complete(main())
    print("ID presenti (parti) ==", is_present)
    file_parts = (dimension/chunksize)
    #number_of_items = check_if_present(digest)
    number_of_items = len(is_present)
    if number_of_items < file_parts:
        was_uploaded = 0
        print("number_of_items ==", number_of_items)
        print("file_parts ==", file_parts)
        print("errore, i file non sono sufficienti!!!", number_of_items ,"è minore di ", file_parts)
        for id in is_present:
            async def main():
                message = await client.get_messages(chatid, ids=id)
                await message.delete()
                time.sleep(3)
            with client:
                client.loop.run_until_complete(main())
        remove_line(digest)
        print("")
    else:
        print("tutti i file sono presenti")
        was_uploaded = 1
    return was_uploaded

def check_after_upload(digest):
    is_present = []
    async def main_is_md5_present():
        message = await client.get_messages(chatid)
        async for message in client.iter_messages(chatid,search=digest):
            is_present.append(message.id)
    with client:
        client.loop.run_until_complete(main_is_md5_present())
    number_of_items = len(is_present)
    #print("number_of_items (remote) ==", number_of_items)
    if number_of_items < 1:
        was_uploaded = 0
    else:
        #print("file presente!!!")
        was_uploaded = 1
    return was_uploaded

def check_if_present(digest): #check if one md5 is in list nel messaggio
    client.start()
    is_present = []
    async def main():
        
        message = await client.get_messages(chatid)
        async for message in client.iter_messages(chatid,search=digest):
            is_present.append(message.id)
    with client:
        client.loop.run_until_complete(main())
    number = len(is_present)
    #print("dentro a check_if_present number == "+str(number))
    if number > 0:
        is_file_present = 1
    else:
        is_file_present = 0
    return is_file_present

def verify_path(dirpath): #verifico che ci sia la cartella, se non esiste, la creo
    var = os.path.split(dirpath)
    print ("var == ",var[0])
    if os.path.exists(var[0]):
        print(var[0] + ' : exists')
    else:
        print(var[0] , 'dosnt exist')
        print("la creo!!!")
        os.makedirs(var[0])
        if os.path.exists(var[0]):
            print(var[0] + ' : exists')



def remove_line(digest):
  with open("d41d8cd98f00b204e9800998ecf8427e", "r") as input:
      with open("temp_file", "w") as output:
          # iterate all lines from file
          for line in input:
              # if substring contain in a line then don't write it
              if digest not in line.strip("\n"):
                  output.write(line)

  # replace file with original name
  os.replace('temp_file', 'd41d8cd98f00b204e9800998ecf8427e')

def replace(file,old,new):
    fin = open(file, "rt")
    data = fin.read()
    data = data.replace(old, new)
    fin.close()
    fin = open(file, "wt")
    fin.write(data)
    fin.close()

def replace_path(digest,dirpath_without_root,timestamp,epoch_localfile):
    with open("d41d8cd98f00b204e9800998ecf8427e") as search:
        for line in search:
            testo = "line ==" + line
            writelog (testo)
            line = line.rstrip()  # remo
            if digest in line and ">>digest_cache<<" not in line:
                replace("d41d8cd98f00b204e9800998ecf8427e",line,">>is_local<<yes>>md5<<"+str(digest)+">>file<<"+dirpath_without_root+">>timestamp<<"+str(timestamp)+">>epoch<<"+str(epoch_localfile)+">>end_of_line<<")

async def update_presence(md5): #aggiorno il messaggio se il file non è piu presente
    async for message in client.iter_messages(chatid,search=md5):
        msg = message.text
        msg_id = message.id
        path = msg.split(">>path<<",1)[1]
        digest = re.search('>>md5<<(.*)>>timestamp<<', message.text)
        md5 = digest.group(1)
        timestamp_tmp = re.search('>>timestamp<<(.*)>>path<<', message.text)
        timestamp = timestamp_tmp.group(1)
        testo = "path ==" + str(path)
        writelog = (testo)
        await client.edit_message(chatid,msg_id,">>is_local<<"+"no"+">>md5<<"+md5+">>timestamp<<"+str(timestamp)+">>path<<"+path)
'''
            md5_tmp = re.search('>>md5<<(.*)>>file<<', line)
            md5 = md5_tmp.group(1)
            if md5 == digest:
                fileold = ">>md5<<"+digest+">>file<<"+path
                filenew= ">>md5<<"+digest+">>file<<"+dirpath_without_root
                print ("sostituisco ",fileold,filenew)
                replace("d41d8cd98f00b204e9800998ecf8427e",fileold,filenew)
                time.sleep(1)
                print("sostituito")
'''
def get_last_time_modified(elem):
    epoch_localfile=math.trunc(os.path.getmtime(elem))
    return epoch_localfile
def get_elem_without_root(elem):
    dirpath_without_root = elem.split(dirName,1)[1]
    return dirpath_without_root

def get_nomefile(elem):
    if os_name == "Linux":
        nomefile = elem[elem.rindex('/')+1:]
    else:
        nomefile = elem[elem.rindex('\\')+1:]
    return nomefile

def get_path(line):
    path_tmp = re.search('>>file<<(.*)>>timestamp<<', line)
    path = path_tmp.group(1)
    return path

def get_epoch(line):
    epoch_tmp = re.search('>>epoch<<(.*)>>end_of_line<<', line)
    epoch = epoch_tmp.group(1)
    return epoch

def get_timestamp(line):
    timestamp_tmp = re.search('>>timestamp<<(.*)>>epoch<<', line)
    timestamp = timestamp_tmp.group(1)

def search_in_array(item,array):
    result = sum(str(item) in s for s in array)
    return result

def search_in_datastore(var):
    strings = []
    with open("d41d8cd98f00b204e9800998ecf8427e") as search:
        for line in search:
            line = line.rstrip()  # remove '\n' at end of line
            if var in line:
                #print("trovato!!",line)
                strings.append(line)
    if strings:
        return strings

def check_if_newer(file_present, epoch_localfile):
    if debug == 1 : 
        ora =  time.strftime('%d %b %p%H:%M %Y')
        with open("log.txt", "a") as logfile:
            print(ora, "in check_if_present line == ", file_present, file = logfile)
    epoch = get_epoch(file_present)
    md5= get_digest(file_present)
    if debug == 1 : 
        ora =  time.strftime('%d %b %p%H:%M %Y')
        with open("log.txt", "a") as logfile:
            print (ora, "in check_if_newer epoch ==", epoch, file = logfile)
    if epoch_localfile > int(epoch):
        update_is_local(md5,"no")
        return 1
    else:
        return 0

def get_digest(line):
    digest = re.search('>>md5<<(.*)>>file<<', line)
    md5 = digest.group(1)
    return md5

def get_digest_cache(line):
    digest = re.search('>>md5<<(.*)>>digest_cache<<', line)
    md5 = digest.group(1)
    return md5

def get_is_file_present(line):
    is_file_present = re.search('>>is_local<<(.*)>>md5<<', line)
    is_file_present = is_file_present.group(1)
    return is_file_present

'''
async def update_presence(md5): #aggiorno il messaggio se il file non è piu presente
    async for message in client.iter_messages(chatid,search=md5):
        msg = message.text
        msg_id = message.id
        path = msg.split(">>path<<",1)[1]
        digest = re.search('>>md5<<(.*)>>timestamp<<', message.text)
        md5 = digest.group(1)
        timestamp_tmp = re.search('>>timestamp<<(.*)>>path<<', message.text)
        timestamp = timestamp_tmp.group(1)
        print("path ==",path)
        await client.edit_message(chatid,msg_id,">>is_local<<"+"no"+">>md5<<"+md5+">>timestamp<<"+str(timestamp)+">>path<<"+path)
'''
print("arrivato alla fine di scripts")