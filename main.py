# -*-coding=utf-8-*-
# Import de la librairie "smbus" pour communiquer via le bus I2C
import smbus

# Import de "Flask" pour la creation d'un serveur
from flask import Flask
# Import de "Threading" pour la gestion des threads
from threading import Thread

# On import les autres librairies nécessaires
from time import sleep
from helpers import *


# Class Gameloop qui gere le systeme
class gameLoop(Thread):
    """docstring for gameLoop"""

    def __init__(self):
        Thread.__init__(self)
        self.continuer = True

    def run(self):
        print('Start Game Loop')
        while self.continuer:
            checkedBox = [] #Stock les bonnes connexions
            for i in range(0, 8):
                # print("1 -> Cable " + str(i) + " Activé")
                bus.write_byte(addr_CABLES, CABLES[i]) #Active les câbles un par un

                # print("2 -> Etat de \"CABLES\" = " + str(bin(bus.read_byte(addr_CABLES)))[2:].zfill(8))

                boxes_data = str(bin(bus.read_byte(addr_BOXES)))[2:].zfill(8) #
                # print("3 -> Etat de \"BOXES\" = " + boxes_data)

                # print("4 -> Connexion = " + str(getBox(boxes_data, i)))

                checkedBox.append(getBox(boxes_data, i))

                # print('')

                # print(checkedBox)
            getLeds(checkedBox)

            bus.write_byte_data(addr_LEDS, GREEN, getLeds(checkedBox))
            bus.write_byte_data(addr_LEDS, 0x13, (159 - getLeds(checkedBox)))

    def stop(self):
        self.continuer = False
        print("Stop Game Loop")


addr_LEDS = 0x20
addr_CABLES = 0x3f
addr_BOXES = 0x38

bus = smbus.SMBus(1)

bus.write_byte_data(addr_LEDS, 0x00, 0x00)
bus.write_byte_data(addr_LEDS, 0x01, 0x00)

GREEN = 0x12
RED = 0x13

CABLES = [0xFE, 0xFD, 0xFB, 0xF7, 0xEF, 0xDF, 0xBF, 0x7F]

bus.write_byte(addr_BOXES, 0xFF)
bus.write_byte_data(addr_LEDS, RED, 159)

print('MODULE 01 Started')
app = Flask(__name__)
global game


@app.route('/start')
def start():
    global game
    game = gameLoop()
    game.start()
    # game.join()
    return "Game Loop started"


@app.route('/stop')
def stop():
    global game
    game.stop()
    bus.write_byte_data(addr_LEDS, GREEN, 0)
    bus.write_byte_data(addr_LEDS, RED, 255)
    return "Game Loop Stopped"
