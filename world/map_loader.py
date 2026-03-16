import pytmx
import pygame

class MapLoader:
    def __init__(self, filename):
        self.tmx_data = pytmx.load_pygame(filename)
        npc_text="Akira- SHHHH! Tell the password --- Monk- (hesitates) --- Akira-Your lord brings destruction to innocents, plunders villages and destroys lifes. \n Yet, You support him. --- Monk- The password is Crimson Shadow! Now leave me!"
        self.width=self.tmx_data.width*self.tmx_data.tilewidth
        self.height=self.tmx_data.height*self.tmx_data.tileheight
        self.collisions = []
        self.transitions=[]
        self.enemy_spawns=[]
        self.documents=[]
        self.npcs=[]
        self.password_doors=[]
        for obj in self.tmx_data.objects:
            if obj.type == "collision":
                rect=pygame.Rect(obj.x,obj.y,obj.width,obj.height)
                self.collisions.append(rect)
            elif obj.type=="transition":
                rect=pygame.Rect(obj.x,obj.y,obj.width,obj.height)
                self.transitions.append({
                    "rect":rect,
                    "target_map":obj.properties["target_map"],
                    "spawn":obj.properties["spawn"]
                })
            elif obj.name=="password_door":
                self.password_doors.append({
                    "rect":pygame.Rect(obj.x,obj.y,obj.width,obj.height),
                    "password":obj.properties["password"],
                    "target_map":obj.properties["target_map"],
                    "spawn":obj.properties["spawn"]
                })
            elif obj.type=="enemy":
                self.enemy_spawns.append(
                    {
                        "name":obj.name,
                        "x":obj.x,
                        "y":obj.y
                    }
                )
            elif obj.name=="scroll" or obj.name=="letter":
                self.documents.append({
                    "name":obj.name,
                    "x":obj.x,
                    "y":obj.y,
                    "text":obj.properties.get("text","")
                })
            elif obj.name=="npc_spawn":
                self.npcs.append({
                    "x":obj.x,
                    "y":obj.y,
                    "text":npc_text
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
             