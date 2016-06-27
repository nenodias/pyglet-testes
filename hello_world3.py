import pyglet

window = pyglet.window.Window()
label = pyglet.text.Label('Hello, world', x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

@window.event
def on_draw():
    window.clear()
    label.x += 1
    label.y += 1
    label.draw()

pyglet.app.run()