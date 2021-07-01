from .connection import Connection
from .vec3 import Vec3
from .event import BlockEvent, ChatEvent, ProjectileEvent
from .entity import Entity
from .block import Block
import math
from .util import flatten

""" Minecraft for serveur v1.15.1

    Note: many methods have the parameter *arg. This solution makes it
    simple to allow different types, and variable number of arguments.
    The actual magic is a mix of flatten_parameters() and __iter__. Example:
    A Cube class could implement __iter__ to work in Minecraft.setBlocks(c, id).

    (Because of this, it's possible to "erase" arguments. CmdPlayer removes
     entityId, by injecting [] that flattens to nothing)

    @author: Aron Nieminen, Mojang AB
    @ modification S. PINET, LPO ROUVIERE TOULON - version 1.2 - jan 2020
    """

""" Updated to include functionality provided by RaspberryJuice:
- getBlocks()
- getDirection()
- getPitch()
- getRotation()
- getPlayerEntityId()
- pollChatPosts()
- setSign()
- spawnEntity()
- getEntities()
- removeEntity()
- removeEntityType()
"""

def intFloor(*args):
    return [int(math.floor(x)) for x in flatten(args)]

class CmdPositioner:
    """Methods for setting and getting positions"""
    def __init__(self, connection, packagePrefix):
        self.conn = connection
        self.pkg = packagePrefix

    def getPos(self, id):
        """Get entity position (entityId:int) => Vec3"""
        s = self.conn.sendReceive(self.pkg + b".getPos", id)
        try:
            return Vec3(*list(map(float, s.split(","))))
        except:
            return s

    def setPos(self, id, *args):
        """Set entity position (entityId:int, x,y,z)"""
        self.conn.send(self.pkg + b".setPos", id, args)

    def getTilePos(self, id):
        """Get entity tile position (entityId:int) => Vec3"""
        s = self.conn.sendReceive(self.pkg + b".getTile", id)
        return Vec3(*list(map(int, s.split(","))))

    def setTilePos(self, id, *args):
        """Set entity tile position (entityId:int) => Vec3"""
        self.conn.send(self.pkg + b".setTile", id, intFloor(*args))

    def setDirection(self, id, *args):
        """Set entity direction (entityId:int, x,y,z)"""
        self.conn.send(self.pkg + b".setDirection", id, args)

    def getDirection(self, id):
        """Get entity direction (entityId:int) => Vec3"""
        s = self.conn.sendReceive(self.pkg + b".getDirection", id)
        return Vec3(*map(float, s.split(",")))

    def setRotation(self, id, yaw):
        """Set entity rotation (entityId:int, yaw)"""
        self.conn.send(self.pkg + b".setRotation", id, yaw)

    def getRotation(self, id):
        """get entity rotation (entityId:int) => float"""
        return float(self.conn.sendReceive(self.pkg + b".getRotation", id))

    def setPitch(self, id, pitch):
        """Set entity pitch (entityId:int, pitch)"""
        self.conn.send(self.pkg + b".setPitch", id, pitch)

    def getPitch(self, id):
        """get entity pitch (entityId:int) => float"""
        return float(self.conn.sendReceive(self.pkg + b".getPitch", id))

    def setting(self, setting, status):
        """Set a player setting (setting, status). keys: autojump"""
        self.conn.send(self.pkg + b".setting", setting, 1 if bool(status) else 0)

class CmdEntity(CmdPositioner):
    """Methods for entities"""
    
    def __init__(self, connection):
        CmdPositioner.__init__(self, connection, b"entity")
    
    def getName(self, id):
        """Get the list name of the player with entity id => [name:str]
        
        Also can be used to find name of entity if entity is not a player."""
        return self.conn.sendReceive(b"entity.getName", id)

    def getEntities(self, id, distance=10, typeId=""):
        """Return a list of entities near entity (playerEntityId:int, distanceFromPlayerInBlocks:int, typeId:int) => [[entityId:int,entityTypeId:int,entityTypeName:str,posX:float,posY:float,posZ:float]]"""
        """If distanceFromPlayerInBlocks:int is not specified then default 10 blocks will be used"""
        s = self.conn.sendReceive(b"entity.getEntities", id, distance, typeId)
        entities = [e for e in s.split("|") if e]
        return [ [int(n.split(",")[0]), int(n.split(",")[1]), n.split(",")[2], float(n.split(",")[3]), float(n.split(",")[4]), float(n.split(",")[5])] for n in entities]

    def removeEntities(self, id, distance=10, typeId=-1):
        """Remove entities all entities near entity (playerEntityId:int, distanceFromPlayerInBlocks:int, typeId:int, ) => (removedEntitiesCount:int)"""
        """If distanceFromPlayerInBlocks:int is not specified then default 10 blocks will be used"""
        return int(self.conn.sendReceive(b"entity.removeEntities", id, distance, typeId))

    def pollBlockHits(self, *args):
        """Only triggered by sword => [BlockEvent]"""
        s = self.conn.sendReceive(b"entity.events.block.hits", intFloor(args))
        events = [e for e in s.split("|") if e]
        return [BlockEvent.Hit(*list(map(int, e.split(",")))) for e in events]

    def pollChatPosts(self, *args):
        """Triggered by posts to chat => [ChatEvent]"""
        s = self.conn.sendReceive(b"entity.events.chat.posts", intFloor(args))
        events = [e for e in s.split("|") if e]
        return [ChatEvent.Post(int(e[:e.find(",")]), e[e.find(",") + 1:]) for e in events]
    
    def pollProjectileHits(self, *args):
        """Only triggered by projectiles => [BlockEvent]"""
        s = self.conn.sendReceive(b"entity.events.projectile.hits", intFloor(args))
        events = [e for e in s.split("|") if e]
        results = []
        for e in events:
            info = e.split(",")
            results.append(ProjectileEvent.Hit(
                int(info[0]), 
                int(info[1]), 
                int(info[2]), 
                int(info[3]), 
                info[4],
                info[5]))
        return results

    def clearEvents(self, *args):
        """Clear the entities events"""
        self.conn.send(b"entity.events.clear", intFloor(args))

class CmdPlayer(CmdPositioner):
    """Methods for the host (Raspberry Pi) player"""
    def __init__(self, connection, id = None, pkg = b"player"):
        CmdPositioner.__init__(self, connection, b"player")
        self._id = []
        
    @property
    def id(self):
        return self._id

    # When a playerid changes then toggle multiplayer/player.  This way RaspberryJuice2
    # knows whether or not the first arg is a playerid
    @id.setter
    def id(self, val):
        if isinstance(val, int):
            self._id = val
            self.pkg = b"multiplayer"
        elif isinstance(val, str) and val != "":
            self._id = val
            self.pkg = b"multiplayer"
        else:
            self._id = []
            self.pkg = b"player"


    def getPos(self):
        return CmdPositioner.getPos(self, self.id)
    def setPos(self, *args):
        return CmdPositioner.setPos(self, self.id, args)
    def getTilePos(self):
        return CmdPositioner.getTilePos(self, self.id)
    def setTilePos(self, *args):
        return CmdPositioner.setTilePos(self, self.id, args)
    def setDirection(self, *args):
        return CmdPositioner.setDirection(self, self.id, args)
    def getDirection(self):
        return CmdPositioner.getDirection(self, self.id)
    def setRotation(self, yaw):
        return CmdPositioner.setRotation(self, self.id, yaw)
    def getRotation(self):
        return CmdPositioner.getRotation(self, self.id)
    def setPitch(self, pitch):
        return CmdPositioner.setPitch(self, self.id, pitch)
    def getPitch(self):
        return CmdPositioner.getPitch(self, self.id)

    def getEntities(self, distance=10, typeId=""):
        """Return a list of entities near entity (distanceFromPlayerInBlocks:int, typeId:int) => [[entityId:int,entityTypeId:int,entityTypeName:str,posX:float,posY:float,posZ:float]]"""
        """If distanceFromPlayerInBlocks:int is not specified then default 10 blocks will be used"""
        s = self.conn.sendReceive(self.pkg + b".getEntities", self.id, distance, typeId)
        entities = [e for e in s.split("|") if e]
        return [ [int(n.split(",")[0]), int(n.split(",")[1]), n.split(",")[2], float(n.split(",")[3]), float(n.split(",")[4]), float(n.split(",")[5])] for n in entities]

    def removeEntities(self, distance=10, typeId=-1):
        """Remove entities all entities near entity (distanceFromPlayerInBlocks:int, typeId:int, ) => (removedEntitiesCount:int)"""
        """If distanceFromPlayerInBlocks:int is not specified then default 10 blocks will be used"""
        return int(self.conn.sendReceive(self.pkg + b".removeEntities", self.id, distance, typeId))

    def pollBlockHits(self):
        """Only triggered by sword => [BlockEvent]"""
        s = self.conn.sendReceive(self.pkg + b".events.block.hits", self.id)
        events = [e for e in s.split("|") if e]
        return [BlockEvent.Hit(*list(map(int, e.split(",")))) for e in events]

    def pollChatPosts(self):
        """Triggered by posts to chat => [ChatEvent]"""
        s = self.conn.sendReceive(self.pkg + b".events.chat.posts", self.id)
        events = [e for e in s.split("|") if e]
        return [ChatEvent.Post(int(e[:e.find(",")]), e[e.find(",") + 1:]) for e in events]
    
    def pollProjectileHits(self):
        """Only triggered by projectiles => [BlockEvent]"""
        s = self.conn.sendReceive(self.pkg + b".events.projectile.hits", self.id)
        events = [e for e in s.split("|") if e]
        results = []
        for e in events:
            info = e.split(",")
            results.append(ProjectileEvent.Hit(
                int(info[0]), 
                int(info[1]), 
                int(info[2]), 
                int(info[3]), 
                info[4],
                info[5]))
        return results

    def clearEvents(self):
        """Clear the players events"""
        self.conn.send(self.pkg + b".events.clear", self.id)

class CmdCamera:
    def __init__(self, connection):
        self.conn = connection

    def setNormal(self, *args):
        """Set camera mode to normal Minecraft view ([entityId])"""
        self.conn.send(b"camera.mode.setNormal", args)

    def setFixed(self):
        """Set camera mode to fixed view"""
        self.conn.send(b"camera.mode.setFixed")

    def setFollow(self, *args):
        """Set camera mode to follow an entity ([entityId])"""
        self.conn.send(b"camera.mode.setFollow", args)

    def setPos(self, *args):
        """Set camera entity position (x,y,z)"""
        self.conn.send(b"camera.setPos", args)

class CmdEvents:
    """Events"""
    def __init__(self, connection):
        self.conn = connection

    def clearAll(self):
        """Clear all old events"""
        self.conn.send(b"events.clear")

    def pollBlockHits(self):
        """Only triggered by sword => [BlockEvent]"""
        s = self.conn.sendReceive(b"events.block.hits")
        events = [e for e in s.split("|") if e]
        return [BlockEvent.Hit(*list(map(int, e.split(",")))) for e in events]

    def pollChatPosts(self):
        """Triggered by posts to chat => [ChatEvent]"""
        s = self.conn.sendReceive(b"events.chat.posts")
        events = [e for e in s.split("|") if e]
        return [ChatEvent.Post(int(e[:e.find(",")]), e[e.find(",") + 1:]) for e in events]
    
    def pollProjectileHits(self):
        """Only triggered by projectiles => [BlockEvent]"""
        s = self.conn.sendReceive(b"events.projectile.hits")
        events = [e for e in s.split("|") if e]
        results = []
        for e in events:
            info = e.split(",")
            results.append(ProjectileEvent.Hit(
                int(info[0]), 
                int(info[1]), 
                int(info[2]), 
                int(info[3]), 
                info[4],
                info[5]))
        return results

class Minecraft:
    """version modified  1.1 - jan 2020
    The main class to interact with a running instance of Minecraft  java server v 1.13 and later
    
    """
    def __init__(self, connection):
        self.conn = connection

        self.camera = CmdCamera(connection)
        self.entity = CmdEntity(connection)
        self.player = CmdPlayer(connection)
        self.events = CmdEvents(connection)

        
    # GetBlock n'utilise que des arguments de position mais renvoie une chaine de caractres
    def getBlock(self, *args):
        """Get block (x,y,z) => return Material type : string -  v 1.15.1 """

        return self.conn.sendReceive(b"world.getBlock", intFloor(args))
        
    def getBlockWithData(self, *args):
        """Get block with data (x,y,z) => Block -  v 1.15.1 """
        return self.conn.sendReceive(b"world.getBlockWithData", intFloor(args))

    def getBlocks(self, *args):
        """Get a cuboid of blocks (x0,y0,z0,x1,y1,z1) - v 1.15.1"""
        s = self.conn.sendReceive(b"world.getBlocks", intFloor(args))
        return map(str, s.split(","))

    def setBlock(self, *args):
        """Set block (x,y,z,material,[data] -  v 1.15.1
        Material must be one of this at :
        https://hub.spigotmc.org/javadocs/bukkit/org/bukkit/Material.html

        except for those with a special BlockData like : Gate, sign, Stairs, Bed
        who need special arguments
        """
        intFloor(args[0:2])
        self.conn.send(b"world.setBlock", args)
       
    def setBlocks(self, *args):
        """Set a cuboid of blocks (x0,y0,z0,x1,y1,z1,Material,[data]) -  v 1.15.1

        Material must be one of this at :
        https://hub.spigotmc.org/javadocs/bukkit/org/bukkit/Material.html

        except for those with a special BlockData like : Gate, sign, Stairs, Bed
        who need special arguments
        """
        intFloor(args[0:5])
        self.conn.send(b"world.setBlocks", args)

    def setBlockDir(self, *args):
        """Set block directionnal (x,y,z,material,direction -  v 1.15.1

        x,y,z (int) : position en X, Y, Z dans le monde
        
        Set Material Block with directional BlockData (see : 
            https://hub.spigotmc.org/javadocs/bukkit/org/bukkit/Material.html)

        for example : ANVIL, ATTACHED_MELON_STEM, ATTACHED_PUMPKIN_STEM, BARREL,
        BLACK_GLAZED_TERRACOTTA, BLACK_SHULKER_BOX, BLACK_WALL_BANNER, BLUE_GLAZED_TERRACOTTA
        BLUE_SHULKER_BOX, BLUE_WALL_BANNER, BROWN_GLAZED_TERRACOTTA, BROWN_SHULKER_BOX
        BROWN_WALL_BANNER, CARVED_PUMPKIN, CHIPPED_ANVIL, CREEPER_WALL_HEAD, CYAN_GLAZED_TERRACOTTA,
        CYAN_SHULKER_BOX, CYAN_WALL_BANNER, DAMAGED_ANVIL, DRAGON_WALL_HEAD, END_ROD,
        GRAY_GLAZED_TERRACOTTA, GRAY_SHULKER_BOX, GRAY_WALL_BANNER, GREEN_GLAZED_TERRACOTTA,
        GREEN_SHULKER_BOX, GREEN_WALL_BANNER, GRINDSTONE, JACK_O_LANTERN, JIGSAW, LIGHT_BLUE_GLAZED_TERRACOTTA
        LIGHT_BLUE_SHULKER_BOX, LIGHT_BLUE_WALL_BANNER, LIGHT_GRAY_GLAZED_TERRACOTTA,
        LIGHT_GRAY_SHULKER_BOX, LIGHT_GRAY_WALL_BANNER, LIME_GLAZED_TERRACOTTA, LIME_SHULKER_BOX,
        LIME_WALL_BANNER, LOOM, MAGENTA_GLAZED_TERRACOTTA, MAGENTA_SHULKER_BOX, MAGENTA_WALL_BANNER
        ORANGE_GLAZED_TERRACOTTA, ORANGE_SHULKER_BOX, ORANGE_WALL_BANNER, PINK_GLAZED_TERRACOTTA
        PINK_SHULKER_BOX, PINK_WALL_BANNER, PLAYER_WALL_HEAD, PURPLE_GLAZED_TERRACOTTA,
        PURPLE_SHULKER_BOX, PURPLE_WALL_BANNER, RED_GLAZED_TERRACOTTA, RED_SHULKER_BOX,
        RED_WALL_BANNER, SHULKER_BOX, SKELETON_WALL_SKULL, STONECUTTER, WALL_TORCH,WHITE_GLAZED_TERRACOTTA,
        WHITE_SHULKER_BOX, WHITE_WALL_BANNER, WITHER_SKELETON_WALL_SKULL, YELLOW_GLAZED_TERRACOTTA
        YELLOW_SHULKER_BOX, YELLOW_WALL_BANNER, ZOMBIE_WALL_HEAD,
        LECTERN


        directionnal :  UP, DOWN,
                        NORTH, SOUTH, EAST, WEST,
                        SOUTH, SOUTH_SOUTH_WEST, SOUTH_WEST, WEST_SOUTH_WEST, WEST,
                        WEST_NORTH_WEST, WEST_NORTH, NORTH_NORTH_WEST, NORTH,
                        NORTH_NORTH_EAST, NORTH_EAST, EAST_NORTH_EAST, EAST,
                        EAST_SOUTH_EAST, SOUTH_EAST, SOUTH_SOUTH_EAST
                        La direction dépend des blocs (wall juste N, S, E, W, )
        """
        intFloor(args[0:2])

        flatargs = []
        for arg in flatten(args):
            flatargs.append(arg)
        intFloor(flatargs[0:3])
        self.conn.send(b"world.setBlockDir",flatargs[0:5])

    def setBlockMultiFace(self, *args):
        """Set block Multiface, BlockData: MultipleFacing (x,y,z,Material,faces*)

        x,y,z (int) : position en X, Y, Z dans le monde
        
        Set Material Block with MultipleFacing BlockData (see : 
            https://hub.spigotmc.org/javadocs/bukkit/org/bukkit/Material.html)
        BROWN_MUSHROOM_BLOCK, CHORUS_PLANT, MOSSY_COBBLESTONE, MUSHROOM_STEM, RED_MUSHROOM_BLOCK,
        VINE (liane - lierre), 

        faces : UP, DOWN,
                NORTH, SOUTH, EAST, WEST,
        """
        
        intFloor(args[0:2])

        flatargs = []
        nb = 1
        for arg in flatten(args):
            flatargs.append(arg)
            nb = nb+1
        intFloor(flatargs[0:3])
        #print(flatargs)
        self.conn.send(b"world.setBlockMultiFace",flatargs[0:nb])

    def setBlockOrient(self, *args):
        """Set block orientable (x,y,z,Material,Orientation -  v 1.15.1

        x,y,z (int) : position en X, Y, Z dans le monde
        
        Set Material Block with BlockData: Orientable (see : 
            https://hub.spigotmc.org/javadocs/bukkit/org/bukkit/Material.html)

        for example : ACACIA_LOG, ACACIA_WOOD, BIRCH_LOG, BIRCH_WOOD, BONE_BLOCK
        DARK_OAK_LOG, DARK_OAK_WOOD, HAY_BLOCK, JUNGLE_LOG, JUNGLE_WOOD, NETHER_PORTAL,
        OAK_LOG, OAK_WOOD, PURPUR_PILLAR, QUARTZ_PILLAR, SPRUCE_LOG, SPRUCE_WOOD STRIPPED_ACACIA_LOG
        STRIPPED_ACACIA_WOOD, STRIPPED_BIRCH_LOG, STRIPPED_BIRCH_WOOD, STRIPPED_DARK_OAK_LOG,
        STRIPPED_DARK_OAK_WOOD, STRIPPED_JUNGLE_LOG, STRIPPED_JUNGLE_WOOD, STRIPPED_OAK_LOG,
        STRIPPED_OAK_WOOD, STRIPPED_SPRUCE_LOG, STRIPPED_SPRUCE_WOOD, 

        Orientation : X, Y ou Z
        """
        
        intFloor(args[0:2])

        flatargs = []
        for arg in flatten(args):
            flatargs.append(arg)
        intFloor(flatargs[0:3])
        self.conn.send(b"world.setBlockOrient",flatargs[0:5])

    def setBlockRotat(self, *args):
        """Set block rotatable  (x,y,z,Material,Orientation, [motif*,couleur*]

        x,y,z (int) : position en X, Y, Z dans le monde
        
        Set Material Block with BlockData: Rotatable (see : 
            https://hub.spigotmc.org/javadocs/bukkit/org/bukkit/Material.html)

        for example : BLACK_BANNER, BLUE_BANNER, BROWN_BANNER, CREEPER_HEAD, CYAN_BANNER,
        DRAGON_HEAD, GRAY_BANNER, GREEN_BANNER, LIGHT_BLUE_BANNER, LIGHT_GRAY_BANNER, LIME_BANNER,
        MAGENTA_BANNER, ORANGE_BANNER, PINK_BANNER, PLAYER_HEAD, PURPLE_BANNER, RED_BANNER,
        SKELETON_SKULL, WHITE_BANNER, WITHER_SKELETON_SKULL, YELLOW_BANNER, ZOMBIE_HEAD, 

        Rotation  :  SOUTH, SOUTH_SOUTH_WEST, SOUTH_WEST, WEST_SOUTH_WEST, WEST,
        WEST_NORTH_WEST, WEST_NORTH, NORTH_NORTH_WEST,
        NORTH, NORTH_NORTH_EAST, NORTH_EAST, EAST_NORTH_EAST,
        EAST, EAST_SOUTH_EAST, SOUTH_EAST, SOUTH_SOUTH_EAST

        Motif :BASE, BORDER, BRICKS, CIRCLE_MIDDLE, CREEPER, CROSS, CURLY_BORDER 	 
        DIAGONAL_LEFT, DIAGONAL_LEFT_MIRROR, DIAGONAL_RIGHT 	 
        DIAGONAL_RIGHT_MIRROR, FLOWER, GLOBE, GRADIENT, GRADIENT_UP 	 
        HALF_HORIZONTAL, HALF_HORIZONTAL_MIRROR, HALF_VERTICAL 	 
        HALF_VERTICAL_MIRROR, MOJANG, RHOMBUS_MIDDLE, SKULL 	 
        SQUARE_BOTTOM_LEFT, SQUARE_BOTTOM_RIGHT, SQUARE_TOP_LEFT 	 
        SQUARE_TOP_RIGHT, STRAIGHT_CROSS, STRIPE_BOTTOM 	 
        STRIPE_CENTER, STRIPE_DOWNLEFT, STRIPE_DOWNRIGHT 	 
        STRIPE_LEFT, STRIPE_MIDDLE, STRIPE_RIGHT, STRIPE_SMALL 	 
        STRIPE_TOP, TRIANGLE_BOTTOM, TRIANGLE_TOP, TRIANGLES_BOTTOM, TRIANGLES_TOP


        Couleur du motif : BLACK, BLUE, BROWN, CYAN, GRAY, GREEN, LIGHT_BLUE,
        LIGHT_GRAY, LIME, MAGENTA, ORANGE, PINK, PURPLE, RED, WHITE, YELLOW

        Il peut y avoir plusieurs couples de motifs qui se supperposent
        les uns aux autres

        """
        
        intFloor(args[0:2])
        nb = 1
        flatargs = []
        for arg in flatten(args):
            flatargs.append(arg)
            nb = nb+1
        intFloor(flatargs[0:3])
        
        self.conn.send(b"world.setBlockRotat",flatargs[0:nb])
        
    def setBlockAge(self, *args) :
        """Set block Ageable (x,y,z,material,age) -  v 1.15.1
        x,y,z,age : int

        x,y,z (int) : position en X, Y, Z dans le monde        
        age (int): âge du Material (voir age max entre parenthèses ci-dessous)
        
        Set Material Block Ageable (plants and vegeatables) BlockData (see : 
            https://hub.spigotmc.org/javadocs/bukkit/org/bukkit/Material.html)

        for example :BEETROOTS (age max = 3), CACTUS (15), CARROTS (7), CHORUS_FLOWER (5),
        FROSTED_ICE (3) , KELP (25), MELON_STEM (7) , NETHER_WART (3) , POTATOES (7),
        PUMPKIN_STEM (7), SUGAR_CANE (15), SWEET_BERRY_BUSH (3), WHEAT (7)
        """
        
        intFloor(args[0:2])
        #self.conn.send(b"world.setBlock", args)
        flatargs = []
        for arg in flatten(args):
            flatargs.append(arg)
        intFloor(flatargs[0:3])
        intFloor(flatargs[4])
        flatargs[4]=str(flatargs[4]);
        self.conn.send(b"world.setBlockAge",flatargs[0:5])               

    def setBlockBisected(self, *args):
        """Set a BlockData : Bisected -like peony, rose_bush (x,y,z, Material, bisected)

        x,y,z (int) : position en X, Y, Z dans le monde

        Material (string) :  LARGE_FERN, LILAC , PEONY, ROSE_BUSH, SUNFLOWER, TALL_GRASS, 

        La fonction place automatiquement les deux blocs du matériaux en commençant par la
        partie haute.
        """
        flatargs = []
        for arg in flatten(args):
            flatargs.append(arg)
        intFloor(flatargs[0:3])

        flatargs[1] = flatargs[1] + 1  # Y+1  --- UPPER
        self.conn.send(b"world.setBlockBisected",flatargs[0:4]+["UPPER"])
        flatargs[1] = flatargs[1] - 1  # Y  --- LOWER
        self.conn.send(b"world.setBlockBisected",flatargs[0:4]+["LOWER"])

    def setBlockSapl(self, *args) :
        """Set block Sapling(x,y,z,material,stage) -  v 1.15.1
        x,y,z : int
        stage : int 0 or 1 (max stage)
                la différence entre 0 ou 1 sur la taille de l'arbre n'est
                visible que pour 'OAK_SAPLING', avec les autres Material
                la taille reste identique que le paramètre soit 0 ou 1
                bug ?  voir dans les versions futures
        material : str
        
        Set Material Block  with Sapling BlockData (see : 
            https://hub.spigotmc.org/javadocs/bukkit/org/bukkit/Material.html)

        for example (trees) : ACACIA_SAPLING, BIRCH_SAPLING, DARK_OAK_SAPLING,
        JUNGLE_SAPLING, OAK_SAPLING, SPRUCE_SAPLING

        """
        
        intFloor(args[0:2])
        #self.conn.send(b"world.setBlock", args)
        flatargs = []
        for arg in flatten(args):
            flatargs.append(arg)
        intFloor(flatargs[0:3])
        intFloor(flatargs[4])
        flatargs[4]=str(flatargs[4]);
        self.conn.send(b"world.setBlockSapl",flatargs[0:5])

    def setBlockLevel(self, *args) :
        """Set block Level(x,y,z,material,Level) org.bukkit.block.data.Levelled -  v 1.15.1
        x,y,z : int - position en X, Y et Z
        
        Level :	 on fixe la valeur de level
        In the case of water and lava blocks the levels have special meanings: 
        a level of 0 corresponds to a source block, 
        1-7 regular fluid heights,
        and 8-15 to "falling" fluids. 
        All falling fluids have the same behaviour, but the level corresponds to that of the block above them,
        equal to this.level - 8 Note that counterintuitively, an adjusted level of 1 is the highest level, 
        whilst 7 is the lowest.
                
        material : str
        
        Set Material Block  with BlockData: Levelled (see : 
            https://hub.spigotmc.org/javadocs/bukkit/org/bukkit/Material.html)

        for example : CAULDRON, COMPOSTER, LAVA, WATER

        """
        
        intFloor(args[0:2])
        #self.conn.send(b"world.setBlock", args)
        flatargs = []
        for arg in flatten(args):
            flatargs.append(arg)
        intFloor(flatargs[0:3])
        intFloor(flatargs[4])
        flatargs[4]=str(flatargs[4]);
        self.conn.send(b"world.setBlockLevel",flatargs[0:5])

    def setSign(self, *args):
        """Set a sign (Wall or Standing see below) (x,y,z,Material,face,[line1,line2,line,line4])

        x,y,z (int) : position en X, Y, Z dans le monde

        Standing signs tels que Material (string) :
        OAK_SIGN, ACACIA_SIGN, DARK_OAK_SIGN, SPRUCE_SIGN, JUNGLE_SIGN, BIRCH_SIGN
        
        nécessitent une orientation de type :
        SOUTH, SOUTH_SOUTH_WEST, SOUTH_WEST, WEST_SOUTH_WEST, WEST,  WEST_NORTH_WEST, WEST_NORTH, NORTH_NORTH_WEST,
        NORTH, NORTH_NORTH_EAST, NORTH_EAST, EAST_NORTH_EAST, EAST, EAST_SOUTH_EAST, SOUTH_EAST, SOUTH_SOUTH_EAST


        Wall signs tels que :
        OAK_WALL_SIGN, ACACIA_WALL_SIGN, DARK_OAK_WALL_SIGN, SPRUCE_WALL_SIGN,
        JUNGLE_WALL_SIGN, BIRCH_WALL_SIGN, LEGACY_WALL_SIGN
        
        nécessitent une orientation de type :
        NORTH, SOUTH, EAST, WEST
        """
        lines = []
        flatargs = []
        for arg in flatten(args):
            flatargs.append(arg)
        for flatarg in flatargs[5:]:
            lines.append(flatarg.replace(",",";").replace(")","]").replace("(","["))
        intFloor(flatargs[0:3])
        self.conn.send(b"world.setSign",flatargs[0:5] , lines)

    def setBed(self, *args):
        """Set a Bed (x,y,z, Material, Position, Facing)

        x,y,z (int) : position en X, Y, Z dans le monde
        
        Material (string) : BLACK_BED, BLUE_BED, BROWN_BED, CYAN_BED,
        GRAY_BED, GREEN_BED, LIGHT_BLUE_BED, LIGHT_GRAY_BED, LIME_BED,
        MAGENTA_BED, ORANGE_BED, PINK_BED, PURPLE_BED, RED_BED, WHITE_BED,
        YELLOW_BED

        Position (string) : HEAD, FOOT

        facing (string) : NORTH, SOUTH, EAST, WEST
        """
        flatargs = []
        for arg in flatten(args):
            flatargs.append(arg)
        intFloor(flatargs[0:3])
        self.conn.send(b"world.setBed",flatargs[0:6])

    def setGate(self, *args):
        """Set a Gate (x,y,z, Material, Facing, DansMur)

        Material (string) : ACACIA_FENCE_GATE, BIRCH_FENCE_GATE, DARK_OAK_FENCE_GATE,
        JUNGLE_FENCE_GATE, OAK_FENCE_GATE, SPRUCE_FENCE_GATE

        facing (string) : NORTH, SOUTH, EAST, WEST

        dansMur(boolean) : True or False (valeur prise par défaut si non indiquée) -
                 indique si le portail est rattaché à un mur
        
        """
        flatargs = []
        nb = 0
        for arg in flatten(args):
            flatargs.append(arg)
            nb = nb + 1
        intFloor(flatargs[0:3])
        if nb == 5 :
            flatargs = flatargs + ['False']
        
        self.conn.send(b"world.setGate",flatargs[0:6])

    def setDoor(self, *args):
        """Set a Door (x,y,z, Material, Facing, Hinge, Moitié)

        x,y,z (int) : position en X, Y, Z dans le monde

        Material (string) : ACACIA_DOOR, BIRCH_DOOR, DARK_OAK_DOOR, IRON_DOOR, JUNGLE_DOOR,
        OAK_DOOR, SPRUCE_DOOR, 

        Facing (string) : NORTH, SOUTH, EAST, WEST

        hinge (string) : coté par lequel la porte est attachée au mur :  LEFT, RIGHT

        Moitié (string) : partie de la porte (haute ou basse) : TOP , BOTTOM (valeur par défaut)

        REMARQUE : Il faut placer la partie haute (TOP) PUIS la partie basse (BOTTOM) sinon
        cela génère une erreur java ... et la partie haute n'est pas placée dans le jeu
        """
        flatargs = []
        for arg in flatten(args):
            flatargs.append(arg)
        intFloor(flatargs[0:3])

        self.conn.send(b"world.setDoor",flatargs[0:7])

    def setTrapDoor(self, *args):
        """Set a TrapDoor (x,y,z, Material, Facing, bisected, Open)

        x,y,z (int) : position en X, Y, Z dans le monde

        Material (string) : ACACIA_TRAPDOOR, BIRCH_TRAPDOOR, DARK_OAK_TRAPDOOR, IRON_TRAPDOOR,
        JUNGLE_TRAPDOOR, OAK_TRAPDOOR, SPRUCE_TRAPDOOR 

        facing (string) : NORTH, SOUTH, EAST, WEST
        diection d'ouverture

        Bisected : position fermée : TOP s'ouvre vers le bas
        et BOTTOM s'ouvre vers le haut : TOP , BOTTOM

        open : booléen : True ou False (défaut)
        indique si la trappe est en position horizontale (false) ou verticale (true)
        

        """
        flatargs = []
        nb = 0
        for arg in flatten(args):
            flatargs.append(arg)
            nb = nb + 1
        intFloor(flatargs[0:3])

        if nb == 6 :
            flatargs = flatargs + ['False']

        self.conn.send(b"world.setTrapDoor",flatargs[0:7])
     
    def setPane(self, *args):
        """Set a Fence - barrière block who is a BlockData : GlassPane ie
        who has facing property (x,y,z, Material, Facing)

        x,y,z (int) : position en X, Y, Z dans le monde

        Material (string) : BLACK_STAINED_GLASS_PANE, BLUE_STAINED_GLASS_PANE, BROWN_STAINED_GLASS_PANE
        CYAN_STAINED_GLASS_PANE,   GRAY_STAINED_GLASS_PANE,  GREEN_STAINED_GLASS_PANE,  LIGHT_BLUE_STAINED_GLASS_PANE
        LIGHT_GRAY_STAINED_GLASS_PANE, LIME_STAINED_GLASS_PANE, MAGENTA_STAINED_GLASS_PANE,
        ORANGE_STAINED_GLASS_PANE, PINK_STAINED_GLASS_PANE, PURPLE_STAINED_GLASS_PANE, RED_STAINED_GLASS_PANE,
        WHITE_STAINED_GLASS_PANE, YELLOW_STAINED_GLASS_PANE, 

        facing (string) : ['NORTH', 'SOUTH','EAST', 'WEST'] on place dans un tableau
        la direction souhaitée pour le panneau, deux pour faire un angle

        # exemple pour une vitre qui s'étend d'est en ouest, perpendiculaire
        àl'axe nord - sud
        for posx in range(x+2, x+6):
            mc.setPane(posx, y+1, z+long, "WHITE_STAINED_GLASS_PANE","WEST","EAST")
            mc.setPane(posx, y+2, z+long, "WHITE_STAINED_GLASS_PANE","WEST","EAST")

        """
        flatargs = []
        nb = 1
        for arg in flatten(args):
            flatargs.append(arg)
            nb = nb + 1
        intFloor(flatargs[0:3])

        self.conn.send(b"world.setPane",flatargs[0:nb])
               
    def setFence(self, *args):
        """Set a Fence - barrière block who is a BlockData : fence ie
        who has facing property (x,y,z, Material, Facing)

        x,y,z (int) : position en X, Y, Z dans le monde

        Material (string) :  ACACIA_FENCE, ANDESITE_WALL, BIRCH_FENCE,
        BRICK_WALL, COBBLESTONE_WALL, DARK_OAK_FENCE, DIORITE_WALL,       
        END_STONE_BRICK_WALL, GLASS_PANE, GRANITE_WALL, IRON_BARS, JUNGLE_FENCE
        MOSSY_COBBLESTONE_WALL, MOSSY_STONE_BRICK_WALL, NETHER_BRICK_FENCE,
        NETHER_BRICK_WALL, OAK_FENCE, PRISMARINE_WALL, RED_NETHER_BRICK_WALL,
        RED_SANDSTONE_WALL, SANDSTONE_WALL, SPRUCE_FENCE, STONE_BRICK_WALL

        facing (string) : NORTH, SOUTH, EAST, WEST

        """
        flatargs = []
        for arg in flatten(args):
            flatargs.append(arg)
        intFloor(flatargs[0:3])

        self.conn.send(b"world.setFence",flatargs[0:5])
        
    def setChest(self, *args):
        """Set a Chest (x,y,z, Material, ChestType, Direction)

        Material (string) : TRAPPED_CHEST, CHEST, 

        ChestType(string) : LEFT ,RIGHT, SINGLE

        Direction (string) : orientation NORTH, SOUTH, EAST, WEST
        """
        flatargs = []
        for arg in flatten(args):
            flatargs.append(arg)
        intFloor(flatargs[0:3])

        self.conn.send(b"world.setChest",flatargs[0:6])

    def setFurnace(self, *args):
        """Set a Blocktype : Furnace (x,y,z, Material, Direction, Light)

        Material (string) : BLAST_FURNACE, FURNACE, SMOKER,  

        Direction (string) : orientation NORTH, SOUTH, EAST, WEST

        Light (boolean) (facultatif) : True (défaut) or False indique si le fourneau est allumé
        """
        flatargs = []
        nb = 0
        for arg in flatten(args):
            flatargs.append(arg)
            nb = nb + 1
        intFloor(flatargs[0:3])

        if nb == 5 :
            flatargs = flatargs + ['True']

        self.conn.send(b"world.setFurnace",flatargs[0:6])

    def setSlab(self, *args):
        """Set a Blocktype : Slab - plaque (x,y,z, Material, Type)

        Material (string) : ACACIA_SLAB, ANDESITE_SLAB, BIRCH_SLAB, BRICK_SLAB, COBBLESTONE_SLAB,    
        CUT_RED_SANDSTONE_SLAB, CUT_SANDSTONE_SLAB, DARK_OAK_SLAB, DARK_PRISMARINE_SLAB, DIORITE_SLAB,
        END_STONE_BRICK_SLAB, GRANITE_SLAB, JUNGLE_SLAB, MOSSY_COBBLESTONE_SLAB, MOSSY_STONE_BRICK_SLAB,
        NETHER_BRICK_SLAB, OAK_SLAB, PETRIFIED_OAK_SLAB, POLISHED_ANDESITE_SLAB, POLISHED_DIORITE_SLAB,
        POLISHED_GRANITE_SLAB, PRISMARINE_BRICK_SLAB, PRISMARINE_SLAB, PURPUR_SLAB, QUARTZ_SLAB,
        RED_NETHER_BRICK_SLAB, RED_SANDSTONE_SLAB, SANDSTONE_SLAB, SMOOTH_QUARTZ_SLAB, SMOOTH_RED_SANDSTONE_SLAB,
        SMOOTH_SANDSTONE_SLAB, SMOOTH_STONE_SLAB, SPRUCE_SLAB, STONE_BRICK_SLAB, STONE_SLAB,

        Type (sting) : TOP, BOTTOM, DOUBLE
        """
        flatargs = []
        nb = 0
        for arg in flatten(args):
            flatargs.append(arg)
            nb = nb + 1
        intFloor(flatargs[0:3])

        self.conn.send(b"world.setSlab",flatargs[0:5])

    def setStairs(self, *args):
        """Set a Stair (x,y,z, Material, Facing, Shape, Half)

        x,y,z (int) : position en X, Y, Z dans le monde

        Material (string) : ACACIA_STAIRS, ANDESITE_STAIRS, BIRCH_STAIRS, BRICK_STAIRS,
        COBBLESTONE_STAIRS, DARK_OAK_STAIRS, DARK_PRISMARINE_STAIRS, DIORITE_STAIRS,
        END_STONE_BRICK_STAIRS, GRANITE_STAIRS, JUNGLE_STAIRS, MOSSY_COBBLESTONE_STAIRS,
        MOSSY_STONE_BRICK_STAIRS, NETHER_BRICK_STAIRS, OAK_STAIRS,POLISHED_ANDESITE_STAIRS,
        POLISHED_DIORITE_STAIRS, POLISHED_GRANITE_STAIRS,PRISMARINE_BRICK_STAIRS,
        PRISMARINE_STAIRS, PURPUR_STAIRS, QUARTZ_STAIRS, RED_NETHER_BRICK_STAIRS,
        RED_SANDSTONE_STAIRS, SANDSTONE_STAIRS, SMOOTH_QUARTZ_STAIRS, SMOOTH_RED_SANDSTONE_STAIRS,
        SMOOTH_SANDSTONE_STAIRS, SPRUCE_STAIRS, STONE_BRICK_STAIRS, STONE_STAIRS
        
        facing (string) : NORTH, SOUTH, EAST, WEST

        Shape (facultatif) (string) : STRAIGHT (défaut), INNER_LEFT, INNER_RIGHT, OUTER_LEFT, OUTER_RIGHT

        Half (facultatif) (string): BOTTOM(defaut), TOP
        
        """
        flatargs = []
        for arg in flatten(args):
            flatargs.append(arg)
        intFloor(flatargs[0:3])
        nb = len(flatargs)
        if nb < 6 :
            flatargs = flatargs + ["STRAIGHT","BOTTOM"]
        elif nb < 7 :
            if flatargs[6] == "BOTTOM":
                flatargs[6] = "STRAIGHT"
                flatargs = flatargs + ["BOTTOM"]
            elif flatargs[6] == "TOP":
                flatargs[6] =  "STRAIGHT"
                flatargs = flatargs + ["TOP"]
            else :
                flatargs = flatargs + ["BOTTOM"]

        self.conn.send(b"world.setStairs",flatargs[0:7])

    def spawnEntity(self, *args):
        """Spawn entity (x,y,z,EntityType,"BABY")  - version 1.15.1
        x,y,z : postition
        EntityType : str parmi la liste des Entités org.bukkit.EntityType: https://hub.spigotmc.org/javadocs/bukkit/org/bukkit/entity/EntityType.html
        
        comme par exemple  : 'ELDER_GUARDIAN', 'WITHER_SKELETON', 'STRAY', 'HUSK', 'ZOMBIE_VILLAGER', 'SKELETON_HORSE', 'ZOMBIE_HORSE', 'ARMOR_STAND', 'DONKEY', 'MULE', 'EVOKER', 'VEX', 'VINDICATOR', 'ILLUSIONER', 'CREEPER', 'SKELETON', 'SPIDER', 'GIANT', 'ZOMBIE', 'SLIME', 'GHAST', 'PIG_ZOMBIE', 'ENDERMAN', 'CAVE_SPIDER', 'SILVERFISH', 'BLAZE', 'MAGMA_CUBE', 'ENDER_DRAGON', 'WITHER', 'BAT', 'WITCH', 'ENDERMITE', 'GUARDIAN', 'SHULKER', 'PIG', 'SHEEP', 'COW', 'CHICKEN', 'SQUID', 'WOLF', 'MUSHROOM_COW', 'SNOWMAN', 'OCELOT', 'IRON_GOLEM', 'HORSE', 'RABBIT', 'POLAR_BEAR', 'LLAMA', 'PARROT', 'VILLAGER', 'TURTLE', 'PHANTOM', 'COD', 'SALMON', 'PUFFERFISH', 'TROPICAL_FISH', 'DROWNED', 'DOLPHIN', 'CAT', 'PANDA', 'PILLAGER', 'RAVAGER', 'TRADER_LLAMA', 'WANDERING_TRADER', 'FOX', 'BEE'
        """
        
        return int(self.conn.sendReceive(b"world.spawnEntity", args))

    def spawnCat(self, *args):
        """Spawn Cat (x,y,z,bebe,catType, CollarColor)  - version 1.15.1
        x,y,z : postition
        
        bebe(str) : "BABY" pour indiquer que l'on veut un chaton
        
        catType : type de chat str parmi la liste 
        https://hub.spigotmc.org/javadocs/bukkit/org/bukkit/entity/Cat.Type.html
        comme par exemple  : ALL_BLACK, BLACK, BRITISH_SHORTHAIR, CALICO,
        JELLIE, PERSIAN, RAGDOLL, RED, SIAMESE, TABBY, WHITE
                
                collarColor (str) : couleur du collierdi chat  dans la liste :
        BLACK,BLUE, BROWN, CYAN, GRAY, GREEN, LIGHT_BLUE, LIGHT_GRAY, LIME, 
        MAGENTA, ORANGE, PINK, PURPLE, RED, WHITE, YELLOW

        """
        
        return int(self.conn.sendReceive(b"world.spawnCat", args))        
             
    def getHeight(self, *args):
        """Get the height of the world (x,z) => int"""
        #print(args)
        return int(self.conn.sendReceive(b"world.getHeight", intFloor(args)))

    def getPlayerEntityIds(self):
        """Get the entity ids of the connected players => [id:int]"""
        ids = self.conn.sendReceive(b"world.getPlayerIds")
        return list(map(int, ids.split("|")))

    def getPlayerEntityId(self, name):
        """Get the entity id of the named player => [id:int]"""
        return int(self.conn.sendReceive(b"world.getPlayerId", name))

    def saveCheckpoint(self):
        """Save a checkpoint that can be used for restoring the world"""
        self.conn.send(b"world.checkpoint.save")

    def restoreCheckpoint(self):
        """Restore the world state to the checkpoint"""
        self.conn.send(b"world.checkpoint.restore")

    def postToChat(self, msg):
        """Post a message to the game chat"""
        self.conn.send(b"chat.post", msg)

    def setting(self, setting, status):
        """Set a world setting (setting, status). keys: world_immutable, nametags_visible"""
        self.conn.send(b"world.setting", setting, 1 if bool(status) else 0)

    def getEntityTypes(self):
        """Return a list of Entity (String) objects representing all the entity types in Minecraft"""  
        s = self.conn.sendReceive(b"world.getEntityTypes")
        types = [t for t in s.split(",") if t]
        #return [Entity(int(e[:e.find(",")]), e[e.find(",") + 1:]) for e in types]
        return [e for e in types]

    def getEntities(self, typeId=""):
        """Return a list of all currently loaded entities (EntityType:str) => [[entityId:int,entityTypeId:int,entityTypeName:str,posX:float,posY:float,posZ:float]]"""
        s = self.conn.sendReceive(b"world.getEntities", typeId)
        entities = [e for e in s.split("|") if e]
        return [[int(n.split(",")[0]), int(n.split(",")[1]), n.split(",")[2], float(n.split(",")[3]), float(n.split(",")[4]), float(n.split(",")[5])] for n in entities]
              
    def removeEntity(self, id):
        """Remove entity by id (entityId:int) => (removedEntitiesCount:int)"""
        return int(self.conn.sendReceive(b"world.removeEntity", int(id)))

    def removeEntities(self, typeId=-1):
        """Remove entities all currently loaded Entities by type (typeId:int) => (removedEntitiesCount:int)"""
        return int(self.conn.sendReceive(b"world.removeEntities", typeId))

    @staticmethod
    def create(address = "localhost", port = 4711):
        return Minecraft(Connection(address, port))


if __name__ == "__main__":
    mc = Minecraft.create()
    mc.postToChat("Hello, Minecraft!")
