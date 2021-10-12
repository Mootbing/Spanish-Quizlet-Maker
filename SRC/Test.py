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

def Define(Word, LinkBase = LinkDef, PartsOfSpeech = "") -> list:

    #Which link to use; If verb use conjugate

    URL = f"{LinkBase}{'%20'.join(Word.split(' ')).lower()}"

    print(URL)

    #bs4 bs
    URLResult = requests.get(URL)
    Soup = BeautifulSoup(URLResult.content, "html.parser")

    #Get correct word from site with accents and tildes
    CorrectedWord = Soup.find("h1", attrs={"class":"cXUN5-ST"})

    if CorrectedWord is not None:
        Word = re.sub("""(<.*">)|(</.*>)""", "", str(CorrectedWord))

    #Get parts of speech
    if PartsOfSpeech == "":
        PartsOfSpeech = Soup.find("a", attrs={"class":"_2VBIE8Jw"})

        if PartsOfSpeech is not None:
            PartsOfSpeech = re.sub("""(<.*">)|(</.*>)""", "", str(PartsOfSpeech))

            #Use conjugation link if verb
            if "verb" in PartsOfSpeech.lower():
                return Define(Word, LinkConj, PartsOfSpeech)

    Conjugations = [[[] for _ in range(5)] for _ in range(6)]
    #If conjugatable, specify conjugations too
    if LinkBase == LinkConj:
        i = 0
        for Conjugation in Soup.find_all("a", attrs={"class":"_3Le9u96E _2cyjHi0d _1zVoo-wU y9F9itDZ"}):

            RidFront = re.sub('''<a.*aria-label="''', "", str(Conjugation))
            RidBack = re.sub('''".*>''', "", RidFront)

            if not re.match("(<|>)", RidBack):
                i += 1
                Conjugations[albreto.floor(i / 30)][i % 5].append(RidBack)
                #change 30 and 5 for others ">

    #Get defination
    Defination = Soup.find("div", attrs={"id":"quickdef1-es"})
    Defination = re.sub('''<div.*">''', "", str(Defination))
    Defination = re.sub('''</.*>''', "", str(Defination))

    if Defination == "None":
        Defination = f">>>Manually check defination on {URL} please.<<<"

    with open(os.path.dirname(os.path.realpath(__file__)) + "/Output.txt", "a", encoding="UTF-8") as File:
        
        CondensedConj = f"({', '.join(Conjugations[0][1])})" if Conjugations[0][1] != [] else " "
        
        File.write(f"{Defination.capitalize()}\t{Word.capitalize()} ({PartsOfSpeech}) {CondensedConj}\n") #flip def and word so spanish is with spanish

for Word in Words:

    Define(Word)

    
