# Screen settings
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
LIGHT_GRAY = (200, 200, 200)

# Game settings
FPS = 60
INITIAL_RED_CREATURES = 3
INITIAL_BLACK_CREATURES = 50
INITIAL_FOOD_COUNT = 500
FOOD_SPAWN_RATE = 1000
MAX_FOOD = 5000

# Creature settings
RED_CREATURE_WIDTH = 20
RED_CREATURE_HEIGHT = 20
BLACK_CREATURE_WIDTH = 15
BLACK_CREATURE_HEIGHT = 15
RED_CREATURE_SPEED = 60
BLACK_CREATURE_SPEED = 80
RED_CREATURE_ACTIVITY = 0.08
BLACK_CREATURE_ACTIVITY = 0.05

# State settings
INITIAL_STATE = 10
SPLIT_THRESHOLD = 20
DEATH_THRESHOLD = 0

# Ecosystem balance parameters
RED_HUNGER_RATE = 0.2
BLACK_HUNGER_RATE = 0.2
RED_SPLIT_THRESHOLD = 20
BLACK_SPLIT_THRESHOLD = 3
RED_MAX_AGE = 3000
BLACK_MAX_AGE = 5000

# Gene settings
GENE_LENGTH = 12  # 가로, 세로, 속도, 활동량, 분열 임계값, 먹이 끌림, 포식자 두려움, 먹이 끌림, 방황욕, 회피 속도, 회피 반응, 회피 방향 변화 포함
MUTATION_RATE = 0.1

# Food settings
FOOD_WIDTH = 5
FOOD_HEIGHT = 5

# Game speed settings
MIN_GAME_SPEED_MULTIPLIER = 1.0
MAX_GAME_SPEED_MULTIPLIER = 50.0
SPEED_CHANGE_RATE = 1

# Hunger rate factors
SIZE_HUNGER_FACTOR = 0.5  # 크기가 클수록 허기가 빨리 증가
SPEED_HUNGER_FACTOR = 0.3  # 속도가 빠를수록 허기가 빨리 증가
ACTIVITY_HUNGER_FACTOR = 0.2  # 활동량이 많을수록 허기가 빨리 증가

# New evasion-related constants
PREDATOR_DETECTION_RANGE = 100  # 포식자 감지 범위
EVASION_COOLDOWN = 2  # 회피 후 쿨다운 시간(초)