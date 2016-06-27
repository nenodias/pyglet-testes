import argparse

import pyglet
from pyglet.window import key

import engine
import gamescene


class MenuScene(engine.TextScene):

    text = 'This Is The Menu, Press Return'

    def on_key_press(self, symbol, modifiers):
        if symbol == key.RETURN:
            new_scene = gamescene.GameScene(self.window_state)
            self.window_state.game.push_scene(new_scene)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--fullscreen', action='store_true',
                        help='Run the game in fullscreen mode')
    args = parser.parse_args()

    g = engine.Game(MenuScene, 'Skeleton', (1024, 768),
                    fullscreen=args.fullscreen)
    g.begin()
    pyglet.app.run()
