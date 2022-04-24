#!/usr/bin/env python
# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from vertex import Vertex        #依赖模块安装：pip install vertex
from heap import PriorityQueue

class NodeGraph():
    '''
    The NodeGraph conception comes from computer science textbooks work on graphs 
    in the mathematical sense―a set of vertices with edges connecting them.
    It contrasts with GridGraph, which looks like a tiled game map
    '''
    pass

class LNodeGraph(NodeGraph): #save as linked list
    def __init__(self, vertices=None, positions=None, weights=None, heuristic=None): #edges
        self.vertices = vertices
        self.positions = positions
        self.weights = weights
        self.heuristic = heuristic

    @property
    def vertices(self):
        return self._vertices

    @vertices.setter 
    def vertices(self, vertices=None):
        self._vertices = {}
        if isinstance(vertices, list):
            for chain in vertices:
                head = Vertex(chain[0])
                head.weight = 0
                for sub_vertex in chain[-1:0:-1]:
                    head.insert(sub_vertex, weight=1)
                self._vertices[chain[0]] = head

    @property 
    def weights(self):  #weight saved in sub/copied vertex, return with edges
        return self.edges

    @weights.setter
    def weights(self, weights):
        if isinstance(weights, dict):
            for from_u, head in self.vertices.items():
                to_v = head.succ
                while to_v:
                    edge = (from_u, to_v.name)
                    if edge in weights:
                        to_v.weight = weights[edge]
                    else:
                        to_v.weight = 0
                    to_v = to_v.succ

    @property 
    def positions(self):
        return self._positions

    @positions.setter 
    def positions(self, positions):
        self._positions = positions

    @property 
    def heuristic(self):
        _heuristic = {}
        for name, ver in self.vertices.items():
            _heuristic[name] = ver.heur
        return _heuristic

    @heuristic.setter 
    def heuristic(self, heuristic):
        if isinstance(heuristic, dict):
            for name, ver in self.vertices.items():
                if name in heuristic:
                    ver.heur = heuristic[name]
                else:
                    ver.heur = float('inf')

    @property
    def edges(self):
        if not hasattr(self, "_edges"):
            self._edges = {}
            for from_u, chain in self.vertices.items():
                to_v = chain.succ
                while to_v:
                    self._edges[(from_u, to_v.name)] = to_v.weight
                    to_v = to_v.succ
        return self._edges

    def check_edge(self, from_u, to_v):
        if from_u not in self.vertices or to_v not in self.vertices:
            return False
        succ = self.vertices[from_u].succ
        while succ:
            if succ.name == to_v:
                return True
            succ = succ.suc
        return False 

    def BFS_reset_vertices(self):
        for v in self.vertices.values():
            v.reset()
            v.dist = float("inf")

    def BFS(self, s):
        if not s in self.vertices:
            return False
        self.BFS_reset_vertices()
        self.vertices[s].visited = 1
        self.vertices[s].dist = 0
        self.vertices[s].weight = 0
        queue = []
        queue.append(s)
        while queue:
            from_u = queue.pop(0)
            succ_ver = self.vertices[from_u].succ
            while succ_ver:
                to_v = succ_ver.name
                if self.vertices[to_v].visited == 0:
                    self.vertices[to_v].visited = 1
                    self.vertices[to_v].prec = from_u #or self.vertices[from_u].dist
                    self.vertices[to_v].dist = self.vertices[from_u].dist + succ_ver.weight
                    self.vertices[to_v].dist = self.vertices[from_u].dist + 1
                    queue.append(to_v)
                succ_ver = succ_ver.succ
            self.vertices[from_u].visited = 2
        return True     

    def DFS_reset_vertices(self):
        for v in self.vertices.values():
            v.reset()
            v.dist = float("inf")

    def DFS_trackback(self, from_u):
        self._steps += 1
        self.vertices[from_u].entry = self._steps
        self.vertices[from_u].visited = 1
        succ_v = self.vertices[from_u].succ
        while succ_v:
            to_v = succ_v.name
            if self.vertices[to_v].visited == 0:
                self.vertices[to_v].prec = from_u
                self.DFS_trackback(succ_v.name)
            succ_v = succ_v.succ
        self._steps += 1
        self.vertices[from_u].back = self._steps
        self.vertices[from_u].visited = 2

    def DFS(self):
        self.DFS_reset_vertices()
        self._steps = 0
        for from_u in self.vertices.keys():
            if self.vertices[from_u].visited == 0:
                self.DFS_trackback(from_u)  

    def Dijkstra_reset_vertices(self):
        for vertex in self.vertices.values():
            vertex.dist = float('inf')
            vertex.prec = None
            # vertex.visited = 0 # not used

    def Dijkstra(self, start):
        self.Dijkstra_reset_vertices()
        self.vertices[start].dist = 0
        #全量加入，逐步加入均可，此处采用全量加入, 增量加入即 OPEN、CLOSE、UNUSED情况，减少节点数
        priQueue = PriorityQueue(list(self.vertices.values()), sortby='dist')
        while priQueue:
            from_u = priQueue.dequeue()
            to_v = from_u.succ
            while to_v:
                new_dist = from_u.dist + to_v.weight
                if new_dist < self.vertices[to_v.name].dist:
                    self.vertices[to_v.name].dist = new_dist
                    self.vertices[to_v.name].prec = from_u.name
                to_v = to_v.succ

    def AStar_reset_vertex(self):
        for vertex in self.vertices.values():
            vertex.dist = float('inf')
            vertex.prec = None
            # vertex.visited = 0 #not used

    def AStar(self, start, goal):
        self.AStar_reset_vertex()
        self.vertices[start].dist = 0
        preQueue = PriorityQueue([self.vertices[start]], sortby=['dist', 'heur']) #按 dist+heur 进行排序
        # preQueue is on behalf of OPEN
        while preQueue:
            from_u = preQueue.dequeue() #dist+heur 值最小的进行选择
            if from_u.name == goal:
                return self.AStar_reconstruct_path(start, goal) #把路径翻转重建
            else:
                to_v = from_u.succ
                while to_v:
                    tentative_dist = from_u.dist + to_v.weight
                    to_v_name = to_v.name
                    if tentative_dist < self.vertices[to_v_name].dist:
                        self.vertices[to_v_name].dist = tentative_dist
                        self.vertices[to_v_name].prec = from_u.name
                        if not to_v in preQueue:
                            preQueue.enqueue(self.vertices[to_v_name]) #重复访问的问题（先出，后进）当heuristic/启发函数的设置满足一致性条件时，每个节点最多访问一次, 会不会陷入死循环呢？
                    to_v = to_v.succ
        return False #未找到目标

    def AStar_reconstruct_path(self, start, goal):
        path = [goal]
        prec_u = self.vertices[goal].prec
        while prec_u:
            path.append(prec_u)
            if prec_u == start:
                break
            prec_u = self.vertices[prec_u].prec
        path = path[-1::-1]
        return path

    @property
    def fig(self):
        if not hasattr(self, "_fig"):
            self._fig = plt.gcf()
            self._fig.set_figheight(6)
            self._fig.set_figwidth(12)
            self._fig.gca().axis("off")
        return self._fig
    
    def draw_init(self):
        return self.fig

    def draw_vertices(self, heuristic=False, color='blue'):
        pos_array = np.array(list(self.positions.values()))
        plt.scatter(pos_array[:, 0], pos_array[:, 1], 
                        s=1000, c=color, marker='o', alpha=0.9)
        for name, pos in self.positions.items():
            plt.annotate(name, (pos[0]-0.009, pos[1]-0.015), 
                            fontsize=20, color='white', multialignment='center')
            if heuristic:
                plt.annotate("h="+str(self.vertices[name].heur), (pos[0]-0.02, pos[1]+0.09), 
                            fontsize=15, color='black', backgroundcolor='white')

    def draw_edges(self, weight=False, color='blue'):
        for edge in self.edges.keys():
            from_u = self.positions[edge[0]]
            to_v = self.positions[edge[1]]
            plt.plot([from_u[0], to_v[0]], [from_u[1], to_v[1]], 
                        color=color, linewidth=2, alpha=0.9)
            # edges' lables
            if weight:
                center = [(from_u[0] + to_v[0])/2-0.009, (from_u[1] + to_v[1])/2-0.015]
                plt.annotate(self.edges[edge], center, 
                            fontsize=15, color='black', backgroundcolor='white')

    def draw_graph(self, node=True, edge=True, node_head=True, edge_label=True):
        self.draw_vertices()
        self.draw_edges()

    def draw_tree(self, color='black'):
        for to_v, head in self.vertices.items():
            if head.prec:
                from_u = self.positions[head.prec]
                to_v = self.positions[to_v]
                dx = from_u[0] - to_v[0]
                dy = from_u[1] - to_v[1]
                plt.arrow(to_v[0], to_v[1], dx, dy, length_includes_head=True, 
                    head_width=0.03, head_length=0.03, shape='full', color=color)

    def draw_BFS_tree(self, color='red'):
        self.draw_tree(color=color)

    def draw_DFS_forest(self, color='green'):
        self.draw_tree(color=color)
    
    def draw_Dijkstra_tree(self, color='magenta'): #'cyan' 'magenta'
        self.draw_tree(color=color)

    def draw_A_star_path(self, start, goal, color='cyan'):
        self.draw_tree(color='magenta') #
        to_v = goal
        while to_v:
            from_u = self.vertices[to_v].prec 
            if from_u:
                to_pos = self.positions[to_v]
                from_pos = self.positions[from_u]
                dx = from_pos[0] - to_pos[0]
                dy = from_pos[1] - to_pos[1]
                plt.arrow(to_pos[0], to_pos[1], dx, dy, length_includes_head=True, 
                    head_width=0.03, head_length=0.03, shape='full', color=color)
                if from_u == start:
                    break
            to_v = from_u

    def show(self):
        plt.show()

    def save(self, name='graph.jpg'):
        plt.savefig(name)

class MNodeGraph(NodeGraph): #save as matrix
    def __init__(self):
        pass


if __name__ == "__main__":
    vertices = [['S', 'A', 'B', 'C'],
                ['A', 'S', 'D', 'E'],
                ['B', 'S', 'E', 'F'],
                ['C', 'S', 'K'],
                ['D', 'A', 'G'],
                ['E', 'A', 'B', 'G'], 
                ['F', 'B', 'K', 'G'],
                ['K', 'C', 'F', 'G'],
                ['G', 'D', 'E', 'F', 'K']]

    positions = {"S":[0.05, 0.5], #0
                "A":[0.3, 0.8], #1
                "B":[0.3, 0.5], #2
                "C":[0.3, 0.2], #3
                "D":[0.6, 0.95], #4
                "E":[0.6, 0.65], #5
                "F":[0.6, 0.4],  #6
                "K":[0.8, 0.2], #7
                "G":[0.99, 0.5],} #8

    weights = { ('S', 'A'): 9, ('S', 'B'): 6, ('S', 'C'): 8, ('A', 'S'): 9, ('B', 'S'): 6, ('C', 'S'): 8,
                ('A', 'D'): 7, ('A', 'E'): 9, ('D', 'A'): 7, ('E', 'A'): 9,
                ('B', 'E'): 8, ('B', 'F'): 8, ('E', 'B'): 8, ('F', 'B'): 8,
                ('C', 'K'): 20, ('K', 'C'): 20,
                ('D', 'G'): 16, ('G', 'D'): 16,
                ('E', 'G'): 13, ('G', 'E'): 13, 
                ('F', 'G'): 13, ('F', 'K'): 5, ('G', 'F'): 13, ('K', 'F'): 5, 
                ('K', 'G'): 6, ('G', 'K'): 6 }

    heuristic = {   "S": 20, #0
                    "A": 15, #1
                    "B": 17, #2
                    "C": 15, #3
                    "D": 11, #4
                    "E": 12, #5
                    "F": 10,  #6
                    "K": 5, #7
                    "G": 0,} #8

    lgraph = LNodeGraph(vertices, positions, weights, heuristic)
    lgraph.BFS('S')
    lgraph.draw_init()
    lgraph.draw_vertices(heuristic=True)
    lgraph.draw_edges(weight=True)
    # lgraph.draw_BFS_tree()
    # lgraph.DFS()
    # lgraph.draw_DFS_forest()  
    # lgraph.Dijkstra('S')
    # lgraph.draw_Dijkstra_tree()
    lgraph.AStar('S', 'G')
    lgraph.draw_A_star_path('S', 'G')
    lgraph.show()
