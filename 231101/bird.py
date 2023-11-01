# 이것은 각 상태들을 객체로 구현한 것임.
# 내 새는 1.5미터 * 1.5미터짜리 새로 할래요 -> 50px * 50px 새 인거죠
# 한시간에 30km 가자

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 30
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

#Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 14
FRAMES_PER_TIME = ACTION_PER_TIME * FRAMES_PER_ACTION

from pico2d import get_time, load_image, load_font, clamp,  SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT
from ball import Ball, BigBall
import game_world
import game_framework
from random import *

# state event check
# ( state event type, event value )


class Run:
    @staticmethod
    def enter(bird, e):
        bird.dir, bird.action, bird.face_dir = 1, 1, 1
        bird.dir, bird.action, bird.face_dir = -1, 0, -1

    @staticmethod
    def exit(bird, e):
        pass

    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAMES_PER_TIME * game_framework.frame_time) % 14
        if int(bird.frame) < 5:
            bird.action = 2
        elif int(bird.frame) < 10:
            bird.action = 1
        else:
            bird.action = 0

        bird.x += bird.dir * RUN_SPEED_PPS * game_framework.frame_time

        if (bird.x <= 25):
            bird.dir = 1
            bird.face_dir = 1
        if (bird.x >= 1575):
            bird.dir = -1
            bird.face_dir = -1
        #bird.x = clamp(25, bird.x, 1600-25)


    @staticmethod
    def draw(bird):
        if(bird.dir == 1):
            bird.image.clip_composite_draw((int(bird.frame) % 5) * 180, bird.action * 170, 180, 170, 0, 'n', bird.x, bird.y, 50, 50)
        else:
            bird.image.clip_composite_draw((int(bird.frame) % 5) * 180, bird.action * 170, 180, 170, 0, 'h', bird.x, bird.y,
                                           50, 50)

class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state = Run
        self.transitions = {}

    def start(self):
        self.cur_state.enter(self.boy, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.boy)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.boy, e)
                self.cur_state = next_state
                self.cur_state.enter(self.boy, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.boy)


class Bird:
    def __init__(self):
        self.x, self.y = randint(200, 600), randint(300, 500)
        self.frame = 0
        self.action = 0
        self.face_dir = 1
        self.dir = -1
        self.image = load_image('bird_animation.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
