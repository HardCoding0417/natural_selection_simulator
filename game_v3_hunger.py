### 빨강이도 진화하는 버전 ###

# 허기 개념을 추가하고
# 빨강이도 번식하도록 했습니다.

import pygame
import random
import time
import math

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

# 하이퍼파라미터
initial_red_creatures = 10
initial_black_creatures = 100
red_creature_width = 20
red_creature_height = 20
black_creature_width = 15
black_creature_height = 15
red_creature_speed = 60
black_creature_speed = 80
red_creature_activity = 0.08
black_creature_activity = 0.05

# 상태 설정
initial_state = 10
split_threshold = 20
death_threshold = 0

# 먹이 설정
initial_food_count = 500
food_spawn_rate = 300  # 초당 생성될 먹이의 개수
food_width = 5
food_height = 5
max_food = 500

# 생태계 균형 파라미터
red_hunger_rate = 0.4
black_hunger_rate = 0.2
red_split_threshold = 15
black_split_threshold = 3
red_max_age = 300
black_max_age = 500

# 돌연변이 설정
mutation_intensity = 10

# FPS 설정
FPS = 60

class Creature(pygame.sprite.Sprite):
    def __init__(self, color, width, height, speed, activity, split_threshold):
        super().__init__()
        self.color = color
        self.width = width
        self.height = height
        self.speed = speed
        self.activity = activity
        self.split_threshold = split_threshold
        self.original_image = pygame.Surface([width, height])
        self.original_image.fill(color)
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - width)
        self.rect.y = random.randint(0, screen_height - height)
        self.heading = random.uniform(0, 360)  # 방향 설정
        self.change_direction_time = time.time() + random.uniform(1, 10) * (1 - self.activity)
        self.state = initial_state
        self.food_eaten = 0
        self.age = 0

    def update(self, dt):
        current_time = time.time()
        if current_time >= self.change_direction_time:
            self.heading = random.uniform(0, 360)  # 방향 변경
            self.change_direction_time = current_time + random.uniform(1, 10) * (1 - self.activity)

        self.rect.x += self.speed * dt * math.cos(math.radians(self.heading))
        self.rect.y += self.speed * dt * math.sin(math.radians(self.heading))

        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.heading = (180 - self.heading) % 360
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            self.heading = (-self.heading) % 360

        self.rect.x = max(0, min(screen_width - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(screen_height - self.rect.height, self.rect.y))

        self.image = pygame.transform.rotate(self.original_image, -self.heading)
        self.rect = self.image.get_rect(center=self.rect.center)

        self.age += dt
        self.state -= (self.activity * 0.5) * dt
        if self.state <= death_threshold:
            self.kill()

    def eat(self):
        self.state = min(self.state + 1, split_threshold)
        self.food_eaten += 1

    def should_split(self):
        return self.food_eaten >= self.split_threshold

    def mutate(self):
        self.width = max(1, self.width + random.randint(-mutation_intensity, mutation_intensity))
        self.height = max(1, self.height + random.randint(-mutation_intensity, mutation_intensity))
        self.speed = max(0.1, self.speed + random.uniform(-mutation_intensity, mutation_intensity))
        self.activity = max(0.01, min(1, self.activity + random.uniform(-mutation_intensity/100, mutation_intensity/100)))
        self.original_image = pygame.Surface([self.width, self.height])
        self.original_image.fill(self.color)
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=self.rect.center)

class RedCreature(Creature):
    def __init__(self):
        super().__init__(RED, red_creature_width, red_creature_height, red_creature_speed, red_creature_activity, red_split_threshold)

    def update(self, dt):
        super().update(dt)
        self.state -= red_hunger_rate * dt
        if self.age > red_max_age:
            self.kill()

    def eat_black_creature(self):
        self.state = min(self.state + 3, split_threshold)
        self.food_eaten += 1

class BlackCreature(Creature):
    def __init__(self):
        super().__init__(BLACK, black_creature_width, black_creature_height, black_creature_speed, black_creature_activity, black_split_threshold)

    def update(self, dt):
        super().update(dt)
        self.state -= black_hunger_rate * dt
        if self.age > black_max_age:
            self.kill()

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([food_width, food_height])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - food_width)
        self.rect.y = random.randint(0, screen_height - food_height)

black_creatures = pygame.sprite.Group()
red_creatures = pygame.sprite.Group()
all_creatures = pygame.sprite.Group()
food_group = pygame.sprite.Group()

for i in range(initial_red_creatures):
    red_creature = RedCreature()
    red_creatures.add(red_creature)
    all_creatures.add(red_creature)

for i in range(initial_black_creatures):
    black_creature = BlackCreature()
    black_creatures.add(black_creature)
    all_creatures.add(black_creature)

for i in range(initial_food_count):
    food = Food()
    food_group.add(food)

running = True
clock = pygame.time.Clock()
food_spawn_timer = 0

# 시뮬레이션 시작 시간
start_time = time.time()
while running:
    dt = clock.tick(FPS) / 1000.0  # 초 단위의 델타 시간

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_creatures.update(dt)

    # 먹이와 충돌 처리 (까망이만)
    for creature in black_creatures:
        collided_food = pygame.sprite.spritecollide(creature, food_group, True)
        for food in collided_food:
            creature.eat()

        if creature.should_split():
            new_creature = BlackCreature()
            new_creature.mutate()  # 돌연변이 적용
            new_creature.rect.x = max(0, min(screen_width - new_creature.rect.width, creature.rect.x + random.randint(-20, 20)))
            new_creature.rect.y = max(0, min(screen_height - new_creature.rect.height, creature.rect.y + random.randint(-20, 20)))
            black_creatures.add(new_creature)
            all_creatures.add(new_creature)
            creature.food_eaten = 0  # 분열 후 먹이 카운트 리셋

    # 빨강이와 까망이의 충돌 처리
    for red_creature in red_creatures:
        collided_black_creatures = pygame.sprite.spritecollide(red_creature, black_creatures, True)
        for black_creature in collided_black_creatures:
            all_creatures.remove(black_creature)
            red_creature.eat_black_creature()

        if red_creature.should_split():
            new_creature = RedCreature()
            new_creature.mutate()  # 돌연변이 적용
            new_creature.rect.x = max(0, min(screen_width - new_creature.rect.width, red_creature.rect.x + random.randint(-20, 20)))
            new_creature.rect.y = max(0, min(screen_height - new_creature.rect.height, red_creature.rect.y + random.randint(-20, 20)))
            red_creatures.add(new_creature)
            all_creatures.add(new_creature)
            red_creature.food_eaten = 0  # 분열 후 먹이 카운트 리셋

    # 새로운 먹이 생성
    food_spawn_timer += dt
    if food_spawn_timer >= 1 / food_spawn_rate:
        if len(food_group) < max_food:
            food = Food()
            food_group.add(food)
        food_spawn_timer = 0

    screen.fill(WHITE)
    all_creatures.draw(screen)
    food_group.draw(screen)
    
    # 현재 총 개체 수 표시
    total_creatures = len(all_creatures)
    red_count = len(red_creatures)
    black_count = len(black_creatures)
    food_count = len(food_group)
    total_creatures_text = font.render(f"Total: {total_creatures} (Red: {red_count}, Black: {black_count})", True, BLACK)
    screen.blit(total_creatures_text, (10, 10))
    
    # 먹이 수 표시
    food_count_text = font.render(f"Food: {food_count}", True, BLACK)
    screen.blit(food_count_text, (10, 50))
    
    # 경과 시간 표시
    elapsed_time = time.time() - start_time
    elapsed_time_text = font.render(f"Elapsed Time: {int(elapsed_time)}s", True, BLACK)
    screen.blit(elapsed_time_text, (10, 90))

    pygame.display.flip()

pygame.quit()
