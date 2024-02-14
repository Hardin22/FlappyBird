import time

import pygame
from sys import exit
from random import randint

class Ostacolo:
    def __init__(self, rett):
        self.rett = rett
        self.superato = False


def movimento_ostacoli(lista_ostacoli_su, lista_ostacoli_giu):
    for ostacolo in lista_ostacoli_su:
        ostacolo.rett.x -= 3
        screen.blit(tubo_su, ostacolo.rett)

    for ostacolo in lista_ostacoli_giu:
        ostacolo.rett.x -= 3
        screen.blit(tubo_giu, ostacolo.rett)

    lista_ostacoli_su = [ostacolo for ostacolo in lista_ostacoli_su if ostacolo.rett.x > -100]
    lista_ostacoli_giu = [ostacolo for ostacolo in lista_ostacoli_giu if ostacolo.rett.x > -100]

    return lista_ostacoli_su, lista_ostacoli_giu


def mostra_punteggio(punteggio):
    punteggio = int (punteggio/2)
    cifre_punteggio = list(str(punteggio))
    larghezza_totale = 0  # Larghezza totale delle immagini del punteggio
    immagini_punteggio = []  # Lista per immagazzinare le immagini del punteggio

    for cifra in cifre_punteggio:
        immagine = numeri[int(cifra)]
        larghezza_totale += immagine.get_width()
        immagini_punteggio.append(immagine)

    # Calcola la posizione di partenza X per il punteggio
    Xstart = (screen.get_width() - larghezza_totale) / 2

    for immagine in immagini_punteggio:
        screen.blit(immagine, (Xstart, screen.get_height() / 5))
        Xstart += immagine.get_width()

def collisioni(giocatore, ostacoli):
    if ostacoli:
        for ostacolo in ostacoli:
            if giocatore.colliderect(ostacolo.rett): return False
    return True

lista_ostacoli_su = []
lista_ostacoli_giu = []
try:
    with open('punteggio_record.txt', 'r') as file:
        punteggio_record = int(file.read())
except FileNotFoundError:
    punteggio_record = 0

pygame.init()

timer_ostacolo = pygame.USEREVENT + 1
pygame.time.set_timer(timer_ostacolo, randint(700, 1300))


screen = pygame.display.set_mode((288, 512))
pygame.display.set_caption('flappy birds')
numeri = [pygame.image.load(f'/Users/Francesco/PycharmProjects/flappybird/flappyart/numeri/{i}.png').convert_alpha() for i in range(10)]
clock = pygame.time.Clock()
gioco_attivo = False
gravità = 0
velocità = 3
punteggio = 0


sfondo = pygame.image.load('/Users/Francesco/PycharmProjects/flappybird/flappyart/background-day.png').convert_alpha()
tubo_su = pygame.image.load('/Users/Francesco/PycharmProjects/flappybird/flappyart/pipe-green.png').convert_alpha()
tubo_giu = pygame.transform.rotate(tubo_su, 180.00)
x = 144
base = pygame.image.load('/Users/Francesco/PycharmProjects/flappybird/flappyart/base.png').convert_alpha()
base_rett = base.get_rect(midtop= (x, 400))

#animazione uccello
birdup = pygame.image.load('/Users/Francesco/PycharmProjects/flappybird/flappyart/yellowbird-upflap.png').convert_alpha()
birdmid = pygame.image.load('/Users/Francesco/PycharmProjects/flappybird/flappyart/yellowbird-midflap.png').convert_alpha()
birddown = pygame.image.load('/Users/Francesco/PycharmProjects/flappybird/flappyart/yellowbird-downflap.png').convert_alpha()

lista_uccello = [birdup, birdmid, birddown]
uccello = lista_uccello[0]
birdup_rett = birdup.get_rect(center=(70, 256))

contatore_frame = 0
contatore_flap = 0

gameover = pygame.image.load('/Users/Francesco/PycharmProjects/flappybird/flappyart/gameover.png').convert_alpha()
messaggio = pygame.image.load('/Users/Francesco/PycharmProjects/flappybird/flappyart/message.png').convert_alpha()

angolo = 0
variazionesu = 3
variazionegiu = 4

prova = 0
i = 0.00

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if gioco_attivo:
            if birdup_rett.bottom < base_rett.top +1:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                            gravità= -8

            if event.type == timer_ostacolo and gioco_attivo:
                x_casuale = randint(295, 340)
                ostacolo_giu = Ostacolo(tubo_giu.get_rect(midbottom=(x_casuale, randint(100, 250))))
                lista_ostacoli_giu.append(ostacolo_giu)

                ostacolo_su = Ostacolo(tubo_su.get_rect(midtop=(x_casuale, ostacolo_giu.rett.bottom + 120)))
                lista_ostacoli_su.append(ostacolo_su)

        else :
             if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                gioco_attivo = True
                punteggio = 0

    contatore_frame += 1

    if gioco_attivo:

        if gravità > 0:
            uccello = birdmid

            if prova > 10:

                uccello = pygame.transform.rotate(uccello, -30.00)

            else :
                prova += 1

        else:
            prova = 0
            if contatore_frame % 5 == 0:

                uccello = lista_uccello[contatore_flap % 3]

                uccello = pygame.transform.rotate(uccello,30.00)
                contatore_flap +=1


        base_rett.x -= velocità
        if base_rett.right <= 0:
            base_rett.left = 0
        screen.blit(sfondo, (0, 0))
        lista_ostacoli_su, lista_ostacoli_giu = movimento_ostacoli(lista_ostacoli_su, lista_ostacoli_giu)
        screen.blit(base, (base_rett))
        screen.blit(base, (base_rett.right, 400))
        screen.blit(uccello, birdup_rett)

        mostra_punteggio(punteggio)

        gravità += 0.6
        birdup_rett.y += gravità
        if birdup_rett.bottom >= base_rett.top:
            birdup_rett.bottom = base_rett.top
        gioco_attivo = collisioni(birdup_rett, lista_ostacoli_su + lista_ostacoli_giu)

        # ... Il resto del tuo codice ...

        # Itera su ogni ostacolo nella lista
        for ostacolo in lista_ostacoli_su + lista_ostacoli_giu:
            if birdup_rett.left > ostacolo.rett.right and not ostacolo.superato:
                ostacolo.superato = True
                punteggio += 1



    else:
        contatore_flap = 0
        lista_ostacoli_giu.clear()
        lista_ostacoli_su.clear()
        birdup_rett.center = (70, 256)
        gravità = 0
        contatore_frame = 0

        if punteggio > punteggio_record:
            punteggio_record = punteggio
            with open('punteggio_record.txt', 'w') as file:
                file.write(str(punteggio_record))

        if punteggio == 0:
            screen.fill((110, 190, 200))
            screen.blit(messaggio, (50, 120))
        else:
            screen.blit(gameover, (55, 190))

    pygame.display.update()
    clock.tick(60)
