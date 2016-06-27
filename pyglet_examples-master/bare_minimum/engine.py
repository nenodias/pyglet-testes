from collections import namedtuple
import weakref

import pyglet


WindowState = namedtuple('WindowState', ['keys', 'window', 'game'])


class GameWindow(pyglet.window.Window):
    """Slight modifications to pyglet.window.Window to easily show frame rate
    and swap out the function that renders the scene
    """

    def __init__(self, show_fps=True, *args, **kwargs):
        super(GameWindow, self).__init__(*args, **kwargs)
        self.show_fps = show_fps
        self.fps_display = pyglet.window.FPSDisplay(self)
        self.draw_func = lambda dt: None

    def on_draw(self, dt=0):
        self.clear()
        self.draw_func(dt)
        if self.show_fps:
            self.fps_display.draw()

    def on_key_press(self, symbol, modifiers):
        # Override default behavior of escape key quitting
        if symbol == pyglet.window.key.ESCAPE:
            return pyglet.event.EVENT_HANDLED


class Game(object):
    """Track and control game state at the user interface flow level"""

    def __init__(self, first_scene_class, name, size, fullscreen=False):
        super(Game, self).__init__()

        self.window = GameWindow(fullscreen=fullscreen,
                                 width=size[0], height=size[1])
        self.window.set_caption(name)

        self.keys = pyglet.window.key.KeyStateHandler()
        self.window.push_handlers(self.keys)

        self.scene_stack = []
        self.window_state = WindowState(self.keys, self.window,
                                        weakref.ref(self)())
        self.push_scene(first_scene_class(self.window_state))

    def begin(self):
        pyglet.clock.schedule_interval(self.window.on_draw, 1/72.0)

    def push_scene(self, scene):
        self.window.draw_func = scene.draw

        if self.scene_stack:
            pyglet.clock.unschedule(self.scene_stack[-1].update)

        self.window.pop_handlers()

        self.scene_stack.append(scene)
        self.window.push_handlers(scene)
        pyglet.clock.schedule_interval(scene.update, 1/72.0)

    def pop_scene(self):
        self.window.pop_handlers()

        pyglet.clock.unschedule(self.scene_stack[-1].update)

        self.scene_stack = self.scene_stack[:-1]

        if self.scene_stack:
            scene = self.scene_stack[-1]
            self.window.push_handlers(scene)
            pyglet.clock.schedule_interval(scene.update, 1/72.0)
            self.window.draw_func = scene.draw


class Scene(object):
    """Render and handle events for a single view such as a menu screen or the
    main game
    """

    def __init__(self, window_state=None):
        self.window_state = window_state

        # background objects
        self.bg_batch = pyglet.graphics.Batch()

        # playable objects
        self.object_batch = pyglet.graphics.Batch()

        # objects that don't move and are drawn in the front (HUD, score, etc)
        self.status_batch = pyglet.graphics.Batch()

        # overwrite this in your subclass if you want to add more batches
        self.batches = (self.bg_batch, self.object_batch, self.status_batch)

    def update(self, dt):
        """Called many times per second (default 72). Put real-time update
        logic here.

        :param dt: seconds since last call (usually about 0.014)
        """
        pass

    def draw(self, dt):
        """Render the scene. In general you should attach things to the batches
        rather than modify this method.
        """
        for batch in self.batches:
            batch.draw()


class TextScene(Scene):

    text = '???'
    size = 48
    font_name = None
    color = (255, 255, 255, 255)

    def __init__(self, *args, **kwargs):
        super(TextScene, self).__init__(*args, **kwargs)

        # add a simple label to the object batch, taking visible values from
        # class variables
        self.title_label = pyglet.text.Label(
            text=self.text,
            x=self.window_state.window.width/2,
            y=self.window_state.window.height/2,
            width=self.window_state.window.width,
            font_size=self.size,
            font_name=self.font_name,
            anchor_x='center',
            anchor_y='center',
            color=self.color,
            batch=self.object_batch,
        )
