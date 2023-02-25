import pygame
import random
from variables import *
import time

class Piece():

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.forme = random.choice(formes)
        self.couleur = random.randint(1,7)
        self.bloc = pygame.image.load(f'images/bloc{self.couleur}.png')
        self.etat = 0

    #Affiche la piece
    def affichage(self, surface, a, b):

        for i in range(4):
            for j in range(4):
                if i*4 + j in self.image(): 
                    x = (TAILLE * (self.x + j)) + a
                    y = (TAILLE * (self.y + i)) + b
                    surface.blit(self.bloc, (x, y))

    #Passe a l'orientation suivante
    def rotation(self):
        self.etat =  (self.etat + 1) % len(self.forme)
    
    #Retourne la forme actuelle de la piece   
    def image(self):
        return self.forme[self.etat]

class Tetris():
    def __init__(self, x, y) -> None:

        self.rect = pygame.Rect(x, y, 400, 800)
        self.piece = Piece(4, 0)
        self.piece_suivante = Piece(4, 0)

        self.col = 10
        self.ligne = 20
        self.grille = [[0 for i in range(self.col)] for j in range(self.ligne)]

        self.mode = 0
        self.score = 0
        self.niveau = 0
        self.inter = .5
        self.compteur = 120

        self.action = False

    def affichage(self, surface):

        #Affiche piece en cours
        self.piece.affichage(surface, self.rect.x, self.rect.y)
        
        #Affiche la piece suivante
        self.piece_suivante.affichage(surface, 380, 350)

        #Affiche pieces precedentes
        for i in range(self.ligne):
            for j in range(self.col):
                if self.grille[i][j] > 0:
                    a = j*TAILLE + self.rect.x
                    b = i*TAILLE + self.rect.y
                    surface.blit(pygame.image.load(f'images/bloc{self.grille[i][j]}.png'), (a, b))

        #Bordures
        pygame.draw.rect(surface, 'grey40', self.rect, 2)
        
        
        self.test_ligne()

        if self.collision() == 1:
            self.ajout()
            self.nouvelle_piece()

        #Condition de fin de partie
        for i in range(self.col):
            if self.grille[0][i] or (self.compteur <= 0 and self.mode == 1):
                return True

        if self.inter < 0:
            self.piece.y += 1
            self.intervalle()
        else:    
            self.movement()

        return False

    #Cree une nouvelle piece
    def nouvelle_piece(self):

        self.piece = self.piece_suivante
        self.piece_suivante = Piece(4, 0)

    def movement(self):

        touche = pygame.key.get_pressed()

        if touche[pygame.K_DOWN] and not self.collision():
            self.piece.y += 1

        elif not self.action:

            if touche[pygame.K_RIGHT] and self.bordures() != 2:
                self.piece.x += 1
                self.action = True
            elif touche[pygame.K_LEFT]  and self.bordures() != 1:
                self.piece.x -= 1
                self.action = True

        if touche[pygame.K_UP] and not self.action:
            self.piece.rotation()
            self.action = True
            if self.bordures() == 1:
                self.piece.x += 1
            if self.bordures() == 2:
                self.piece.x -= 1
    
    #Retourne True si la piece est en contact avec les bords de droite et gauche
    def bordures(self):

        for i in range(4):
            for j in range(4):
                if i*4 + j in self.piece.image():
                    if self.piece.x + j <= 0 or self.grille[i + self.piece.y][self.piece.x + j-1] > 0:
                        return 1
                    elif self.piece.x + j >= self.col-1 or self.grille[i + self.piece.y][self.piece.x + j+1] > 0:
                        return 2
        return 0

    #Retourne True si la piece entre en contact avec le bas de la grille ou une autre piece
    def collision(self):
        for i in range(4):
            for j in range(4):
                if i*4 + j in self.piece.image():
                    if self.piece.y + i >= self.ligne-1:
                        return True
                    if self.grille[i+1 + self.piece.y][self.piece.x + j] > 0:
                        return True
        return False

    #Place la piece dans la grille
    def ajout(self):

        for i in range(4):
            for j in range(4):
                if i*4 + j in self.piece.image():
                    self.grille[self.piece.y + i][self.piece.x + j] = self.piece.couleur

    #Teste si une ligne est remplie
    def test_ligne(self):

        combo = 0

        for i in range(self.ligne):

            plein = True

            for j in range(self.col):
                if self.grille[i][j] == 0:
                    plein = False

            #Retire la ligne si elle est pleine et insere une nouvelle en haut
            if plein:
                self.grille.pop(i)
                self.grille.insert(0, [0 for i in range(self.col)] )
                combo += 1

        if combo > 0:
            self.score += 10 * (combo * 3)

    #Definis la vitesse du jeu en fonction du niveau
    def intervalle(self):

        if  800 > self.score >= 400:
            self.niveau = 1
        elif 1200 > self.score >= 800:
            self.niveau = 2
        elif 1600 > self.score >= 1200:
            self.niveau = 3
        elif self.score >= 1600:
            self.niveau = 4

        match self.niveau:
            case 0:
                self.inter = .5
            case 1:
                self.inter = .4
            case 2:
                self.inter = .3
            case 3:
                self.inter = .2
            case 4:
                self.inter = .1


class Bouton():
    def __init__(self, message, x, y, police, couleur):
        self.texte = police.render(message, 1, couleur)
        self.rect = self.texte.get_rect()
        self.rect.topleft = (x-self.rect.w/2, y)
        self.rect.w = self.texte.get_width()+20
        self.rect.h = self.texte.get_height()+20

    #Affiche le bouton retourne True lorsque l'on clique a l'interieur
    def affichage(self, surface):
        
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):

            if (pygame.mouse.get_pressed()[0] == 1):
                action = True

        surface.blit(self.texte, ( self.rect.x, self.rect.y))

        return action