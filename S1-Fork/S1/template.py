# coding: utf-8
########################################################################
# Mall för labb S1, DD1361 Programmeringsparadigm.
# Författare: Per Austrin
########################################################################

########################################################################
# Dessa funktioner är det som ska skrivas för att lösa de olika
# uppgifterna i labblydelsen.
########################################################################

def dna():          # uppgift 1
    return ""

def sorted():       # uppgift 2
    return ""

def hidden1(x):     # uppgift 3
    # indata x är strängen som vi vill konstruera ett regex för att söka efter
    return ""

def hidden2(x):     # uppgift 4
    # indata x är strängen som vi vill konstruera ett regex för att söka efter
    return ""

def equation():     # uppgift 5
    return ""

def parentheses():  # uppgift 6
    return ""

def sorted3():      # uppgift 7
    return ""


########################################################################
# Raderna nedan är lite testkod som du kan använda för att provköra
# dina regexar.  Koden definierar en main-metod som läser rader från
# standard input och kollar vilka av de olika regexarna som matchar
# indata-raden.  För de två hidden-uppgifterna används söksträngen
# x="test" (kan lätt ändras nedan).  Du behöver inte sätta dig in i hur
# koden nedan fungerar om du inte känner för det.
#
# För att provköra från terminal, kör:
# $ python s1.py
# Skriv in teststrängar:
# [skriv något roligt]
# ...
########################################################################
from sys import stdin
import re

def main():
    def hidden1_test(): return hidden1('test')
    def hidden2_test(): return hidden2('test')
    tasks = [dna, sorted, hidden1_test, hidden2_test, equation, parentheses, sorted3]
    print('Skriv in teststrängar:')
    while True:
        line = stdin.readline().rstrip('\r\n')
        if line == '': break
        for task in tasks:
            result = '' if re.search(task(), line) else 'INTE '
            print('%s(): "%s" matchar %suttrycket "%s"' % (task.__name__, line, result, task()))


if __name__ == '__main__': main()
