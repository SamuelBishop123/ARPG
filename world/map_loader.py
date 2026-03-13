import pytmx
import pygame

class MapLoader:
    def __init__(self, filename):
        self.tmx_data = pytmx.load_pygame(filename)
        self.width=self.tmx_data.width*self.tmx_data.tilewidth
        self.height=self.tmx_data.height*self.tmx_data.tileheight
        self.collisions = []
        self.transitions=[]
        for obj in self.tmx_data.objects:
            if obj.type == "collision":
                rect=pygame.Rect(obj.x,obj.y,obj.width,obj.height)
                self.collisions.append(rect)
            if obj.type=="transition":
                rect=pygame.Rect(obj.x,obj.y,obj.width,obj.height)
                self.transitions.append({
                    "rect":rect,
                    "target_map":obj.properties["target_map"],
                    "spawn":obj.properties["spawn"]
                })
    def draw(self, surface, camera_x, camera_y):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer,pytmx.TiledTileLayer):
                for x,y,gid in layer:
                    tile=self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(
                            tile,
                            (
                                x*self.tmx_data.tilewidth-camera_x,
                                y*self.tmx_data.tileheight-camera_y
                            )
                        )
    def get_spawn(self, name):
        for obj in self.tmx_data.objects:
             if obj.name==name:
                return obj.x, obj.y
             