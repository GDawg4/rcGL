import pygame
from pygame.locals import *
from math import sqrt, sin, cos, tan, radians

from main import Renderer
import shaders

deltaTime = 0.0

# Inicializacion de pygame
pygame.init()
clock = pygame.time.Clock()
screenSize = (960, 540)
screen = pygame.display.set_mode(screenSize, DOUBLEBUF | OPENGL)

# Inicializacion de nuestro Renderer en OpenGL
r = Renderer(screen)
r.set_shaders(shaders.vertex_shader, shaders.fragment_shader)
r.create_objects()

cubeX = 0
cubeY = 0
cubeZ = 0
roll = 0
pitch = 0
yaw = 0
distance = 0

isPlaying = True
while isPlaying:

    # Para revisar si una tecla esta presionada
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        yaw -= 90 * deltaTime % 360
        positions = r.get_info()
        cube_pos = positions[0]
        cam_pos = positions[1]
        distance = sqrt((cube_pos.x - cam_pos.x) ** 2 + (cube_pos.y - cam_pos.y) ** 2 + (cube_pos.z - cam_pos.z) ** 2)
        cubeX = sin(radians(yaw)) * 3
        cubeZ = cos(radians(yaw)) * 3 - 3
    if keys[pygame.K_d]:
        yaw += 90*deltaTime % 360
        positions = r.get_info()
        cube_pos = positions[0]
        cam_pos = positions[1]
        distance = sqrt((cube_pos.x - cam_pos.x) ** 2 + (cube_pos.y - cam_pos.y) ** 2 + (cube_pos.z - cam_pos.z) ** 2)
        cubeX = sin(radians(yaw))*3
        cubeZ = cos(radians(yaw))*3 - 3
    if keys[pygame.K_q]:
        cubeZ -= 2 * deltaTime
        cubeZ = max(-2, cubeZ)
    if keys[pygame.K_e]:
        cubeZ += 2 * deltaTime
        cubeZ = min(2, cubeZ)
    if keys[pygame.K_w]:
        pitch += 90 * deltaTime % 360
        positions = r.get_info()
        cube_pos = positions[0]
        cam_pos = positions[1]
        distance = sqrt((cube_pos.x - cam_pos.x) ** 2 + (cube_pos.y - cam_pos.y) ** 2 + (cube_pos.z - cam_pos.z) ** 2)
        cubeY = -sin(radians(pitch))*3
        cubeZ = cos(radians(pitch))*3 - 3
    if keys[pygame.K_s]:
        pitch -= 90 * deltaTime % 360
        positions = r.get_info()
        cube_pos = positions[0]
        cam_pos = positions[1]
        distance = sqrt((cube_pos.x - cam_pos.x) ** 2 + (cube_pos.y - cam_pos.y) ** 2 + (cube_pos.z - cam_pos.z) ** 2)
        cubeY = -sin(radians(pitch)) * 3
        cubeZ = cos(radians(pitch)) * 3 - 3


    # if keys[pygame.K_t]:
    #     roll += 10 * deltaTime
    # if keys[pygame.K_g]:
    #     roll -= 10 * deltaTime
    # if keys[pygame.K_r]:
    #     pitch += 10 * deltaTime
    # if keys[pygame.K_f]:
    #     pitch -= 10 * deltaTime
    # if keys[pygame.K_z]:
    #     yaw += 90 * deltaTime
    # if keys[pygame.K_x]:
    #     yaw -= 90 * deltaTime

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            isPlaying = False
        elif ev.type == pygame.KEYDOWN:
            # para revisar en el momento que se presiona una tecla
            if ev.key == pygame.K_1:
                r.filled_mode()
            elif ev.key == pygame.K_2:
                r.wireframe_mode()
            elif ev.key == pygame.K_SPACE:
                positions = r.get_info()
                cube_pos = positions[0]
                cam_pos = positions[1]
                distance = sqrt((cube_pos.x-cam_pos.x)**2 + (cube_pos.y-cam_pos.y)**2 + (cube_pos.z-cam_pos.z)**2)
                print(positions)
                print(distance)
                print(cube_pos.z, cam_pos.z)
                #r.next_figure()
                #r.set_shaders(shaders.vertex_shader, shaders.fragment_shader)
            elif ev.key == pygame.K_ESCAPE:
                isPlaying = False

    r.translate_camera(cubeX, cubeY, cubeZ)
    r.roll_camera(roll)
    r.pitch_camera(pitch)
    r.yaw_camera(yaw)

    # Main Renderer Loop
    r.render()

    pygame.display.flip()
    clock.tick(60)
    deltaTime = clock.get_time() / 1000

pygame.quit()
