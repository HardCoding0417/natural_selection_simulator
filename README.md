# 자연선택 시뮬레이터 (Natural Selection Simulator)

자연선택을 모델링한 생태계 시뮬레이션 프로젝트입니다.  

## 사용 기술
Python, Pygame

## 학습 목적

1. 프로그래밍을 통해 복잡한 시스템을 모델링하는 방법을 학습
2. 데이터 시각화를 경험
3. 자연선택 이해하기

## 시작하기

필요한 라이브러리 설치:

```bash
pip install pygame
```

## 버전별 특징 및 주요 포인트

### game_v1: 기본 모델
- **구성**: 피식자(까망이)와 포식자(빨강이) 간의 상호작용
- **특징**: 
  - 까망이는 번식하고, 빨강이는 까망이를 잡아먹음
  - 번식 시 랜덤으로 크기, 속도, 활동량 등의 수치가 변화
- **관찰 포인트**: 
  - 시간이 지남에 따라 생존에 유리한 특성을 가진 까망이의 비율 변화

### game_v2: 먹이 개념 도입
- **새로운 요소**: 
  - 까망이가 먹이를 먹는 메커니즘 추가
  - 까망이는 일정량의 먹이를 먹어야 번식 가능
- **관찰 포인트**: 
  - 먹이를 잘 먹는 능력과 포식자를 피하는 능력 사이의 균형
  - 어떤 전략이 더 효과적인지 관찰 (잘 먹기 vs 안 잡아먹히기)

### game_v3: 포식자 진화와 허기 개념
- **확장 사항**: 
  - 빨강이(포식자)도 진화 과정에 참여
  - 허기 개념 도입: 빨강이가 일정 시간 동안 먹이를 못 먹으면 굶어 죽음
- **관찰 포인트**: 
  - 피식자와 포식자의 공진화 과정
  - 포식 성공률에 따른 포식자 개체군의 변화

### game_v4: 유전적 연속성 강화
- **새로운 메커니즘**: 
  - 형질변화계수 도입으로 부모의 특성이 자손에게 더 많이 보존됨
  - 까망이의 행동 패턴을 더 생명체와 유사하게 개선
  - 빨강이에 대한 반응(접근 또는 회피)을 유전적 특성으로 결정
- **관찰 포인트**: 
  - 세대를 거치며 나타나는 뚜렷한 행동 패턴 (겁쟁이 vs 모험가)
  - 유전적 다양성과 환경 적응의 관계

### game_v5: 복합적 생존 전략
- **시스템 개선**: 
  - 회피 능력을 더 복잡하게 구현 (회피력 단순 증가가 항상 유리하지 않도록)
  - 속도와 허기의 관계 구현: 빠른 속도는 더 많은 에너지 소모
  - 회피 관련 파라미터를 3개로 세분화
- **관찰 포인트**: 
  - 다양한 생존 전략의 출현과 그 효과
  - 복잡한 환경에서의 최적 전략 탐색

## 기여 방법

Pull Request를 통해 프로젝트에 참여해 주세요.
