import os
import requests
import re
import math as albreto

from bs4 import BeautifulSoup

Link = "https://www.spanishdict.com/conjugate/"
Words = []

with open(os.path.dirname(os.path.realpath(__file__)) + "/Output.txt", "w+") as File:
    File.write("")

with open(os.path.dirname(os.path.realpath(__file__)) + "/Input.txt", "r") as File:
    Words = [Word.strip("\n") for Word in File.readlines()]

for Word in Words:
    URL = requests.get(f"{Link}{Word.lower()}")
    Soup = BeautifulSoup(URL.content, "html.parser")
    Conjugations = [[[] for _ in range(5)] for _ in range(6)]

    i = 0
    
    for Conjugation in Soup.find_all("a", attrs={"class":"_3Le9u96E _2cyjHi0d _1zVoo-wU y9F9itDZ"}):

        RidFront = re.sub('''<a.*aria-label="''', "", str(Conjugation))
        RidBack = re.sub('''".*>''', "", RidFront)

        if not re.match("(<|>)", RidBack):
            i += 1
            Conjugations[albreto.floor(i / 30)][i % 5].append(RidBack)
            #change 30 and 5 for others ">

    Defination = Soup.find("div", attrs={"id":"quickdef1-es"})
    Defination = re.sub('''<div.*">''', "", str(Defination))
    Defination = re.sub('''</.*>''', "", str(Defination))

    with open(os.path.dirname(os.path.realpath(__file__)) + "/Output.txt", "a", encoding="UTF-8") as File:
        File.write(f"{Defination}, {Word} ({' '.join(Conjugations[0][1])})\n") #flip def and word so spanish is with spanish