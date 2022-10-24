# 八数码问题练习包

Language: [English](https://github.com/VincentSHI1230/eight-puzzle-search/blob/main/README_en.md) | 简体中文 (Simplified Chinese)

---

一款用于辅助学习八数码问题搜索求解的 Python 包

## 安装

```bash
pip install --upgrade eight-puzzle-search
```

## 引入

```python
import eight_puzzle_search as eps
```

## 输入和输出

### eps.input_box() 交互式输入九宫格对象

`input_box(prompt: str = '') -> 'Box'`

使用高鲁棒性的交互式命令行输入九宫格对象。具有如下特性 (无需详阅)：

1. 允许分三行输入八数码问题的九宫格，也允许在第一行一次性输入；
1. 同时支持以任意数量空格 ` ` 和英文逗号 `,` 作为间隔输入；当分三行输入时，亦支持不间隔连续输入；
1. 同时支持以 `0`、`*`、`9` 表示九宫格的空格；当以英文逗号 `,` 作为间隔输入时亦支持以两个连续逗号 (`,,` 或 `, ,`) 表示；当不间隔连续输入时亦支持以空格 ` ` 表示；
1. 能够自动排除错误或不合理的输入；
1. 具有完善的提示文本，用户无需注意输入细则。

#### 传入参数

| \   | 参数名 | 数据类型 | 是否必填 | 默认值 | 说明     |
| --- | ------ | -------- | -------- | ------ | -------- |
| 1   | prompt | str      | 否       | ''     | 提示信息 |

#### 返回参数

| \   | 数据类型 | 说明                 |
| --- | -------- | -------------------- |
| 1   | `Box`    | 返回新建的九宫格对象 |

#### 示例 1

```python
a = eps.input_box()
# 输入 283
# 输入 164
# 输入 7 5
print(a)

```

```text
请按提示直接输入数值. 0 或 * 可代表空位.
enter the value directly as prompted.
0 or * can be used to represent blank.
第 1 行 | row 1: 283
第 2 行 | row 2: 164
第 3 行 | row 3: 7 5
[ 2 8 3
  1 6 4
  7 * 5 ]

moved via -> :
[ 2 8 3
  1 6 4
  7 * 5 ]

```

#### 示例 2

```python
b = eps.input_box('请输入变量 b 的值: ')
# 输入 1, 2, 3, 8,  , 4, 7, 6, 5
print(b)

```

```text
请输入变量 b 的值:
第 1 行 | row 1: 1, 2, 3, 8,  , 4, 7, 6, 5
[ 1 2 3
  8 * 4
  7 6 5 ]

moved via -> :
[ 1 2 3
  8 * 4
  7 6 5 ]

```

### Box() 九宫格的实例化

`Box(value: list, history: str = '') -> 'Box'`

由于求解的基本单位，将在后文中详述。可以直接实例化该对象以输入九宫格。
若要使用该方式，必须保证 value 是由 0 - 9 九个 整型 `int` 数字组成的数组，其中 `0` 代表空格。

#### 传入参数

| \   | 参数名  | 数据类型  | 是否必填 | 默认值 | 说明                 |
| --- | ------- | --------- | -------- | ------ | -------------------- |
| 1   | value   | List[int] | 是       | -      | 九宫格对象的值       |
| 2   | history | str       | 否       | ''     | 九宫格对象的移动历史 |

#### 返回参数

| \   | 数据类型 | 说明                   |
| --- | -------- | ---------------------- |
| 1   | `Box`    | 返回实例化的九宫格对象 |

#### 示例

```python
c = eps.Box([0, 2, 3, 1, 8, 4, 7, 6, 5])
print(c)

```

```text
moved via -> :
[ * 2 3
  1 8 4
  7 6 5 ]

```

### 九宫格对象的格式化输出

在上文中已经可见，九宫格对象经过优化，可以直接使用 `print()` 内置函数输出。

## 基础用法：使用预置函数进行盲目搜索

盲目搜索是最基础的搜索算法。在本代码包中，你可以直接使用函数运行盲目搜索，并观察它们。

### breadth_first_search() 宽度优先搜索

`breadth_first_search(start: 'Box', end: 'Box') -> None`
`bfs(start: 'Box', end: 'Box') -> None`

#### 传入参数

| \    | 参数名 | 数据类型 | 是否必填 | 默认值 | 说明           |
| ---- | ------ | -------- | -------- | ------ | -------------- |
| 1    | start  | `Box`    | 是       | -      | 起始九宫格对象 |
| 2    | end    | `Box`    | 是       | -      | 目标九宫格对象 |

#### 返回参数 `None`

搜索结果直接打印，无返回参数

#### 示例

```python
eps.bfs(a, b)

```

```text
-> 
-> D
-> L
-> R
-> DU
-> DD
...
-> DDRUU
-> DDRUD
-> DDRUL
moved via -> DDRUL:
[ 1 2 3
  8 * 4
  7 6 5 ]

```

### depth_first_search() 宽度优先搜索

`depth_first_search(start: 'Box', end: 'Box') -> None`
`dfs(start: 'Box', end: 'Box') -> None`

**警告：深度优先搜索是不完备的搜索算法，在八数码问题中具有严重缺陷，本函数仅供展示，不可用于求解。**

#### 传入参数

| \    | 参数名 | 数据类型 | 是否必填 | 默认值 | 说明           |
| ---- | ------ | -------- | -------- | ------ | -------------- |
| 1    | start  | `Box`    | 是       | -      | 起始九宫格对象 |
| 2    | end    | `Box`    | 是       | -      | 目标九宫格对象 |

#### 返回参数 `None`

搜索结果直接打印，无返回参数

#### 示例

```python
eps.dfs(a, b)
# 输入: y

```

```text
SyntaxWarning: 深度优先搜索是不完备的搜索算法, 在八数码问题中具有严重缺陷, 本函数仅供展示, 不可用于求解.    
The typical depth-first search is an incomplete search algorithm, which has serious defects here.
This function is only for demonstration and cannot be used for search.

是否仍要继续? (y/n) | continue? (y/n): y
-> 
-> D
-> DU
-> DUD
-> DUDU
...
-> DUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUD
-> DUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDUDU
Traceback (most recent call last):
    eps.dfs(a, b)
RecursionError: maximum recursion depth exceeded in comparison

```

### depth_limited_search() 有限深度优先搜索

`depth_limited_search(start: 'Box', end: 'Box') -> None`
`dls(start: 'Box', end: 'Box') -> None`

**警告：有限深度优先搜索是不完备的搜索算法**

#### 传入参数

| \    | 参数名 | 数据类型 | 是否必填 | 默认值 | 说明           |
| ---- | ------ | -------- | -------- | ------ | -------------- |
| 1    | start  | `Box`    | 是       | -      | 起始九宫格对象 |
| 2    | end    | `Box`    | 是       | -      | 目标九宫格对象 |
| 3    | limit  | int      | 是       | -      | 搜索深度限制   |

#### 返回参数 `None`

搜索结果直接打印，无返回参数

#### 示例 1

```python
eps.dls(a, b, 1)

```

```text
SyntaxWarning: 有限深度优先搜索是不 完备的搜索算法 | depth limited search is an incomplete search algorithm
->
-> D
-> L
-> R
未能在限定深度内找到解 | cannot find solution within the depth limit 

```

#### 示例 2

```python
eps.dls(a, b, 5)

```

```text
SyntaxWarning: 有限深度优先搜索是不 完备的搜索算法 | depth limited search is an incomplete search algorithm
->
-> D
-> DU
-> DUD
-> DUDU
-> DUDUD
...
-> DDRUU
-> DDRUD
-> DDRUL
moved via -> DDRUL:
[ 1 2 3
  8 * 4
  7 6 5 ]

```

### double_breadth_first_search() 双向宽度优先搜索

`double_breadth_first_search(start: 'Box', end: 'Box') -> None`
d`bfs(start: 'Box', end: 'Box') -> None`

#### 传入参数

| \    | 参数名 | 数据类型 | 是否必填 | 默认值 | 说明           |
| ---- | ------ | -------- | -------- | ------ | -------------- |
| 1    | start  | `Box`    | 是       | -      | 起始九宫格对象 |
| 2    | end    | `Box`    | 是       | -      | 目标九宫格对象 |

#### 返回参数 `None`

搜索结果直接打印，无返回参数

#### 示例

```python
eps.dbfs(a, b)

```

```text
start -> 
forward -> D
forward -> L
forward -> R
reverse -> U
reverse -> D
...
reverse -> UD
reverse -> UL
reverse -> UR
...
forward -> DDU
forward -> DDL
forward -> DDR
forward moved via -> DDR:
[ * 2 3
  1 8 4
  7 6 5 ]

reverse moved via -> RD:
[ * 2 3
  1 8 4
  7 6 5 ]

totally moved via -> DDRUL:
[ 1 2 3
  8 * 4
  7 6 5 ]

```

