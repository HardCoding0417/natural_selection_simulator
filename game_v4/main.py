import pygame
import random
import time
from typing import List, Union
from dataclasses import dataclass
from creatures import RedCreature, BlackCreature, Food
from stats import PopulationStats
from constants import *

pygame.init()


@dataclass
class SimulationState:
    screen: pygame.Surface
    font: pygame.font.Font
    black_creatures: pygame.sprite.Group
    red_creatures: pygame.sprite.Group
    all_creatures: pygame.sprite.Group
    food_group: pygame.sprite.Group
    red_stats: PopulationStats
    black_stats: PopulationStats
    start_time: float
    game_speed_multiplier: float
    show_info: bool  # 새로운 필드: 정보창 표시 여부

def initialize_simulation() -> SimulationState:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('자연 선택 시뮬레이터')
    font = pygame.font.SysFont(None, 36)  # 폰트 크기를 24로 변경

    black_creatures = pygame.sprite.Group()
    red_creatures = pygame.sprite.Group()
    all_creatures = pygame.sprite.Group()
    food_group = pygame.sprite.Group()

    for _ in range(INITIAL_RED_CREATURES):
        spawn_new_creature(RedCreature(), red_creatures, all_creatures)

    for _ in range(INITIAL_BLACK_CREATURES):
        spawn_new_creature(BlackCreature(), black_creatures, all_creatures)

    for _ in range(INITIAL_FOOD_COUNT):
        food_group.add(Food())

    return SimulationState(
        screen, font, black_creatures, red_creatures, all_creatures, food_group,
        PopulationStats(), PopulationStats(), time.time(), 1.0, False  # show_info를 False로 초기화
    )

def spawn_new_creature(creature: Union[RedCreature, BlackCreature], group: pygame.sprite.Group, all_creatures: pygame.sprite.Group):
    new_creature = creature.reproduce()
    group.add(new_creature)
    all_creatures.add(new_creature)
    creature.food_eaten = 0


def handle_events(state: SimulationState) -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                state.game_speed_multiplier = min(MAX_GAME_SPEED_MULTIPLIER, state.game_speed_multiplier + SPEED_CHANGE_RATE)
            elif event.key == pygame.K_w:
                state.game_speed_multiplier = max(MIN_GAME_SPEED_MULTIPLIER, state.game_speed_multiplier - SPEED_CHANGE_RATE)
            elif event.key == pygame.K_i:  # 'i' 키를 누르면 정보창 토글
                state.show_info = not state.show_info
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 좌클릭
                # 정보창 토글 버튼 영역 (우측 상단)
                if SCREEN_WIDTH - 100 <= event.pos[0] <= SCREEN_WIDTH and 0 <= event.pos[1] <= 30:
                    state.show_info = not state.show_info
    return True

def update_creatures(state: SimulationState, dt: float):
    for creature in state.all_creatures:
        creature.update(dt, state.all_creatures, state.food_group)
        
        if isinstance(creature, BlackCreature):
            state.black_stats.add_creature(creature)
            collided_food = pygame.sprite.spritecollide(creature, state.food_group, True)
            for _ in collided_food:
                creature.eat()
            if creature.should_split():
                spawn_new_creature(creature, state.black_creatures, state.all_creatures)
        
        elif isinstance(creature, RedCreature):
            state.red_stats.add_creature(creature)
            collided_black_creatures = pygame.sprite.spritecollide(creature, state.black_creatures, True)
            for black_creature in collided_black_creatures:
                state.all_creatures.remove(black_creature)
                creature.eat_black_creature()
            if creature.should_split():
                spawn_new_creature(creature, state.red_creatures, state.all_creatures)

def spawn_food(state: SimulationState, dt: float, food_spawn_timer: float) -> float:
    food_spawn_timer += dt
    if food_spawn_timer >= 1 / FOOD_SPAWN_RATE:
        if len(state.food_group) < MAX_FOOD:
            state.food_group.add(Food())
        food_spawn_timer = 0
    return food_spawn_timer




def update_display(state: SimulationState):
    state.screen.fill(WHITE)
    state.all_creatures.draw(state.screen)
    state.food_group.draw(state.screen)
    
    # 정보창 토글 버튼 그리기
    pygame.draw.rect(state.screen, LIGHT_GRAY, (SCREEN_WIDTH - 100, 0, 100, 30))
    button_text = state.font.render("Toggle Info", True, BLACK)
    state.screen.blit(button_text, (SCREEN_WIDTH - 95, 5))
    
    if state.show_info:
        red_cv = state.red_stats.calculate_cv()
        black_cv = state.black_stats.calculate_cv()
        
        # 메인 정보 (상단)
        main_info = [
            f"Total: {len(state.all_creatures)} (Red: {len(state.red_creatures)}, Black: {len(state.black_creatures)})",
            f"Food: {len(state.food_group)}",
            f"Elapsed Time: {int((time.time() - state.start_time) * state.game_speed_multiplier)}s",
            f"Game Speed: x{state.game_speed_multiplier:.2f}"
        ]
        
        cv_labels = [
            "Width", "Height", "Speed", "Activity", "Split Threshold", 
            "Food Attraction", "Predator Fear", "Prey Attraction", "Wanderlust",
            "Evasion Speed", "Evasion Reaction", "Evasion Direction Change"
        ]
        
        # 블랙 CV 정보 (좌측 하단)
        black_cv_text = ["Black CV:"] + [f"{label}: {value:.2f}" for label, value in zip(cv_labels, black_cv.values())]
        
        # 레드 CV 정보 (우측 하단)
        red_cv_text = ["Red CV:"] + [f"{label}: {value:.2f}" for label, value in zip(cv_labels, red_cv.values())]
        
        # 반투명한 배경 그리기
        info_surface = pygame.Surface((SCREEN_WIDTH, 30 * len(main_info)))
        info_surface.set_alpha(200)
        info_surface.fill(LIGHT_GRAY)
        state.screen.blit(info_surface, (0, 0))
        
        cv_surface = pygame.Surface((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        cv_surface.set_alpha(200)
        cv_surface.fill(LIGHT_GRAY)
        state.screen.blit(cv_surface, (0, SCREEN_HEIGHT // 2))
        state.screen.blit(cv_surface, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        
        # 메인 정보 그리기
        for i, text in enumerate(main_info):
            text_surface = state.font.render(text, True, BLACK)
            state.screen.blit(text_surface, (10, 5 + i * 25))
        
        # 블랙 CV 정보 그리기
        for i, text in enumerate(black_cv_text):
            text_surface = state.font.render(text, True, BLACK)
            state.screen.blit(text_surface, (10, SCREEN_HEIGHT // 2 + 5 + i * 20))
        
        # 레드 CV 정보 그리기
        for i, text in enumerate(red_cv_text):
            text_surface = state.font.render(text, True, BLACK)
            state.screen.blit(text_surface, (SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 + 5 + i * 20))

    pygame.display.flip()

def main():
    state = initialize_simulation()
    running = True
    clock = pygame.time.Clock()
    food_spawn_timer = 0

    while running:
        base_dt = clock.tick(FPS) / 1000.0
        dt = base_dt * state.game_speed_multiplier

        running = handle_events(state)

        state.red_stats.reset()
        state.black_stats.reset()

        update_creatures(state, dt)
        food_spawn_timer = spawn_food(state, dt, food_spawn_timer)
        update_display(state)

    pygame.quit()

if __name__ == "__main__":
    main()