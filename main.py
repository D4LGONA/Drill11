from pico2d import open_canvas, delay
import play_mode

open_canvas()
play_mode.init()
# game loop
while play_mode.running:
    play_mode.handle_events()
    play_mode.update()
    play_mode.draw()
    delay(0.01)
# finalization code
play_mode.finish()
#close_canvas()