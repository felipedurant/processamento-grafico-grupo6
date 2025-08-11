from typing import Optional
from camera import Camera
from object import Object
from ray import Ray
from image import Image
from scene import Scene, Light, RectangularLight
from math import floor, pow
from vector import Vector
from sphere import Sphere

def add_colors(c1, c2):
    return (c1[0] + c2[0], c1[1] + c2[1], c1[2] + c2[2])

def multiply_color_by_scalar(c, s):
    return (c[0] * s, c[1] * s, c[2] * s)

def multiply_colors_componentwise(c1, c2):
    """Multiplica as componentes de duas cores (escala 0-255)."""
    # Normaliza para [0,1], multiplica, e retorna para [0,255]
    r = (c1[0] / 255) * (c2[0] / 255) * 255
    g = (c1[1] / 255) * (c2[1] / 255) * 255
    b = (c1[2] / 255) * (c2[2] / 255) * 255
    return (r, g, b)


class Renderer:
    def __init__(self, camera: Camera, scene: Scene, max_depth: int = 3, shadow_samples: int = 16, background_color: tuple = (0, 0, 0)):
        self.camera = camera
        self.scene = scene
        self.max_depth = max_depth
        # Feature: Armazena o número de amostras de sombra, garantindo que seja pelo menos 1.
        self.shadow_samples = max(1, shadow_samples)
        self.background_color = background_color
        
    def find_closest_intersection(self, ray: Ray) -> Optional[tuple]:
        closest_distance = float('inf')
        closest_object = None
        for obj in self.scene.objects:
            distance = obj.intersects(ray)
            if distance is not None and distance < closest_distance:
                closest_distance = distance
                closest_object = obj
        if closest_object:
            return (closest_distance, closest_object)
        return None
    
    def shade(self, obj: Object, hit_point, normal, ray: Ray) -> tuple:
        material = obj.material

        if material.is_checkerboard:
            check = (floor(hit_point.x) + floor(hit_point.z)) % 2
            base_diffuse_color = material.diffuse if check == 0 else (20, 20, 20)
        else:
            base_diffuse_color = material.diffuse

        final_color = multiply_colors_componentwise(self.scene.ambient_light, material.ambient)
        view_dir = (ray.origin - hit_point).normalize()

        for light in self.scene.lights:
            if isinstance(light, RectangularLight):
                # A luz irradia da superfície do painel.
                total_diffuse = Vector(0,0,0)
                total_specular = Vector(0,0,0)

                for _ in range(self.shadow_samples):
                    random_light_point = light.get_random_point()
                    vec_to_light = random_light_point - hit_point
                    dist_to_light_point = vec_to_light.magnitude()
                    light_dir = vec_to_light.normalize()
                    
                    
                    shadow_ray = Ray(hit_point + normal * obj.shadow_bias, Vector(0, 0, 0)) #light_dir
                    shadow_hit = self.find_closest_intersection(shadow_ray)
                    
                    if shadow_hit is None or shadow_hit[0] > dist_to_light_point:
                        
                        # Componente Difusa
                        diffuse_intensity = max(0, normal.dot_product(light_dir))
                        if diffuse_intensity > 0:
                            color_diffuse = multiply_colors_componentwise(light.intensity, base_diffuse_color)
                            total_diffuse += Vector(color_diffuse[0], color_diffuse[1], color_diffuse[2]) * diffuse_intensity

                        # Componente Especular
                        reflection_dir = (-light_dir).reflect(normal)
                        specular_intensity = max(0, view_dir.dot_product(reflection_dir))
                        if specular_intensity > 0:
                            specular_power = pow(specular_intensity, material.shininess)
                            color_specular = multiply_colors_componentwise(light.intensity, material.specular)
                            total_specular += Vector(color_specular[0], color_specular[1], color_specular[2]) * specular_power
                
                # Adiciona a média das contribuições a cor final
                avg_diffuse = total_diffuse / self.shadow_samples
                avg_specular = total_specular / self.shadow_samples
                final_color = add_colors(final_color, (avg_diffuse.x, avg_diffuse.y, avg_diffuse.z))
                final_color = add_colors(final_color, (avg_specular.x, avg_specular.y, avg_specular.z))

            elif isinstance(light, Light):
                light_dir = (light.position - hit_point).normalize()
                distance_to_light = (light.position - hit_point).magnitude()
                shadow_ray = Ray(hit_point + normal * obj.shadow_bias, light_dir)
                shadow_hit = self.find_closest_intersection(shadow_ray)
                if shadow_hit is not None and shadow_hit[0] < distance_to_light:
                    continue
                diffuse_intensity = max(0, normal.dot_product(light_dir))
                diffuse_contribution = multiply_colors_componentwise(light.intensity, base_diffuse_color)
                diffuse_color = multiply_color_by_scalar(diffuse_contribution, diffuse_intensity)
                final_color = add_colors(final_color, diffuse_color)
                reflection_dir = (-light_dir).reflect(normal)
                specular_intensity = max(0, view_dir.dot_product(reflection_dir))
                if specular_intensity > 0:
                    specular_power = pow(specular_intensity, material.shininess)
                    specular_contribution = multiply_colors_componentwise(light.intensity, material.specular)
                    specular_color = multiply_color_by_scalar(specular_contribution, specular_power)
                    final_color = add_colors(final_color, specular_color)

        return final_color
    
    def trace(self, ray: 'Ray', depth: int) -> tuple:
        if depth <= 0: return (0, 0, 0)
        hit = self.find_closest_intersection(ray)
        if hit is None: return self.background_color
        distance, obj_hit = hit
        material = obj_hit.material
        hit_point = ray.point_at(distance)
        local_hit_point = obj_hit.inverse_transform * hit_point
        local_normal = obj_hit.get_normal_at(local_hit_point)
        world_normal = (obj_hit.inverse_transform_transpose * local_normal).normalize()
        if material.emission_color: return material.emission_color
        final_color = (0, 0, 0)
        is_transparent = sum(material.transparency_color) > 0
        if is_transparent:
            ior_air = 1.0
            cosi = ray.direction.dot_product(world_normal)
            if cosi < 0: etai, etat, incident_normal = ior_air, material.ior, world_normal
            else: etai, etat, incident_normal = material.ior, ior_air, -world_normal
            reflectance = ray.direction.fresnel(incident_normal, etai, etat)
            refracted_color = (0, 0, 0)
            if reflectance < 1.0:
                ior_ratio = etai / etat
                refraction_dir = ray.direction.refract(incident_normal, ior_ratio)
                if refraction_dir is not None:
                    refraction_ray = Ray(hit_point - incident_normal * obj_hit.shadow_bias, refraction_dir)
                    color_from_refraction = self.trace(refraction_ray, depth - 1)
                    tinted_color = multiply_colors_componentwise(color_from_refraction, material.diffuse)
                    refracted_color = multiply_color_by_scalar(multiply_colors_componentwise(tinted_color, material.transparency_color), 1 - reflectance)
            reflection_dir = ray.direction.reflect(incident_normal)
            reflection_ray = Ray(hit_point + incident_normal * obj_hit.shadow_bias, reflection_dir)
            color_from_reflection = self.trace(reflection_ray, depth - 1)
            reflected_color = multiply_color_by_scalar(multiply_colors_componentwise(color_from_reflection, (255,255,255)), reflectance)
            specular_highlights = self.shade(obj_hit, hit_point, world_normal, ray)
            final_color = add_colors(add_colors(reflected_color, refracted_color), (specular_highlights[0]*0.1, specular_highlights[1]*0.1, specular_highlights[2]*0.1))
        else:
            local_color = self.shade(obj_hit, hit_point, world_normal, ray)
            reflected_color = (0, 0, 0)
            if sum(material.reflection_color) > 0:
                reflection_dir = ray.direction.reflect(world_normal)
                reflection_ray = Ray(hit_point + world_normal * obj_hit.shadow_bias, reflection_dir)
                color_from_reflection = self.trace(reflection_ray, depth - 1)
                reflected_color = multiply_colors_componentwise(color_from_reflection, material.reflection_color)
            final_color = add_colors(local_color, reflected_color)
        return (min(255, final_color[0]), min(255, final_color[1]), min(255, final_color[2]))

    def render(self) -> 'Image':
        final_image = Image(self.camera.screen_width, self.camera.screen_height)
        for y in range(self.camera.screen_height):
            if y > 0 and y % 20 == 0:
                print(f"Renderizando... {int((y / self.camera.screen_height) * 100)}%")
            for x in range(self.camera.screen_width):
                ray = self.camera.generate_ray_for_pixel(x, y)
                color = self.trace(ray, self.max_depth)
                final_image.set_pixel(x, y, color)
        print("Renderização concluída!")
        return final_image