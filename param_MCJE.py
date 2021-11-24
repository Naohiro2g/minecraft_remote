# Minecraft Java Edition 1.16.5
# Connection and blockID : MCJE
# World parameters : MCJE

print("param_MCJE loaded")

# axis parameters
AXIS_WIDTH = 40       # x, z: -40 .. 0 .. 40
AXIS_TOP = 127
AXIS_Y_V_ORG = 96     # y of virtual origin
AXIS_BOTTOM = 63      # y: 63 .. 96 .. 127

# virtical levels
Y_TOP = 255           # the top where blocks can be set
Y_CLOUD_BOTTOM = 128  # the bottom of clouds
Y_SEA = 62            # the sea level
Y_BOTTOM = 0          # the bottom where blocks can be set
Y_BOTTOM_STEVE = -64  # the bottom where Steve can go down

# connection port
PORT_MC = 14712

# block IDs  You can find IDs here: https://minecraft-ids.grahamedgecombe.com/
AIR = "air"
STONE = "stone"
GRASS_BLOCK = "grass_block"
GOLD_BLOCK = "gold_block"
IRON_BLOCK = "iron_block"
GLOWSTONE = "glowstone"
SEA_LANTERN_BLOCK = "sea_lantern"

# some good blocks for grid like patterns you can count blocks easily
GLASS = "glass"
TNT = "tnt"
DIAMOND_BLOCK = "diamnd_block"
FURNACE_INACTIVE = "furnace"
FURNACE_ACTIVE = "lit_furnace"
GLASS_PANE = "glass_pane"
