#圖片、音效、音樂、文字檔案微軟正黑體font.ttf這些資料都要放在C:\Users\CBC
from tkinter import CENTER
import pygame
import time
import random
import os#為了避免路徑不同發生錯誤，引入os模組，注意!!圖片資料夾要跟vscode同一個資料夾!!
#不會做更改的變數名稱都是用大寫來呈現
FPS = 60 #幀率(Frame Per Second; fps) 即是指一秒鐘的影片含有多少張靜態圖片
WIDTH = 500
HEIGHT = 600

BLACK = (0,0,0)
WHITE = (255,255,255) 
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)

# 遊戲初始化跟創建視窗
pygame.init()  #把遊戲做初始化動作
pygame.mixer.init()#把音樂做初始化
screen = pygame.display.set_mode((WIDTH,HEIGHT)) 

running = True  #讓遊戲可以重覆執行
pygame.display.set_caption("數學太空戰")#將遊戲標題另外命名
clock = pygame.time.Clock()#創建一個物件，對時間做管理及操控，因為每個人的電腦執行速度不一樣

#載入圖片
background_img = pygame.image.load(os.path.join("img", "background.png")).convert()#載入背景圖片
player_img = pygame.image.load(os.path.join("img", "player.png")).convert()#載入飛船圖片

player_mini_img = pygame.transform.scale(player_img, (25,19))#這一行跟下一行是要用小張的飛船圖片代表還剩下幾條命
player_mini_img.set_colorkey(BLACK)

pygame.display.set_icon(player_mini_img)#遊戲畫面標題旁邊加上小圖片
bullet_img = pygame.image.load(os.path.join("img", "bullet.png")).convert()
plus_img = pygame.image.load(os.path.join("img", "plus.jpg")).convert()
plus_img = pygame.transform.scale(plus_img,(20,20))
minus_img = pygame.image.load(os.path.join("img", "minus.jpg")).convert()
minus_img = pygame.transform.scale(minus_img,(20,20))

target_img = pygame.image.load(os.path.join("img", "target.png")).convert()
target_img = pygame.transform.scale(target_img,(75,75))
target_img.set_colorkey(BLACK)


#創建數字圖片表
num_imgs = []
for i in range(1,10):
    num_imgs.append(pygame.image.load(os.path.join("img", f"num{i}.jpg")).convert())

image_to_score = {
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9
}

expl_anim = {}#當子彈打到石頭是大爆炸，石頭撞到飛船是小爆炸，用字典來寫，來存放
expl_anim['lg'] = []#lg=large
expl_anim['sm'] = []#sm=small
expl_anim['player'] = []#新增主角死亡爆炸
for i in range(9):  #把九張爆炸照片引入進來
    expl_img = pygame.image.load(os.path.join("img", f"expl{i}.png")).convert()#複製33行把rock改成expl
    expl_img.set_colorkey(BLACK)
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (75,75)))#75乘上75大爆炸
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (30,30)))#小爆炸30*30
    player_expl_img = pygame.image.load(os.path.join("img", f"player_expl{i}.png")).convert()#複製39行，主角爆炸，一樣是9張圖片做成的動畫，程式加上player
    player_expl_img.set_colorkey(BLACK)#程式加上player
    expl_anim['player'].append(player_expl_img)#程式加上player，用原本的大小即可


#載入音樂、音效
shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))#把射擊的聲音給引入進來
die_sound = pygame.mixer.Sound(os.path.join("sound", "rumble.ogg"))#複製上一行，增加主角死亡音效，rumble.ogg是死亡的音效檔案名稱
expl_sounds = [#引入石頭爆炸的聲音，音檔有兩個採取隨機撥放的方式，用列表來寫
    pygame.mixer.Sound(os.path.join("sound", "expl0.wav")),#把兩個爆炸的音效引入
    pygame.mixer.Sound(os.path.join("sound", "expl1.wav"))
]

shoot_sound.set_volume(0.0001)#把背音樂音量調小，參數裡面代表的是音量大小，數字是0到1！！！！
die_sound.set_volume(0.0001)#把背音樂音量調小，參數裡面代表的是音量大小，數字是0到1！！！！
expl_sounds[0].set_volume(0.0001)#把背音樂音量調小，參數裡面代表的是音量大小，數字是0到1！！！！
expl_sounds[1].set_volume(0.0001)#把背音樂音量調小，參數裡面代表的是音量大小，數字是0到1！！！！

pygame.mixer.music.load(os.path.join("sound", "background.ogg"))#背景音樂引入
pygame.mixer.music.set_volume(0.0001)#把背音樂音量調小，參數裡面代表的是音量大小，數字是0到1！！！！


font_name = os.path.join("font.ttf")#改字體

def draw_text(surf, text, size, x, y):#寫一個函式處理文字顯示在畫面上的動作，第一個參數是顯示在甚麼平面上，第二個參數是要顯示的文字，第三個是文字的大小，最後是寫在甚麼座標
    font = pygame.font.Font(font_name, size)#函式一開始先創建一個文字的物件，第一個參數是字體，第二個是文字的大小
    text_surface = font.render(text, True, WHITE)#把文字的物件給渲染出來，第一個參數是渲染的文字，第二個是布林值(代表的是要不要反鋸齒，讓字體比較滑順平順)，第三個參數是文字的顏色
    text_rect = text_surface.get_rect()#把文字做一個定位
    text_rect.centerx = x #定位在傳進來的X
    text_rect.top = y #top定位在傳進來的Y
    surf.blit(text_surface, text_rect)#把它畫在傳進來的平面上，傳進來的文字是text_surface，位置是text_rect

def new_num():
    r = Num()#所以在裡面創建數字圖
    all_sprites.add(r)#把它加回all_sprites群組裡面，加回去才可以被更新及畫面顯示出來
    Nums.add(r)#加回數字群組

def draw_lives(surf, lives, img, x, y):#定義一個畫飛船的函式，把飛船還有幾條命畫出來，定義畫在哪一個平面，還剩幾條命，畫的圖片是甚麼，XY座標要畫在哪裡
    for i in range(lives):#先看還剩幾條命
        img_rect = img.get_rect()#把圖片定位畫出來
        img_rect.x = x + 30*i#把三個飛船間隔30象素，這樣才不會重疊在一起
        img_rect.y = y
        surf.blit(img, img_rect)#把它畫出來，畫在剛剛定位的地方

#目標圖片
def draw_target(surf, img, x, y):
    img_rect = img.get_rect() #把圖片定位畫出來
    img_rect.x = x
    img_rect.y = y
    surf.blit(img, img_rect) #把它畫出來，畫在剛剛定位的地方

#初始畫面的函式
def draw_init():
    screen.blit(background_img, (0,0)) #背景
    draw_text(screen, '數學太空站!', 64, WIDTH/2, HEIGHT/4)#遊戲名稱跟操作說明，用65行的draw_text這個定義，第一個是顯示在甚麼平面上，第二個是要顯示甚麼文字，文字大小，X座標，Y座標
    draw_text(screen, '← →移動飛船 空白鍵發射子彈~', 18, WIDTH/2, HEIGHT/2)
    draw_text(screen, '按任意鍵開始遊戲!', 12, WIDTH/2, HEIGHT*3/4)#高度在往下一點，移到四分之三位置
    pygame.display.update()#這一行程式要寫才會畫出來
    waiting = True#用一個while迴圈，代表玩家有按下任意按鍵才開始遊戲
    while waiting:
        clock.tick(FPS)
            #取得輸入
        for event in pygame.event.get(): #用for迴圈把每個事件拿出來檢查，pygame.event.get():它是一個函式，會回傳所有發生的事件(像是滑鼠滑過)
            if event.type == pygame.QUIT:#檢查事件的類型是不是把pygame給關閉
                pygame.quit()          
                return True 
            elif event.type == pygame.KEYUP:
                waiting = False
                return False
#結束畫面
def draw_end():
    screen.blit(background_img, (0,0))
    draw_text(screen, '結束挑戰！再接再厲！', 40, WIDTH/2, HEIGHT/4)#遊戲名稱跟操作說明，用65行的draw_text這個定義，第一個是顯示在甚麼平面上，第二個是要顯示甚麼文字，文字大小，X座標，Y座標
    draw_text(screen, '你的分數為',32 , WIDTH/2, HEIGHT/3)
    draw_text(screen,str(score), 24, WIDTH/2, HEIGHT/2)
    draw_text(screen,'按下Enter即可回到主畫面', 12, WIDTH/2, HEIGHT*3/4)
    pygame.display.update()
    waiting = True #用一個while迴圈，代表玩家有按下Enter才重新開始遊戲
    while waiting:
        clock.tick(FPS)
            #取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()          
                return True 
            elif event.type == pygame.KEYUP and event.key == pygame.K_RETURN : #按下Enter才會回到遊戲初始畫面
                waiting = False
                return False

class Player(pygame.sprite.Sprite):
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50,38)) #pygame.transform.scale這個函式可以重新定義圖片，第一個傳入的值是圖片，第二個傳入的是要轉換成甚麼大小
        self.image.set_colorkey(BLACK) #去背，set_colorkey這個函式可以傳入RGB的值，然後把顏色更改為透明
        self.rect = self.image.get_rect() #rect是拿來定位這張圖片，把圖片定位框起來  
        self.radius = 20 #增加一個屬型是飛船的半徑
        #設定座標
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT -10

        self.speedx = 8#用變數控制速度
        self.lives = 3 #設定有幾條命就是在player這邊多一個屬性
        self.hidden = False #判斷飛船是不是在隱藏中
        self.hide_time = 0 #紀錄隱藏的時間

    def update(self):
        now = pygame.time.get_ticks()#子彈等級過一段時間會自動下降

        if self.hidden and now - self.hide_time > 1000:#如果主角死亡的時間比現在更新的時間還要超過一秒則讓主角顯示回來
            self.hidden = False
            self.rect.centerx = WIDTH/2#把主角定位回去
            self.rect.bottom = HEIGHT -10

        key_pressed = pygame.key.get_pressed()#會回傳一個布林值，如果被按則回傳TRUE沒有就FALSE
        if key_pressed[pygame.K_RIGHT]:#判斷右鍵有沒有被按下去，有按則回傳TRUE沒有就FALSE
            self.rect.x +=self.speedx#原本是self.rect.x +=2，現在改為用變數
        if key_pressed[pygame.K_LEFT]:#判斷右鍵有沒有被按下去，有按則回傳TRUE沒有就FALSE
            self.rect.x -=self.speedx
        
        #判斷腳色有無超出視窗
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    
    def shoot(self):#創建一個shoot函式
        if not(self.hidden):#如果不是在隱藏中才讓主角發射子彈(因為主角死掉會隱藏)
            bullet = Bullet(self.rect.centerx, self.rect.top)#發射子彈，子彈要傳入兩個資料，飛船的中間點X跟底部
            all_sprites.add(bullet)#把子彈加到all_sprite群組裡面
            bullets.add(bullet)#把子彈加到子彈的群組
            shoot_sound.play()#播放音效

    
    def shoot_plus(self):
        bullet = plus(self.rect.centerx, self.rect.top)#發射子彈，子彈要傳入兩個資料，飛船的中間點X跟底部
        all_sprites.add(bullet)#把子彈加到all_sprite群組裡面
        plus_bullets.add(bullet)#把子彈加到子彈的群組
        shoot_sound.play()#播放音效

    def shoot_minus(self):
        bullet = minus(self.rect.centerx, self.rect.top)#發射子彈，子彈要傳入兩個資料，飛船的中間點X跟底部
        all_sprites.add(bullet)#把子彈加到all_sprite群組裡面
        minus_bullets.add(bullet)#把子彈加到子彈的群組
        shoot_sound.play()#播放音效
    
    def hide(self):#主角死亡時要用到的程式
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()#把時間給記下來
        self.rect.center = (WIDTH/2, HEIGHT+500)#把飛船給定義到視窗的外面

class Num(pygame.sprite.Sprite):#去繼承內建的Sprite類別
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.num = random.randint(1, 9)
        self.image = num_imgs[self.num - 1]  # 使用圖片列表載入對應的圖片
        self.image.set_colorkey(BLACK) #去背
        self.image = pygame.transform.scale(self.image, (50,50)) #調整圖片大小  
        self.rect = self.image.get_rect()#定位中心點，把圖片定位框起來  
        self.radius = int(self.rect.width)
        self.rect.centerx = random.randrange(0,WIDTH - self.rect.width)#設定石頭X座標在隨機的位置，randrange是一個函式(最小值，最大值畫面寬度減掉石頭寬度)
        self.rect.y = -100
        self.speedy = 1.5
        self.speedx = 0 #水平速度

    def update(self): 
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:#超出畫面重新出現
            self.kill()
            # new_num()

class Bullet(pygame.sprite.Sprite):#去繼承內建的Sprite類別，Bullet是子彈
    def __init__(self,x,y) :#子彈要跟著飛船移動，所以要創建X跟Y的資訊
        pygame.sprite.Sprite.__init__(self)#去呼叫(call)內建的sprite初始函式
        self.image = bullet_img #圖片用匯入取代
        self.image.set_colorkey(BLACK) #去背
        self.rect = self.image.get_rect()#rect是拿來定位這張圖片，把圖片定位框起來  
        self.rect.centerx = x
        self.rect.bottom = y
        #self.speedy = 2#用變數控制速度
        self.speedy = -10#因為子彈是向上射

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:#往上射出了視窗就把它刪除掉
            self.kill()#這個kill是Sprite裡面的函式

class plus(pygame.sprite.Sprite):#去繼承內建的Sprite類別，Bullet是子彈
    def __init__(self,x,y) :#子彈要跟著飛船移動，所以要創建X跟Y的資訊
        pygame.sprite.Sprite.__init__(self)#去呼叫(call)內建的sprite初始函式
        self.image = plus_img #圖片用匯入取代
        self.image.set_colorkey(BLACK) #去背
        self.rect = self.image.get_rect()#rect是拿來定位這張圖片，把圖片定位框起來  
        self.rect.centerx = x
        self.rect.bottom = y
        #self.speedy = 2#用變數控制速度
        self.speedy = -10#因為子彈是向上射

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:#往上射出了視窗就把它刪除掉
            self.kill()#這個kill是Sprite裡面的函式

class minus(pygame.sprite.Sprite):#去繼承內建的Sprite類別，Bullet是子彈
    def __init__(self,x,y) :#子彈要跟著飛船移動，所以要創建X跟Y的資訊
        pygame.sprite.Sprite.__init__(self)#去呼叫(call)內建的sprite初始函式
        self.image = minus_img #圖片用匯入取代
        self.image.set_colorkey(BLACK) #去背
        self.rect = self.image.get_rect()#rect是拿來定位這張圖片，把圖片定位框起來  
        self.rect.centerx = x
        self.rect.bottom = y
        #self.speedy = 2#用變數控制速度
        self.speedy = -10#因為子彈是向上射

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:#往上射出了視窗就把它刪除掉
            self.kill()#這個kill是Sprite裡面的函式

class Explosion(pygame.sprite.Sprite):#複製整個class Bullet，改成Explosion，處理爆炸這件事
    def __init__(self,center,size) :#爆炸的中心點，用SIZE決定是大爆炸還是小爆炸
        pygame.sprite.Sprite.__init__(self)#去呼叫(call)內建的sprite初始函式
        self.size = size #把大爆炸或是小爆炸存起來
        self.image = expl_anim[self.size][0]#爆炸的第一張圖片，看是大爆炸或是小爆炸的第0張圖片，0123
        self.rect = self.image.get_rect()#rect是拿來定位這張圖片，把圖片定位框起來  
        self.rect.center = center#把中心點定位在中心點
        self.frame = 0#更新到第幾張圖片，一開始是第0張
        self.last_update = pygame.time.get_ticks()#紀錄一下最後一次更新圖片的時間，這個函式會回傳從初始化到現在的毫秒數
        self.frame_rate = 50#設定要更新多少毫秒才會進入到下一張圖片，數字變大動畫變慢

    def update(self):
        now = pygame.time.get_ticks()#過了50毫秒才更新圖片，記錄現在的時間
        if now - self.last_update > self.frame_rate:
            self.last_update = now#把最後一次更新時間改成現在
            self.frame += 1#把更新到第幾張圖片+1
            if self.frame == len(expl_anim[self.size]):#判斷現在的frame有沒有執行到最後一張，會等於他的length長度
                self.kill()#更新到最後一張圖片就把他刪掉
            else:#反之就把它更新到下一張
                self.image = expl_anim[self.size][self.frame]#把圖片做變更，看是大爆炸還是小爆炸，然後是第幾張圖片
                center = self.rect.center#將圖片做重新定位，把中心點先記起來
                self.rect= self.image.get_rect()#把爆炸的圖片做重新定位
                self.rect.center = center

#創建一個sprite群組，名字叫做all_sprites，群組裡面可以放很多個物件(創建群組是為了後面碰撞)
all_sprites = pygame.sprite.Group() 
Nums = pygame.sprite.Group()
bullets = pygame.sprite.Group()
plus_bullets = pygame.sprite.Group()
minus_bullets = pygame.sprite.Group()
player = Player() #創建一個player物件
all_sprites.add(player) #把player加到all_sprites裡面

pygame.mixer.music.play(-1)#播放音樂，參數裡面表示的是要重復播放幾次，-1代表的是無限重復播放

#遊戲迴圈
show_init = True #判斷初始畫面要不要顯示
show_end = False

falling_time = random.randint(1000, 2000)
last_fall_time = 0  # 紀錄上一次掉落物品的時間
shoot_count = 0

while running:
    current_time = pygame.time.get_ticks()  # 取得當前時間
    if show_init:#在迴圈一開始判斷要不要顯示初始畫面
        close = draw_init()#如果要顯示就把它畫出來，用init這個函式把它畫出來，用close判斷有沒有關閉
        if close:
            break
        show_init = False
        all_sprites = pygame.sprite.Group()#創建一個sprite群組，名字叫做all_sprites，群組裡面可以放很多個物件
        Nums = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        plus_bullets = pygame.sprite.Group()
        minus_bullets = pygame.sprite.Group()
        player = Player()#創建一個player物件
        all_sprites.add(player)#把player加到all_sprites裡面
        
        target_num = random.randint(0, 60) - 30
        score = 0

    if target_num == 0:
        target_num = random.randint(0, 60) - 30
        if shoot_count <= 5:
            score += 1000
        if 5 < shoot_count <= 10:
            score += 500
        if 10 < shoot_count:
            score += 250
        shoot_count = 0



    if current_time - last_fall_time > falling_time:
        for i in range(1):  # 一次掉下多少東西
            new_num()
            last_fall_time = current_time  # 更新最後掉落物品的時間
        falling_time = random.randint(1000, 2000)
        
    clock.tick(FPS)#在程式裡面一秒鐘之內最多只能執行FPS次

    for event in pygame.event.get(): #檢查事件，會回傳所有發生的事件(像是滑鼠滑過)
        if event.type == pygame.QUIT: #檢查事件是否為關閉遊戲
            running = False          
        elif event.type == pygame.KEYDOWN:#做一個判斷是不是按下鍵盤按鍵
            if event.key == pygame.K_SPACE:#判斷它按下了什麼鍵，如果是空白鍵
                player.shoot()#呼叫shoot函式，發射
            if event.key == pygame.K_q:#判斷它按下了什麼鍵，如果是空白鍵
                player.shoot_plus()#呼叫shoot函式，發射
            if event.key == pygame.K_w:#判斷它按下了什麼鍵，如果是空白鍵
                player.shoot_minus()#呼叫shoot函式，發射

    # 更新遊戲
    all_sprites.update()#就會執行群組裡面每一個update的函式

    # 判斷數字、消除子彈相撞
    hits = pygame.sprite.groupcollide(Nums, bullets, True, True) #這邊會把子彈跟石頭的位置做更新看碰撞，石頭跟子彈群組傳進去，判斷碰撞之後石頭和子彈要不要刪掉(要就是TRUE)
    for hit in hits: #每碰撞到一次就補一顆石頭給他
        random.choice(expl_sounds).play() #隨機爆炸音效
        expl = Explosion(hit.rect.center,'lg') #當石頭跟子彈碰撞到的時候就創建一個explosion的split，爆炸的中心點
        all_sprites.add(expl) #最後把他加到all_sprites裡面，這樣才會畫出爆炸動畫
        # new_num()

    # 判斷數字、加號子彈相撞
    hits = pygame.sprite.groupcollide(Nums, plus_bullets, True, True)
    for hit in hits: 
        random.choice(expl_sounds).play() #隨機爆炸音效
        target_num += image_to_score[hit.num] #利用數字編號
        expl = Explosion(hit.rect.center,'lg') 
        all_sprites.add(expl)
        shoot_count += 1
        # new_num()

    # 判斷數字、負號子彈相撞
    hits = pygame.sprite.groupcollide(Nums, minus_bullets, True, True)
    for hit in hits: 
        random.choice(expl_sounds).play() #隨機爆炸音效
        target_num -= image_to_score[hit.num] #利用數字編號
        expl = Explosion(hit.rect.center,'lg') 
        all_sprites.add(expl)
        shoot_count += 1
        # new_num()

    #判斷石頭飛船碰撞
    hits = pygame.sprite.spritecollide(player, Nums, True)
    for hit in hits: #扣血的方式
        #下面這三行是飛船撞到石頭之後石頭會不見，要把他增加回畫面
        # new_num()
        expl = Explosion(hit.rect.center,'sm') #石頭碰到飛船是小爆炸
        all_sprites.add(expl)
        death_expl = Explosion(player.rect.center, 'player')#主角死亡，爆炸的中心點是飛船的中央，SIZE是player
        all_sprites.add(death_expl)
        die_sound.play() #死亡音效播放
        player.lives -= 1
        player.hide() #主角死亡之後先緩衝一段時間再復活

#目前為遊戲關閉，但可以再多一個頁面顯示計分
    if player.lives == 0:
        show_end = True
        if show_end:#在迴圈一開始判斷要不要顯示初始畫面
            reset = draw_end()#如果要顯示就把它畫出來，用init這個函式把它畫出來，用close判斷有沒有關閉
        if reset:
            break
        show_init = True

    # 畫面顯示
    screen.fill(BLACK)#背景顏色用填滿方式，用WHITE變數代替，也可以寫screen.fill((255,255,255))，數字是RGB
    screen.blit(background_img, (0,0)) #背景(因為要占滿整個視窗所以畫在左上角(0,0)也就是XY座標)
    all_sprites.draw(screen) #把all_sprites裡面的物件全部畫出來
    draw_text(screen, str(score), 18, WIDTH/2, 10) #分數的位置
    draw_lives(screen, player.lives, player_mini_img, WIDTH - 100, 15) #生命數量的位置
    draw_target(screen,target_img,10,10)


    draw_text(screen, str(target_num), 30, 45,22.5) #分數的位置 #想辦法置中(目前只是看起來，可以尋求更好的方法)
    pygame.display.update()

pygame.quit()   #在外面把pygame的視窗關掉，跳出迴圈關閉視窗 