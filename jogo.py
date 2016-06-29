import pyglet
from pyglet.window import key, mouse

fps_display = pyglet.clock.ClockDisplay()
window = pyglet.window.Window()

keyboard = key.KeyStateHandler()
window.push_handlers(keyboard)

batch_draw = pyglet.graphics.Batch()

sprite_image = pyglet.resource.image('snake.png')

# Criando camadas para agrupar imagens
background = pyglet.graphics.OrderedGroup(0)
tiles = pyglet.graphics.OrderedGroup(1)
foreground = pyglet.graphics.OrderedGroup(2)

sprite_fundo = pyglet.resource.image('fundo.png')
fundo = pyglet.sprite.Sprite(sprite_fundo, 0, 0, batch=batch_draw, group=background)

blocos = []

#Desenhando GRID
for j in range(15):
    for i in range(20):
        box_image = pyglet.resource.image('box.png')
        x = int( 32.0 * i )
        y = int( 32.0 * j )
        blocos.append( pyglet.sprite.Sprite(box_image, x, y, batch=batch_draw, group=tiles) )

list_images = []

snake_parts = []

snake_parts.append( pyglet.sprite.Sprite(sprite_image, 8*32, 8*32, batch=batch_draw, group=foreground) )

position = dict(x=0, y=0)
direction = None
acelerate = 0
insert = False

def atualizar_snake(direction, snake_parts):
    global insert
    last = None
    tamanho = len(snake_parts)
    old = None
    for index in range(tamanho):
        snake = snake_parts[index]
        if index == 0:
            old = (snake.x, snake.y)
            if direction == key.RIGHT:
                snake.x += 32
            if direction == key.UP:
                snake.y += 32
            if direction == key.DOWN:
                snake.y -= 32
            if direction == key.LEFT:
                snake.x -= 32
        else:
            aux = (snake.x, snake.y)
            snake.x, snake.y = old[0], old[1]
            old = aux
    if insert:
        snake_parts.append( pyglet.sprite.Sprite(sprite_image, old[0], old[1], batch=batch_draw, group=foreground) )
        insert = False

def update(dt):
    #print(dt) # time elapsed since last time we were called
    global acelerate
    global direction
    global snake_parts
    global insert

    # adicionar nova parte de cobra
    if acelerate >= 9 and keyboard[key.SPACE] and direction:
        insert = True
        

    acelerate += 1
    if acelerate >= 10:
        acelerate = 0
        atualizar_snake( direction, snake_parts)


    if keyboard[key.RIGHT]:
        direction = key.RIGHT
    if keyboard[key.UP]:
        direction = key.UP
    if keyboard[key.DOWN]:
        direction = key.DOWN
    if keyboard[key.LEFT]:
        direction = key.LEFT


@window.event
def on_draw():
    window.clear()
    batch_draw.draw()
    fps_display.draw()


pyglet.clock.schedule_interval(update, 1.0/60.0)
pyglet.app.run()