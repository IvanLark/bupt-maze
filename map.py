class Map:
    def __init__(self, width: int, height: int):
        # 初始化邻接矩阵，采用行排列
        self.matrix = [[1 if row_index == column_index else 0 for column_index in range(width*height)]
                       for row_index in range(width*height)]
        self.width = width
        self.height = height
        self.edge_list = []
        for index in range(width * height):
            for round_index in self.round_node_list(index):
                self.edge_list.append((index, round_index))
    # 通过坐标获取下标
    def get_coord_from_index(self, index: int):
        row = int(index / self.width) + 1
        column = int(index % self.width) + 1
        return row, column
    # 通过下标获取坐标
    def get_index_from_coord(self, row: int, column: int):
        return ((row-1) * self.width + column) - 1
    # 判断两个点是否连接
    def judge_link(self, index_a: int, index_b: int):
        return self.matrix[index_a][index_b] == 1
    # 节点上下左右点的下标
    def round_node_list(self, index: int):
        row, column = self.get_coord_from_index(index)
        round_index_list = []
        if row+1 <= self.height:
            round_index_list.append(self.get_index_from_coord(row+1, column))
        if row-1 >= 1:
            round_index_list.append(self.get_index_from_coord(row-1, column))
        if column+1 <= self.width:
            round_index_list.append(self.get_index_from_coord(row, column+1))
        if column-1 >= 1:
            round_index_list.append(self.get_index_from_coord(row, column-1))
        return round_index_list
    # 和节点连接的点的下标
    def link_node_list(self, index: int):
        link_node_list = []
        round_node_list = self.round_node_list(index)
        for round_node_index in round_node_list:
            if self.judge_link(index, round_node_index):
                link_node_list.append(round_node_index)
        return link_node_list
    # 未和节点连接的点的下标
    def not_link_node_list(self, index: int):
        not_link_node_list = []
        round_node_list = self.round_node_list(index)
        for round_node_index in round_node_list:
            if not self.judge_link(index, round_node_index):
                not_link_node_list.append(round_node_index)
        return not_link_node_list
    # 连接两个节点
    def link_node(self, index_a: int, index_b: int):
        self.matrix[index_a][index_b] = 1
        self.matrix[index_b][index_a] = 1
    # 获取上面的点的index
    def get_up_index(self, index: int):
        row, column = self.get_coord_from_index(index)
        return self.get_index_from_coord(row-1, column) if row-1 >= 1 else None
    def get_down_index(self, index: int):
        row, column = self.get_coord_from_index(index)
        return self.get_index_from_coord(row+1, column) if row+1 <= self.height else None
    def get_left_index(self, index: int):
        row, column = self.get_coord_from_index(index)
        return self.get_index_from_coord(row, column-1) if column-1 >= 1 else None
    def get_right_index(self, index: int):
        row, column = self.get_coord_from_index(index)
        return self.get_index_from_coord(row, column+1) if column+1 <= self.width else None
