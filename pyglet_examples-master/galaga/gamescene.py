import weakref

import pyglet
from pyglet.window import key

import engine


PLAYER_SPEED = 300
BULLET_SPEED = 400
BASE_BULLET_SPACING = 0.6


def constrain_range(minimum, maximum):

    def constrain_func(val):
        if val < minimum:
            return minimum
        if val > maximum:
            return maximum
        return val

    return constrain_func


class Object(object):

    IMAGE_NAME = None

    def __init__(self, x, y, scene):
        super(Object, self).__init__()
        self.sprite = pyglet.sprite.Sprite(scene.res(self.IMAGE_NAME), x=x, y=y,
                                           batch=scene.object_batch)
        self.dead = False
        self.new_objects = False
        self.scene = scene

    def update(self, dt):
        pass


class Player(Object):

    IMAGE_NAME = 'spaxesheep'

    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        half_width = self.sprite.image.width/2
        self.constrain_x = constrain_range(half_width,
                                           self.scene.width - half_width)

    def update(self, dt):
        if self.scene.key(key.LEFT) != self.scene.key(key.RIGHT):
            direction = -1 if self.scene.key(key.LEFT) else 1
            self.sprite.x += dt * PLAYER_SPEED * direction

        self.sprite.x = self.constrain_x(self.sprite.x)


class Bullet(Object):

    IMAGE_NAME = 'lazor'

    def update(self, dt):
        self.sprite.y += dt * BULLET_SPEED
        if self.sprite.y > self.scene.height + 20:
            self.dead = True


class GameScene(engine.Scene):

    def __init__(self, ws):
        super(GameScene, self).__init__(ws)

        self.weakref = weakref.ref(self)
        self.objects = set()
        self.player = Player(self.width/2, 32, self.weakref())
        self.objects.add(self.player)
        self.firing = False
        self.can_fire = True

    def add_object(self, cls, x, y):
        self.objects.add(cls(x, y, self.weakref()))

    def update(self, dt):
        dead = set()
        for obj in self.objects:
            obj.update(dt)
            if obj.dead:
                dead.add(obj)

        for obj in dead:
            self.objects.remove(obj)

    def _fire_on_schedule(self, dt=0):
        if self.firing:
            self.can_fire = False
            self.add_object(Bullet, self.player.sprite.x,
                            self.player.sprite.y + 22)
            pyglet.clock.schedule_once(self._fire_on_schedule,
                                       BASE_BULLET_SPACING)
        else:
            self.can_fire = True

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.window_state.game.pop_scene()
            return True

        if symbol == key.SPACE:
            self.firing = True
            if self.can_fire:
                self.add_object(Bullet, self.player.sprite.x,
                                self.player.sprite.y + 22)
                self.can_fire = False
                pyglet.clock.schedule_once(self._fire_on_schedule,
                                           BASE_BULLET_SPACING)

    def on_key_release(self, symbol, modifiers):
        if symbol == key.SPACE:
            self.firing = False
