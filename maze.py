import time
import sys
from disjoint_set_union import DSU
from map import Map
import random
import tkinter as tk
from queue import PriorityQueue
from stack import Stack


class Status:
    NOT_VISITED = 0
    VISITED = 1

class Maze:
    def __init__(self, width: int, height: int):
        self.map = Map(width, height)
        self.width = width
        self.height = height

    # 深度优先算法生成迷宫
    def dfs_generate(self, draw_link):
        # 0：未访问，1：已访问
        status_list = [Status.NOT_VISITED for _ in range(self.width*self.height)]
        # edge_list作为栈存储节点并附带来源信息
        edge_list = [{"from": 0, "to": 0}]
        while edge_list: # 只要index_list不为空则一直循环
            # 栈顶出栈
            top_edge = edge_list.pop()
            top_index = top_edge['to']
            # 如果已经访问过则跳过
            if status_list[top_index] == Status.VISITED:
                continue
            # 访问节点
            self.map.link_node(top_edge['from'], top_index)
            if draw_link:
                draw_link(top_edge['from'], top_index)
            # 标记访问
            status_list[top_index] = Status.VISITED
            # 获取相邻节点
            round_index_list = self.map.round_node_list(top_index)
            # 打乱顺序增加随机性
            random.shuffle(round_index_list)
            # 将未访问过的相邻节点入栈
            for round_index in round_index_list:
                if status_list[round_index] == Status.NOT_VISITED:
                    edge_list.append({"from": top_index, "to": round_index})

    # Prim算法生成迷宫（加点法）
    def prim_generate(self, draw_link):
        # 0：未访问，1：已访问
        status_list = [Status.NOT_VISITED for _ in range(self.width * self.height)]
        node_list = [0]
        status_list[0] = Status.VISITED
        while len(node_list) != self.width*self.height:
            not_visited_list = []
            # 找到所有在已访问点周围但是又没访问过的点
            for node_index in node_list:
                for round_index in self.map.round_node_list(node_index):
                    if status_list[round_index] == Status.NOT_VISITED:
                        not_visited_list.append({"from": node_index, "to": round_index})
            # 打乱增加随机性
            random.shuffle(not_visited_list)
            # 访问节点
            from_index = not_visited_list[0]['from']
            to_index = not_visited_list[0]['to']
            self.map.link_node(from_index, to_index)
            if draw_link:
                draw_link(from_index, to_index)
            # 标记访问
            status_list[to_index] = Status.VISITED
            # 加入node_list
            node_list.append(to_index)

    # Kruskal算法生成迷宫（加边法）
    def kruskal_generate(self, draw_link):
        # 初始化并查集
        dsu = DSU(self.width*self.height)
        # 打乱增加随机性
        random.shuffle(self.map.edge_list)
        # 遍历所有边
        for edge in self.map.edge_list:
            # 如果已经连接则跳过
            if self.map.judge_link(edge[0], edge[1]):
                continue
            # 如果两点连通则跳过
            if dsu.find(edge[0]) == dsu.find(edge[1]):
                #print(f'{edge[0]+1} 和 {edge[1]+1} 节点连通')
                continue
            # 连接两点
            #print(f'连接: {edge[0]+1} 和 {edge[1]+1}')
            self.map.link_node(edge[0], edge[1])
            if draw_link:
                draw_link(edge[0], edge[1])
            dsu.join(edge[0], edge[1])

    # 深度优先算法迷宫寻路
    def dfs_solve(self, draw_path):
        path_list = []
        # 0：未访问，1：已访问
        status_list = [Status.NOT_VISITED for _ in range(self.width * self.height)]
        # node_stack作为栈存储节点并附带路径信息
        node_stack = Stack()
        node_stack.put({"cur_index": 0, "path": []})
        while not node_stack.empty():  # 只要栈不为空则一直循环
            # 栈顶出栈
            top_node = node_stack.pop()
            top_index = top_node['cur_index']
            # 如果已经访问过则跳过
            if status_list[top_index] == Status.VISITED:
                continue
            # 访问节点
            if draw_path and top_node['path']:
                last = top_node['path'][-1]
                draw_path(last[0], last[1])
            if top_index == self.width*self.height-1:
                path_list.append(top_node['path'])
                for edge in top_node['path']:
                    draw_path(edge[0], edge[1], 'blue')
                continue
                # return top_node['path']
            # 标记访问
            status_list[top_index] = Status.VISITED
            # 获取相邻节点
            link_node_list = self.map.link_node_list(top_index)
            # 打乱顺序增加随机性
            random.shuffle(link_node_list)
            # 将未访问过的相邻节点入栈
            for round_index in link_node_list:
                if status_list[round_index] == Status.NOT_VISITED:
                    node_stack.put({"cur_index": round_index, "path": top_node['path'] + [(top_index, round_index)]})
        return path_list

    # 广度优先算法迷宫寻路
    def bfs_solve(self, draw_path):
        path_list = []
        # 0：未访问，1：已访问
        status_list = [Status.NOT_VISITED for _ in range(self.width * self.height)]
        # node_list作为队列存储节点并附带路径信息
        node_list = [{"cur_index": 0, "path": []}]
        while node_list:  # 只要队列不为空则一直循环
            # 队首出队
            top_node = node_list.pop(0)
            top_index = top_node['cur_index']
            # 如果已经访问过则跳过
            if status_list[top_index] == Status.VISITED:
                continue
            # 访问节点
            if draw_path and top_node['path']:
                last = top_node['path'][-1]
                draw_path(last[0], last[1])
            if top_index == self.width * self.height - 1:
                path_list.append(top_node['path'])
                for edge in top_node['path']:
                    draw_path(edge[0], edge[1], 'blue')
                # return top_node['path']
                continue
            # 标记访问
            status_list[top_index] = Status.VISITED
            # 获取相邻节点
            link_node_list = self.map.link_node_list(top_index)
            # 打乱顺序增加随机性
            random.shuffle(link_node_list)
            # 将未访问过的相邻节点入队
            for round_index in link_node_list:
                if status_list[round_index] == Status.NOT_VISITED:
                    node_list.append({"cur_index": round_index, "path": top_node['path'] + [(top_index, round_index)]})
        return path_list

    # a-star算法迷宫寻路
    # 优先队列PriorityQueue的坑：如果存放元组，则默认比较元组的第一个元素，小的在队列头部，如果第一元素相同则比较第二个元素，如果还相同依次往后比较，其实这应该是内置的元组大小比较函数定义的比较方式。
    # https://zhuanlan.zhihu.com/p/445507165
    def astar_solve(self, draw_path):
        class AStarNode:
            def __init__(self, index: int, cost_so_far: int, path: list):
                self.index = index
                self.cost_so_far = cost_so_far
                self.path = path

            def __lt__(self, other):
                if other.cost_so_far > self.cost_so_far:
                    return True
                return False

        # 获取某个点到终点的曼哈顿距离
        def manhattan_distance(index: int):
            row, column = self.map.get_coord_from_index(index)
            return (self.height - row) + (self.width - column)

        path_list = []
        # 状态列表，0：未访问，1：已访问
        status_list = [Status.NOT_VISITED for _ in range(self.width * self.height)]
        # 优先队列
        node_queue = PriorityQueue()
        node_queue.put((0, AStarNode(index=0, cost_so_far=0, path=[])))

        while not node_queue.empty(): # 只要队列非空则一直循环
            # 队首出队
            cur_node = node_queue.get()[1]
            cur_index = cur_node.index
            cur_cost_so_far = cur_node.cost_so_far

            # 如果已经访问过则跳过
            if status_list[cur_index] == Status.VISITED:
                continue
            # 访问节点
            if draw_path and cur_node.path:
                last = cur_node.path[-1]
                draw_path(last[0], last[1])
            if cur_index == self.width * self.height - 1:
                path_list.append(cur_node.path)
                for edge in cur_node.path:
                    draw_path(edge[0], edge[1], 'blue')
                continue
            # 标记访问
            status_list[cur_index] = Status.VISITED

            # 获取相连接的节点
            link_index_list = self.map.link_node_list(cur_index)
            for link_index in link_index_list:
                # 将未访问过的相邻节点入队
                if status_list[link_index] == Status.NOT_VISITED:
                    # 计算cost
                    link_cost_so_far = cur_cost_so_far + 1
                    link_cost = link_cost_so_far + manhattan_distance(link_index)
                    node_queue.put((link_cost, AStarNode(index=link_index, cost_so_far=link_cost_so_far,
                                  path=cur_node.path + [(cur_index, link_index)])))
        return path_list

    # 画出迷宫
    def draw_maze(self):
        # 外围间隔
        peripheral_gap = 10
        # 地图宽
        map_width = 500
        # 地图高
        map_height = 500
        # 地图行数
        map_row_num = self.height
        # 地图列数
        map_column_num = self.width
        # 画布宽
        canvas_width = map_width + peripheral_gap
        # 画布高
        canvas_height = map_height + peripheral_gap
        # 单元格宽
        cell_width = map_width / map_column_num
        # 单元格高
        cell_height = map_height / map_row_num
        # 每个单元格左上角坐标
        cell_coord_list = []
        for row_index in range(map_row_num):
            for column_index in range(map_column_num):
                cell_coord_list.append((
                    column_index * cell_width + peripheral_gap,
                    row_index * cell_height + peripheral_gap
                ))
        # 创建主窗口
        root = tk.Tk()
        root.title("迷宫")
        # 创建画布
        canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
        canvas.pack()
        # 画迷宫
        for cell_index in range(len(cell_coord_list)):
            cell_coord = cell_coord_list[cell_index]
            x = cell_coord[0]
            y = cell_coord[1]
            # 当前单元格位于第几行第几列
            row, column = self.map.get_coord_from_index(cell_index)
            print(f'{cell_index + 1} 位于第 {row} 行，第 {column} 列')
            up_index = self.map.get_index_from_coord(row-1, column) if row-1 >= 1 else None
            print(f'{cell_index + 1}的上边是{up_index + 1 if up_index else '无'}')
            down_index = self.map.get_index_from_coord(row+1, column) if row+1 <= map_row_num else None
            print(f'{cell_index + 1}的下边是{down_index + 1 if down_index else '无'}')
            left_index = self.map.get_index_from_coord(row, column-1) if column-1 >= 1 else None
            print(f'{cell_index+1}的左边是{left_index+1 if left_index else '无'}')
            right_index = self.map.get_index_from_coord(row, column+1) if column+1 <= map_column_num else None
            print(f'{cell_index + 1}的右边是{right_index + 1 if right_index else '无'}')
            if up_index:
                if not self.map.judge_link(cell_index, up_index):
                    print(f'{cell_index + 1}和{up_index + 1}不连接')
                    print(f'画{cell_index + 1}上边')

                    # 上边
                    canvas.create_line(x, y, x + cell_width, y)
            if down_index:
                if not self.map.judge_link(cell_index, down_index):
                    print(f'{cell_index + 1}和{down_index + 1}不连接')
                    print(f'画{cell_index + 1}下边')
                    # 下边
                    canvas.create_line(x, y + cell_height, x + cell_width, y + cell_height)
            if left_index:
                if not self.map.judge_link(cell_index, left_index):
                    print(f'{cell_index + 1}和{left_index + 1}不连接')
                    print(f'画{cell_index + 1}左边')
                    # 左边
                    canvas.create_line(x, y, x, y + cell_height)
            if right_index:
                if not self.map.judge_link(cell_index, right_index):
                    print(f'{cell_index + 1}和{right_index + 1}不连接')
                    print(f'画{cell_index + 1}右边')
                    # 右边
                    canvas.create_line(x + cell_width, y, x + cell_width, y + cell_height)

            if up_index is None and cell_index != 0: # cell_index != 0 是为了打开迷宫入口
                # 上边
                print(f'画{cell_index + 1}上边')
                canvas.create_line(x, y, x + cell_width, y)
            if down_index is None and cell_index != map_row_num*map_column_num-1: # cell_index != map_row_num*map_column_num-1 是为了打开迷宫出口
                # 下边
                print(f'画{cell_index + 1}下边')
                canvas.create_line(x, y + cell_height, x + cell_width, y + cell_height)
            if left_index is None:
                # 左边
                print(f'画{cell_index + 1}左边')
                canvas.create_line(x, y, x, y + cell_height)
            if right_index is None:
                # 右边
                print(f'画{cell_index + 1}右边')
                canvas.create_line(x + cell_width, y, x + cell_width, y + cell_height)

        root.mainloop()

    # 动态生成迷宫和寻路
    def dynamic_draw_maze(self, generate_name: str, solve_name: str, generate_sleep: float, solve_sleep: float):
        # 外围间隔
        peripheral_gap = 20
        # 顶部间隔
        top_gap = 50
        # 地图宽
        map_width = 600
        # 地图高
        map_height = 600
        # 地图行数
        map_row_num = self.height
        # 地图列数
        map_column_num = self.width
        # 画布宽
        canvas_width = map_width + (peripheral_gap * 2)
        # 画布高
        canvas_height = map_height + (peripheral_gap * 2) + top_gap
        # 单元格宽
        cell_width = map_width / map_column_num
        # 单元格高
        cell_height = map_height / map_row_num
        # 每个单元格左上角坐标
        cell_coord_list = []
        for row_index in range(map_row_num):
            for column_index in range(map_column_num):
                cell_coord_list.append((
                    column_index * cell_width + peripheral_gap,
                    row_index * cell_height + peripheral_gap + top_gap
                ))
        # 创建主窗口
        root = tk.Tk()
        root.title("迷宫")
        # 窗口居中显示
        # 获取屏幕的宽度和高度
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        # 计算窗口左上角的坐标，使其居中显示
        x = (screen_width - canvas_width) // 2
        y = (screen_height - canvas_height) // 2 - 35
        # 设置窗口的几何形状，包括位置和大小
        root.geometry(f'{canvas_width}x{canvas_height}+{x}+{y}')
        # 创建画布
        canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
        canvas.pack()
        # 迷宫初始化
        wall_id_matrix = [[sys.maxsize for _ in range(map_row_num*map_column_num)] for _ in range(map_row_num*map_column_num)]
        # 墙的厚度
        wall_width = 3
        for cell_index in range(len(cell_coord_list)):
            cell_coord = cell_coord_list[cell_index]
            x = cell_coord[0]
            y = cell_coord[1]
            # 上边
            if cell_index != 0:
                up_wall_id = canvas.create_line(x, y, x + cell_width, y, width=wall_width)
                up_index = self.map.get_up_index(cell_index)
                if up_index is not None:
                    wall_id_matrix[cell_index][up_index] = up_wall_id
            # 下边
            if cell_index != map_row_num*map_column_num-1:
                down_wall_id = canvas.create_line(x, y + cell_height, x + cell_width, y + cell_height, width=wall_width)
                down_index = self.map.get_down_index(cell_index)
                if down_index is not None:
                    wall_id_matrix[cell_index][down_index] = down_wall_id
            # 左边
            left_wall_id = canvas.create_line(x, y, x, y + cell_height, width=wall_width)
            left_index = self.map.get_left_index(cell_index)
            if left_index is not None:
                wall_id_matrix[cell_index][left_index] = left_wall_id
            # 右边
            right_wall_id = canvas.create_line(x + cell_width, y, x + cell_width, y + cell_height, width=wall_width)
            right_index = self.map.get_right_index(cell_index)
            if right_index is not None:
                wall_id_matrix[cell_index][right_index] = right_wall_id

        def delete_wall(from_index: int, to_index: int):
            if from_index == to_index:
                return
            # print(f'打通: {from_index+1} 到 {to_index+1}, 线的id为: {wall_id_matrix[from_index][to_index]}')
            canvas.delete(wall_id_matrix[from_index][to_index])
            canvas.delete(wall_id_matrix[to_index][from_index])
            time.sleep(generate_sleep)
            canvas.update()

        path_id_list = []

        def draw_path(from_index: int, to_index: int, color: str = '#CC9900'):
            if from_index == to_index:
                return
            # 路径宽
            path_width = 8
            from_coord = cell_coord_list[from_index]
            to_coord = cell_coord_list[to_index]
            path_id = canvas.create_line(
                from_coord[0] + (cell_width / 2), from_coord[1] + (cell_height / 2),
                to_coord[0] + (cell_width / 2), to_coord[1] + (cell_height / 2),
                fill=color, width=path_width
            )
            path_id_list.append(path_id)
            time.sleep(solve_sleep)
            canvas.update()

        switch_name = {
            'dfs': '深度优先',
            'bfs': '广度优先',
            'prim': 'Prim',
            'kruskal': 'Kruskal',
            'a-star': 'A-Star'
        }

        canvas.create_text(315, 35, text=f'生成算法: {switch_name[generate_name]}, 寻路算法: {switch_name[solve_name]}', font=('SimSun', 18, 'bold'))
        canvas.update()
        # 选择生成算法
        if generate_name == 'dfs':
            self.dfs_generate(delete_wall)
        elif generate_name == 'prim':
            self.prim_generate(delete_wall)
        elif generate_name == 'kruskal':
            self.kruskal_generate(delete_wall)
        # 选择寻路算法
        path_list = []
        if solve_name == 'a-star':
            path_list = self.astar_solve(draw_path)
        elif solve_name == 'dfs':
            path_list = self.dfs_solve(draw_path)
        elif solve_name == 'bfs':
            path_list = self.bfs_solve(draw_path)
        print(f'所有路径: {path_list}')
        # 找到最短路径
        shortest_path = path_list[0]
        for path in path_list:
            if len(path) < len(shortest_path):
                shortest_path = path
        print(f'最短路径：{shortest_path}')
        # 画出最短路径
        for edge in shortest_path:
            draw_path(edge[0], edge[1], 'red')
        root.mainloop()
