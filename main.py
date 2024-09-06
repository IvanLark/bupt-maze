from maze import Maze

# 生成 20*20 大小的迷宫
maze = Maze(20, 20)
# 迷宫生成算法可选: dfs, prim, kruskal
# 迷宫寻路算法可选: dfs, bfs, a-star
# 使用深度优先算法进行迷宫生成，使用A-Star算法进行迷宫寻路
maze.dynamic_draw_maze('dfs', 'a-star', 0.02, 0.03)
