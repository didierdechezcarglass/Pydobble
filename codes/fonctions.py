"""
Ecrit par Quentin Bartolone, élève de Terminale au lycée
Henri Moissan
"""
from random import randint, sample
import pygame


def menuprincipal(ecran):
    """
    Permet de retourner au menu principal
    """
    bouton_jouer = pygame.image.load("images\\boutons\\button_jouer.png")
    bouton_retour = pygame.image.load("images\\boutons\\button_regles.png")
    bouton_quitter = pygame.image.load("images\\boutons\\button_quitter.png")
    men = pygame.image.load("images\\menu\\menu.jpg")
    ecran.blit(pygame.transform.scale(men, (800, 600)), (0, 0))
    jouer = ecran.blit(pygame.transform.scale(bouton_jouer, (200, 50)), (300, 250))
    retour = ecran.blit(pygame.transform.scale(bouton_retour, (200, 50)), (300, 305))
    quitter = ecran.blit(pygame.transform.scale(bouton_quitter, (200, 50)), (300, 360))
    return jouer, retour, quitter


simb = [(350, 150), (410, 130), (465, 180), (460, 230),
        (340, 265), (410, 200), (405, 275), (320, 205),
        # coord carte 1
        (350, 385), (410, 365), (465, 415), (460, 465),
        (340, 500), (410, 435), (405, 510), (320, 430)
        # coord carte 2
        ]


def gameloop(cartes, carte, dico_cartes, ecran):
    """
    Permet de configurer le menu de jeu
    """
    taille_img = []
    indicateur_rota = []
    ecran.blit(pygame.transform.scale(carte, (275, 275)), (280, 95))
    ecran.blit(pygame.transform.scale(carte, (275, 275)), (280, 330))
    cartemillieu = cartes[randint(0, len(cartes) - 1)]
    cartes.pop(cartes.index(cartemillieu))
    cartej = cartes[randint(0, len(cartes) - 1)]
    cartes.pop(cartes.index(cartej))
    for i in enumerate(cartemillieu):
        for j in enumerate(cartej):
            if cartej[j[0]] == cartemillieu[i[0]]:
                correspondantem = cartemillieu[i[0]]
                correspondantep = cartej[j[0]]
                taille_img, indicateur_rota, index_joueur, index_millieu = blitcarte(
                    (cartemillieu, cartej, correspondantem,
                        dico_cartes, ecran, taille_img, indicateur_rota))
                return (correspondantem, correspondantep, cartemillieu,
                        cartej, taille_img, indicateur_rota, index_joueur, index_millieu)
    return "Erreur. Le programme s\'arrête"


def generateurdiag(grille, symb_2, manquante_cop, manquantet_cop):
    """
    générateur des symboles verticaux, permet de séparer la fonction en 2
    """
    # indicateur de la valeur à laquelle il faut additionner d1i
    symb = symb_2.copy()
    manquante_copy = manquante_cop.copy()
    for i in range(1, 7):
        for j in range(7):
            random = randint(0, len(symb) - 1)
            d1i = j
            for d1k in range(7):
                if d1i > 6:
                    d1i -= 7
                grille[d1k][d1i].append(symb[random])
                d1i += i
            manquantet_cop.append(symb[random])
            symb.pop(random)
        manquante_copy.append(manquantet_cop)
        manquantet_cop = []
    return grille, symb, manquante_copy, manquantet_cop


def generateur(symboles):
    """
    Génération des cartes de Dobble qui utilise le principe de la géométrie finie.
    Dans le cas de Dobble, c\'est une liste de taille 7*7 (en anglais: array).
    Ne fonctionne que si n dans n*n est un nombre premier.
    """
    symboles_2 = symboles.copy()
    grille = []  # grille 7*7 dédiée à la création des cartes
    manquante = []  # carte manquantes
    # symboles horizontaux
    manquantet = []  # liste des cartes manquantes
    for i in range(7):
        random = randint(0, len(symboles_2) - 1)
        grille.append([[symboles_2[random]] for j in range(7)])
        manquantet.append(symboles_2[random])
        symboles_2.pop(random)
    manquante.append(manquantet)
    manquantet = []
    # symboles verticaux
    for i in range(7):
        random = randint(0, len(symboles_2) - 1)
        for j in range(7):
            grille[j][i].append(symboles_2[random])
        manquantet.append(symboles_2[random])
        symboles_2.pop(random)
    manquante.append(manquantet)
    manquantet = []
    # symboles diagonaux
    grille, symboles_2, manquante, manquantet = generateurdiag(
        grille, symboles_2, manquante, manquantet)
    for i in enumerate(manquante):
        manquante[i[0]].append(symboles_2[0])
    symboles_2.pop(0)
    # liste cartes
    tableau = grille
    carteliste = []
    for i in tableau:
        for carte in i:
            carteliste.append(sample(carte, len(carte)))
    for cartem in manquante:
        carteliste.append(sample(cartem, len(cartem)))
    return carteliste


def blitcarte(stockage):
    """
    Permet d\'afficher les cartes
    """
    if not stockage[6]:
        for i in range(len(stockage[0])):
            stockage[6].append(randint(0, 359))
    if not stockage[5]:
        for i in range(len(stockage[0])):
            stockage[5].append(randint(40, 50))
    for i in range(len(stockage[0])):
        if stockage[0][i] != stockage[2]:
            stockage[4].blit(pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
                "images\\cartes\\symboles\\" + stockage[3][stockage[0][i]]),
                (stockage[5][i], stockage[5][i])), stockage[6][i]), simb[i])
        else:
            indicateur_correspondance_millieu = stockage[5][i], stockage[5][i]
    stockage[5].pop()
    stockage[6].pop()
    for i in range(8, len(stockage[1]) + 8):
        if stockage[1][i - 8] != stockage[2]:
            stockage[6].append(randint(0, 359))
            stockage[5].append(randint(40, 50))
            stockage[4].blit(pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
                "images\\cartes\\symboles\\" + stockage[3][stockage[1][i - 8]]),
                (stockage[5][i - 8], stockage[5][i - 8])), stockage[6][i - 8]), simb[i])
        else:
            stockage[6].append(randint(0, 359))
            stockage[5].append(randint(40, 50))
            indicateur_correspondance_joueur = i - 8
    taille = stockage[5].copy()
    rotation = stockage[6].copy()
    return taille, rotation, indicateur_correspondance_joueur, indicateur_correspondance_millieu


def changecarte(stock):
    """
    Remplace la carte du milieu par l\'ancienne et
    met une nouvelle carte prise dans la pile
    """
    stock[4].blit(pygame.transform.scale(stock[2], (275, 275)), (280, 95))
    stock[4].blit(pygame.transform.scale(stock[2], (275, 275)), (280, 330))
    cartemillieu = stock[0]
    cartej = stock[1][randint(0, len(stock[1]) - 1)]
    stock[1].pop(stock[1].index(cartej))
    for i in enumerate(cartemillieu):
        for j in enumerate(cartej):
            if j[1] == i[1]:
                correspondantem = i[1]
                correspondantep = j[1]
                taille_image, indicateur_rotation, index_joueur, index_millieu = blitcarte(
                    (cartemillieu, cartej, correspondantem, stock[3], stock[4], stock[5], stock[6]))
                return (correspondantem, correspondantep, cartemillieu,
                        cartej, taille_image, indicateur_rotation, index_joueur, index_millieu)
    return "Erreur. Le programme s\'arrête"


def update(items):
    """
    Mise à jour de l\'écran.
    """
    corr = changecarte((items[0][3], items[2], items[3], items[1], items[4], items[5], items[6]))
    corrm = corr[0]
    corrp = corr[1]
    listetaille = corr[4]
    listerotation = corr[5]
    index_j = corr[6]
    index_m = corr[7]
    ccorrm = simb[corr[2].index(corrm)]
    ccorrp = simb[corr[3].index(corrp) - 8]
    corrmi = items[4].blit(pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
        "images\\cartes\\symboles\\" + items[1][corrm]), (
        index_m[0], index_m[0])), index_m[1]), ccorrm)
    corrpi = items[4].blit(pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
        "images\\cartes\\symboles\\" + items[1][corrp]), (
            listetaille[index_j], listetaille[index_j])),
        listerotation[index_j]), ccorrp)
    return corr, corrmi, corrpi, listetaille, listerotation
