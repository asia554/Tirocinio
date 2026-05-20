import pigpio
import sys
import tty
import termios
import time

#Mappa dei PIN dei motori (seguendo la guida MeArm)
PIN_BASE = 4    # Destra/Sinistra
PIN_LEFT = 17   #AVANTI/INDIETRO
PIN_RIGHT = 27  #su/giu
PIN_CLAW = 22   #apre/chiude

#Funzione per leggere un tasto senza dover premere INVIO
def leggi_tasto():
    fd = sys.stdin.fileno()
    vecchie_impostazioni = termios.tcgetattr(fd)    #per memorizzare le vecchie impostazioni
    try:
        tty.setraw(sys.stdin.fileno())
        carattere = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, vecchie_impostazioni)
    return carattere

#Connessione ai motori
pi = pigpio.pi()

if not pi.connected:
    print("ERRORE: pigpiod non è avviato")
    exit()

#Impostiamo la Base al centro (1500 è il centro, range da 500 a 2500)
posizione_base = 1500
pi.set_servo_pulsewidth(PIN_BASE, posizione_base)

posizione_left = 1500
pi.set_servo_pulsewidth(PIN_LEFT, posizione_left)

posizione_right = 1500
pi.set_servo_pulsewidth(PIN_RIGHT, posizione_right)

posizione_claw = 1500
pi.set_servo_pulsewidth(PIN_CLAW, posizione_claw)

print("Legenda:")
print("Premi 'a' per girare a Sinistra")
print("Premi 'd' per girare a Destra")
print("Premi 'j' per andare indietro")
print("Premi 'l' per andare avanti")
print("Premi 't' per andare in su")
print("Premi 'g' per andare in giù")
print("Premi 'v' per chiudere pinza")
print("Premi 'b' per aprire pinza")
print("Premi 'q' per uscire")

#Il Ciclo di controllo
try:
    while True:
        tasto = leggi_tasto()
        
        if tasto == 'a':
            posizione_base += 50   # Aggiunge 50 per girare da un lato
            print(f"\rSinistra -> Posizione: {posizione_base}", end="")
            
        elif tasto == 'd':
            posizione_base -= 50   # Toglie 50 per girare dall'altro
            print(f"\rDestra -> Posizione: {posizione_base}  ", end="")

        elif tasto == 'j':
            posizione_left -= 50   # Toglie 50 per andare inietro

        elif tasto == 'l':
            posizione_left += 50   # Aggiungere 50 per andare avanti
            
        elif tasto == 't':
            posizione_right += 50   # Toglie 50 per andare in su

        elif tasto == 'g':
            posizione_right -= 50   # Aggiungere 50 per andare in giù

        elif tasto == 'v':
            posizione_claw -= 50   # Toglie 50 per chiudere la pinza

        elif tasto == 'b':
            posizione_claw += 50   # Aggiungere 50 per aprire la pinza

        elif tasto == 'q':
            break
            
        # Limiti di sicurezza per evitare di sforzare la plastica
        #base
        if posizione_base > 2400: posizione_base = 2400
        if posizione_base < 600: posizione_base = 600

        #left
        if posizione_left > 2100: posizione_left = 2100
        if posizione_left < 900: posizione_left = 900

        #right
        if posizione_right > 2000: posizione_right = 2000
        if posizione_right < 1000: posizione_right = 1000

        #claw
        if posizione_claw > 1900: posizione_claw = 1900
        if posizione_claw < 1200: posizione_claw = 1200
        
        # Manda il segnale elettrico al motore
        pi.set_servo_pulsewidth(PIN_BASE, posizione_base)
        pi.set_servo_pulsewidth(PIN_LEFT, posizione_left)
        pi.set_servo_pulsewidth(PIN_RIGHT,posizione_right)
        pi.set_servo_pulsewidth(PIN_CLAW,posizione_claw)

except KeyboardInterrupt:
    print("\r\nInterrotto da tastiera.")
finally:
    # Quando usciamo, spegniamo il segnale del motore per farlo riposare
    pi.set_servo_pulsewidth(PIN_BASE, 0)
    pi.set_servo_pulsewidth(PIN_LEFT, 0)
    pi.set_servo_pulsewidth(PIN_RIGHT, 0)
    pi.set_servo_pulsewidth(PIN_CLAW, 0)
    pi.stop()