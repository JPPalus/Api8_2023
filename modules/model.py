from modules.mesh import SolidCubeMesh, WireCubeMesh, TexturedCubeMesh
import modules.glmath as glmath
import pygame.image as pgimage
import numpy as np
import moderngl
import glm


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
                 surface_brightness: float = 56.0, 
                 ambient_incidence: tuple[float, float, float] = (1, 1, 1),
                 diffuse_incidence: tuple[float, float, float] = (1, 1, 1),
                 specular_incidence: tuple[float, float, float] = (1, 1, 1)) -> None:
        
        self._surface_brightness = surface_brightness
        self._ambient_incidence = glm.vec3(ambient_incidence)
        self._diffuse_incidence = glm.vec3(diffuse_incidence)
        self._specular_incidence = glm.vec3(specular_incidence)
        
    @property
    def surface_brightness(self) -> float:
        return self._surface_brightness
    
    @property
    def ambient_incidence(self) -> glm.fvec3:
        return self._ambient_incidence
    
    @property
    def diffuse_incidence(self) -> glm.fvec3:
        return self._diffuse_incidence
    
    @property
    def specular_incidence(self) -> glm.fvec3:
        return self._specular_incidence
    
    @surface_brightness.setter
    def surface_brightness(self, brightness: float) -> None:
        self._surface_brightness = brightness
        
    @ambient_incidence.setter
    def ambient_incidence(self, ambient_incidence: tuple[float, float, float]) -> None:
        self._ambient_incidence = glm.vec3(ambient_incidence)
        
    @diffuse_incidence.setter
    def diffuse_incidence(self, diffuse_incidence: tuple[float, float, float]) -> None:
        self._diffuse_incidence = glm.vec3(diffuse_incidence)
        
    @specular_incidence.setter
    def specular_incidence(self, specular_incidence: tuple[float, float, float]) -> None:
        self._specular_incidence = glm.vec3(specular_incidence)
    
    def set_material(self, material: str = 'basic') -> None:
        if material == 'basic':
            self._surface_brightness = 1.0
            self._ambient_incidence = glm.vec3((1, 1, 1))
            self._diffuse_incidence = glm.vec3((1, 1, 1))
            self._specular_incidence = glm.vec3((1, 1, 1))
        elif material == 'emerald':
            self._surface_brightness = 0.6
            self._ambient_incidence = glm.vec3((0.0215, 0.1745, 0.0215))
            self._diffuse_incidence = glm.vec3((0.07568, 0.61424, 0.07568))
            self._specular_incidence = glm.vec3((0.633, 0.727811, 0.633))
        elif material == 'gold':
            self._surface_brightness = 0.4
            self._ambient_incidence = glm.vec3((0.24725, 0.1995, 0.0745))
            self._diffuse_incidence = glm.vec3((0.75164, 0.60648, 0.22648))
            self._specular_incidence = glm.vec3((0.628281, 0.555802, 0.366065))
        
        
class Model:
    def __init__(self, engine, shader_program_path: str = 'shaders/default', position: tuple[float, float, float] = (0, 0, 0)) -> None:
        self._engine = engine
        self._position = glm.vec3(position)
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
    def model_matrix(self) -> glm.fmat4x4:
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
        model_matrix = glm.translate(model_matrix, self._position)
        return model_matrix
     
    def transform(self,  transformations: glm.fmat4x4) -> glm.fmat4x4:
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
        self.material.set_material('gold')
        
        
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
         
        
        
        