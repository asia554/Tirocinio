import pigpio
import time

PIN_BASE = 4    # Destra/Sinistra
PIN_LEFT = 17   #AVANTI/INDIETRO
PIN_RIGHT = 27  #su/giu
PIN_CLAW = 22   #apre/chiude

pi = pigpio.pi()

if not pi.connected:
    print("ERRORE: pigpiod non è avviato")
    exit()

def sequenza_prendi():
    pi.set_servo_pulsewidth(PIN_CLAW, 1900) #apre del tutto la pinza
    time.sleep(1)
    pi.set_servo_pulsewidth(PIN_BASE, 1750)
    time.sleep(1)
    pi.set_servo_pulsewidth(PIN_LEFT, 1350)
    time.sleep(1)
    pi.set_servo_pulsewidth(PIN_RIGHT, 1200)
    time.sleep(1)
    pi.set_servo_pulsewidth(PIN_CLAW, 1250)
    time.sleep(1)
    pi.set_servo_pulsewidth(PIN_RIGHT, 1500)
    time.sleep(1)

posizione_base = 1500
pi.set_servo_pulsewidth(PIN_BASE, posizione_base)
posizione_left = 1500
pi.set_servo_pulsewidth(PIN_LEFT, posizione_left)
posizione_right = 1500
pi.set_servo_pulsewidth(PIN_RIGHT, posizione_right)
posizione_claw = 1500
pi.set_servo_pulsewidth(PIN_CLAW, posizione_claw)

if pi.connected:
    sequenza_prendi()
    pi.set_servo_pulsewidth(PIN_BASE, 0)
    pi.set_servo_pulsewidth(PIN_LEFT, 0)
    pi.set_servo_pulsewidth(PIN_RIGHT, 0)
    pi.set_servo_pulsewidth(PIN_CLAW, 0)
    pi.stop()
else:
    print("Erroe: pigpiod non risponde")