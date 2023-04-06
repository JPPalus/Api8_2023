from modules.mesh import SolidCubeMesh, WireCubeMesh, TexturedCubeMesh
import modules.glmath as glmath
import pygame.image as pgimage
import numpy as np
import moderngl



class Texture:
    def __init__(self, context: moderngl.Context, path: str) -> None:
        self._gl_context = context
        self._texture = self.get_texture(path)
        
    def get_texture(self, path: str) -> moderngl.Texture:
        raw_pic = pgimage.load(path).convert()
        size = raw_pic.get_size()
        texture_data = pgimage.tostring(raw_pic, 'RGB')
        texture = self._gl_context.texture(size = size, 
                                           components = 3, 
                                           data = texture_data)
        return texture
    
    def use(self) -> None:
        self._texture.use()
    
    def destroy(self) -> None:
        self._texture.release()
        
        
class Material:
    def __init__(self, 
                 surface_brightness: float = None, 
                 ambient_incidence: tuple[float, float, float] = None,
                 diffuse_incidence: tuple[float, float, float] = None,
                 specular_incidence: tuple[float, float, float] = None,
                 name: str = None) -> None:
        
        if name:
            self.set_default_material(name)
        else:
            self.set_default_material()
        if surface_brightness:   
            self._surface_brightness = surface_brightness
        if ambient_incidence: 
            self._ambient_incidence = glmath.vec3f(ambient_incidence)
        if diffuse_incidence:
            self._diffuse_incidence = glmath.vec3f(diffuse_incidence)
        if specular_incidence:
            self._specular_incidence = glmath.vec3f(specular_incidence)
        
    @property
    def surface_brightness(self) -> float:
        return self._surface_brightness
    
    @property
    def ambient_incidence(self) -> glmath.vec3f:
        return self._ambient_incidence
    
    @property
    def diffuse_incidence(self) -> glmath.vec3f:
        return self._diffuse_incidence
    
    @property
    def specular_incidence(self) -> glmath.vec3f:
        return self._specular_incidence
    
    @surface_brightness.setter
    def surface_brightness(self, brightness: float) -> None:
        self._surface_brightness = brightness
        
    @ambient_incidence.setter
    def ambient_incidence(self, ambient_incidence: tuple[float, float, float]) -> None:
        self._ambient_incidence = glmath.vec3f(ambient_incidence)
        
    @diffuse_incidence.setter
    def diffuse_incidence(self, diffuse_incidence: tuple[float, float, float]) -> None:
        self._diffuse_incidence = glmath.vec3f(diffuse_incidence)
        
    @specular_incidence.setter
    def specular_incidence(self, specular_incidence: tuple[float, float, float]) -> None:
        self._specular_incidence = glmath.vec3f(specular_incidence)
    
    # numbers come from :
    # teapots.c, Silicon Graphics 1994, Mark J. Kilgard
    # Distinguished Professor Emeritus Charles (Chuck) Hansen personnal (dead) webpage
    # Børre Stenseth former former (dead) webpage
    def set_default_material(self, material: str = 'basic') -> None:
        # spam
        if material == 'basic':
            self._surface_brightness = 42.0
            self._ambient_incidence = glmath.vec3f((1, 1, 1))
            self._diffuse_incidence = glmath.vec3f((1, 1, 1))
            self._specular_incidence = glmath.vec3f((1, 1, 1))
        # metals
        elif material == 'brass':
            self._surface_brightness = 27.8974
            self._ambient_incidence = glmath.vec3f((0.329412, 0.223529, 0.027451))
            self._diffuse_incidence = glmath.vec3f((0.780392, 0.568627, 0.113725))
            self._specular_incidence = glmath.vec3f((0.992157, 0.941176, 0.807843))
        elif material == 'bronze':
            self._surface_brightness = 25.6
            self._ambient_incidence = glmath.vec3f((0.2125, 0.1275, 0.054))
            self._diffuse_incidence = glmath.vec3f((0.714, 0.4284, 0.18144))
            self._specular_incidence = glmath.vec3f((0.393548, 0.271906, 0.166721))
        elif material == 'polished_bronze':
            self._surface_brightness = 76.8
            self._ambient_incidence = glmath.vec3f((0.25, 0.148, 0.06475))
            self._diffuse_incidence = glmath.vec3f((0.4, 0.2368,  0.1036))
            self._specular_incidence = glmath.vec3f((0.774597, 0.458561, 0.200621))
        elif material == 'chrome':
            self._surface_brightness = 84.48
            self._ambient_incidence = glmath.vec3f((0.25, 0.25, 0.25))
            self._diffuse_incidence = glmath.vec3f((0.4, 0.4, 0.4))
            self._specular_incidence = glmath.vec3f((0.774597, 0.774597, 0.774597))
        elif material == 'copper':
            self._surface_brightness = 12.8
            self._ambient_incidence = glmath.vec3f((0.19125, 0.0735, 0.0225))
            self._diffuse_incidence = glmath.vec3f((0.7038, 0.27048, 0.0828))
            self._specular_incidence = glmath.vec3f((0.256777, 0.137622, 0.086014))
        elif material == 'polished_copper':
            self._surface_brightness = 51.2
            self._ambient_incidence = glmath.vec3f((0.2295, 0.08825, 0.0275))
            self._diffuse_incidence = glmath.vec3f((0.5508, 0.2118, 0.066))
            self._specular_incidence = glmath.vec3f((0.580594, 0.223257, 0.0695701))
        elif material == 'gold':
            self._surface_brightness = 51.2
            self._ambient_incidence = glmath.vec3f((0.24725, 0.1995, 0.0745))
            self._diffuse_incidence = glmath.vec3f((0.75164, 0.60648, 0.22648))
            self._specular_incidence = glmath.vec3f((0.628281, 0.555802, 0.366065))
        elif material == 'polished_gold':
            self._surface_brightness = 83.2
            self._ambient_incidence = glmath.vec3f((0.24725, 0.2245, 0.0645))
            self._diffuse_incidence = glmath.vec3f((0.34615, 0.3143, 0.0903))
            self._specular_incidence = glmath.vec3f((0.797357, 0.723991, 0.208006))
        elif material == 'pewter':
            self._surface_brightness = 9.84615
            self._ambient_incidence = glmath.vec3f((0.105882, 0.058824, 0.113725))
            self._diffuse_incidence = glmath.vec3f((0.427451, 0.470588, 0.541176))
            self._specular_incidence = glmath.vec3f((0.333333, 0.333333, 0.521569))
        elif material == 'silver':
            self._surface_brightness = 51.2
            self._ambient_incidence = glmath.vec3f((0.19225, 0.19225, 0.19225))
            self._diffuse_incidence = glmath.vec3f((0.50754, 0.50754, 0.50754))
            self._specular_incidence = glmath.vec3f((0.508273, 0.508273, 0.508273))
        elif material == 'polished_silver':
            self._surface_brightness = 89.6
            self._ambient_incidence = glmath.vec3f((0.23125, 0.23125, 0.23125))
            self._diffuse_incidence = glmath.vec3f((0.2775, 0.2775, 0.2775))
            self._specular_incidence = glmath.vec3f((0.773911, 0.773911, 0.773911))
        # gems
        elif material == 'emerald':
            self._surface_brightness = 76.8
            self._ambient_incidence = glmath.vec3f((0.0215, 0.1745, 0.0215))
            self._diffuse_incidence = glmath.vec3f((0.07568, 0.61424, 0.07568))
            self._specular_incidence = glmath.vec3f((0.633, 0.727811, 0.633))
        elif material == 'jade':
            self._surface_brightness = 12.8
            self._ambient_incidence = glmath.vec3f((0.135, 0.2225, 0.1575))
            self._diffuse_incidence = glmath.vec3f((0.54, 0.89, 0.63))
            self._specular_incidence = glmath.vec3f((0.316228, 0.316228, 0.316228))
        elif material == 'obsidian':
            self._surface_brightness = 38.4
            self._ambient_incidence = glmath.vec3f((0.05375, 0.05, 0.06625))
            self._diffuse_incidence = glmath.vec3f((0.18275, 0.17, 0.22525))
            self._specular_incidence = glmath.vec3f((0.332741, 0.328634, 0.346435))
        elif material == 'pearl':
            self._surface_brightness = 113.664
            self._ambient_incidence = glmath.vec3f((0.25, 0.20725, 0.20725))
            self._diffuse_incidence = glmath.vec3f((1.0, 0.829, 0.829))
            self._specular_incidence = glmath.vec3f((0.296648, 0.296648, 0.296648))
        elif material == 'ruby':
            self._surface_brightness = 76.8
            self._ambient_incidence = glmath.vec3f((0.1745, 0.01175, 0.01175))
            self._diffuse_incidence = glmath.vec3f((0.61424, 0.04136, 0.04136))
            self._specular_incidence = glmath.vec3f((0.727811, 0.626959, 0.626959))
        elif material == 'turquoise':
            self._surface_brightness = 12.8
            self._ambient_incidence = glmath.vec3f((0.1, 0.18725, 0.1745))
            self._diffuse_incidence = glmath.vec3f((0.396, 0.74151, 0.69102))
            self._specular_incidence = glmath.vec3f((0.297254, 0.30829, 0.306678))
        # artificial
        elif material == 'black_plastic':
            self._surface_brightness = 32.0
            self._ambient_incidence = glmath.vec3f((0.0, 0.0, 0.0))
            self._diffuse_incidence = glmath.vec3f((0.01, 0.01, 0.01))
            self._specular_incidence = glmath.vec3f((0.5, 0.5, 0.5))
        elif material == 'cyan_plastic':
            self._surface_brightness = 32.0
            self._ambient_incidence = glmath.vec3f((0.0, 0.1, 0.06))
            self._diffuse_incidence = glmath.vec3f((0.0, 0.50980392, 0.50980392))
            self._specular_incidence = glmath.vec3f((0.50196078, 0.50196078, 0.50196078))
        elif material == 'green_plastic':
            self._surface_brightness = 32.0
            self._ambient_incidence = glmath.vec3f((0.0, 0.0, 0.0))
            self._diffuse_incidence = glmath.vec3f((0.1, 0.35, 0.1))
            self._specular_incidence = glmath.vec3f((0.45, 0.55, 0.45))
        elif material == 'red_plastic':
            self._surface_brightness = 32.0
            self._ambient_incidence = glmath.vec3f((0.0, 0.0, 0.0))
            self._diffuse_incidence = glmath.vec3f((0.5, 0.0, 0.0))
            self._specular_incidence = glmath.vec3f((0.7, 0.6, 0.6))
        elif material == 'white_plastic':
            self._surface_brightness = 32.0
            self._ambient_incidence = glmath.vec3f((0.0, 0.0, 0.0))
            self._diffuse_incidence = glmath.vec3f((0.55, 0.55, 0.55))
            self._specular_incidence = glmath.vec3f((0.7, 0.7, 0.7))
        elif material == 'yellow_plastic':
            self._surface_brightness = 32.0
            self._ambient_incidence = glmath.vec3f((0.0, 0.0, 0.0))
            self._diffuse_incidence = glmath.vec3f((0.5, 0.5, 0.0))
            self._specular_incidence = glmath.vec3f((0.6, 0.6, 0.5))
        elif material == 'black_rubber':
            self._surface_brightness = 10.0
            self._ambient_incidence = glmath.vec3f((0.02, 0.02, 0.02))
            self._diffuse_incidence = glmath.vec3f((0.01, 0.01, 0.01))
            self._specular_incidence = glmath.vec3f((0.4, 0.4, 0.4))
        elif material == 'cyan_rubber':
            self._surface_brightness = 10.0
            self._ambient_incidence = glmath.vec3f((0.02, 0.05, 0.05))
            self._diffuse_incidence = glmath.vec3f((0.4, 0.5, 0.5))
            self._specular_incidence = glmath.vec3f((0.04, 0.7, 0.7))
        elif material == 'green_rubber':
            self._surface_brightness = 10.0
            self._ambient_incidence = glmath.vec3f((0.0, 0.05, 0.0))
            self._diffuse_incidence = glmath.vec3f((0.4, 0.5, 0.4))
            self._specular_incidence = glmath.vec3f((0.04, 0.7, 0.04))
        elif material == 'red_rubber':
            self._surface_brightness = 10.0
            self._ambient_incidence = glmath.vec3f((0.05, 0.0, 0.0))
            self._diffuse_incidence = glmath.vec3f((0.5, 0.4, 0.4))
            self._specular_incidence = glmath.vec3f((0.7, 0.04, 0.04))
        elif material == 'white_rubber':
            self._surface_brightness = 10.0
            self._ambient_incidence = glmath.vec3f((0.05, 0.05, 0.05))
            self._diffuse_incidence = glmath.vec3f((0.5, 0.5, 0.5))
            self._specular_incidence = glmath.vec3f((0.7, 0.7, 0.7))
        elif material == 'yellow_rubber':
            self._surface_brightness = 10.0
            self._ambient_incidence = glmath.vec3f((0.05, 0.05, 0.0))
            self._diffuse_incidence = glmath.vec3f((0.5, 0.5, 0.4))
            self._specular_incidence = glmath.vec3f((0.7, 0.7, 0.04))
            
            
class Model:
    def __init__(self, engine, shader_program_path: str = 'shaders/default', position: tuple[float, float, float] = (0, 0, 0)) -> None:
        self._engine = engine
        self._position = glmath.vec3f(position)
        self._gl_context = engine.gl_context
        self._shader_program = self.get_shader_program(shader_program_path)
        self._texture: Texture = None
        self._material = Material()
        
        self._vbo: moderngl.Buffer = None
        self._vao: moderngl.VertexArray = None
        self._model_matrix = self.get_model_matrix()
        
    @property
    def material(self) -> float:
        return self._material
    
    @property
    def model_matrix(self) -> glmath.mat4x4f:
        return self._model_matrix
    
    @property
    def shader_program(self) -> moderngl.Program:
        return self._shader_program
    
    @property
    def material(self) -> Material:
        return self._material
    
    @property
    def texture(self) -> Texture:
        return self._texture
    
    def use_texture(self) -> None:
        self._texture.use()
    
    def set_material(self, material: Material) -> None:
        self._material = material
        
    def set_texture(self, texture: Texture) -> None:
        self._texture = texture
        
    def set_vbo(self, vertex_data: np.ndarray) -> None:
        self._vbo = self._gl_context.buffer(vertex_data)
        
    def set_vao(self, format: str, attributes: list[str]) -> None:
        self._vao = self._gl_context.vertex_array(self._shader_program, 
                                                [(self._vbo, format, *attributes)])
        
    def get_shader_program(self, shader_program_path: str, vertex: bool = True, fragment: bool  = True, 
                                 geometry: bool  = False, tess: bool  = False) -> moderngl.Program:
        if vertex:
            with open(f'{shader_program_path}.vert') as file:
                vertex_shader = file.read()
        else: 
            vertex_shader = None
            
        if fragment:
            with open(f'{shader_program_path}.frag') as file:
                fragment_shader = file.read()
        else:   
            fragment_shader = None  
            
        if geometry:
            with open(f'{shader_program_path}.geom') as file:
                geometry_shader = file.read()
        else:
            geometry_shader = None
            
        if tess:
            with open(f'{shader_program_path}.tesc') as file:
                tessellation_control_shader = file.read()
            with open(f'{shader_program_path}.tese') as file:
                tessellation_evaluation_shader = file.read()
        else:
            tessellation_control_shader = None
            tessellation_evaluation_shader = None  
            
        program = self._gl_context.program(vertex_shader = vertex_shader, 
                                           fragment_shader = fragment_shader,
                                           geometry_shader = geometry_shader, 
                                           tess_control_shader = tessellation_control_shader,
                                           tess_evaluation_shader = tessellation_evaluation_shader)
        return program
    
    def get_model_matrix(self):
        model_matrix = glmath.identity_matrix()
        model_matrix = glmath.translate(model_matrix, self._position)
        return model_matrix
     
    def transform(self,  transformations: glmath.mat4x4f) -> glmath.mat4x4f:
        self._model_matrix *= transformations
    
    def render(self, mode = moderngl.TRIANGLES) -> None:
        self.use_texture()
        self._vao.render(mode)
        
    def destroy(self) -> None:
        self._shader_program.release()
        self._texture.destroy()
        
         
class CompanionCubeModel(Model):
    def __init__(self, engine, shader_program_path: str = 'shaders/default', position: tuple[float, float, float] = (0, 0, 0)) -> None:
        super().__init__(engine, shader_program_path, position)
        # shader program
        self._shader_program = self.get_shader_program('shaders/texturedCube')
        # cube mesh
        self._mesh = TexturedCubeMesh(self._engine)
        # vbo
        vertex_data = self._mesh.get_vertex_data()
        self.set_vbo(vertex_data)
        # vao
        format = '2f 3f 3f'
        attributes = ['in_texcoord', 'in_normal', 'in_position']
        self.set_vao(format, attributes)
        # texture
        texture = Texture(context = self._gl_context, path = 'textures/companion_cube.png')
        self.set_texture(texture)
        
        
class WoodenBoxModel(Model):
    def __init__(self, engine, shader_program_path: str = 'shaders/default', position: tuple[float, float, float] = (0, 0, 0)) -> None:
        super().__init__(engine, shader_program_path, position)
        # shader program
        self._shader_program = self.get_shader_program('shaders/texturedCube')
        # cube mesh
        self._mesh = TexturedCubeMesh(self._engine)
        # vbo
        vertex_data = self._mesh.get_vertex_data()
        self.set_vbo(vertex_data)
        # vao
        format = '2f 3f 3f'
        attributes = ['in_texcoord', 'in_normal', 'in_position']
        self.set_vao(format, attributes)
        # texture
        texture = Texture(context = self._gl_context, path = 'textures/wooden_box.png')
        self.set_texture(texture)
        

class MetalBoxModel(Model):
    def __init__(self, engine, shader_program_path: str = 'shaders/default', position: tuple[float, float, float] = (0, 0, 0)) -> None:
        super().__init__(engine, shader_program_path, position)
        # shader program
        self._shader_program = self.get_shader_program('shaders/texturedCube')
        # cube mesh
        self._mesh = TexturedCubeMesh(self._engine)
        # vbo
        vertex_data = self._mesh.get_vertex_data()
        self.set_vbo(vertex_data)
        # vao
        format = '2f 3f 3f'
        attributes = ['in_texcoord', 'in_normal', 'in_position']
        self.set_vao(format, attributes)
        # texture
        texture = Texture(context = self._gl_context, path = 'textures/METAL_BOX.png')
        self.set_texture(texture)
        # material
        self.material.set_default_material('chrome')
        
        
class GoldenBoxModel(Model):
    def __init__(self, engine, shader_program_path: str = 'shaders/default', position: tuple[float, float, float] = (0, 0, 0)) -> None:
        super().__init__(engine, shader_program_path, position)
        # shader program
        self._shader_program = self.get_shader_program('shaders/texturedCube')
        # cube mesh
        self._mesh = TexturedCubeMesh(self._engine)
        # vbo
        vertex_data = self._mesh.get_vertex_data()
        self.set_vbo(vertex_data)
        # vao
        format = '2f 3f 3f'
        attributes = ['in_texcoord', 'in_normal', 'in_position']
        self.set_vao(format, attributes)
        # texture
        texture = Texture(context = self._gl_context, path = 'textures/golden_box.png')
        self.set_texture(texture)
        # material
        self.material.set_default_material('polished_gold')
        
        
class TexturedCubeModel(Model):
    def __init__(self, engine, shader_program_path: str = 'shaders/default', position: tuple[float, float, float] = (0, 0, 0)) -> None:
        super().__init__(engine, shader_program_path, position)
        # shader program
        self._shader_program = self.get_shader_program('shaders/texturedCube')
        # cube mesh
        self._mesh = TexturedCubeMesh(self._engine)
        # vbo
        vertex_data = self._mesh.get_vertex_data()
        self.set_vbo(vertex_data)
        # vao
        format = '2f 3f 3f'
        attributes = ['in_texcoord', 'in_normal', 'in_position']
        self.set_vao(format, attributes)
        # texture
        texture = Texture(context = self._gl_context, path = 'textures/test.png')
        self.set_texture(texture)
        

class ColoredCubeModel(Model):
    def __init__(self, engine, shader_program_path: str = 'shaders/default', position: tuple[float, float, float] = (0, 0, 0)) -> None:
        super().__init__(engine, shader_program_path, position)
        # shader program
        self._shader_program = self.get_shader_program('shaders/color_gradiant')
        # cube mesh
        self._mesh = SolidCubeMesh(self._engine)
        # vbo
        vertex_data = self._mesh.get_vertex_data()
        self.set_vbo(vertex_data)
        # vao
        format = '3f 3f'
        attributes = ['in_color', 'in_position']
        self.set_vao(format, attributes)
        
        
# must be rendered with LINE STRIP
class WireCubeModel(Model):
    def __init__(self, engine, shader_program_path: str = 'shaders/default', position: tuple[float, float, float] = (0, 0, 0)) -> None:
        super().__init__(engine, shader_program_path, position)
        # shader program
        self._shader_program = self.get_shader_program('shaders/outline')
        # cube mesh
        self._mesh = WireCubeMesh(self._engine)
        # vbo
        vertex_data = self._mesh.get_vertex_data()
        self.set_vbo(vertex_data)
        # vao
        format = '3f 3f'
        attributes = ['in_color', 'in_position']
        self.set_vao(format, attributes)
         
        
        
        