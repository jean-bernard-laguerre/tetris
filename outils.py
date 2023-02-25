import pygame
import json

#Joue un son sur le canal 1
def jouer_son(titre):
    son = pygame.mixer.Sound(titre)
    pygame.mixer.Channel(1).play(son)


#Ajoute le score dans scores.json
def enregistrer(score,type):

    f = open("scores.json", "r+")
    scores = json.load(f)

    if f"{type}" not in scores:
        scores[f"{type}"] = []

    if score > 0:
        scores[f"{type}"].append(score)
    
    scores[f"{type}"] = sorted(scores[f"{type}"], reverse=True)

    f.seek(0)
    json.dump(scores, f, indent=4)

    f.close()

#Recupere les dix meilleurs scores
def recuperer():

    f = open("scores.json", "r+")
    scores = json.load(f)

    f.close()
    return scores