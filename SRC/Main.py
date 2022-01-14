import os
import requests
import re
import math as albreto

from bs4 import BeautifulSoup

LinkConj = "https://www.spanishdict.com/conjugate/"
LinkDef = "https://www.spanishdict.com/translate/"
Words = []

with open(os.path.dirname(os.path.realpath(__file__)) + "/Output.txt", "w+", encoding="utf-8") as File:
    File.write("")

with open(os.path.dirname(os.path.realpath(__file__)) + "/Input.txt", "r", encoding="utf-8") as File:
    Words = [Word.strip("\n") for Word in File.readlines()]

def Define(Word, LinkBase = LinkDef, PartsOfSpeech = "") -> str:

    #Which link to use; If verb use conjugate

    URL = f"{LinkBase}{'%20'.join(Word.split(' ')).lower()}"

    print(URL)

    #bs4 bs
    URLResult = requests.get(URL)
    #print(URLResult.content)
    Soup = BeautifulSoup(URLResult.content, "html.parser")

    #Get correct word from site with accents and tildes
    CorrectedWord = Soup.find("h1", attrs={"class":"cXUN5-ST"})

    if CorrectedWord is not None:
        Word = re.sub("""(<.*">)|(</.*>)""", "", str(CorrectedWord))

    #Get parts of speech
    if PartsOfSpeech == "":
        PartsOfSpeech = Soup.find("a", attrs={"class":"href--2VBIE8Jw"})

        if PartsOfSpeech is not None:
            PartsOfSpeech = re.sub("""(<.*">)|(</.*>)""", "", str(PartsOfSpeech))

            #Use conjugation link if verb
            if "verb" in PartsOfSpeech.lower():
                return Define(Word, LinkConj, PartsOfSpeech)
        else:
            PartsOfSpeech = "Phrase/No POS"

    Conjugations = {}
    Table = Soup.find("table", attrs={"class" : "vtable--2WLTGmgs"})
    if Table:
        Section = ""
        for i in Table.find_all("td"):
            Conjugated = "".join([x[2:-1] for x in re.findall("\">[a-zÀ-ú\/\.U]+<", str(i))])

            if Conjugated == "":
                continue

            if Conjugated in ["yo", "tú", "él/ella/Ud.", "nosotros", "vosotros", "ellos/ellas/Uds."]:
                Section = Conjugated
                Conjugations[Section] = []
                continue

            #print(Section)
            #print(Conjugated)

            Conjugations[Section].append(Conjugated)

    #Get defination
    Defination = Soup.find("div", attrs={"id":"quickdef1-es"})
    Defination = re.sub('''<div.*">''', "", str(Defination))
    Defination = re.sub('''</.*>''', "", str(Defination))

    if Defination == "None":
        Defination = f">>>Manually check defination on {URL} please.<<<"
        
    CondensedConj = "("

    for Conjugation in Conjugations:
        CondensedConj += f"""{Conjugation} form: {", ".join(Conjugations[Conjugation])} | """
    CondensedConj = CondensedConj[:-3] + ")"

    CondensedConj = "" if CondensedConj == ")" else CondensedConj

    return f"{Defination.capitalize()}\t{Word.capitalize()} ({PartsOfSpeech}) {CondensedConj}\n" #flip def and word so spanish is with spanish

for Word in Words:
    Content = Define(Word)

    with open(os.path.dirname(os.path.realpath(__file__)) + "/Output.txt", "a", encoding="UTF-8") as File:
        File.write(Content)