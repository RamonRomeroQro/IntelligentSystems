'''
    Copyright 2019 © Ramón Romero @RamonRomeroQro
    Intelligent Systems, ITESM.
    A01700318 for ITESM

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    Special thanks to: 
    @rhomeister, @alelopezperez, @eduardolarios and the FLOSS/sudo comunity.
'''


from collections import deque
import random
import sys


class GraphSearchSpace():
    def __init__(self, m_h,):
        self.nodes = {}
        self.heuristic = {}
        self.max_height = m_h

    def generate_heuristic(self, goal_structure):
        for k, v in self.nodes.items():
            m1f = (v.structure)
            m2f = (goal_structure)
            #print('->>', v.structure,m1f )

            self.heuristic[k] = self.evaluate(m1f, m2f)

    def generate_bad_heuristic(self, goal_structure):
        random.seed(50)
        for k, v in self.nodes.items():
            self.heuristic[k] = random.randint(80, 100)

    def evaluate(self, m1, m2):
        d1 = {}
        d2 = {}
        h = {}
        for i in range(len(m1)):
            for j in range(len(m1[i])):
                if m1[i][j] != 'X':
                    d1[m1[i][j]] = (i, j)

        for i in range(len(m2)):
            for j in range(len(m2[i])):
                if m2[i][j] != 'X':
                    d2[m2[i][j]] = (i, j)
        s = 0
        for k, v in d1.items():
            # s=s+abs(d2[k][0]-d1[k][0])+abs(len(m1[d1[k][0]])-d1[k][1])+abs(len(m1[d2[k][0]])-d2[k][1])
            if k in d2:
                s = s+abs(d2[k][0]-d1[k][0])
        return s

    def filling(self, mat):
        for s in mat:
            if len(s) < self.max_height:
                for i in range(0, abs(len(s)-self.max_height)):
                    s.append('*')
        return mat

    def __str__(self):

        s = ""
        for i in self.nodes:
            s = s+i.__str__()+"\n"

        return s


class Node:

    def __str__(self):
        return str(self.id)

    def __init__(self, structure):
        self.num_stacks = len(structure)
        self.structure = structure
        self.conections = {}
        self.id = tuple(map(tuple, self.structure))

    def generate_node(self, origin_stack, destination_stack, gsp):
        if len(self.structure[destination_stack]) < gsp.max_height and (len(self.structure[origin_stack])) > 0:
            new_structure = list(map(list, self.structure))
            e = new_structure[origin_stack].pop()
            new_structure[destination_stack].append(e)
            new_node = Node(new_structure)
            return new_node

        else:
            return None

    def generate_paths(self, gsp):
        execution_queue = deque([])
        gsp.nodes[self.id] = self
        execution_queue.append(self)
        while(len(execution_queue) > 0):
            ex_node = execution_queue.popleft()
            for i in range(0, ex_node.num_stacks):
                for j in range(0, ex_node.num_stacks):
                    if i != j:
                        new_node = ex_node.generate_node(i, j, gsp)
                        cost = 1+abs(i-j)
                        if (new_node != None):
                            if new_node.id not in gsp.nodes:
                                gsp.nodes[new_node.id] = new_node
                                ex_node.conections[(
                                    i, j, cost)] = gsp.nodes[new_node.id]
                                execution_queue.append(new_node)
                            else:
                                existent_node = gsp.nodes[new_node.id]
                                ex_node.conections[(
                                    i, j, cost)] = existent_node


def search(start_node, goal_node, gsp, greedy, heuristic):
    explored = {}
    pq = PriorityQueue()
    # nodo, currentsume, path, heuristica
    if heuristic == True:
        sortk = (0)+gsp.heuristic[start_node.id]
    else:
        sortk = 0+0
    pq.add((gsp.nodes[start_node.id], 0, [], sortk))
    kek = 0
    while(True):
        kek = kek+1
        if pq.is_empty() == True:
            return "No solution found", kek
        nodo, latest_cost, path = pq.pop()
        #print("...", path)
        if greedy == True:
            if greedy_evaluation(nodo.structure, goal_node.structure) == True:
                explored[nodo.id] = nodo
                # print(cost, nodo)
                # print(path)
                # print(latest_cost)
                return str(latest_cost)+"\n"+"; ".join([str(x) for x in (path)]), kek

        else:
            if nodo.id == goal_node.id:
                explored[nodo.id] = nodo
                # print(cost, nodo)
                # print(path)
                # print(latest_cost)
                return str(latest_cost)+"\n"+"; ".join([str(x) for x in (path)]), kek
        # print("expanded ___!", nodo, cost)
        explored[nodo.id] = nodo
        for t, n in nodo.conections.items():  # expansion
            conex = n
            cost_n = t[2]
            trans = (t[0], t[1])
            n_path = list(path)
            # print(n_path)
            n_path.append(trans)
            if conex.id not in explored:  # or conex not frontier:
                # print('sss')
                if heuristic == True:
                    sortk = (cost_n+latest_cost)+gsp.heuristic[conex.id]
                else:
                    sortk = (cost_n+latest_cost)+0
                f = False
                for x in range(len(pq.q)):
                    if pq.q[x][0].id == conex.id:
                        x = (conex, cost_n+latest_cost, n_path,  sortk)
                        f = True
                        break
                if f == False:
                    pq.add((conex, cost_n+latest_cost, n_path,  sortk))


def greedy_evaluation(m1, g):
    for i in range(len(g)):
        if g[i] != ['X'] and m1[i] != g[i]:
            return False
    return True


class PriorityQueue():

    def is_empty(self):
        if len(self.q) == 0:
            return True
        return False

    def __init__(self):
        self.q = deque([])

    def __str__(self):
        s = "\n-----------\n"
        for i in self.q:
            s = s+str(i[0])+", "+str(i[1])+";\n"
        return s

    def pop(self):
        self.q = sorted(self.q, key=lambda x: (x[3]))
        self.q = deque(self.q)
        a = self.q.popleft()
        return a[0], a[1], (a[2])

    def add(self, paired):
        self.q.append(paired)
        self.q = sorted(self.q, key=lambda x: (x[3]))


def main():
    # PARSING INPUT
    max_height = int(input())
    start_structure = str(input())
    goal_structure = str(input())
    start_structure = start_structure.strip().split(";")
    goal_structure = goal_structure.strip().split(";")
    start_structure = list(
        map(lambda x: x.strip().strip("(").strip(")"), start_structure))
    goal_structure = list(
        map(lambda x: x.strip().strip("(").strip(")"), goal_structure))
    start_structure = list(map(lambda x: x.split(
        ", ") if x != '' else [], start_structure))
    goal_structure = list(map(lambda x: x.split(
        ", ") if x != '' else [], goal_structure))

    # DEBUG PAARSING
    # print('G?->', goal_structure)
    # print('S?->', start_structure)
    # Initial Node Creation

    # Dummy Node for Debug
    # max_height = 2
    # goal_structure = [['A', 'C'], [], []]
    # start_structure = [['A'], ['B'], ['C']]

    # Graph Search Space Creation
    gsp = GraphSearchSpace(max_height)
    initialState = Node(start_structure)
    goalState = Node(goal_structure)
    initialState.generate_paths(gsp)

    # for k,v in gsp.nodes.items():
    #    print(k)

    greedy = False
    for l in goal_structure:
        for i in l:
            if i == "X":
                greedy = True
                break
    if greedy == False:
        if goalState.id not in gsp.nodes:
            print("No solution found")
            return 0

    if len(sys.argv) == 4:

        # ucs
        uc, itucs = search(initialState, goalState, gsp, greedy, False)
        print(itucs)
        print(uc)
        # a+
        gsp.generate_heuristic(goalState.structure)
        ast, ita = search(initialState, goalState, gsp, greedy, True)
        print(ita)
        print(ast)
        # a-
        gsp.generate_bad_heuristic(goalState.structure)
        ast, ita = search(initialState, goalState, gsp, greedy, True)
        print(ita)
        print(ast)

    elif len(sys.argv) == 2:

        if sys.argv[1] == '+a':
            gsp.generate_heuristic(goalState.structure)
            ast, ita = search(initialState, goalState, gsp, greedy, True)
            # print(ita)
            print(ast)
        elif sys.argv[1] == '-a':
            gsp.generate_bad_heuristic(goalState.structure)
            ast, ita = search(initialState, goalState, gsp, greedy, True)
            # print(ita)
            print(ast)
        elif sys.argv[1] == '+u':
            uc, itucs = search(initialState, goalState, gsp, greedy, False)
            # print(itucs)
            print(uc)
        else:
            print("error: args")
            return 0

    elif len(sys.argv) == 3:
        it = 0
        if sys.argv[1] == '+a':
            gsp.generate_heuristic(goalState.structure)
            ast, it = search(initialState, goalState, gsp, greedy, True)
            # print(ita)
            print(ast)
        elif sys.argv[1] == '-a':
            gsp.generate_bad_heuristic(goalState.structure)
            ast, it = search(initialState, goalState, gsp, greedy, True)
            # print(ita)
            print(ast)
        elif sys.argv[1] == '+u':
            uc, it = search(initialState, goalState, gsp, greedy, False)
            # print(itucs)
            print(uc)
        else:
            print("error: args")
            return 0

        print(it)

    elif len(sys.argv) == 1:
        gsp.generate_heuristic(goalState.structure)
        ast, ita = search(initialState, goalState, gsp, greedy, True)
        # print(ita)
        print(ast)

    else:
        print("error: args")
        return 0

    return 0


if __name__ == "__main__":
    main()
