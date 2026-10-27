"""Jev chunk accuracy test: 8 items per language (4 real chunks, 4 ordinary phrases).

Reads the API key from the TYPESAFE_API_KEY environment variable; never stores it.
Writes per-item results and a per-language summary next to this script.
"""
import json
import os
import sys
import time
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jev_client import ask

# (language, sentence, phrase, is_chunk)
ITEMS = [
    ("English", "She decided to give up smoking last year.", "give up", True),
    ("English", "He always takes after his father.", "takes after", True),
    ("English", "It's raining cats and dogs outside.", "raining cats and dogs", True),
    ("English", "They finally came up with a solution.", "came up with", True),
    ("English", "She gave the book to her brother.", "gave the book", False),
    ("English", "The red car stopped at the light.", "red car", False),
    ("English", "He walked into the room slowly.", "walked into the room", False),
    ("English", "They ate dinner at home.", "ate dinner", False),

    ("Spanish", "Me di cuenta de que había perdido las llaves.", "me di cuenta de", True),
    ("Spanish", "Tomó el pelo a su hermano toda la tarde.", "tomó el pelo", True),
    ("Spanish", "Estamos a punto de salir.", "a punto de", True),
    ("Spanish", "No te preocupes, echo de menos a mi familia.", "echo de menos", True),
    ("Spanish", "Compré pan en la panadería.", "compré pan", False),
    ("Spanish", "El gato duerme en el sofá.", "duerme en el sofá", False),
    ("Spanish", "Ella lee un libro interesante.", "lee un libro", False),
    ("Spanish", "Mi hermano vive en Madrid.", "vive en Madrid", False),

    ("French", "Il faut que je me rende compte de la situation.", "me rende compte", True),
    ("French", "Elle a pris le taureau par les cornes.", "pris le taureau par les cornes", True),
    ("French", "Je n'ai pas envie de sortir ce soir.", "n'ai pas envie de", True),
    ("French", "Il pleut des cordes depuis ce matin.", "pleut des cordes", True),
    ("French", "Le chat dort sur le canapé.", "dort sur le canapé", False),
    ("French", "J'ai acheté du pain ce matin.", "acheté du pain", False),
    ("French", "Elle lit un livre intéressant.", "lit un livre", False),
    ("French", "Nous habitons dans une petite maison.", "petite maison", False),

    ("German", "Er rief mich gestern Abend an.", "rief ... an", True),
    ("German", "Sie gibt sich viel Mühe mit dem Kuchen.", "gibt sich viel Mühe", True),
    ("German", "Das geht mir auf die Nerven.", "auf die Nerven", True),
    ("German", "Er hat Schwein gehabt.", "Schwein gehabt", True),
    ("German", "Der Hund schläft auf dem Sofa.", "schläft auf dem Sofa", False),
    ("German", "Ich habe Brot gekauft.", "Brot gekauft", False),
    ("German", "Sie liest ein interessantes Buch.", "liest ein interessantes Buch", False),
    ("German", "Wir wohnen in einem kleinen Haus.", "kleinen Haus", False),

    ("Italian", "Non ce la faccio più a lavorare così.", "ce la faccio", True),
    ("Italian", "Ha preso in giro suo fratello tutto il pomeriggio.", "preso in giro", True),
    ("Italian", "Mi è venuto in mente un'idea.", "venuto in mente", True),
    ("Italian", "In bocca al lupo per l'esame!", "In bocca al lupo", True),
    ("Italian", "Il gatto dorme sul divano.", "dorme sul divano", False),
    ("Italian", "Ho comprato il pane stamattina.", "comprato il pane", False),
    ("Italian", "Lei legge un libro interessante.", "legge un libro", False),
    ("Italian", "Abitiamo in una piccola casa.", "piccola casa", False),

    ("Portuguese", "Ele deu a volta por cima depois da crise.", "deu a volta por cima", True),
    ("Portuguese", "Ela tirou o cavalo da chuva.", "tirou o cavalo da chuva", True),
    ("Portuguese", "Não vejo a hora de viajar.", "vejo a hora de", True),
    ("Portuguese", "Fiquei de queixo caído com a notícia.", "queixo caído", True),
    ("Portuguese", "O gato dorme no sofá.", "dorme no sofá", False),
    ("Portuguese", "Comprei pão na padaria.", "comprei pão", False),
    ("Portuguese", "Ela lê um livro interessante.", "lê um livro", False),
    ("Portuguese", "Moramos numa casa pequena.", "casa pequena", False),
]


def question(language, phrase):
    return {
        "chunk": {
            "type": "noul",
            "instructions": (
                f"The sentence is in {language}. Is the phrase \"{phrase}\" in this sentence "
                "a fixed expression, idiom, phrasal verb, or collocation whose meaning a language "
                "learner would not get by translating the words one by one?"
            ),
        }
    }


def main():
    rows = []
    for language, sentence, phrase, truth in ITEMS:
        status, body, dt = ask(sentence, question(language, phrase))
        if status != 200:
            print(f"stopped: HTTP {status}: {str(body)[:300]}")
            break
        p = body["chunk"]["noul"] if isinstance(body, dict) and "chunk" in body else None
        rows.append({"language": language, "sentence": sentence, "phrase": phrase,
                     "truth": truth, "p": p, "seconds": round(dt, 2)})
        time.sleep(0.2)

    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "results.json"), "w") as f:
        json.dump(rows, f, ensure_ascii=False, indent=1)

    by_lang = defaultdict(list)
    for r in rows:
        if r["p"] is not None:
            by_lang[r["language"]].append(r)
    total_ok = total = 0
    for lang, rs in by_lang.items():
        ok = sum((r["p"] >= 0.5) == r["truth"] for r in rs)
        pos = [r["p"] for r in rs if r["truth"]]
        neg = [r["p"] for r in rs if not r["truth"]]
        print(f"{lang}: {ok}/{len(rs)} correct; mean p(chunk) real={sum(pos)/len(pos):.2f} "
              f"ordinary={sum(neg)/len(neg):.2f}")
        total_ok += ok
        total += len(rs)
    if total:
        print(f"overall: {total_ok}/{total}")


if __name__ == "__main__":
    main()
