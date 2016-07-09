#!/usr/bin/python

# -*- coding: utf-8 -*-

from time import sleep
import RPi.GPIO as GPIO
import subprocess

def play_mp3(path):
    subprocess.Popen(['mpg123', '-q', path])

def play_drum1_sound():
    play_mp3("drum1.mp3")

def play_drum2_sound():
    play_mp3("drum2.mp3")

CS_DRUM1 = 8
CS_DRUM2 = 7
DOUT = 9
CLK = 11

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(CS_DRUM1, GPIO.OUT)
GPIO.setup(CS_DRUM2, GPIO.OUT)
GPIO.setup(DOUT, GPIO.IN)
GPIO.setup(CLK, GPIO.OUT)

def get_drum_val(cs):
    GPIO.output(cs, True)
    GPIO.output(CLK, True)
    GPIO.output(cs, False)
    binData = 0
    i1 = 14

    while (i1 >= 0):
        GPIO.output(CLK, False)
        bitDOUT = GPIO.input(DOUT)
        GPIO.output(CLK, True)
        bitDOUT = bitDOUT << i1
        binData |= bitDOUT
        i1 -= 1

    GPIO.output(cs, True)
    binData &= 0xFFF

    return int(round(512.0 * binData / 4096.0, 0))

while (True):
    drum1_val = get_drum_val(CS_DRUM1)
    drum2_val = get_drum_val(CS_DRUM2)

    if drum1_val >= 2:
        play_drum1_sound()

    if drum2_val >= 2:
        play_drum2_sound()

    if drum1_val >= 2 or drum2_val >= 2:
        print "%d - %d" % (drum1_val, drum2_val)
        sleep(0.05)

    if drum1_val > 10 or drum2_val > 10:
        sleep(0.1)

    sleep(0.001)
