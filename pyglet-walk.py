import pyglet

def sprite_type(type_ = "standing"):
    if type_ == "moving-forward":
        moving_forward_image_list = [pyglet.image.load('assassin2.png'), pyglet.image.load('assassin3.png')]
        moving_forward_animation = pyglet.image.Animation.from_image_sequence(moving_forward_image_list, 0.3) 
        return moving_forward_animation
    if type_ == "standing":
        standing_animation = pyglet.image.load("assassin1.png")
        return standing_animation

class Assassin(pyglet.sprite.Sprite):
    def __init__(self, batch, img):
        pyglet.sprite.Sprite.__init__(self, img, x = 50, y = 30)

    def stand(self, batch, img):
        self.batch = batch
        self.img = img

    def move(self, batch, img):
        self.batch = batch
        self.img = img      

class Game(pyglet.window.Window):
    def __init__(self):
        pyglet.window.Window.__init__(self, width = 315, height = 220)
        self.batch_draw = pyglet.graphics.Batch()
        self.player = Assassin(batch = self.batch_draw, img = sprite_type())
        self.fps_display = pyglet.clock.ClockDisplay()
        self.keys_held = []      
        self.schedule = pyglet.clock.schedule_interval(func = self.update, interval = 1/60.) 

    def on_draw(self): 
        self.clear()         
        self.fps_display.draw()
        self.batch_draw.draw()
        if self.player:
            self.player.draw()

    def on_key_press(self, symbol, modifiers):
        self.keys_held.append(symbol)
        if symbol == pyglet.window.key.RIGHT:
            self.player = self.player.move(batch = self.batch_draw, img = sprite_type("moving-forward") )
            print("The 'RIGHT' key was pressed")

    def on_key_release(self, symbol, modifiers):
        self.keys_held.pop(self.keys_held.index(symbol))
        if self.player:
            print( self.player.stand(batch = self.batch_draw, img = sprite_type("standing") ) )

    def update(self, interval):
        if pyglet.window.key.RIGHT in self.keys_held:
            if self.player:
                self.player.x += 50 * interval

if __name__ == "__main__":
    window = Game()
pyglet.app.run()