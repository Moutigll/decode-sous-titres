import pygame
import json
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

with open('f.json', 'r') as f:
    subtitles_data = json.load(f)

pen_colors = {}
for pen_id, pen in enumerate(subtitles_data["pens"]):
    if 'fcForeColor' in pen:
        color = pen['fcForeColor']
        r = (color >> 16) & 255
        g = (color >> 8) & 255
        b = color & 255
        pen_colors[pen_id] = (r, g, b)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Sous-titres visuels')

def draw_subtitle_line(line_data, y):
    x = 0
    for seg in line_data['segs']:
        pixel_count = len(seg['utf8'])
        pen_id = seg.get('pPenId', 0)
        color = pen_colors.get(pen_id, (255, 255, 255))

        for _ in range(pixel_count):
            if x < SCREEN_WIDTH:
                pygame.draw.rect(screen, color, (x, y, 10, 10))
                x += 10

def play_subtitles():
    start_time = time.time() * 1000

    while True:
        current_time = time.time() * 1000 - start_time
        screen.fill((0, 0, 0))

        for subtitle in subtitles_data['events']:
            t_start = subtitle['tStartMs']
            duration = subtitle['dDurationMs']
            t_end = t_start + duration

            if t_start <= current_time <= t_end:
                win_pos_id = subtitle['wpWinPosId']
                line_y = win_pos_id * 12
                draw_subtitle_line(subtitle, line_y)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

play_subtitles()
pygame.quit()
