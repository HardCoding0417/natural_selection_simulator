### 기본 게임 ###

# 까망이는 번식하고 빨강이는 까망이를 잡아먹습니다.

# generation_interval마다 까망이가 번식하는데,
# 이 때 랜덤으로 크기, 속도, 활동량 등의 수치가 변합니다.
# 시간이 지나면 적절한 파라미터를 가진 까망이들이 대다수가 됩니다.


import pygame
import random
import time

# Pygame 초기화
pygame.init()

# 화면 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('자연 선택 시뮬레이터')

# 색상 정의
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# 폰트 설정
font = pygame.font.SysFont(None, 36)

# 하이퍼파라미터 설정

# 초기 크리쳐 수
initial_red_creatures = 5
initial_black_creatures = 50

# 초기 크리쳐 스펙
red_creature_size = 20
black_creature_size = 20
red_creature_speed = 10
black_creature_speed = 10
red_creature_activity = 0.1
black_creature_activity = 0.05

# 세대 
generation_interval = 3

# 최대 생물체 수
max_creatures = 300

# 생물체 클래스 정의
class Creature(pygame.sprite.Sprite):
    def __init__(self, color, size, speed, activity):
        super().__init__()
        self.image = pygame.Surface([size, size])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - size)
        self.rect.y = random.randint(0, screen_height - size)
        self.speed = speed
        self.activity = activity
        self.direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.change_direction_time = time.time() + random.uniform(1, 10) * (1 - self.activity)

    def update(self):
        current_time = time.time()
        if current_time >= self.change_direction_time:
            self.direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
            self.change_direction_time = current_time + random.uniform(1, 10) * (1 - self.activity)

        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        # 벽에 부딪히면 방향 반대로
        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.direction.x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            self.direction.y *= -1

        self.rect.x = max(0, min(screen_width - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(screen_height - self.rect.height, self.rect.y))

# 변수 설정
black_creatures = pygame.sprite.Group()
red_creatures = pygame.sprite.Group()
all_creatures = pygame.sprite.Group()

# 초기 생물체 생성
for i in range(initial_red_creatures):
    red_creature = Creature(RED, red_creature_size, red_creature_speed, red_creature_activity)
    red_creatures.add(red_creature)
    all_creatures.add(red_creature)

for i in range(initial_black_creatures):
    black_creature = Creature(BLACK, black_creature_size, black_creature_speed, black_creature_activity)
    black_creatures.add(black_creature)
    all_creatures.add(black_creature)

# 시뮬레이션 루프
running = True
last_split_time = time.time()
generation = 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 까망이 분열
    current_time = time.time()
    if current_time - last_split_time > generation_interval:
        last_split_time = current_time
        generation += 1
        if len(all_creatures) < max_creatures:
            for creature in list(black_creatures):
                if len(all_creatures) >= max_creatures:
                    break
                new_size = max(5, creature.rect.width + random.randint(-2, 2))
                new_speed = max(1, creature.speed + random.randint(-1, 1))
                new_activity = max(0.01, min(1, creature.activity + random.uniform(-0.01, 0.01)))
                new_creature = Creature(BLACK, new_size, new_speed, new_activity)
                black_creatures.add(new_creature)
                all_creatures.add(new_creature)

    # 업데이트
    all_creatures.update()

    # 충돌 감지 및 삭제
    for red in red_creatures:
        collided = pygame.sprite.spritecollide(red, black_creatures, True)
        if collided:
            for creature in collided:
                all_creatures.remove(creature)

    # 화면 그리기
    screen.fill(WHITE)
    all_creatures.draw(screen)
    
    # 세대 수 표시
    generation_text = font.render(f"Generation: {generation}", True, BLACK)
    screen.blit(generation_text, (10, 10))

    pygame.display.flip()

    # FPS 조절
    pygame.time.Clock().tick(30)

pygame.quit()
