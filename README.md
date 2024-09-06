# 程序内容描述
北邮数据结构小学期作业-迷宫问题

# 程序运行方法
python虚拟环境在`venv`中，只需要在`PowerShell`中进入本文件所在文件夹，
然后执行`./venv/Scripts/python.exe main.py` 即可运行主程序。
本程序没用依赖第三方库，只依赖了python内置库，如果您安装了python环境也可以执行`python main.py`
注：本程序所用python版本为`3.12`

`main.py`中dynamic_draw_maze()函数能动态可视化迷宫生成和迷宫寻路过程
迷宫生成算法可选: dfs, prim, kruskal
迷宫寻路算法可选: dfs, bfs, a-star

# 程序目录结构
- main.py：主程序
- maze.py：定义迷宫类
- map.py：定义地图类
- stack.py：定义栈
- disjoint_set_union.py：定义并查集
