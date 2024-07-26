### 먹이가 존재하는 버전 ###

# 그냥 번식하는 게 아니라 먹이를 일정량 먹어야 번식합니다.

import pygame
import random
import time

# Pygame 초기화
pygame.init()

# 화면 설정
screen_width = 1200
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('자연 선택 시뮬레이터')

# 색상 정의
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# 폰트 설정
font = pygame.font.SysFont(None, 36)

# 크리쳐 설정
initial_red_creatures = 10
initial_black_creatures = 50
red_creature_size = 20
black_creature_width = 20
black_creature_height = 20
red_creature_speed = 10
black_creature_speed = 10
red_creature_activity = 0.1
black_creature_activity = 0.05
generation_interval = 2
max_creatures = 300

# 먹이 설정
initial_food_count = 50
food_spawn_count = 3  # 매 틱당 생성될 먹이의 개수
food_size = 5

# 돌연변이 강도
mutation_intensity = 30

# 생물체 클래스 정의
class Creature(pygame.sprite.Sprite):
    def __init__(self, color, width, height, speed, activity):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - width)
        self.rect.y = random.randint(0, screen_height - height)
        self.speed = speed
        self.activity = activity
        self.direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.change_direction_time = time.time() + random.uniform(1, 10) * (1 - self.activity)
        self.food_eaten = 0

    def update(self):
        current_time = time.time()
        if current_time >= self.change_direction_time:
            self.direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
            self.change_direction_time = current_time + random.uniform(1, 10) * (1 - self.activity)

        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.direction.x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            self.direction.y *= -1

        self.rect.x = max(0, min(screen_width - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(screen_height - self.rect.height, self.rect.y))

    def eat(self):
        self.food_eaten += 1

    def should_split(self):
        return self.food_eaten >= 5

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([food_size, food_size])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - food_size)
        self.rect.y = random.randint(0, screen_height - food_size)

black_creatures = pygame.sprite.Group()
red_creatures = pygame.sprite.Group()
all_creatures = pygame.sprite.Group()
food_group = pygame.sprite.Group()

for i in range(initial_red_creatures):
    red_creature = Creature(RED, red_creature_size, red_creature_size, red_creature_speed, red_creature_activity)
    red_creatures.add(red_creature)
    all_creatures.add(red_creature)

for i in range(initial_black_creatures):
    black_creature = Creature(BLACK, black_creature_width, black_creature_height, black_creature_speed, black_creature_activity)
    black_creatures.add(black_creature)
    all_creatures.add(black_creature)

for i in range(initial_food_count):
    food = Food()
    food_group.add(food)

running = True

# 시뮬레이션 시작 시간
start_time = time.time()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_creatures.update()

    for creature in black_creatures:
        collided_food = pygame.sprite.spritecollide(creature, food_group, True)
        for food in collided_food:
            creature.eat()

        if pygame.sprite.spritecollide(creature, red_creatures, False):
            creature.kill()
            all_creatures.remove(creature)

        if creature.should_split():
            new_width = max(0.5, creature.rect.width + random.randint(-mutation_intensity, mutation_intensity))
            new_height = max(0.5, creature.rect.height + random.randint(-mutation_intensity, mutation_intensity))
            new_speed = max(0.1, creature.speed + random.randint(-mutation_intensity, mutation_intensity))
            new_activity = max(0.01, creature.activity + random.uniform(-mutation_intensity / 100, mutation_intensity / 100))
            new_creature = Creature(BLACK, new_width, new_height, new_speed, new_activity)
            black_creatures.add(new_creature)
            all_creatures.add(new_creature)
            creature.food_eaten = 0

    # 새로운 먹이 생성
    for _ in range(food_spawn_count):
        food = Food()
        food_group.add(food)

    screen.fill(WHITE)
    all_creatures.draw(screen)
    food_group.draw(screen)
    
    # 현재 총 개체 수 표시
    total_creatures = len(all_creatures)
    total_creatures_text = font.render(f"Total Creatures: {total_creatures}", True, BLACK)
    screen.blit(total_creatures_text, (10, 10))
    
    # 경과 시간 표시
    elapsed_time = time.time() - start_time
    elapsed_time_text = font.render(f"Elapsed Time: {int(elapsed_time)}s", True, BLACK)
    screen.blit(elapsed_time_text, (10, 50))

    pygame.display.flip()

    pygame.time.Clock().tick(30)

pygame.quit()
