import moderngl
import modules.glmath as glmath
from typing import Any
from modules.light import Light
from modules.model import (
    Model, 
    CompanionCubeModel,
    TexturedCubeModel,
    WoodenBoxModel, 
    MetalBoxModel,
    GoldenBoxModel,
    ColoredCubeModel, 
    WireCubeModel)



class Scene:
    def __init__(self, engine) -> None:
        self._engine = engine
        self._gl_context = engine.gl_context
        self._camera = engine.camera
        self._light: Light = None
        self._models: list[Model] = []
        
    @property
    def models(self) -> list[Model]:
        return self._models
    
    @property
    def light(self) -> Light:
        return self._light
    
    def set_default_light(self) -> Light:
        return Light()
    
    def set_models(self, models: list[Model]) -> None:
        self._models = models
        
    def add_model(self, model: Model, shader_name: str) -> None:
        self._models.append((model, shader_name))
        
    def load_uniform(self, model_index: int, attribute: str, data: Any) -> None:
        shader_program = self._models[model_index].shader_program
        if type(data) == float or type(data) == int:
            shader_program[attribute] = (data) 
        else:   
            shader_program[attribute].write(data)
            
    def load_projection_matrices(self) -> None:
        for model in self._models:
            shader_program = model.shader_program
            shader_program['projection_matrix'].write(self._camera.projection_matrix)
    
    def load_view_matrices(self) -> None:
        for model in self._models:
            shader_program = model.shader_program
            shader_program['view_matrix'].write(self._camera.view_matrix)
            
    def load_model_matrices(self) -> None:
        for model in self._models:
            shader_program = model.shader_program
            shader_program['model_matrix'].write(model.model_matrix)
        
    def set_light(self, light: Light) -> None:
        self._light = light
    
    def render(self) -> None:
        for model in self._models:
            self.load_model_matrices()
            self.load_view_matrices()
            model.render(mode = moderngl.TRIANGLES)
            
    def destroy(self) -> None:
        for model in self._models:
            model.destroy()          

        
class TestCube(Scene):
    def __init__(self, engine) -> None:
        super().__init__(engine)
        # model
        self._models = [ColoredCubeModel(engine), WireCubeModel(engine)]
        # send transformation matrices to the CPU
        self.load_model_matrices()
        self.load_view_matrices()
        self.load_projection_matrices()
            
    def render(self) -> None:
        rotation = glmath.rotate(0.02, glmath.vec3f(0, 1, 0))
        self._models[0].transform(rotation)
        self._models[1].transform(rotation)
        self.load_model_matrices()
        self.load_view_matrices()
        self._models[0].render()
        self._models[1].render(moderngl.LINE_STRIP)
            

class CompanionCube(Scene):
    def __init__(self, engine) -> None:
        super().__init__(engine)
        # model
        self._models = [CompanionCubeModel(engine)]
        # light
        self._light = self.set_default_light()
        self.load_uniform(0, 'light.position', self.light._position)
        self.load_uniform(0, 'light.color', self.light._color)
        self.load_uniform(0, 'light.ambient_intensity', self.light._ambient_intensity)
        self.load_uniform(0, 'light.diffuse_intensity', self.light._diffuse_intensity)
        self.load_uniform(0, 'light.specular_intensity', self.light._specular_intensity)
        self.load_uniform(0, 'surface_brightness', self._models[0].material)
        # texture
        self.load_uniform(0, 'utexture', 0)
        # send transformation matrices to the CPU
        self.load_model_matrices()
        self.load_view_matrices()
        self.load_projection_matrices()
        
    def render(self) -> None:
        rotation = glmath.rotate(0.02, glmath.vec3f(0, 1, 0))
        for model in self._models:
            model.transform(rotation)
            self.load_model_matrices()
            self.load_view_matrices()
            self.load_uniform(0, 'camera_position', self._engine.camera.position)
            model.render()
       
            
class TestingField(Scene):
    def __init__(self, engine) -> None:
        super().__init__(engine)
        # model
        self._models = [CompanionCubeModel(engine),
                        GoldenBoxModel(engine, position = (-3.5, 0, 0)),
                        WoodenBoxModel(engine, position = (3.5, 0, 0)),
                        MetalBoxModel(engine, position = (-3.5, 3.5, 0)),
                        TexturedCubeModel(engine, position = (0, 3.5, 0)),
                        TexturedCubeModel(engine, position = (3.5, 3.5, 0))]
        # light
        self._light = self.set_default_light()
        self._light.set_position((-5, 3, 9))
        # camera
        self._engine.camera.set_position((0, 2, 9))
        # textures
        self._models[4].material.set_default_material('pearl')
        self._models[5].material.set_default_material('yellow_plastic')
        # uniforms
        for i in range(0, len(self._models)):
            self.load_uniform(i, 'light.position', self.light._position)
            self.load_uniform(i, 'light.color', self.light._color)
            self.load_uniform(i, 'light.ambient_intensity', self.light._ambient_intensity)
            self.load_uniform(i, 'light.diffuse_intensity', self.light._diffuse_intensity)
            self.load_uniform(i, 'light.specular_intensity', self.light._specular_intensity)
            self.load_uniform(i, 'material.surface_brightness', self._models[i].material.surface_brightness)
            self.load_uniform(i, 'material.ambient_incidence', self._models[i].material.ambient_incidence)
            self.load_uniform(i, 'material.diffuse_incidence', self._models[i].material.diffuse_incidence)
            self.load_uniform(i, 'material.specular_incidence', self._models[i].material.specular_incidence)
            self.load_uniform(i, 'utexture', 0)
        # send transformation matrices to the CPU
        self.load_model_matrices()
        self.load_view_matrices()
        self.load_projection_matrices()
        
    def render(self) -> None:
        rotation = glmath.rotate(0.02, glmath.vec3f(0, 1, 0))
        self.load_model_matrices()
        self.load_view_matrices()
        for i in range(0, len(self._models)):
            self._models[i].transform(rotation)
            self.load_uniform(i, 'camera_position', self._engine.camera.position)
            self._models[i].render()
            



        
        