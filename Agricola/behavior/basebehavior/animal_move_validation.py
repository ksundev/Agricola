"""
동물의 이동을 검증하는 클래스
:param: 필드 객체 배열 (7*11), 포지션(3*5 기준)
:return: 동물의 이동 가능 여부
"""
from collections import deque
from copy import deepcopy

from behavior.behavior import Behavior
from entity.animal_type import AnimalType
from entity.field_type import FieldType


class AnimalMoveValidation(Behavior):
    def __init__(self, field_status, animal_type, position):
        self.field_status = deepcopy(field_status)
        self.animal_type = animal_type
        self.position = position
        self.log_text = None

    def execute(self):
        return self.check_already_placed() and self.check_same_type()

    def check_already_placed(self):
        if self.field_status[self.position[0] * 2 + 1][self.position[1] * 2 + 1].field_type != FieldType.NONE_FIELD \
                and self.field_status[self.position[0] * 2 + 1][self.position[1] * 2 + 1].field_type != FieldType.CAGE:
            self.log_text = "다른 구조물 위에 동물을 놓을 수 없습니다."
            return False
        return True

    def check_same_type(self):
        check = [[0 for i in range(11)] for j in range(7)]
        queue = deque()
        check[self.position[0]][self.position[1]] = 1
        queue.append((self.position[0], self.position[1]))
        while queue:
            x, y = queue.popleft()
            dx = [0, 0, -1, 1]
            dy = [-1, 1, 0, 0]
            for i in range(4):
                p = x + dx[i]
                q = y + dy[i]
                r = p + dx[i]
                s = q + dy[i]
                if 7 > r >= 0 == check[r][s] and 0 <= s < 11 \
                        and self.field_status[p][q].field_type != FieldType.FENCE:
                    if self.field_status[r][s].kind != AnimalType.NONE \
                            and self.field_status[r][s].kind != self.animal_type:
                        self.log_text = "한 울타리 안에는 서로 다른 종류의 동물이 존재할 수 없습니다."
                        return False
                    check[r][s] = 1
                    queue.append((r, s))
        return True

    def log(self):
        return self.log_text


"""
1. 집, 밭, 다른 동물이 존재하는 곳 여부
2. 동물 같은 종류 여부
"""
