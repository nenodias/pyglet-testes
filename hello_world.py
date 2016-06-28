import pyglet
from pyglet.window import key, mouse

window = pyglet.window.Window()

keyboard = key.KeyStateHandler()
window.push_handlers(keyboard)

image = pyglet.resource.image('exemplo.png')
image.anchor_x = image.width // 2
image.anchor_y = image.height // 2

explosion = pyglet.resource.media('explosion.wav', streaming=False)

position = dict(x=0, y=0)

def boom(dt):
    explosion.play()

def update(dt):
    print(dt) # time elapsed since last time we were called
    position['x'] += 1
    position['y'] += 1

    if keyboard[key.RIGHT]:
        position['x'] += 4
    if keyboard[key.UP]:
        position['y'] += 4
    if keyboard[key.DOWN]:
        position['y'] -= 4
    if keyboard[key.LEFT]:
        position['x'] -= 4

@window.event
def on_draw():
    window.clear()
    image.blit(position['x'], position['y'])
  

@window.event
def on_mouse_press(x, y, button, modifiers):
  if button == mouse.LEFT:
    position['x'] = x
    position['y'] = y



pyglet.clock.schedule_interval(update, 1.0/60.0) # cause a timed event as fast as you can!
pyglet.clock.schedule_interval(boom, 1.0)

@window.event
def on_close():
    if keyboard[key.UP]: # Só irá fechar a tela se o ESC que é a tecla padrão para sair for apertada junto com a tecla UP
        pass
    else:
        return pyglet.event.EVENT_HANDLED

pyglet.app.run()