import pygame
from math import *
import time

res = 200

screen = pygame.display.set_mode((res, res))




scale = 1

LightPos = (-5, 8, 0)
CameraPos = (0, 4, 10)

def sub(vec1, vec2):
    return [vec1[0]-vec2[0], vec1[1]-vec2[1], vec1[2]-vec2[2]]

def add(vec1, vec2):
    return [vec1[0]+vec2[0], vec1[1]+vec2[1], vec1[2]+vec2[2]]

def mul(vec1, vec2):
    return [vec1[0]*vec2[0], vec1[1]*vec2[1], vec1[2]*vec2[2]]



def length(vector):
    return sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)

def normalize(vector):
    mag = length(vector)
    if mag == 0:
        return [0, 0, 0]
    return [vector[0] / mag, vector[1] / mag, vector[2] / mag]


def dotproduct(vec1, vec2):
    return vec1[0] * vec2[0] + \
           vec1[1] * vec2[1] + \
           vec1[2] * vec2[2]

def scene(p):
    d1 = length(sub(p, (2, 1.5, 0))) - 1.5

    d2 = length(sub(p, (-2, 2, 0))) - 2


    d3 = p[1]
    return min(min(d1, d2), d3)


def raymarch(startPos, raydir):
    dist = 0
    p = list(startPos)
    for i in range(100):
        d = scene(p)
        dist += d
        if d <= 0.001 or dist >= 100:
            break
        p = add(startPos, mul(raydir, [dist, dist, dist]))
    return [dist, p]

def getNormal(p):
    d = scene(p)
    n = [d-scene(sub(p, [0.001, 0, 0])), 
         d-scene(sub(p, [0, 0.001, 0])), 
         d-scene(sub(p, [0, 0, 0.001]))]
    return normalize(n)

def getLight(pos):
    l = normalize(sub(LightPos, pos))
    normal = getNormal(pos)
    
    dif = max(min(dotproduct(normal, l), 1), 0)

    d = raymarch(add(pos, mul(normal, [0.002, 0.002, 0.002])), l) 


    if d[0] <= length(sub(LightPos, pos)):
        dif *= 0.2
    
    #return mul(add(normal, [1, 1, 1]), [255/2, 255/2, 255/2])
    return dif*0.8

def shader(pos, t):
    direction = normalize([pos[0]*2, -pos[1]*2, -1])
    r = raymarch((0, 4, 10), direction)
    
    d = getLight(r[1])*255

    return (d, d, d)


st = time.time()
while True:
    t = time.time()-st


    LightPos = (cos(t), 5, sin(t))
    for x in range(res):
        for y in range(res):
            color = shader([x/res-0.5, y/res-0.5], t)
            pygame.draw.line(screen, (color[0], color[1], color[2]), [x, y], [x, y])
    pygame.display.update()

