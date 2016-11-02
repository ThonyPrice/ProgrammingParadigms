# Project:              S1 - Programmeringsparadigm
# Authors:              Thony Price 
# Last revision:        2016-11-01

#!/usr/bin/python
import re

def dna():              # Uppgift 1
    return "^[ACGT]+$"
    
def sorted():           # Uppgift 2
    return "^9*8*7*6*5*4*3*2*1*0*$"
    
def hidden1(x):         # Uppgift 3
    # Indata x är strängen som vi vill konstruera ett regex för att söka efter
    return x
    
def hidden2(x):         # Uppgift 4
    # Indata x är strängen som vi vill konstruera ett regex för att söka efter
    # Tanke: Om x är "progp" kan regex vara: .*p.*r.*o.*g.*p.*
    r = ""
    for letter in x:
        r += ".*" + str(letter)
    r += ".*"
    return r

def equation():         # Uppgift 5
    return "^(\+|\-)?\d+([\+\-\*\/]\d+)*([\=](\+|\-)?\d+([\+\-\*\/]\d+)*)?$"

def parentheses():      # Uppgift 6
    return "^(\((\((\((\((\(\))*\))*\))*\))*\))*$"

def sorted3():          # Uppgift 7
    return ""


