import time
debug = 1
def logs(testo):
    ora =  time.strftime('%d %b %p%H:%M %Y')
    if debug == 1:
        print(ora, testo)
var = "mario"
testo = "ciao "+ var
logs(testo)