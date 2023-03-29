import glm
from modules.light import Light
from modules.model import CompanionCube



class Scene:
    def __init__(self, engine) -> None:
        self._engine = engine
        self._gl_context = engine.gl_context
        self._camera = engine.camera
        self._light = self.get_default_light()
        self._models = []
        
    @property # TODO types
    def models(self):
        return self._models
    
    @property # TODO types
    def light(self):
        return self._light
    
    # TODO types  
    def get_default_light(self):
        light = Light()
        return light
    
    def set_models(self, models) -> None:
        self._models = models
        
    def add_model(self, model, shader_name) -> None:
        self._models.append((model, shader_name))
        
    def load_uniform(self, model_index, attribute, data) -> None:
        shader_program = self._models[model_index].shader_program
        if type(data) == float or int:
            shader_program[attribute] = (data) 
        else:   
            shader_program[attribute].write(data)
        
    def load_textures(self) -> None:
        for model in self._models:
            model.use_textures()
            
    def load_projection_matrix(self) -> None:
        for model in self._models:
            shader_program = model.shader_program
            shader_program['projection_matrix'].write(self._camera.projection_matrix)
    
    def load_view_matrix(self) -> None:
        for model in self._models:
            shader_program = model.shader_program
            shader_program['view_matrix'].write(self._camera.view_matrix)
            
    def load_model_matrix(self) -> None:
        for model in self._models:
            shader_program = model.shader_program
            shader_program['model_matrix'].write(model.model_matrix)
        
    def set_light(self, light) -> None:
        self._light = light
    
    def render(self) -> None:
        for model in self._models:
            self.load_model_matrix()
            self.load_view_matrix()
            model.render()
            
    def destroy(self) -> None:
        for model in self._models:
            model.destroy()           
            

class CompanionCubeScene(Scene):
    def __init__(self, engine) -> None:
        super().__init__(engine)
        # model
        self._models = [CompanionCube(engine)]
        # light
        self.load_uniform(0, 'light.position', self.light._position)
        self.load_uniform(0, 'light.color', self.light._color)
        self.load_uniform(0, 'light.ambient_intensity', self.light._ambient_intensity)
        self.load_uniform(0, 'light.diffuse_intensity', self.light._diffuse_intensity)
        self.load_uniform(0, 'light.specular_intensity', self.light._specular_intensity)
        self.load_uniform(0, 'surface_brightness', self._models[0].material)
        # texture
        self.load_uniform(0, 'utexture_0', 0)
        self.load_textures()
        # send transformation matrices to the CPU
        self.load_model_matrix()
        self.load_view_matrix()
        self.load_projection_matrix()
        
        
    def render(self) -> None:
        rotation = glm.rotate(0.02, glm.vec3(0, 1, 0))
        for model in self._models:
            model.transform(rotation)
            self.load_model_matrix()
            self.load_view_matrix()
            self.load_uniform(0, 'camera_position', self._engine.camera.position)
            model.render()



        
        