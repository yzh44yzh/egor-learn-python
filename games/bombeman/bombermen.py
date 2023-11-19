import pygame
import tkinter
from tkinter import messagebox
import random
import player
import bomb
import labyrinth
import brick
import skin
import monster

FPS = 50

pygame.init()
pygame.display.set_caption('Bomberman')
surface = pygame.display.set_mode((721, 721))
clock = pygame.time.Clock()

#TODO: смерть монстров
#TODO: смерть игрока от них
#TODO: смена скина бомбы
#TODO: картинка с прозр фоном(взрыва и остальных)
#TODO: звуки

curr_skin = skin.skin_1
bomber = player.Player(curr_skin.name, surface)
bombs = []
laby = labyrinth.Labyrinth(curr_skin.brick_color)
bricks = laby.fill_with_bricks(curr_skin)
monsters = []
for i in range(5):
    mons = monster.Monster(surface, 17 * 40, 17 * 40)
    monsters.append(mons)

mons1 = monsters[0]

def change_skin(skin_number):
    global curr_skin
    global bricks
    if skin_number == 1:
        curr_skin = skin.skin_1
    elif skin_number == 2:
        curr_skin = skin.skin_2
    elif skin_number == 3:
        curr_skin = skin.skin_3
    bomber.set_skin(curr_skin.name)
    laby.color = curr_skin.brick_color
    for brick in bricks:
        brick.set_skin(curr_skin.name)

def game_over():
    tkinter.messagebox.showinfo('GAME OVER','OK')


running = True

while running:
    clock.tick(FPS)
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False
            break

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                bomber.step_left()
            elif event.key == pygame.K_d:
                bomber.step_right()
            elif event.key == pygame.K_w:
                bomber.step_up()
            elif event.key == pygame.K_s:
                bomber.step_down()
            elif event.key == pygame.K_SPACE:
                b = bomb.Bomb(bomber.x, bomber.y, curr_skin.name)
                bombs.append(b)
            elif event.key == pygame.K_1:
                change_skin(1)
            elif event.key == pygame.K_2:
                change_skin(2)
            elif event.key == pygame.K_3:
                change_skin(3)

            if event.key == pygame.K_LEFT:
                mons1.step_left()
            elif event.key == pygame.K_RIGHT:
                mons1.step_right()
            elif event.key == pygame.K_UP:
                mons1.step_up()
            elif event.key == pygame.K_DOWN:
                mons1.step_down()

    for mons in monsters:
        mons.walk()
        
    
    surface.fill(curr_skin.background_color)

    laby.draw(surface)

    exploded_bricks = [] 

    for brick in bricks:
        brick.draw(surface)
        if bomber.check_hit(brick):
            bomber.step_back()
        for mons in monsters:
            if mons.check_hit(brick):
                mons.step_back()
        for b in bombs:
            if b.check_hit(brick):
                exploded_bricks.append(brick)

    for mons in monsters:
        if bomber.check_hit(mons):
            bomber.step_back()

    bricks = list(set(bricks) - set(exploded_bricks))
    
    exploded_bombs = []

    for b in bombs:
        if b.tick():
            b.draw(surface)
        else:
            exploded_bombs.append(b)
        if bomber.check_hit(b):
            bomber.step_back()
        if b.check_hit(bomber):
            running = False
            game_over()
            break
        for mons in monsters:
            if b.check_hit(mons):
                mons.delete()
                #TODO: убрать монстра из списка, use deleted_monsters
                
    bombs = list(set(bombs) - set(exploded_bombs))
    
    
    bomber.draw()
    for mons in monsters:
        mons.draw()

    pygame.display.update()

pygame.quit()