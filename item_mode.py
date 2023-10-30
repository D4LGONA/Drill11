import pico2d
#from pico2d import load_image, clear_canvas, update_canvas, get_events, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE
import game_framework
import game_world
import play_mode
from pannel import Pannel


def init():
    global  pannel
    pannel = Pannel()
    game_world.add_object(pannel, 3)
    pass

def finish():
    game_world.remove_object(pannel)
    pass

def update():
    game_world.update()
    pass

def draw():
    pico2d.clear_canvas()
    game_world.render()
    pico2d.update_canvas()
    pass

def handle_events():
    events = pico2d.get_events()
    for event in events:
        if event.type == pico2d.SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (pico2d.SDL_KEYDOWN, pico2d.SDLK_SPACE):
            game_framework.change_mode(play_mode)
        elif event.type == pico2d.SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_ESCAPE:
                    game_framework.pop_mode()
                case pico2d.SDLK_0:
                    play_mode.boy.item = None
                    game_framework.pop_mode()
                case pico2d.SDLK_1:
                    play_mode.boy.item = 'Ball'
                    game_framework.pop_mode()
                case pico2d.SDLK_2:
                    play_mode.boy.item = 'Bigball'
                    game_framework.pop_mode()

    pass

