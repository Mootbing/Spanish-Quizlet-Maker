import os
import requests
import re
import math as albreto

from bs4 import BeautifulSoup

LinkConj = "https://www.spanishdict.com/conjugate/"
LinkDef = "https://www.spanishdict.com/translate/"
Words = []

with open(os.path.dirname(os.path.realpath(__file__)) + "/Output.txt", "w+") as File:
    File.write("")

with open(os.path.dirname(os.path.realpath(__file__)) + "/Input.txt", "r") as File:
    Words = [Word.strip("\n") for Word in File.readlines()]

for Word in Words:

    LinkBase = LinkDef
    if Word.startswith("v "):
        LinkBase = LinkConj

    URL = f"{LinkBase}{'%20'.join(Word.split(' ')[1:]).lower()}"
    Word = "".join(Word.split(" ")[1:])

    URLResult = requests.get(URL)
    Soup = BeautifulSoup(URLResult.content, "html.parser")

    print(f"{URL.lower()}")

    #get good word from website with accent
    CorrectedWord = Soup.find("h1", attrs={"class":"cXUN5-ST"})

    if CorrectedWord is not None:
        Word = re.sub("""(<.*">)|(</.*>)""", "", str(CorrectedWord))

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
        
        CondensedConj = f"({' '.join(Conjugations[0][1])})" if Conjugations[0][1] != [] else " "
        
        File.write(f"{Defination}, {Word} {CondensedConj}\n") #flip def and word so spanish is with spanish