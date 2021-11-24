# Minecraft Pi Edition
# Connection and blockID : MCPI
# World parameters : MCPI

print("param_MCPI loaded")

# axis parameters for MCPI
AXIS_WIDTH = 20    # x, z: -20 .. 0 .. 20
AXIS_TOP = 40
AXIS_Y_V_ORG = 20  # y of virtual origin
AXIS_BOTTOM = 0    # y: 0 .. 20 .. 40

# virtical levels for MCPI
Y_TOP = 63         # the top where blocks can be set
Y_SEA = -1         # the sea level

# connection port for MCPI
PORT_MC = 4711

# block IDs for MCPI  ## see block.py
AIR = 0
STONE = 1
GRASS_BLOCK = 2
GOLD_BLOCK = 41
IRON_BLOCK = 42
GLOWSTONE = 89
SEA_LANTERN_BLOCK = GLOWSTONE  # not available in MCPI

# some good blocks for grid like patterns you can count blocks easily
GLASS = 20
TNT = 46
DIAMOND_BLOCK = 57
FURNACE_INACTIVE = 61
FURNACE_ACTIVE = 62
GLASS_PANE = 102
STONE_CUTTER = 245
GLOWING_OBSIDIAN = 246
NETHER_REACTOR_CORE = 247
