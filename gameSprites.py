import pygame as pg
from pygame.draw import rect
from pygame.locals import *

# ToDo: get the actual screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WIDTH = 64
HEIGHT = 64

class GameSprite(pg.sprite.Sprite):
    """self animating sprite to inhearit animate()
    do not use this sprite, inherit from it. it is a time saver helping with shared functions of sprite"""
    def __init__(self) -> None:
        super().__init__()
        self.animation_frames = {"animationName":{"images":[],"cycleSpeed":30}}
        self.animationData = {"animation":"","frame":0,"sinceLast":0}

    def animate(self):
        if self.animationData["sinceLast"] == self.animation_frames[self.animationData["animation"]]["cycleSpeed"]: #if it's time to change animation
            self.animationData["frame"]+=1  #next frame
            if self.animationData["frame"] == len(self.animation_frames[self.animationData["animation"]]["images"]):
                self.animationData["frame"] = 0     #reset if this was the last frame
            self.animationData["sinceLast"]=0   #reset the count
            #change the image to the next 
            self.image.fill(self.animation_frames[self.animationData["animation"]]["images"][self.animationData["frame"]])
        self.animationData["sinceLast"]+=1


class PlayerSprite(GameSprite):
    """player controlled charecter, provide a rect for movment"""
    def __init__(self, platform_rect):
        super().__init__()
        self.image = pg.Surface([WIDTH, HEIGHT])
        self.image.fill(pg.Color(50, 168, 82))
        self.rect = self.image.get_rect(topleft = (SCREEN_WIDTH/4,SCREEN_HEIGHT-HEIGHT-100))
        self.platform_rect = platform_rect.inflate(-platform_rect.width/5, -HEIGHT) #makes the rect smaller so it fits the image
        self.rect.centerx = self.platform_rect.centerx
        self.speed = 5
        # dict containing animation frames:
        self.animation_frames = {
            "idle":{"images":[pg.Color(50, 168, 82)], "cycleSpeed":25},      #cycle speed means - how many updates untill next frame (diffrent for each animation)
            "running":{"images":[pg.Color(219, 255, 110),pg.Color(22, 16, 102),pg.Color(252, 3, 240)], "cycleSpeed":20},
            "jumping":[],
            "sliding":[]
        }
        self.animationData={"animation":"running", "frame":0,"sinceLast":0}    # animation= name of animation, frame= current frame displayed, sincelast=how many updates passed since last call

    def update(self):
        """moves the player and handles animaion"""
        pressed_keys = pg.key.get_pressed()
        if self.rect.left > self.platform_rect.left:   
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-self.speed, 0)
        if self.rect.right <self.platform_rect.right:  
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(self.speed, 0)

        super().animate()
        
        

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Obsticale(GameSprite):
    """obsticale needed to be dodged"""
    def __init__(self, platform_rect):
        super().__init__()
        self.image = pg.Surface([32,32])
        self.image.fill(pg.Color(22, 130, 111))
        self.platform_rect = platform_rect
        self.rect = self.image.get_rect(topleft = (self.platform_rect.centerx,self.platform_rect.height//4))
        self.speed = 3

        self.animation_frames = {
            "idle":{"images":[pg.Color(219, 255, 110),pg.Color(22, 16, 102),pg.Color(252, 3, 240)], "cycleSpeed":20}  
        }
        self.animationData={"animation":"idle", "frame":0,"sinceLast":0}    

    def update(self):
        """increase the size of self rect, image, each call.
        on max size Obsticale is killed"""
        self.rect.move_ip(0, self.speed)
        self.image = pg.transform.scale(self.image,(self.rect.width + 1,self.rect.height +1))   #too fast
        self.rect = self.image.get_rect(topleft= self.rect.topleft)

        super().animate()

        if(not self.platform_rect.contains(self.rect)):
            print("killed")
            self.kill()
        

class Planform(GameSprite):
    """The platform player charecter is running on"""
    def __init__(self):
        super().__init__()
        # self.image = pg.Surface([SCREEN_WIDTH/2,SCREEN_HEIGHT])
        # self.image.fill(pg.Color(100, 130, 200))
        self.image = pg.transform.scale(pg.image.load(r"resources\models\platform.png"),(SCREEN_WIDTH//2,SCREEN_HEIGHT)).convert_alpha()
        self.rect = self.image.get_rect(topleft = (SCREEN_WIDTH/4,0))

        self.animation_frames = {
            "rolling":{"images":[], "cycleSpeed":20}   #cycle speed means - how many updates untill next frame (diffrent for each animation)
        }
        self.animationData={"animation":"rolling", "frame":0,"sinceLast":0}

    def update(self):
        """cycle animations of the platform"""
        pass
        #super().animate()

    def draw(self, surface):
        surface.blit(self.image, self.rect)


