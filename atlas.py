import pyglet

# Create and open a window
window = pyglet.window.Window(200, 200)

# Create a static sprite
sprite = pyglet.resource.image('assassin_sheet.png')
static = False # Show or Not a static sheet

# Cut our cat up into a 5x5 grid of images to move through (sprite sheet)
raw = pyglet.image.load('assassin_sheet.png')
raw_seq = pyglet.image.ImageGrid(raw, 2, 4)
anim = pyglet.image.Animation.from_image_sequence(raw_seq, 0.1, True)
sprite2 = pyglet.sprite.Sprite(anim)

@window.event
def on_draw():
  window.clear()
  if static:
    sprite.blit(25, 25, width=150, height=150)
  sprite2.draw()

if __name__ == '__main__':
  pyglet.app.run()