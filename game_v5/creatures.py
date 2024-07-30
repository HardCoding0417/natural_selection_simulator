import numpy as np
import pygame
import random
import time
import math
from constants import *

class Gene:
    def __init__(self, values=None):
        if values is None:
            self.values = np.random.rand(GENE_LENGTH)
        else:
            self.values = values.copy()
        
        # 유전적 특성 정의
        self.width = self.values[0]
        self.height = self.values[1]
        self.speed = self.values[2]
        self.activity = self.values[3]
        self.split_threshold = self.values[4]
        self.food_attraction = self.values[5]
        self.predator_fear = self.values[6]
        self.prey_attraction = self.values[7]
        self.wanderlust = self.values[8]
        # 새로운 회피 관련 유전자
        self.evasion_speed = self.values[9]
        self.evasion_reaction = self.values[10]
        self.evasion_direction_change = self.values[11]

    def mutate(self):
        for i in range(GENE_LENGTH):
            if random.random() < MUTATION_RATE:
                self.values[i] += random.uniform(-0.1, 0.1)
                self.values[i] = max(0, min(1, self.values[i]))
        
        # 유전적 특성 업데이트
        self.width = self.values[0]
        self.height = self.values[1]
        self.speed = self.values[2]
        self.activity = self.values[3]
        self.split_threshold = self.values[4]
        self.food_attraction = self.values[5]
        self.predator_fear = self.values[6]
        self.prey_attraction = self.values[7]
        self.wanderlust = self.values[8]
        self.evasion_speed = self.values[9]
        self.evasion_reaction = self.values[10]
        self.evasion_direction_change = self.values[11]


class Creature(pygame.sprite.Sprite):
    def __init__(self, *, color, base_width, base_height, base_speed, base_activity, base_split_threshold, genes=None):
        super().__init__()
        self.color = color
        self.genes = Gene() if genes is None else genes
        self.base_width = base_width
        self.base_height = base_height
        self.base_speed = base_speed
        self.base_activity = base_activity  # 새로 추가된 속성
        self.width = int(self.base_width * (0.5 + self.genes.width))
        self.height = int(self.base_height * (0.5 + self.genes.height))
        self.max_speed = self.base_speed * (0.5 + self.genes.speed)
        self.current_speed = 0
        self.activity = self.base_activity * (0.5 + self.genes.activity)
        self.split_threshold = base_split_threshold * (0.5 + self.genes.split_threshold)
        self.original_image = pygame.Surface([self.width, self.height])
        self.original_image.fill(color)
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.height)
        self.heading = random.uniform(0, 360)
        self.target_heading = self.heading
        self.change_direction_time = time.time() + random.uniform(1, 10) * (1 - self.activity)
        self.state = INITIAL_STATE
        self.food_eaten = 0
        self.age = 0
        self.last_rotation = self.heading

    def calculate_hunger_rate(self):
        size_factor = ((self.width * self.height) / (self.base_width * self.base_height) - 1) * SIZE_HUNGER_FACTOR
        speed_factor = (self.max_speed / self.base_speed - 1) * SPEED_HUNGER_FACTOR
        activity_factor = (self.activity / self.base_activity - 1) * ACTIVITY_HUNGER_FACTOR
        
        return 1 + size_factor + speed_factor + activity_factor

    def update(self, dt, all_creatures, food_group):
        self.age += dt
        hunger_rate = self.calculate_hunger_rate()
        self.state -= (self.activity * 0.5 * hunger_rate) * dt
        if self.state <= DEATH_THRESHOLD:
            self.kill()
            return

        food_vector = self.calculate_attraction_vector(food_group, self.genes.food_attraction)
        wanderlust_vector = self.calculate_wanderlust_vector()
        
        if isinstance(self, RedCreature):
            prey_vector = self.calculate_attraction_vector([c for c in all_creatures if isinstance(c, BlackCreature)], self.genes.prey_attraction)
            total_vector = food_vector + wanderlust_vector + prey_vector
        elif isinstance(self, BlackCreature):
            predator_vector = self.calculate_repulsion_vector([c for c in all_creatures if isinstance(c, RedCreature)], self.genes.predator_fear)
            total_vector = food_vector + wanderlust_vector + predator_vector

        if np.linalg.norm(total_vector) > 0:
            self.target_heading = math.degrees(math.atan2(total_vector[1], total_vector[0])) % 360

        self.rotate_towards_target(dt)
        self.accelerate(dt)
        self.move(dt)


    def calculate_attraction_vector(self, group, attraction_strength):
        vector = np.zeros(2)
        for item in group:
            dx = item.rect.centerx - self.rect.centerx
            dy = item.rect.centery - self.rect.centery
            distance = math.hypot(dx, dy)
            if distance > 0:
                vector += np.array([dx, dy]) / (distance ** 2)
        return vector * attraction_strength

    def calculate_repulsion_vector(self, group, repulsion_strength):
        return -self.calculate_attraction_vector(group, repulsion_strength)

    def calculate_wanderlust_vector(self):
        angle = random.uniform(0, 2 * math.pi)
        return np.array([math.cos(angle), math.sin(angle)]) * self.genes.wanderlust

    def rotate_towards_target(self, dt):
        angle_diff = (self.target_heading - self.heading + 180) % 360 - 180
        rotation_speed = 180 * dt  # 초당 180도 회전
        if abs(angle_diff) < rotation_speed:
            self.heading = self.target_heading
        else:
            self.heading += math.copysign(rotation_speed, angle_diff)
        self.heading %= 360

    def accelerate(self, dt):
        if self.current_speed < self.max_speed:
            self.current_speed = min(self.max_speed, self.current_speed + self.max_speed * dt)
        elif self.current_speed > self.max_speed:
            self.current_speed = max(self.max_speed, self.current_speed - self.max_speed * dt)

    def move(self, dt):
        dx = self.current_speed * dt * math.cos(math.radians(self.heading))
        dy = self.current_speed * dt * math.sin(math.radians(self.heading))
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy

        if new_x <= 0 or new_x >= SCREEN_WIDTH - self.rect.width:
            self.heading = (180 - self.heading) % 360
            self.target_heading = self.heading
        if new_y <= 0 or new_y >= SCREEN_HEIGHT - self.rect.height:
            self.heading = (-self.heading) % 360
            self.target_heading = self.heading

        self.rect.x = max(0, min(SCREEN_WIDTH - self.rect.width, new_x))
        self.rect.y = max(0, min(SCREEN_HEIGHT - self.rect.height, new_y))

        if abs(self.heading - self.last_rotation) > 1:
            rotated_image = pygame.transform.rotate(self.original_image, -self.heading)
            self.image = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
            self.image.blit(rotated_image, (self.width / 2 - rotated_image.get_width() / 2,
                                            self.height / 2 - rotated_image.get_height() / 2))
            self.rect = self.image.get_rect(center=self.rect.center)
            self.last_rotation = self.heading

    def eat(self):
        self.state = min(self.state + 1, SPLIT_THRESHOLD)
        self.food_eaten += 1

    def should_split(self):
        return self.food_eaten >= self.split_threshold

    def reproduce(self):
        child_genes = Gene(self.genes.values)
        child_genes.mutate()
        return self.__class__(color=self.color, 
                              base_width=self.base_width, 
                              base_height=self.base_height, 
                              base_speed=self.max_speed / (0.5 + self.genes.speed), 
                              base_activity=self.activity / (0.5 + self.genes.activity), 
                              base_split_threshold=self.split_threshold / (0.5 + self.genes.split_threshold), 
                              genes=child_genes)

class RedCreature(Creature):
    def __init__(self, *, base_width=RED_CREATURE_WIDTH, 
                 base_height=RED_CREATURE_HEIGHT, 
                 base_speed=RED_CREATURE_SPEED, 
                 base_activity=RED_CREATURE_ACTIVITY, 
                 base_split_threshold=RED_SPLIT_THRESHOLD, 
                 genes=None, **kwargs):
        super().__init__(color=RED, 
                         base_width=base_width, 
                         base_height=base_height, 
                         base_speed=base_speed, 
                         base_activity=base_activity, 
                         base_split_threshold=base_split_threshold, 
                         genes=genes)

    def update(self, dt, all_creatures, food_group):
        super().update(dt, all_creatures, food_group)
        hunger_rate = self.calculate_hunger_rate()
        self.state -= RED_HUNGER_RATE * dt * (2 - self.genes.values[3]) * hunger_rate
        if self.age > RED_MAX_AGE * self.genes.values[4]:
            self.kill()

    def eat_black_creature(self):
        self.state = min(self.state + 3 * self.genes.values[2], SPLIT_THRESHOLD)
        self.food_eaten += 1

class BlackCreature(Creature):
    def __init__(self, *, base_width=BLACK_CREATURE_WIDTH, 
                 base_height=BLACK_CREATURE_HEIGHT, 
                 base_speed=BLACK_CREATURE_SPEED, 
                 base_activity=BLACK_CREATURE_ACTIVITY, 
                 base_split_threshold=BLACK_SPLIT_THRESHOLD, 
                 genes=None, **kwargs):
        super().__init__(color=BLACK, 
                         base_width=base_width, 
                         base_height=base_height, 
                         base_speed=base_speed, 
                         base_activity=base_activity, 
                         base_split_threshold=base_split_threshold, 
                         genes=genes)
        self.evading = False
        self.evasion_cooldown = 0

    def update(self, dt, all_creatures, food_group):
        super().update(dt, all_creatures, food_group)
        hunger_rate = self.calculate_hunger_rate()
        self.state -= BLACK_HUNGER_RATE * dt * (2 - self.genes.activity) * hunger_rate
        if self.age > BLACK_MAX_AGE * (0.5 + self.genes.split_threshold):
            self.kill()

        # 회피 로직
        if self.evasion_cooldown > 0:
            self.evasion_cooldown -= dt
        else:
            nearby_predators = [c for c in all_creatures if isinstance(c, RedCreature) and 
                                math.hypot(c.rect.centerx - self.rect.centerx, 
                                           c.rect.centery - self.rect.centery) < PREDATOR_DETECTION_RANGE]
            if nearby_predators and random.random() < self.genes.evasion_reaction:
                self.evade(nearby_predators[0])

    def evade(self, predator):
        self.evading = True
        self.evasion_cooldown = EVASION_COOLDOWN

        # 포식자로부터 도망가는 방향 계산
        dx = self.rect.centerx - predator.rect.centerx
        dy = self.rect.centery - predator.rect.centery
        
        # 회피 방향에 무작위성 추가
        angle = math.atan2(dy, dx) + random.uniform(-math.pi/4, math.pi/4) * self.genes.evasion_direction_change
        
        self.target_heading = math.degrees(angle) % 360
        
        # 회피 속도 증가
        self.current_speed = self.max_speed * (1 + self.genes.evasion_speed)

    def move(self, dt):
        if self.evading:
            # 회피 중일 때 더 빠르게 회전
            self.rotate_towards_target(dt * (1 + self.genes.evasion_reaction))
            
            # 일정 시간 후 회피 종료
            if self.evasion_cooldown <= 0:
                self.evading = False
                self.current_speed = self.max_speed

        super().move(dt)


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([FOOD_WIDTH, FOOD_HEIGHT])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - FOOD_WIDTH)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - FOOD_HEIGHT)