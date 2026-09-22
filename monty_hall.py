"""
Monty Hall Problem Simulation
확률과 통계 과제 - Stay 전략과 Switch 전략의 승률을 시뮬레이션으로 비교한다.
"""

import random

# 시뮬레이션 횟수 (필요하면 이 값만 바꾸면 된다)
NUM_SIMULATIONS = 10000

# 문의 개수는 3개로 고정 (0, 1, 2번 문)
DOORS = [0, 1, 2]


def play_one_round(switch: bool) -> bool:
    """
    Monty Hall 게임을 한 번 진행한다.
    switch=True 이면 Switch 전략, switch=False 이면 Stay 전략을 사용한다.
    최종 선택한 문에 자동차가 있으면 True(승리), 아니면 False(패배)를 반환한다.
    """

    # 1. 자동차를 세 문 중 하나에 무작위로 배치한다.
    car_door = random.choice(DOORS)

    # 2. 플레이어가 세 문 중 하나를 무작위로 선택한다.
    player_choice = random.choice(DOORS)

    # 3. 사회자는 "플레이어가 고르지 않았고, 자동차도 없는 문" 중에서 하나를 공개한다.
    #    -> 자동차가 있는 문과 플레이어가 고른 문은 절대 공개하지 않는다.
    revealable_doors = [
        door for door in DOORS
        if door != player_choice and door != car_door
    ]
    revealed_door = random.choice(revealable_doors)

    # 4. Stay 전략: 처음 선택을 그대로 유지한다.
    #    Switch 전략: 처음 선택과 공개된 문을 제외한 나머지 문으로 바꾼다.
    if switch:
        final_choice = [
            door for door in DOORS
            if door != player_choice and door != revealed_door
        ][0]
    else:
        final_choice = player_choice

    # 5. 최종 선택한 문 뒤에 자동차가 있는지 확인한다.
    return final_choice == car_door


def run_simulation(switch: bool, num_trials: int) -> int:
    """주어진 전략(switch)으로 num_trials번 게임을 반복하고, 승리 횟수를 반환한다."""
    wins = 0
    for _ in range(num_trials):
        if play_one_round(switch):
            wins += 1
    return wins


def main():
    # Stay 전략 시뮬레이션
    stay_wins = run_simulation(switch=False, num_trials=NUM_SIMULATIONS)

    # Switch 전략 시뮬레이션
    switch_wins = run_simulation(switch=True, num_trials=NUM_SIMULATIONS)

    # 승률을 백분율(%)로 계산
    stay_rate = stay_wins / NUM_SIMULATIONS * 100
    switch_rate = switch_wins / NUM_SIMULATIONS * 100

    # 결과 출력
    print(f"전체 시뮬레이션 횟수: {NUM_SIMULATIONS}회")
    print()
    print(f"[Stay 전략]   승리 횟수: {stay_wins}회 / 승률: {stay_rate:.2f}%")
    print(f"[Switch 전략] 승리 횟수: {switch_wins}회 / 승률: {switch_rate:.2f}%")


if __name__ == "__main__":
    main()
