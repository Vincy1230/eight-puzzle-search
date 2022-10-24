"""
-** eight_puzzle_search **-
--------------------------------------------
crate_date: 2022-10-16
update_date: 2022-10-24
author: Vincent SHI | 史文朔
blog: https://blog.vincent1230.top/
--------------------------------------------
"""
import warnings
from functools import wraps
from time import process_time
from typing import *


class Box:
    """
    Box(value: List[int], history: str = '') -> 'Box'

    八数码问题处理的九宫格对象 | Box object for 8-puzzle problem
    >> value: 九宫格对象的值 | value of Box object
    >> history: 九宫格对象的移动历史 | history of Box object
    << 实例化新的九宫格对象 | new Box object
    """

    def __init__(self, value: List[int], history: str = '') -> None:
        if len(value) != 9 or set(value) != {0, 1, 2, 3, 4, 5, 6, 7, 8}:
            raise ValueError(
                '输入值必须是由 0-8 组成的 9 位整数列表 | value must be a list of 9 int in 0-8')
        if history[:3] == '-> ':
            history = history[3:]
        elif history[:2] == '->':
            history = history[2:]
        if set(history) - {'U', 'D', 'L', 'R'}:
            raise ValueError(
                "历史记录只能含有 'U', 'D', 'L' 和 'R' | history can only contain 'U', 'D', 'L' and 'R'")
        self._value = value
        self._history = history
        self._zero = self._value.index(0)

    def __repr__(self):
        """九宫格对象的格式化输出 | formatted output of Box object"""
        return 'moved via -> {}:\n[ {} {} {}\n  {} {} {}\n  {} {} {} ]\n'.format(
            self._history, *[i if i != 0 else '*' for i in self._value])

    @property
    def value(self) -> List[int]:
        """
        'Box'.value -> list[int]

        九宫格对象的值 | value of Box object
        """
        return self._value

    def set_value(self, value: List[int]) -> None:
        """
        'Box'.set_value(value: list[int]) -> None

        修改当前九宫格对象的值而不改变其历史记录 | change value of Box object without change history
        >> value: 新的值 | new value
        """
        if len(value) != 9 or set(value) != {0, 1, 2, 3, 4, 5, 6, 7, 8}:
            raise ValueError(
                '输入值必须是由 0-8 组成的 9 位整数列表 | value must be a list of 9 int in 0-8')
        self._value = value
        self._zero = self._value.index(0)
        # 警告: set_value 方法不会改变历史记录 | Warning: set_value method will not change history
        warnings.warn(
            'set_value 方法不会改变历史记录 | set_value method will not change history', SyntaxWarning)

    @property
    def history(self) -> str:
        """
        'Box'.history -> str

        九宫格对象的移动历史 | history of Box object
        """
        return self._history

    def add_history(self, history: str) -> None:
        """
        'Box'.add_history(history: str) -> None

        添加历史记录而不改变九宫格对象的值 | add history without change value of Box object
        >> history: 新的历史记录 | new history
        """
        if set(history) - {'U', 'D', 'L', 'R'}:
            raise ValueError(
                "历史记录只能含有 'U', 'D', 'L' 和 'R' | history can only contain 'U', 'D', 'L' and 'R'")
        self._history += history
        # 警告: add_history 方法不会改变九宫格对象的值 | Warning: add_history method will not change value of Box object
        warnings.warn(
            'add_history 方法不会改变九宫格对象的值 | add_history method will not change value of Box object',
            SyntaxWarning)

    def del_history(self, length: int = 1) -> str:
        """
        'Box'.del_history(length: int = 1) -> str

        删除历史记录而不改变九宫格对象的值 | delete history without change value of Box object
        >> length: 删除的长度 | length of deleted history
        << 返回被删除的历史记录 | return deleted history
        """
        if length < 1:
            raise ValueError('length 必须大于 0 | length must be greater than 0')
        if length > len(self._history):
            raise ValueError(
                'length 不能大于历史记录长度 | length cannot be greater than length of history')
        deleted_history = self._history[-length:]
        self._history = self._history[:-length]
        # 警告: del_history 方法不会改变九宫格对象的值 | Warning: del_history method will not change value of Box object
        warnings.warn(
            'del_history 方法不会改变九宫格对象的值 | del_history method will not change value of Box object',
            SyntaxWarning)
        return deleted_history

    def copy(self) -> 'Box':
        """
        'Box'.copy() -> 'Box'

        复制当前的九宫格对象 | copy Box object
        << 返回复制的九宫格对象 | return copied Box object
        """
        return Box(self._value.copy(), self._history)

    def up(self) -> None:
        """
        'Box'.up() -> None

        在当前的九宫格对象内向上移牌 | move up in current Box object
        """
        if self._zero in (6, 7, 8):
            raise ValueError('不能向上移牌 | cannot move up')
        self._value[self._zero], self._value[self._zero +
                                             3] = self._value[self._zero + 3], self._value[self._zero]
        self._zero += 3
        self._history += 'U'

    @property
    def upped(self) -> 'Box':
        """
        'Box'.upped -> 'Box'

        返回向上移牌后的九宫格对象 | return Box object after move up
        """
        if self._zero in (6, 7, 8):
            raise ValueError('不能向上移牌 | cannot move up')
        value = self._value.copy()
        value[self._zero], value[self._zero +
                                 3] = value[self._zero + 3], value[self._zero]
        return Box(value, self._history + 'U')

    def down(self) -> None:
        """
        'Box'.down() -> None

        在当前的九宫格对象内向下移牌 | move down in current Box object
        """
        if self._zero in (0, 1, 2):
            raise ValueError('不能向下移牌 | cannot move down')
        self._value[self._zero], self._value[self._zero -
                                             3] = self._value[self._zero - 3], self._value[self._zero]
        self._zero -= 3
        self._history += 'D'

    @property
    def downed(self) -> 'Box':
        """
        'Box'.downed -> 'Box'

        返回向下移牌后的九宫格对象 | return Box object after move down
        """
        if self._zero in (0, 1, 2):
            raise ValueError('不能向下移牌 | cannot move down')
        value = self._value.copy()
        value[self._zero], value[self._zero -
                                 3] = value[self._zero - 3], value[self._zero]
        return Box(value, self._history + 'D')

    def left(self) -> None:
        """
        'Box'.left() -> None

        在当前的九宫格对象内向左移牌 | move left in current Box object
        """
        if self._zero in (2, 5, 8):
            raise ValueError('不能向左移牌 | cannot move left')
        self._value[self._zero], self._value[self._zero +
                                             1] = self._value[self._zero + 1], self._value[self._zero]
        self._zero += 1
        self._history += 'L'

    @property
    def lefter(self) -> 'Box':
        """
        'Box'.lefter -> 'Box'

        返回向左移牌后的九宫格对象 | return Box object after move left
        """
        if self._zero in (2, 5, 8):
            raise ValueError('不能向左移牌 | cannot move left')
        value = self._value.copy()
        value[self._zero], value[self._zero +
                                 1] = value[self._zero + 1], value[self._zero]
        return Box(value, self._history + 'L')

    def right(self) -> None:
        """
        'Box'.right() -> None

        在当前的九宫格对象内向右移牌 | move right in current Box object
        """
        if self._zero in (0, 3, 6):
            raise ValueError('不能向右移牌 | cannot move right')
        self._value[self._zero], self._value[self._zero -
                                             1] = self._value[self._zero - 1], self._value[self._zero]
        self._zero -= 1
        self._history += 'R'

    @property
    def righter(self) -> 'Box':
        """
        'Box'.righter -> 'Box'

        返回向右移牌后的九宫格对象 | return Box object after move right
        """
        if self._zero in (0, 3, 6):
            raise ValueError('不能向右移牌 | cannot move right')
        value = self._value.copy()
        value[self._zero], value[self._zero -
                                 1] = value[self._zero - 1], value[self._zero]
        return Box(value, self._history + 'R')

    @property
    def able(self) -> Set[str]:
        """
        'Box'.able -> Set[str]

        查询可用的移动方向 | query available move direction
        << 返回可用的移动方向 | return usable move direction
        """
        able = set()
        if self._zero not in (6, 7, 8):
            able.add('U')
        if self._zero not in (0, 1, 2):
            able.add('D')
        if self._zero not in (2, 5, 8):
            able.add('L')
        if self._zero not in (0, 3, 6):
            able.add('R')
        return able

    def expand(self) -> List['Box']:
        """
        'Box'.expand() -> List['Box']

        拓展下一层 | expand next layer
        << 返回新的九宫格对象列表 | return list of new Box object
        """
        new = []
        if self._zero not in (6, 7, 8):
            new.append(self.upped)
        if self._zero not in (0, 1, 2):
            new.append(self.downed)
        if self._zero not in (2, 5, 8):
            new.append(self.lefter)
        if self._zero not in (0, 3, 6):
            new.append(self.righter)
        return new


def input_box(prompt: str = '') -> 'Box':
    """
    input_box(prompt: str = '') -> 'Box'

    交互式输入九宫格对象 | interactive input Box object
    >> prompt: 提示信息 | prompt message
    << 返回新建的九宫格对象 | return new Box object
    """
    _WDICT = {'0': 0, ' ': 0, '': 0, '*': 0, '9': 0, '1': 1,
              '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8}

    def _handle(word: str) -> int:
        try:
            return _WDICT[word]
        except KeyError:
            raise ValueError('无法识别你的输入 | cannot recognize your input')

    value = []
    print(prompt if prompt else '请按提示直接输入数值. 0 或 * 可代表空位. \n'
                                'enter the value directly as prompted. \n0 or * can be used to represent blank.')
    for i in range(1, 4):
        line = input('第 {} 行 | row {}: '.format(i, i))
        if ',' in line:
            line = line.replace(' ', '').split(',')
        elif len(line) == 3:
            pass
        elif ' ' in line:
            line = line.split()
        else:
            raise ValueError('无法识别你的输入 | cannot recognize your input')
        if len(line) == 3:
            value += [_handle(i) for i in line]
        elif len(line) == 4 and line[3] == '':
            value += [_handle(i) for i in line[:3]]
        elif len(line) == 9 and i == 1:
            value += [_handle(i) for i in line]
            break
        else:
            raise ValueError('无法识别你的输入 | cannot recognize your input')
    print('[ {} {} {}\n  {} {} {}\n  {} {} {} ]\n'.format(
        *[i if i != 0 else '*' for i in value]))
    return Box(value)


def search(start: 'Box', end: 'Box', fn: Callable[[Dict[str, any]], int]) -> None:
    """
    search(start: 'Box', end: 'Box', fn: Callable[[Dict[str, any]], int]) -> None

    通用启发式搜索函数 | universal heuristic search function
    >> start: 起始九宫格对象 | start Box object
    >> end: 目标九宫格对象 | end Box object
    >> fn: 启发函数 | evaluation function | fn(task: dict) -> int
    >> >> task: 用于完成评估的基本信息 | basic information for evaluation
    >> >> - task['start']: 求解的起始值 | start value
    >> >> - task['end']: 求解的目标值 | end value
    >> >> - task['now']: 需评价的当前节点的值 | current node value to be evaluated
    >> >> - task['history']: 当前节点的历史记录 | current node history
    >> << 评估得出的搜索代价 | evaluation result of search cost
    """
    goal = end.value
    print('->', start.history)
    if start.value == goal:
        print('起点已在目标状态 | start Box is already in target state')
        print(start)
        return

    def _key(now: 'Box') -> int:
        task = {
            'start': start.value,
            'end': goal,
            'now': now.value,
            'history': now.history
        }
        return fn(task)

    front = [start]
    while front:
        front.sort(key=_key)
        for check in front.pop(0).expand():
            print('->', check.history)
            if check.value == goal:
                print(check)
                return
            front.append(check)


def breadth_first_search(start: 'Box', end: 'Box') -> None:
    """
    breadth_first_search(start: 'Box', end: 'Box') -> None

    宽度优先搜索 | breadth first search
    >> start: 起始九宫格对象 | start Box object
    >> end: 目标九宫格对象 | end Box object
    """
    goal = end.value
    print('->', start.history)
    if start.value == goal:
        print('起点已在目标状态 | start Box is already in target state')
        print(start)
        return

    def _bfs(layer: List['Box']) -> None:
        next_layer = []
        for now in layer:
            for check in now.expand():
                print('->', check.history)
                if check.value == goal:
                    print(check)
                    return
                next_layer.append(check)
        _bfs(next_layer)

    _bfs([start])


def depth_first_search(start: 'Box', end: 'Box') -> None:
    """
    depth_first_search(start: 'Box', end: 'Box') -> None

    深度优先搜索 (不可用于求解) | depth first search (cannot be used for search)
    >> start: 起始九宫格对象 | start Box object
    >> end: 目标九宫格对象 | end Box object
    """
    # 警告: 典型的深度优先搜索是不完备的搜索算法, 在八数码问题中具有严重缺陷, 本函数仅供展示, 不可用于求解.
    # Warning: The typical depth-first search is an incomplete search algorithm, which has serious defects here.
    # This function is only for demonstration and cannot be used for search.
    warnings.warn('深度优先搜索是不完备的搜索算法, 在八数码问题中具有严重缺陷, 本函数仅供展示，不可用于求解.\n'
                  'The typical depth-first search is an incomplete search algorithm, which has serious defects here.\n'
                  'This function is only for demonstration and cannot be used for search.', SyntaxWarning)
    if input('\n是否仍要继续? (y/n) | continue? (y/n): ') not in ('y', 'Y', 'yes', 'Yes', 'YES', '是', '是的', '', ' '):
        return
    goal = end.value
    print('->', start.history)
    if start.value == goal:
        print('起点已在目标状态 | start Box is already in target state')
        print(start)
        return

    def _dfs(now: 'Box') -> None:
        for next_layer in now.expand():
            print('->', next_layer.history)
            if next_layer.value == goal:
                print(next_layer)
                return
            _dfs(next_layer)

    _dfs(start)


def depth_limited_search(start: 'Box', end: 'Box', limit: int) -> None:
    """
    depth_limited_search(start: 'Box', end: 'Box', limit: int) -> None

    有限深度优先搜索 | depth limited search
    >> start: 起始九宫格对象 | start Box object
    >> end: 目标九宫格对象 | end Box object
    >> limit: 搜索深度限制 | search depth limit
    """
    # 警告: 有限深度优先搜索是不完备的搜索算法 | Warning: depth limited search is an incomplete search algorithm
    warnings.warn(
        '有限深度优先搜索是不完备的搜索算法 | depth limited search is an incomplete search algorithm', SyntaxWarning)
    if limit < 0:
        raise ValueError('深度限制不能小于 0 | depth limit cannot be less than 0')
    goal = end.value
    print('->', start.history)
    if start.value == goal:
        print('起点已在目标状态 | start Box is already in target state')
        print(start)
        return

    def _dls(now: 'Box', depth: int) -> bool:
        if depth == limit:
            return False
        for next_layer in now.expand():
            print('->', next_layer.history)
            if next_layer.value == goal:
                print(next_layer)
                return True
            if _dls(next_layer, depth + 1):
                return True
        return False

    if not _dls(start, 0):
        print('未能在限定深度内找到解 | cannot find solution within the depth limit')


def double_breadth_first_search(start: 'Box', end: 'Box') -> None:
    """
    double_breadth_first_search(start: 'Box', end: 'Box') -> None

    双向宽度优先搜索 | double breadth first search
    >> start: 起始九宫格对象 | start Box object
    >> end: 目标九宫格对象 | end Box object
    """
    goal = end.value
    print('start ->', start.history)
    if start.value == goal:
        print('起点已在目标状态 | start Box is already in target state')
        print(start)
        return

    def _dbfs(push: List['Box'], wait: List['Box'], forward: bool) -> None:
        next_layer = []
        for now in push:
            for check in now.expand():
                print('forward' if forward else 'reverse', '->', check.history)
                for box in wait:
                    if check.value == box.value:
                        if not forward:
                            check, box = box, check
                        print('forward', check)
                        print('reverse', box)
                        reverse_replace = {
                            'U': 'D', 'D': 'U', 'L': 'R', 'R': 'L'}
                        reverse_history = ''.join(
                            [reverse_replace[i] for i in box.history[::-1]])
                        print('totally', Box(
                            goal, check.history + reverse_history))
                        return
                next_layer.append(check)
        _dbfs(wait, next_layer, not forward)

    _dbfs([start], [end], True)


def lowest_step(task: dict) -> int:
    """
    lowest_step(task: dict) -> int

    为 search() 函数构建的估价函数 (fn): 最小步数 | heuristic function (fn) for search(): lowest step
    采用历史记录的长度作为评价标准, 单独使用时类似于广度优先搜索.
    using the length of the history record as the estimation criterion,
    it works like breadth first search when used independently.
    >> task: 用于完成评估的基本信息 | basic information for evaluation
    << 评估得出的搜索代价 | evaluation result of search cost
    """
    return len(task['history'])


def most_at_place(task: dict) -> int:
    """
    most_at_place(task: dict) -> int

    为 search() 函数构建的估价函数 (fn): 最多在位 | heuristic function (fn) for search(): most at place
    采用当前状态与目标状态的相同元素个数作为评价标准.
    using the number of identical elements in the current state and the target state as the evaluation criterion.
    >> task: 用于完成评估的基本信息 | basic information for evaluation
    << 评估得出的搜索代价 | evaluation result of search cost
    """
    s = 9
    for i in range(9):
        if task['now'][i] == task['end'][i]:
            s -= 1
    return s


def manhattan_distance(task: dict) -> int:
    """
    manhattan_distance(task: dict) -> int

    为 search() 函数构建的估价函数 (fn): 曼哈顿距离 | heuristic function (fn) for search(): manhattan distance
    采用当前状态与目标状态的曼哈顿距离作为评价标准.
    using the manhattan distance between the current state and the target state as the evaluation criterion.
    >> task: 用于完成评估的基本信息 | basic information for evaluation
    << 评估得出的搜索代价 | evaluation result of search cost
    """
    s = 0
    for i in range(9):
        now, goal = task['now'].index(i), task['end'].index(i)
        s += abs(now // 3 - goal // 3) + abs(now % 3 - goal % 3)
    return s


def run_time(func: Callable) -> Callable:
    """
    @run_time

    用于计算函数运行时间的装饰器 | decorator for calculating function running time
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = process_time()
        result = func(*args, **kwargs)
        print('运行时间 | run time: {:.7f}s'.format(process_time() - start))
        return result

    return wrapper


def run_time_5(func: Callable) -> Callable:
    """
    @run_time_5

    重复运行 5 次并计算平均运行时间的装饰器 | decorator for repeating 5 times and calculating average running time
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        times = []
        for _ in range(1, 5):
            start = process_time()
            func(*args, **kwargs)
            times.append(process_time() - start)
        start = process_time()
        result = func(*args, **kwargs)
        times.append(process_time() - start)
        print('--------------------------------')
        for i in range(1, 6):
            print('  {}  |  {:>16.7f}s'.format(i, times[i - 1]))
        print('--------------------------------')
        print('平均时间 | average time: {:.7f}s\n'.format(sum(times) / 5))
        return result

    return wrapper


bfs = breadth_first_search
dfs = depth_first_search
dls = depth_limited_search
dbfs = double_breadth_first_search
ls = lowest_step
mp = most_at_place
mhd = manhattan_distance
rt = run_time
rt5 = run_time_5

if __name__ == '__main__':
    print(__doc__)
