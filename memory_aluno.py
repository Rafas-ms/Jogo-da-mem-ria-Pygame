import pygame, sys
import random

from pygame import mixer
from pygame.locals import *

'''
ATENCAO: procure pelas marcações 'TODO', pois elas indicam 
onde deverá ser codificado. Leia os comentarios ao longo do 
código. Leia a documentação do pygame para os métodos que você
tiver dúvida.
'''

# Constantes
FPS = 60
W_SIZE = [800, 100]
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (34, 139, 34)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CLOCK = pygame.time.Clock()

NUMBER_CARDS = 16
CARD_SIZE = [W_SIZE[0] / NUMBER_CARDS, W_SIZE[1]]

# setup inicial da biblioteca e da janela - DISPLAYSURF é onde desenham-se os elementos
pygame.init()
# DISPLAYSURF = pygame.display.set_mode((W_SIZE[0], W_SIZE[1]))
DISPLAYSURF = pygame.display.set_mode((800, 500))
pygame.display.set_caption('Memory')
pygame.time.set_timer(pygame.USEREVENT, 1000)  # veja na doc. do pygame

# Sons
mixer.music.load('sons-musicas/retro-90s-arcade-machine.mp3')
mixer.music.play(-1)

acerto = mixer.Sound("sons-musicas/arcade-game-complete-or-approved-mission-205.wav")
vitoria = mixer.Sound("sons-musicas/win.mp3")

# Background
bg = pygame.image.load("background/Fundo.png")
bg2 = pygame.image.load("background/fundoMenu.png")


# Helpers
def init():
    """ Inicializa variaveis globais """
    global deck_cards, exposed, cards_clicked, cards_paired
    global state, number_turns, t_count, font_surf, font_messg, surf_messg

    define_message("")
    t_count = 0  # conta os segundos
    state = 0  # estado do jogo: relativo as cartas viradas pelo usuario (uma ou duas)
    number_turns = 0  # numero de turnos (duas cartas viradas = 1 turno)
    cards_clicked = []  # salva o par de cartas clicadas, pelos seus indices
    cards_paired = 0  # quantidade de pares de cartas descobertas
    # cartas do jogo
    # deck_cards = [(str(i) if i < NUMBER_CARDS/2 else str(NUMBER_CARDS%i)) for i in range(NUMBER_CARDS)]
    deck_cards = ["background/img1.png", "background/img1.png", "background/img3.png", "background/img3.png",
                  "background/img4.png", "background/img4.png", "background/img6.png", "background/img6.png",
                  "background/img7.png", "background/img7.png", "background/img8.png", "background/img8.png",
                  "background/img9.png", "background/img9.png", "background/img10.png", "background/img10.png"]
    random.shuffle(deck_cards)
    exposed = [False] * NUMBER_CARDS  # guarda os indices relativos ao deck de cartas

    # texto para as cartas: repare que ele é relativo ao deck de cartas
    font_obj = pygame.font.Font('freesansbold.ttf', 50)
    font_surf = []

    for c in deck_cards:
        surf = pygame.font.Font.render(font_obj, c, True, WHITE)
        rect = surf.get_rect()
        font_surf.append([surf, rect])

    # texto para a mensagem no fim do jogo
    font_messg = pygame.font.Font('freesansbold.ttf', 20)
    surf_messg = pygame.font.Font.render(font_messg, msg_intro, True, YELLOW)


def define_message(msg):
    """ Mostra menssagens """
    global msg_intro
    msg_intro = msg


# Event handlers
def timer_handler():
    """ Contador do tempo (seg.):
    O comando pygame.time.set_timer(pygame.USEREVENT, 1000) customiza
    um evento (USEREVENT) que sera disparado a cada segundo. Esse evento
    sera capturado (no loop principal) e esta funcao sera chamada.
    """
    global t_count
    t_count += 1


def draw():
    """ Desenha """
    global font_surf

    i = 0
    j = CARD_SIZE[0] / 2 - 25
    for x in range(NUMBER_CARDS):
        ''' 
        TODO: Se uma carta estiver exposta, entao o vetor 'font_surf' 
        deve ser usado para centralizar a sua posicao. Caso contrario,
        um poligono deve ser desenhado. A variável 'j' irá auxiliar para
        definir posicao central do texto da carta, enquanto a variavel 'i' 
        irá te auxiliar a definir a posicao do poligono. Pense em como
        você também pode usar a variavel 'CARD_SIZE' para definir os pontos
        do polígono.
        '''
        if exposed[x]:
            font_surf[x][1] = (j, 0, 28, 50)
            # aqui vc deve completar com codigo
        else:
            pygame.draw.rect(DISPLAYSURF, RED, pygame.Rect(i, 0, CARD_SIZE[0], CARD_SIZE[1]), 1)  # Draw on it.
            # aqui vc deve completar com codigo

        i += CARD_SIZE[0]
        j += CARD_SIZE[0]
    pass


def mouse_click(pos):
    """
    Recupera o indice da carta clicada e
    atualiza o numero de turnos
    """
    global state, number_turns, cards_clicked, cards_paired
    global msg_intro, exposed, surf_messg

    # indice da carta
    # TODO: recuperar o indice da carta clicada pelo local do clique
    position = 50
    index = 0
    cont = 0
    while cont == 0:
        for x in range(position):
            if pos[0] == x:
                cont = 1
        if cont == 1:
            break
        index += 1
        position += 50

    if not exposed[index]:
        if state == 0:
            state = 1
        elif state == 1:
            state = 2
            number_turns += 1  # fim de um turno
            # TODO: determinar o fim do jogo
            if cards_paired == 7:  # aqui vc deve completar com codigo
                define_message("Otimo! Voce terminou em " + str(t_count // 60) + "min" + str(
                    t_count % 60) + "segs" + " e fez " + str(number_turns) + " jogadas")
                surf_messg = pygame.font.Font.render(font_messg, msg_intro, True, BLACK)
                vitoria.play()
        else:
            state = 1
            '''
            TODO: aqui deve existir um teste condicional para esconder a dupla de cartas
            que o usuario tentou advinhar, mas não eram iguais. Essas cartas devem ser
            escondidas novamente.
            '''
            if deck_cards[cards_clicked[0]] != deck_cards[cards_clicked[1]]:  # aqui vc deve completar com codigo
                exposed[cards_clicked[0]] = False
                exposed[cards_clicked[1]] = False
                # aqui vc deve completar com codigo
            else:
                cards_paired += 1

            cards_clicked = []

        cards_clicked.append(index)

        exposed[index] = True
    # Tocar um som quando acerta uma combinação de cartas
    if cards_clicked.__len__() == 2 and deck_cards[cards_clicked[0]] == deck_cards[cards_clicked[1]]:
        acerto.play()


class Button():
    def __init__(self, pos, text_input, font, pos_text):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.x_pos_text = pos_text[0]
        self.y_pos_text = pos_text[1]
        self.font = font
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, WHITE)
        self.text_rect = self.text.get_rect(center=(self.x_pos_text, self.y_pos_text))
    def create(self, screen):
        screen.blit(self.text, self.text_rect)

    def clique(self, position):
        if position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in range(self.text_rect.top,
                                                                                              self.text_rect.bottom):
            return True
        return False


def main():
    global font_surf, surf_messg
    DISPLAYSURF = pygame.display.set_mode((W_SIZE[0], W_SIZE[1]))
    init()
    while True:
        # INSIDE OF THE GAME LOOP
        # Background
        DISPLAYSURF.blit(bg, (0, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                mouse_click(pos)
            if event.type == pygame.USEREVENT:
                timer_handler()

        # desenha
        draw()

        for x in range(NUMBER_CARDS):
            if exposed[x]:
                # DISPLAYSURF.blit(font_surf[x][0], font_surf[x][1])
                cd = pygame.image.load(deck_cards[x])
                DISPLAYSURF.blit(cd, font_surf[x][1])

        DISPLAYSURF.blit(surf_messg, [5, W_SIZE[1] - 20])

        pygame.display.update()
        CLOCK.tick(FPS)


def main_menu():
    #Fonte
    title_font = pygame.font.SysFont("comicsans", 70)
    button_font = pygame.font.SysFont("comicsans", 20)
    # Botão
    play = Button(pos=(325, 150), text_input = "Jogar", font = button_font, pos_text=(400, 175))
    read = Button(pos=(325, 250), text_input="Sobre o jogo", font=button_font, pos_text=(400, 275))
    quit = Button(pos=(325, 350), text_input="Sair", font=button_font, pos_text=(400, 375))

    #Loop
    run = True
    while run:
        pos = pygame.mouse.get_pos()
        DISPLAYSURF.blit(bg2, (0, 0))
        for button in [play, read, quit]:
            button.create(DISPLAYSURF)
        # Titulo
        menu_text = title_font.render("Jogo da Memória", True, WHITE)
        menu_rect = menu_text.get_rect(center=(400, 50))
        DISPLAYSURF.blit(menu_text, menu_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play.clique(pos):
                    main()
                if read.clique(pos):
                    sobre()
                if quit.clique(pos):
                    pygame.quit()
                    sys.exit()



def sobre():
    title_font = pygame.font.SysFont("comicsans", 70)
    button_font = pygame.font.SysFont("comicsans", 20)
    while True:
        pos = pygame.mouse.get_pos()
        DISPLAYSURF.blit(bg2, (0, 0))

        sobre_text = title_font.render("Sobre o jogo", True, WHITE)
        sobre_rect = sobre_text.get_rect(center=(400, 50))
        DISPLAYSURF.blit(sobre_text, sobre_rect)

        sobre_text = button_font.render("Jogo da memória criado pelo aluno Rafael Martins Silva", True, WHITE)
        sobre_rect = sobre_text.get_rect(center=(400, 225))
        DISPLAYSURF.blit(sobre_text, sobre_rect)

        back = Button(pos=(325, 150), text_input="Voltar", font=button_font, pos_text=(400, 375))
        back.create(DISPLAYSURF)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.clique(pos):
                    main_menu()

        pygame.display.update()



main_menu()
