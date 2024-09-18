import pygame
import sys
import serial
import time

ser = serial.Serial('COM10', 9600, timeout=1)
time.sleep(2)

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1)

winner_sound = pygame.mixer.Sound("winner.mp3")

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()

background = pygame.image.load("pista.png")
background = pygame.transform.scale(background, (screen_width, screen_height))

publico = pygame.image.load("publico.png")
publico_height = screen_height // 11
publico = pygame.transform.scale(publico, (screen_width, publico_height))
publico_position = (0, screen_height - publico_height)

linea_meta_width = 10
linea_meta_x = screen_width - 300 - linea_meta_width
linea_meta_surface = pygame.Surface((linea_meta_width, screen_height - publico_height), pygame.SRCALPHA)
linea_meta_surface.fill((255, 255, 255, 128))

font = pygame.font.SysFont(None, 150, bold=True)
text_surface = font.render("F I N I S H", True, (255, 255, 255, 128))
text_surface = pygame.transform.rotate(text_surface, 90)

text_x = screen_width - text_surface.get_width() - 100
text_y = (screen_height - publico_height - text_surface.get_height()) // 2

patrocinador1 = pygame.image.load("patrocinador1.png")
patrocinador2 = pygame.image.load("patrocinador2.png")
patrocinador_width = 250
patrocinador_height = 100
patrocinador1 = pygame.transform.scale(patrocinador1, (patrocinador_width, patrocinador_height))
patrocinador2 = pygame.transform.scale(patrocinador2, (patrocinador_width, patrocinador_height))

patrocinador1_x = screen_width - patrocinador_width - 50
patrocinador1_y = text_y - patrocinador_height - 50

patrocinador2_x = screen_width - patrocinador_width - 50
patrocinador2_y = text_y + text_surface.get_height() + 50

espacio_superior = screen_height // 18
fuente_tamano = (3 * screen_height) // 18
altura_bici_ganadora = (3 * screen_height) // 18
espacio_entre_bicis = screen_height // 18
altura_bicis_restantes_total = (10 * screen_height) // 18
altura_bici_restante = altura_bicis_restantes_total // 9

font_ganador = pygame.font.SysFont(None, fuente_tamano, bold=True)
ganador_text = font_ganador.render("GANADOR", True, (255, 255, 255))
ganador_text_rect = ganador_text.get_rect(center=(screen_width // 2, espacio_superior))


bici_images = []
bici_positions = []
bici_height_full = screen_height // 11
margin = 5
bici_height = bici_height_full - 2 * margin
bici_width = 200

def inicializar_bicis():
    global bici_positions
    bici_positions = []
    for i in range(1, 11):
        bici_image = pygame.image.load(f"bici{i}.png")
        bici_image = pygame.transform.scale(bici_image, (bici_width, bici_height))
        bici_position_x = 0
        bici_position_y = (i - 1) * bici_height_full + margin
        bici_images.append(bici_image)
        bici_positions.append([bici_position_x, bici_position_y])

inicializar_bicis()

def mover_bici(bici_num, delta_x):
    if 1 <= bici_num <= 10:
        bici_x, bici_y = bici_positions[bici_num - 1]
        bici_positions[bici_num - 1][0] = bici_x + delta_x

def verificar_ganador():
    for i in range(10):
        bici_x, bici_y = bici_positions[i]
        if bici_x + bici_width >= linea_meta_x:
            return i + 1
    return None

def mostrar_ganador(bici_num):
    ganador_surface = pygame.Surface((screen_width, screen_height))
    ganador_surface.fill((128, 128, 128))

    screen.blit(ganador_surface, (0, 0))
    screen.blit(ganador_text, ganador_text_rect.topleft)

    bici_ganadora = bici_images[bici_num - 1]
    bici_ganadora_aspect_ratio = bici_ganadora.get_width() / bici_ganadora.get_height()
    bici_ganadora_width = int(altura_bici_ganadora * bici_ganadora_aspect_ratio)
    bici_ganadora = pygame.transform.scale(bici_ganadora, (bici_ganadora_width, altura_bici_ganadora))
    bici_rect = bici_ganadora.get_rect(center=(screen_width // 2, ganador_text_rect.bottom + espacio_superior + altura_bici_ganadora // 2))

    screen.blit(bici_ganadora, bici_rect.topleft)

    espacio_y = bici_rect.bottom + espacio_entre_bicis

    posiciones_restantes = sorted(enumerate(bici_positions), key=lambda p: p[1][0], reverse=True)
    font_posicion = pygame.font.SysFont(None, 50, bold=True)
    rank = 2

    for index, pos in posiciones_restantes:
        if index + 1 == bici_num:
            continue

        bici_resized = bici_images[index]
        aspect_ratio = bici_resized.get_width() / bici_resized.get_height()
        resized_width = int(altura_bici_restante * aspect_ratio)
        bici_resized = pygame.transform.scale(bici_resized, (resized_width, altura_bici_restante))

        pos_x = 50
        pos_y = espacio_y + ((rank - 2) * altura_bici_restante)

        screen.blit(bici_resized, (pos_x, pos_y))

        texto_posicion = f"{rank}da"
        posicion_text = font_posicion.render(texto_posicion, True, (255, 255, 255))
        screen.blit(posicion_text, (pos_x + resized_width + 20, pos_y + 10))

        rank += 1

    pygame.display.flip()

running = True
ganador = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and ganador is not None:
            ganador = None
            inicializar_bicis()
            winner_sound.stop()
            pygame.mixer.music.load("background.mp3")
            pygame.mixer.music.play(-1)

    if ganador is not None:
        mostrar_ganador(ganador)
        continue

    if ser.in_waiting > 0:
        data = ser.read().decode('utf-8')
        if data == 'i':
            mover_bici(4, 10)
        if data == '1':
            mover_bici(1, 10)

    ganador = verificar_ganador()

    if ganador is not None:
        pygame.mixer.music.stop()
        winner_sound.play()

    screen.blit(background, (0, 0))
    screen.blit(linea_meta_surface, (linea_meta_x, 0))
    screen.blit(text_surface, (text_x, text_y))
    screen.blit(publico, publico_position)
    screen.blit(patrocinador1, (patrocinador1_x, patrocinador1_y))
    screen.blit(patrocinador2, (patrocinador2_x, patrocinador2_y))

    for i in range(10):
        screen.blit(bici_images[i], bici_positions[i])

    pygame.display.flip()

pygame.quit()
ser.close()
sys.exit()
