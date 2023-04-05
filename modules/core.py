import sys
import dearpygui.dearpygui as dpg
import pygame as pg
import pygame.time as pgtime
import pygame.event as pgevent
import pygame.mouse as pgmouse
import moderngl
from typing import Any
from modules.camera import Camera
from modules.scene import Scene





class GLEngine:
    def __init__(self, win_size: tuple[int, int] = (1280, 720), 
                 fps: int = 60, 
                 debug: bool = False, 
                 mouse_controls: bool = False, 
                 cull_face: bool = True,
                 wire_mode: bool = False) -> None:
        
        self._allow_debug_mode = debug
        self._allow_wire_mode = wire_mode
        self._allow_cull_face = cull_face
        self._allow_mouse_controls = mouse_controls
        self._fps = fps
        # init pygame window
        pg.init()
        self._WIN_SIZE = win_size
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 4)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 1)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        # create OpenGL context
        pg.display.set_mode(self._WIN_SIZE, flags = pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)
        # keeps track of time
        self._clock = pgtime.Clock()
        self._time = 0
        self._delta_time = 0
        # keyboard event handler
        self._keys_state = {int : bool}
        # detect and use existing OpenGL context
        self._gl_context = moderngl.create_context()
        if self._allow_cull_face :
            self.gl_context.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE | moderngl.PROGRAM_POINT_SIZE)
        else : 
            self.gl_context.enable_only(moderngl.DEPTH_TEST | moderngl.PROGRAM_POINT_SIZE)
        # mouse settings
        pgmouse.set_visible(False)
        pgevent.set_grab(self._allow_mouse_controls)
        # background color
        self._gl_context.clear(color=(0.9, 0.8, 0.01)) # "The fact that gold exists makes every other colours equally inferior."
        # camera
        self._camera = Camera(self)
        # scene
        self._scenes: list[Scene] = []
        
        # debug window
        if self._allow_debug_mode:
            DebugWindow(self)
            dpg.show_viewport()

    @property
    def gl_context(self) -> moderngl.Context:
        return self._gl_context

    @property
    def win_size(self) -> tuple[int, int]:
        return self._WIN_SIZE
    
    @property
    def camera(self) -> Camera:
        return self._camera
    
    @property
    def time(self) -> float:
        return self._time
    
    @property
    def debug(self) -> bool:
        return self._allow_debug_mode
    
    @property 
    def scenes(self) -> list[Scene | Any]:
        for scene in self._scenes:
            yield scene
    
    def set_camera(self, camera: Camera) -> None:
        self._camera = camera
        
    def set_default_camera(self) -> None:
        self._camera.set_default_camera()

    def set_scenes(self, scenes: list[Scene]) -> None:
        self._scenes = scenes
        
    # main loop
    def run(self) -> None:
        while True:
            self.event_handler()
            self.render()
            self._delta_time = self._clock.tick(self._fps)
            self.update_time()

    def render(self) -> None:
        # clear the framebuffer
        self._gl_context.clear(color=(0.9, 0.8, 0.01)) # "The fact that gold exists makes every other colours equally inferior." Big E.
        # render the scene
        for scene in self._scenes:
            scene.render()
        # swap buffers
        pg.display.flip()
        # dgp
        if self._allow_debug_mode and dpg.is_dearpygui_running():
            dpg.render_dearpygui_frame()
    
    def event_handler(self) -> None:
        self.on_key_hold()
        self.on_mouse_motion()
        for event in pgevent.get():
            if event.type == pg.QUIT:
                self.on_close()
            elif event.type == pg.KEYDOWN:
                self.on_key_press(event.key)

    def on_key_press(self, symbol: int) -> None:
        # options 
        # esc : quit 
        if symbol == pg.K_ESCAPE:
            self.on_close()
        # j : activate / deactivate debug mode
        if symbol == pg.K_j:
            self._allow_debug_mode = not self._allow_debug_mode
            debug_state = 'activated' if self._allow_debug_mode else 'deactivated'
            print(f'debug mode {debug_state}')   
        # k : activate / deactivate wire mode
        if symbol == pg.K_k:
            self._allow_wire_mode = not self._allow_wire_mode
            self._gl_context.wireframe = self._allow_wire_mode
            if self._allow_debug_mode:
                wire_mode_state = 'activated' if self._allow_wire_mode else 'deactivated'
                print(f'wire mode {wire_mode_state}')
        # r : reset camera and models to default position
        if symbol == pg.K_r:
            self._camera.reset_camera()
            if self._allow_debug_mode:
                print(f'camera reset to {self._camera._default_position}')
        # l : look at the scene being rendered
        if symbol == pg.K_l:
            self._camera.look_at_scene()
        # m : allow / disable mouse camera controls
        if symbol == pg.K_m:
            self._allow_mouse_controls = not self._allow_mouse_controls
            pgevent.set_grab(self._allow_mouse_controls)
            if self._allow_debug_mode:
                mouse_controls_state = 'activated' if self._allow_mouse_controls else 'deactivated'
                print(f'camera controls with mouse {mouse_controls_state}')
        
    def on_key_hold(self) -> None:
        keys = pg.key.get_pressed()
        # move controls
        if keys[pg.K_z]:
            self._camera.move("forward", self._delta_time)
        if keys[pg.K_s]:
            self._camera.move("backward", self._delta_time)
        if keys[pg.K_q]:
            self._camera.move("straf_left", self._delta_time)
        if keys[pg.K_d]:
            self._camera.move("straf_right", self._delta_time)
        if keys[pg.K_a]:
            self._camera.move("straf_up", self._delta_time)
        if keys[pg.K_e]:
            self._camera.move("straf_down", self._delta_time)
        if keys[pg.K_RIGHT]:
            self._camera.move("right", self._delta_time)
        if keys[pg.K_LEFT]:
            self._camera.move("left", self._delta_time)
        if keys[pg.K_UP]:
            self._camera.move("up", self._delta_time)
        if keys[pg.K_DOWN]:
            self._camera.move("down", self._delta_time)
            
    def on_mouse_motion(self) -> None:
        x, y = pgmouse.get_pos()
        dx, dy = pgmouse.get_rel()
        if self._allow_mouse_controls == True :
            self._camera.rotate(x, y, dx, dy)
            
    def update_time(self) -> None:
        self._time += self._delta_time

    def on_close(self) -> None:
        for scene in self._scenes:
            scene.destroy()
        dpg.destroy_context()
        pg.quit()
        sys.exit()


class DebugWindow:
    def __init__(self, engine: GLEngine) -> None:
        self._camera = engine.camera
        
        dpg.create_context()
        dpg.create_viewport(title = "Debug window", width = 500, height = 350)
        dpg.setup_dearpygui()
        
        with dpg.window(label = "Camera", autosize = True):
            dpg.add_slider_int(label = "X", 
                               default_value = int(self._camera.position.x), 
                               min_value = -5, 
                               max_value = 5, 
                               callback = self.set_camera_position)
            dpg.add_slider_int(label = "Y", 
                               default_value = int(self._camera.position.y), 
                               min_value = -5, 
                               max_value = 5, 
                               callback = self.set_camera_position)
            dpg.add_slider_int(label = "Z", 
                               default_value = int(self._camera.position.z), 
                               min_value = -5, 
                               max_value = 15, 
                               callback = self.set_camera_position)
    
    def set_camera_position(self, sender, value) -> None:
        axe = dpg.get_item_label(sender)
        if axe == 'X':
            self._camera.move_to_position((value,
                                           self._camera.position.y, 
                                           self._camera.position.z))
        elif axe == 'Y':
            self._camera.move_to_position((self._camera.position.x,
                                           value, 
                                           self._camera.position.z))
        elif axe == 'Z':
            self._camera.move_to_position((self._camera.position.x,
                                           self._camera.position.y, 
                                           value))
