import pyglet

window = pyglet.window.Window()
label = pyglet.text.Label('Hello, world', x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

def update(dt):
    print(dt) # time elapsed since last time we were called
    label.x += 1
    label.y += 1
    if label.x > window.width:
        label.x = 0
    if label.y > window.height:
        label.y = 0

@window.event
def on_draw():
    window.clear()
    label.draw()

#pyglet.clock.schedule(update) # cause a timed event as fast as you can!
pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()