import pyglet
from pyglet.window import key, mouse

#Frame counter
fps_display = pyglet.clock.ClockDisplay()

# Right way to load a resource
#data_file = pyglet.resource.file('file.txt')

window = pyglet.window.Window()

keyboard = key.KeyStateHandler()
window.push_handlers(keyboard)

batch = pyglet.graphics.Batch()

sprite_image = pyglet.resource.image('exemplo.png')
sprite_image.anchor_x = sprite_image.width // 2
sprite_image.anchor_y = sprite_image.height // 2

# Criando camadas para agrupar imagens
background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)

# Adicionando imagem de fundo
sprite_fundo = pyglet.resource.image('fundo.png')
fundo = pyglet.sprite.Sprite(sprite_fundo, 0, 0, batch=batch, group=background)

list_images = []


list_images.append(pyglet.sprite.Sprite(sprite_image, sprite_image.width // 2, sprite_image.height // 2, batch=batch, group=foreground))


explosion = pyglet.resource.media('explosion.wav', streaming=False)
print(dir(explosion))

'''
Para utilizar músicas com formato mp3/ogg é necessário instalar o AVIBin
Link: http://avbin.github.io/AVbin/Download.html


pyglet.lib.load_library('avbin')
pyglet.have_avbin=True

music = pyglet.resource.media('another_brick_the_wall.ogg')
'''
pyglet.options['audio'] = ('openal', 'pulse', 'silent')# bugfix para Linux
music = pyglet.resource.media('another_brick_the_wall.wav')
player = pyglet.media.Player()
player.queue(music)
player.play()


position = dict(x=0, y=0)

def boom(dt):
    explosion.play()

def update(dt):
    #print(dt) # time elapsed since last time we were called
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

    # Updating image position
    for image in list_images:
        image.x, image.y = position['x'], position['y']

@window.event
def on_draw():
    window.clear()
    batch.draw()
    fps_display.draw()
  

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
        player.pause()
        pass
    else:
        return pyglet.event.EVENT_HANDLED

pyglet.app.run()