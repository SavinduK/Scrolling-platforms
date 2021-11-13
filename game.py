import pygame
import random
pygame.init()
win = pygame.display.set_mode((600,600))
pygame.display.set_caption("PyGame")

main_font = pygame.font.SysFont("comicsans", 50)
tile_img = [pygame.image.load("Assets/block4.png"),pygame.image.load("Assets/block6.png"),pygame.image.load("Assets/cloud1.png")] 
player_img = [ pygame.image.load("Assets/player1.png"), pygame.image.load("Assets/player2.png")]
coin_img = [pygame.image.load("Assets/coin1.png"),pygame.image.load("Assets/coin2.png")]
bomb_img = pygame.image.load("Assets/bomb1.png")
balloon_img =pygame.image.load("Assets/balloon2.png") 
background_img = pygame.image.load("Assets/background.png")
background = pygame.transform.scale(background_img,(600,600))
btn = pygame.image.load("Assets/start_btn.png")
spike =  pygame.image.load("Assets/spike.png")
run = False
clock = pygame.time.Clock()
move_dir = 0 # 1 left 2 right 0 stop
#----------------------------------------------------------------------------------------------------------------------------------
y1 = 0
y2 = 600
def draw_background():
    global y1,y2
    img1 = background
    img2 = background
    win.blit(img1,(0,y1))
    win.blit(img2,(0,y2))
    y1 -= 3
    y2 -= 3
    if y1 <= -600 :
        y1 = 600
    if y2 <= -600 :
        y2 = 600
#----------------------------------------------------------------------------------------------------------------------------------
class Player():
    def __init__ (self,x,y) :
     self.x = x
     self.y = y
     self.anim_index = 0
     self.anim_timer = pygame.time.get_ticks()
     self.image = player_img[self.anim_index]
     self.image = pygame.transform.scale(self.image,(int(self.image.get_rect().width * 2),int(self.image.get_rect().height * 2)))
     self.rect = self.image.get_rect()
     self.hitbox = pygame.Rect(0,0,self.rect.width*0.35,self.rect.height*0.75)
     self.rect.center = (x,y)
     self.hitbox.center = (x,y)
     self.y_vel = 0
     self.flip = False
    def draw(self,win):
      if pygame.time.get_ticks() - self.anim_timer > 200 :
        self.anim_timer = pygame.time.get_ticks()
        self.anim_index += 1
      if self.anim_index >= 2 :
          self.anim_index = 0   
      self.image = player_img[self.anim_index]
      self.image = pygame.transform.scale(pygame.transform.flip(self.image,self.flip,False),(int(self.image.get_rect().width * 2),int(self.image.get_rect().height * 1.75)))
      #pygame.draw.rect(win,(255,0,0),self.rect)
      #pygame.draw.rect(win,(0,255,0),self.hitbox)
      win.blit(self.image,self.rect)
    def move(self,move_dir):
        #print(move_dir)
        dx = 0
        dy = 0
        in_air = 0 # 1 on block 2 air
        if move_dir == 1 :
          dx -= 6
          self.flip = True
        if move_dir == 2:
          dx += 6
          self.flip = False
        self.y_vel += 0.25
        if self.y_vel > 5:
            self.y_vel = 5
        dy += self.y_vel
        """
        check x and y collisons seperately
        2 rects 
        pygame.Rect(self.hitbox.x+dx,self.hitbox.y,self.hitbox.width,self.hitbox.height)
        pygame.Rect(self.hitbox.x,self.hitbox.y+dy,self.hitbox.width,self.hitbox.height)
        """
        rect = pygame.Rect(self.hitbox.x+dx,self.hitbox.y+dy,self.hitbox.width,self.hitbox.height)
        if rect.x <= 0 or rect.x + rect.width >=600 :
            dx = 0
        #pygame.draw.rect(win,(255,255,255),rect)
        for tile in tiles :
            if tile.rect.colliderect(rect):
                c1 = tile.rect.collidepoint(rect.x,rect.y+rect.height)
                c2 = tile.rect.collidepoint(rect.x+rect.width,rect.y+rect.height)
                if  rect.bottom  > tile.rect.top :
                 if  (c1 or c2) :   
                  dy = 0
                  dx = 0
                  self.y_vel = 0
                  self.hitbox.bottom = tile.rect.top
                  #rect.bottom = tile.rect.top
                 else :
                   if rect.x < tile.rect.x :  
                    self.hitbox.right = tile.rect.left
                   else :
                     self.hitbox.left = tile.rect.right
        for platform in platforms:
           if platform.rect.colliderect(rect):
                c1 = platform.rect.collidepoint(rect.x,rect.y+rect.height)
                c2 = platform.rect.collidepoint(rect.x+rect.width,rect.y+rect.height)
                if  rect.bottom  > platform.rect.top :
                 if  (c1 or c2) :   
                  dy = 0
                  dx = 0
                  self.y_vel = 0
                  self.hitbox.bottom = platform.rect.top
                  #rect.bottom = tile.rect.top
                 else :
                   if rect.x < tile.rect.x :  
                    self.hitbox.right = platform.rect.left
                   else :
                     self.hitbox.left = platform.rect.right 
       
        self.hitbox.x += dx
        self.hitbox.y += dy
        self.rect.center = self.hitbox.center
#---------------------------------------------------------------------------------------------------------------------------------------      
class Tile():
    def __init__(self,x,y,tile_type):
        self.x = x
        self.y = y
        self.tile_type = tile_type
        self.moving = False
        self.move_timer = pygame.time.get_ticks()
        self.move_dir = 0
        if random.randrange(0,2)==1:
            self.move_dir = 1
        else :
            self.move_dir = -1
        self.image = tile_img[tile_type]
        self.image = pygame.transform.scale(self.image,(int(self.image.get_rect().width * 3),int(self.image.get_rect().height * 1.25)))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    def draw(self,win):
        win.blit(self.image,self.rect)
    def move(self):
       if self.moving :
        if self.x -self.rect.x > 200 :
            self.move_dir = +1
        if self.rect.x - self.x > 200 :
            self.move_dir = -1
        if self.rect.x <= 6 :
            self.move_dir = 1
        if self.rect.x + self.rect.width >= 594 :
            self.move_dir = -1
        if pygame.time.get_ticks() - self.move_timer > 200 :
            self.move_timer = pygame.time.get_ticks()
            if self.move_dir == 1:
                self.rect.x += 6
            if self.move_dir == -1:
                self.rect.x -= 6
#---------------------------------------------------------------------------------------------------------------------------------------
class Coin():
    def __init__(self,x,y,):
        self.x = x
        self.y = y
        self.anim_index = 0
        self.image = coin_img[self.anim_index]
        self.image = pygame.transform.scale(self.image,(int(self.image.get_rect().width * 0.5),int(self.image.get_rect().height * 0.5)))
        self.rect = self.image.get_rect()
        self.anim_timer = pygame.time.get_ticks()
        self.rect.center = (x,y)
    def draw(self,win):
        if pygame.time.get_ticks() - self.anim_timer > 250 :
            self.anim_timer = pygame.time.get_ticks()
            self.anim_index += 1
        if  self.anim_index >= 2:
            self.anim_index = 0
        self.image = coin_img[self.anim_index]
        self.image = pygame.transform.scale(self.image,(int(self.image.get_rect().width *0.75),int(self.image.get_rect().height * 0.75)))
        win.blit(self.image,self.rect)
    def collide(self,rect):
        return self.rect.colliderect(rect)
#-------------------------------------------------------------------------------------------------------------------------------------
class Bullet():
    def __init__ (self,x,y,direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.image = spike
        self.image = pygame.transform.scale(self.image,(int(self.image.get_rect().width * 1.5),int(self.image.get_rect().height * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.timer = pygame.time.get_ticks()
    def draw(self,win):
        win.blit(self.image,self.rect)
    def move(self):
        if pygame.time.get_ticks() - self.timer > 50 :
            self.timer = pygame.time.get_ticks()
            self.rect.x += self.direction * 6
#---------------------------------------------------------------------------------------------------------------------------------------        
player = Player(100,150)
tiles = [Tile(100+random.randrange(-30,30,5),200, 0)]
platforms=[]
coins = []
bullets =[]
score = 0
highscore = 0
with open("score.txt","r+")as f:
    highscore = int(f.read())
health = 1
platform_no = 3
gameover = False
#---------------------------------------------------------------------------------------------------------------------------------------
def add_tiles():
  global tiles
  global coins
  global score
  for tile in tiles :
      if tile.rect.y <= 50:
          tiles.remove(tile)
  for coin in coins :
      if coin.rect.y <= 50:
          coins.remove(coin)
  if len(tiles)<= 8 :
      last_tile = tiles[len(tiles)-1]
      lane_no = random.randrange(0,3)
      new_x = (lane_no * 200 + 100)+ random.randrange(-30,30,10)
      new_y = last_tile.rect.y + 150 + random.randrange(0,20,5)
      if score > 35 and random.randrange(0,3)== 2 :  
        new_tile = Tile(new_x,new_y,1)
      else :
        new_tile = Tile(new_x,new_y,0)
      if score > 20 and random.randrange(0,2)== 1:
          new_tile.moving = True
      tiles.append(new_tile)
      if new_tile.tile_type != 1 and new_tile.moving == False:
       no_of_coins = int( new_tile.rect.width / coin_img[0].get_rect().width)
       cx = new_tile.rect.x + 25
       while no_of_coins - 1 > 0 :
          no_of_coins -= 1
          coins.append(Coin(cx,new_tile.rect.y - 25 ))
          cx += 40
#---------------------------------------------------------------------------------------------------------------------------------------      
timer = pygame.time.get_ticks()      
def scroll () :
  global timer
  global tiles
  global player
  if pygame.time.get_ticks() - timer > 100 :
      timer = pygame.time.get_ticks()
      for tile in tiles:
          tile.rect.y -= 5
      player.hitbox.y -=5
      player.rect.y -= 5
      for coin in coins :
          coin.rect.y -= 5
      for platform in platforms :
          platform.rect.y -= 5
#----------------------------------------------------------------------------------------------------------------------------------------

while True :          
 while run :
  clock.tick(60)
  win.blit(background,background.get_rect())
  #draw_background()
  pygame.draw.line(win,(255,0,0),(0,50),(600,50))
  add_tiles()
  scroll()
  player.draw(win)
  player.move(move_dir)
  for tile in tiles:
      tile.draw(win)
      tile.move()
      if tile.y <= 0 :
          tiles.remove(tile)
      if tile.tile_type == 1 and tile.rect.colliderect(player.rect):
          health = 0
  for coin in coins :
      coin.draw(win)
      if coin.collide(player.hitbox):
          coins.remove(coin)
          score += 1
  score_label = main_font.render(f"{score}", 1, (0,0,0))
  cloud_label = main_font.render(f"{platform_no}", 1, (0,0,0))
  win.blit(score_label,(75,9))
  win.blit(coin_img[0],(25,9))
  win.blit(cloud_label,(575,9))
  win.blit(tile_img[2],(525,9))
  for platform in platforms :
      platform.draw(win)
      if platform.x <= 50 :
          platforms.remove(platform)
  if player.rect.y <= 50 :
      health = 0
  if player.rect.y + player.rect.height >= 600 :
      health = 0
  if health == 0 :  
    gameover = True
    run = False
    if score > highscore :
        highscore = score
        with open ("score.txt","w+")as f:
           f.write(f"{highscore}")
            
  if len(bullets)<= 1 and random.randrange(0,15)==4 and score > 40:
      y = random.randrange(0,2)
      if y == 1:
         x = 0
         direction = 1
      else :
          x = 600
          direction = -1
      bullets.append(Bullet(x,random.randrange(50,600,10),direction))
  for bullet in bullets:
      bullet.draw(win)
      bullet.move()
      if bullet.rect.colliderect(player.hitbox):
          health = 0
      if bullet.rect.x <= -50  :
          bullets.remove(bullet)
      if bullet.rect.x >= 650 :
          bullets.remove(bullet)
  pygame.display.update()
  
 
  for event in pygame.event.get():
      if event.type == pygame.QUIT :
          pygame.quit()
          run = False
      if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_a:
              move_dir = 1
          if event.key == pygame.K_d:
              move_dir = 2
          if event.key == pygame.K_SPACE :
              if platform_no > 0 :
                 platforms.append(Tile(player.hitbox.x-30,player.hitbox.y + player.hitbox.height*1.5,2))
                 platform_no -= 1
      if event.type == pygame.KEYUP:
          move_dir = 0
          if event.key == pygame.K_a:
              move_dir = 0
          if event.key == pygame.K_d:
              move_dir = 0
#------------------------------------------------------------------------------------------------------------------------------

 while not run:
  background_img = pygame.transform.scale(background_img,(600,600))
  win.blit(background_img,(0,0))
  btn = pygame.transform.scale(btn,(200,75))
  rect = pygame.Rect(200,200,200,75)
  win.blit(btn,rect)
  if gameover :
     score_label = main_font.render(f"Your_Score: {score}", 1, (0,0,0))
     Hscore_label = main_font.render(f"Highscore: {highscore}", 1, (0,0,0))
     win.blit(score_label,(183,350))
     win.blit(Hscore_label,(200,400))
  #pygame.draw.rect(win,(255,255,255),rect)
  for event in pygame.event.get():
     if event.type == pygame.QUIT:
        pygame.quit()
     if event.type == pygame.MOUSEBUTTONDOWN:
       print("123") 
       if rect.collidepoint(pygame.mouse.get_pos()):
          score = 0
          run = True
          gameover = False
          player = Player(100,150)
          tiles = [Tile(100+random.randrange(-30,30,5),200, 0)]
          coins = []
          health = 1
          platform_no = 3
          print("3")
          print(run)
          move_dir = 0
  pygame.display.update()
