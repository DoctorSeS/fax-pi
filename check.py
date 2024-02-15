import fileinput
from termcolor import colored, cprint
import os

def enrole():
  file = open("all_servers.txt", "r")
  all = file.read()
  all2 = str(all).replace("[", "")
  all3 = str(all2).replace("]", "")
  all4 = str(all3).replace(",", "")
  all5 = str(all4).replace("'", "")
  cprint("Enroling executed.", "blue")
  return list(all5.split(" "))

all = enrole()

if all:
  cprint("Running main...", "green")
  exec(open('main.py').read())
else:
  cprint("DEPLOYMENT FAILED, CANNOT READ ALL SERVERS\nPLEASE RESOLVE THIS ISSUE ASAP", "red")
  os.system("kill 1")
