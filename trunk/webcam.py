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
pygame.display.set_caption('Infinite Webcam Recording')
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
max_duration_in_seconds = 24 * 60 * 60
frames_per_second = 10
shots_every_second = 1. / frames_per_second
shots = 0
max_shots = max_duration_in_seconds * frames_per_second
last_capture_time = time.time()
snapshots_persisted = False
monitor = True

while monitor:
    camshot = ImageEnhance.Brightness(cam.getImage()).enhance(brightness)
    camshot = ImageEnhance.Contrast(camshot).enhance(contrast)
    
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
            if event.key == pygame.K_s:
                command_line = "ffmpeg.exe -r " + str(frames_per_second) + \
                               " -i " + current_directory + "/%03d.jpg " + \
                               current_directory + ".mp4"
                subprocess.call(command_line)
                current_directory = str(time.time())
                snapshots_persisted = True
        
    current_capture_time = time.time()
    capture_time_diff = current_capture_time - last_capture_time
    if (capture_time_diff > shots_every_second):
        if snapshots_persisted:
            os.mkdir(current_directory)
            snapshots_persisted = False
    
        last_capture_time = current_capture_time
        filename = current_directory + "/" + str(shots % max_shots).zfill(3) + ".jpg"
        cam.saveSnapshot(filename, quality=80, timestamp=3)
        shots += 1
    camshot = pygame.image.frombuffer(camshot.tostring(), res, "RGB")
    screen.blit(camshot, (0,0))
    disp("shots:" + str(shots), (10,4))
    disp("brightness:" + str(brightness), (10,16))
    disp("contrast:" + str(contrast), (10,28))
    disp("fps:" + str(frames_per_second), (10, 40))
    pygame.display.flip()

del cam
pygame.quit()
