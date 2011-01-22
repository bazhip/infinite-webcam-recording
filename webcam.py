from VideoCapture import Device
import ImageDraw, sys, pygame, time
from pygame.locals import *
from PIL import ImageEnhance
import os, subprocess

res = (640,480)
pygame.init()
cam = Device()
cam.setResolution(res[0],res[1])
screen = pygame.display.set_mode(res)
pygame.display.set_caption('Webcam')
pygame.event.set_allowed(KEYUP)
pygame.event.set_allowed(QUIT)
pygame.font.init()
font = pygame.font.SysFont("Courier",11)
current_directory = str(time.time())
os.mkdir(current_directory)

def disp(phrase,loc):
    s = font.render(phrase, True, (200,200,200))
    sh = font.render(phrase, True, (50,50,50))
    screen.blit(sh, (loc[0]+1,loc[1]+1))
    screen.blit(s, loc)

brightness = 1.0
contrast = 1.0
shots = 0
max_shots = 300
shots_every_second = 0.066667
last_capture_time = time.time()
snapshots_persisted = False
persist_allowed = True
persist_delay = 10
persist_time = time.time()
monitor = True

while monitor:
    camshot = ImageEnhance.Brightness(cam.getImage()).enhance(brightness)
    camshot = ImageEnhance.Contrast(camshot).enhance(contrast)

    if time.time() - persist_time > persist_delay:
        persist_allowed = True
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: monitor = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_1: brightness -= .1
            if event.key == pygame.K_2: brightness += .1
            if event.key == pygame.K_3: contrast -= .1
            if event.key == pygame.K_4: contrast += .1
            if event.key == pygame.K_q: cam.displayCapturePinProperties()
            if event.key == pygame.K_w: cam.displayCaptureFilterProperties()
            if event.key == pygame.K_ESCAPE: pygame.event.post(pygame.event.Event(QUIT,))
            if event.key == pygame.K_s and persist_allowed:
                command_line = "ffmpeg.exe -r 15 -i " + current_directory + "/%03d.jpg " + current_directory + ".mp4"
                print(command_line)
                subprocess.call(command_line)
                print("finished encoding")
                current_directory = str(time.time())
                snapshots_persisted = True
                persist_allowed = False
                persist_time = time.time()
        
    current_capture_time = time.time()
    capture_time_diff = current_capture_time - last_capture_time
    if (capture_time_diff > shots_every_second):
        if snapshots_persisted:
            os.mkdir(current_directory)
            snapshots_persisted = False
    
        last_capture_time = current_capture_time
        filename = current_directory + "/" + str(shots % max_shots).zfill(3) + ".jpg"
        cam.saveSnapshot(filename, quality=80, timestamp=0)
        shots += 1
    camshot = pygame.image.frombuffer(camshot.tostring(), res, "RGB")
    screen.blit(camshot, (0,0))
    disp("S:" + str(shots), (10,4))
    disp("B:" + str(brightness), (10,16))
    disp("C:" + str(contrast), (10,28))
    disp("capture_time_diff:" + str(capture_time_diff), (10, 40))
    pygame.display.flip()

del cam
pygame.quit()
