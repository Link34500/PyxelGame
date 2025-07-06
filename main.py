import pyxel

WIDTH = 128
HEIGHT = 128

class Screen:
    MAIN_MENU = "MAIN_MENU"
    GAMESCREEN = "GAME_SCREEN"
    PAUSE_MENU = "PAUSE_MENU"
    GAME_OVER = "GAME_OVER"

CURRENT_SCREEN = Screen.MAIN_MENU
SOLID = []
COINS = []
PAGE = 0
LEVEL = 1

class Start:
    def __init__(self):
        pyxel.init(WIDTH,HEIGHT,"",fps=30)
        pyxel.load("4.pyxres")
        # Chargemment des assets
        SOLIDS_TILES = [(2,8),(3,8),(6,6),(7,6),(7,7),(6,7)]
        COIN_TILES = (18,6)
        for y in range(pyxel.tilemaps[0].height):
            for x in range(pyxel.tilemaps[0].width):
                tile = pyxel.tilemaps[0].pget(x,y)
                if tile in SOLIDS_TILES:
                    SOLID.append(Objet(x*8,y*8,8,8))
                if tile == COIN_TILES:
                    print(f"Tile crée aux cooordonée : {x},{y}")
                    COINS.append(Coin(x*8,y*8,16,16))
                    print(len(COINS))
                    
        self.cursor = Cursor(pyxel.mouse_x,pyxel.mouse_y,8,8)
        self.title = Text(text="Nuit du code",x=WIDTH/2,y=HEIGHT/6)
        self.button_play = Button(
            text="Play",
            x=WIDTH/2,
            y=HEIGHT/2,
            width=32,
            height=16,
            font_color=5,
            text_color=7,
            hfc=6,
            htc=7
        )
        # Game Screen : 
        self.score = 0
        self.title_score = Text(text=f"Score : {self.score}",x=len(f"Score : {self.score}")*2,y=pyxel.FONT_HEIGHT/2,text_color=9)
        self.player = Player(24*8,8*8,16,16,6,3)
        # Game over Screen : 
        gap = 5
        self.gameover_title = Text("Perdu Looser",WIDTH/2,HEIGHT/6,7)
        self.try_again_button = Button("Try Again",WIDTH/2,HEIGHT/1.5,48,16,3,7,11)
        self.menu_button = Button("Main Menu",WIDTH/2,HEIGHT/1.5+16+gap,48,16,8,7,14)
        self.buttons = [self.button_play,self.try_again_button,self.menu_button]
        pyxel.run(self.update,self.draw)
    
    def update(self):
        self.cursor.update()
        # Le design des boutons
        for button in self.buttons:
            if button.hitbox.collision(self.cursor):
                button.hover()
                if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                    match button:
                        case b if b in [self.button_play,self.try_again_button]:
                            global CURRENT_SCREEN
                            CURRENT_SCREEN = Screen.GAMESCREEN
                        case self.menu_button:
                            CURRENT_SCREEN = Screen.MAIN_MENU
            else:
                button.un_hover()
        match CURRENT_SCREEN:
            case Screen.GAMESCREEN:
                
                self.player.update()

                if self.player.x > WIDTH:
                    self.player.x = self.player.width
                    global PAGE
                    PAGE += 1
                    for solid in SOLID:
                        solid.x -= 128
                    for coin in COINS:
                        coin.x -= 128
                for solid in SOLID:
                    solid.y = solid.y - LEVEL*(128)
                for coin in COINS:
                    coin.y =  - LEVEL*128
                if self.player.x < 0 and PAGE != 0:
                    self.player.x = WIDTH-self.player.width
                    PAGE -= 1
                    for solid in SOLID:
                        solid.x += 128
                    for coin in COINS:
                        coin.x += 128

                # Efface la pièce de l'écran si le joueur la touche
                for coin in COINS:
                    
                    if self.player.hitbox.collision(coin):
                        pyxel.tilemaps[0].pset((coin.x+PAGE*128)//8,(coin.y+LEVEL*128)//8,(0,0))
                        pyxel.tilemaps[0].pset((coin.x+PAGE*128)//8+1,(coin.y+LEVEL*128)//8,(0,0))
                        pyxel.tilemaps[0].pset((coin.x+PAGE*128)//8,(coin.y+LEVEL*128)//8+1,(0,0))
                        pyxel.tilemaps[0].pset((coin.x+PAGE*128)//8+1,(coin.y+LEVEL*128)//8+1,(0,0))
                        COINS.remove(coin)
                        self.score += 100
                        self.title_score.text = f"Score : {self.score}"

                if pyxel.btn(pyxel.KEY_UP) and self.player.y > 0:
                    self.player.y -= 1
                
            

    def draw(self):
        pyxel.cls(0)
        match CURRENT_SCREEN:
            case Screen.MAIN_MENU:
                Cursor.draw()
                self.title.draw()
                self.button_play.draw()
                self.button_play.hitbox.draw()
                self.cursor.hitbox.draw()
            case Screen.GAMESCREEN:
                pyxel.mouse(False)
                pyxel.bltm(0,0,0,PAGE*WIDTH,LEVEL*HEIGHT,WIDTH,HEIGHT)
                self.player.draw()
                self.player.hitbox.draw()
                self.title_score.draw()
                for coin in COINS:
                    coin.hitbox.draw()
                for solid in SOLID:
                    solid.hitbox.draw()
            case Screen.GAME_OVER:
                Cursor.draw()
                self.try_again_button.draw()
                self.menu_button.draw()
                self.gameover_title.draw()


class Objet:
    def __init__(self,x:float,y:float,width:int,height:int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height 
        self.hitbox = Hitbox(self)

class ImgObjet(Objet):
    def __init__(self, x, y, width, height,row,column):
        super().__init__(x, y, width, height)
        self.row = row*width
        self.column = column*height
        
class Cursor(Objet):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def update(self):
        self.x = pyxel.mouse_x
        self.y = pyxel.mouse_y

    @staticmethod
    def draw():
        pyxel.mouse(True)

class Coin(Objet):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)


class Text(Objet):
    def __init__(self, text,x, y,text_color:int=7):
        super().__init__(x-len(text)*pyxel.FONT_WIDTH/2, y-pyxel.FONT_HEIGHT/2, len(text)*pyxel.FONT_WIDTH, pyxel.FONT_HEIGHT)
        self.text = text
        self.color = text_color
    
    def draw(self):
        pyxel.text(self.x,self.y,self.text,self.color)

class Player(ImgObjet):
    def __init__(self, x, y, width, height,row,column):
        super().__init__(x, y, width, height,row,column)
        self.vie = 3
        self.armure = True
        self.velocity = 2
    def update(self):
        print(f"{self.x},{self.y}")
        if pyxel.btn(pyxel.KEY_DOWN) and self.y < HEIGHT:
            self.y += self.velocity

        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.velocity
            self.width = self.width
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.velocity
    
    def draw(self):
        return pyxel.blt(self.x,self.y,0,self.row,self.column,self.width,self.height,pyxel.COLOR_PURPLE)

class Button(Objet):
    def __init__(self,text,x, y, width, height,font_color:int,text_color:int,hfc=None,htc=None):
        super().__init__(x-width/2, y-width/2, width, height)
        self.font_color = font_color
        self.hfc = hfc
        self.htc = htc
        self.fc = font_color
        self.tc = text_color
        self.text = Text(text,self.x+self.width/2,self.y+self.height/2,text_color)

    def draw(self):
        pyxel.rect(self.x,self.y,self.width,self.height,self.font_color)
        pyxel.text(x=self.text.x,y=self.text.y,s=self.text.text,col=self.text.color)

    
    def hover(self):
        if not self.hfc is None:
            self.font_color = self.hfc
        if not self.htc is None:
            self.text.color = self.htc
        
    def un_hover(self):
        if not self.hfc is None:
            self.font_color = self.fc
        if not self.htc is None:
            self.text.color = self.tc
        


class Hitbox:
    def __init__(self,objet:Objet):
        self.objet = objet
        self.hitbox_color = 8

    def draw(self):
        pyxel.rectb(self.objet.x,self.objet.y,self.objet.width,self.objet.height,self.hitbox_color)

    def collision(self,collision:Objet):
        return (self.objet.x < collision.x + collision.width and self.objet.x + self.objet.width > collision.x and self.objet.y < collision.y + collision.height and self.objet.y + self.objet.height > collision.y)


Start()