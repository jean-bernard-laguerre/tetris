import pygame
from classes import *
from outils import *

pygame.init()

fenetre = pygame.display.set_mode((800,900))
tdr = pygame.time.Clock()

jeu = Tetris(50, 50)
police = pygame.font.Font('polices/Orbitron-Regular.ttf', 32)
bg_image = pygame.image.load('images/bg_tetris.jpg')
bg_image_rect = bg_image.get_rect()
tps = 0
statut_partie = 0


def ecran_menu():
    
    if Bouton("Survie", 200, 600, police, "white").affichage(fenetre):
        nouvelle_partie()
        navigation(1)

    if Bouton("Course", 600, 600, police, "white").affichage(fenetre):
        nouvelle_partie()
        jeu.mode = 1
        navigation(1)

    if Bouton("Scores", 400, 750, police, "white").affichage(fenetre):
        navigation(3)


def ecran_jeu():

    score = police.render(f"Score: {jeu.score}", 1 ,'white')
    lbl_temps = police.render(f"{jeu.compteur//1}", 1 ,'white')
    lbl_suivant = police.render("Suivant:", 1, 'white')

    fenetre.blit(lbl_suivant, (550, 275))
    fenetre.blit(score, (550, 100))

    if jeu.mode == 1:
        fenetre.blit(lbl_temps, (600, 800))

    if jeu.affichage(fenetre):
        enregistrer(jeu.score, jeu.mode)
        navigation(2)
                

def ecran_fin():

    lbl_fin = police.render("Game Over", 1, 'white')
    score = police.render(f"Score: {jeu.score}", 1, 'white')

    if Bouton("Menu", 200, 750, police, "white").affichage(fenetre):
        navigation(0)

    if Bouton("Scores", 600, 750, police, "white").affichage(fenetre):
        navigation(3)

    fenetre.blit(lbl_fin,(300,500))
    fenetre.blit(score,(300,600))


def ecran_score():
    global statut_partie

    lbl_score = police.render("Meilleurs scores", 1, 'white')
    lbl_survie = police.render("Survie", 1, 'white')
    lbl_course = police.render("Course", 1, 'white')

    fenetre.blit(lbl_score, (250, 50))
    fenetre.blit(lbl_survie, (200, 125))
    fenetre.blit(lbl_course, (450, 125))

    scores = recuperer()

    for i,categories in enumerate(scores):
        for j,score in enumerate(scores[categories][:10]):
            texte = police.render(f"{score}", 1, 'white')
            fenetre.blit(texte, (215 + (i*250), (200+(j*40))))

    if Bouton("Menu", 600, 750, police, 'white').affichage(fenetre):

        navigation(0)


def navigation(page):
    global statut_partie
    statut_partie = page

def nouvelle_partie():
    global jeu
    jeu = Tetris(50, 50)


en_cours = True
while en_cours:

    tps = tdr.tick(30) / 2000

    fenetre.blit(bg_image, bg_image_rect)

    match statut_partie:
        case 0:
            ecran_menu()
        case 1:
            ecran_jeu()
            jeu.inter -= tps
            jeu.compteur -= tps
        case 2:
            ecran_fin()
        case 3:
            ecran_score()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False

        if event.type != pygame.KEYDOWN:
            jeu.action = False

    pygame.display.update()

pygame.quit()