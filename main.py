import argparse
import pwn
import numpy as np
from typing import *

"""
MOVE|"nu livreur"|"TLRB" => OK ou NOK|message d’erreur
TEAMS => OK|4
GETBIKERS|"nu livreur" => OK|0;3;5
GETBIKERS => OK|0;3;5|1;12;13
GETMAP => OK|EERRRHEEEERS (R (route), E (case vide), H (maison), S (restaurant))
GETDELIVERIES => OK|100;120,00;12;10;23;14;30|101;80,48…
TAKE|"nu livreur"|"code commande" => OK ou NOK|message d’erreur
DELIVER|"nu livreur"|"code commande" => OK ou NOK|message d’erreur 
ENDTURN => OK
SCORE|"nu livreur" => OK|"score"

NAME => "nom team"
START => "nu livreur"
ENDGAME => 1350|1205|520|-1520  (scores des équipes)

#Inpiré de https://www.geeksforgeeks.org/python-program-for-dijkstras-shortest-path-algorithm-greedy-algo-7/
class Graph():
 
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]
 
    def printSolution(self, dist):
        print("Vertex tDistance from Source")
        for node in range(self.V):
            print(node, "t", dist[node])
 
    # A utility function to find the vertex with
    # minimum distance value, from the set of vertices
    # not yet included in shortest path tree
    def minDistance(self, dist, sptSet):
 
        # Initilaize minimum distance for next node
        min = sys.maxsize
 
        # Search not nearest vertex not in the
        # shortest path tree
        for v in range(self.V):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v
 
        return min_index
 
    # Function that implements Dijkstra's single source
    # shortest path algorithm for a graph represented
    # using adjacency matrix representation
    def dijkstra(self, src):
 
        dist = [sys.maxsize] * self.V
        dist[src] = 0
        sptSet = [False] * self.V
 
        for cout in range(self.V):
 
            # Pick the minimum distance vertex from
            # the set of vertices not yet processed.
            # u is always equal to src in first iteration
            u = self.minDistance(dist, sptSet)
 
            # Put the minimum distance vertex in the
            # shotest path tree
            sptSet[u] = True
 
            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shotest path tree
            for v in range(self.V):
                if self.graph[u][v] > 0 and
                   sptSet[v] == False and
                   dist[v] > dist[u] + self.graph[u][v]:
                    dist[v] = dist[u] + self.graph[u][v]
 
        self.printSolution(dist)
 
 
# Driver program
g = Graph(9)
g.graph = map
g.dijkstra(0)
"""


def recv(r) -> str:
    return r.recv().decode("utf8")[:-2]


def split(message: str) -> list[tuple[int, ...]]:
    return [tuple(int(n) for n in tuple_.split(";"))
            for tuple_ in message.replace(",", ".").split("|")[1:]]


def move(r, num_livr, direction):
    r.send(f"MOVE|{num_livr}|{direction}")
    return recv(r) == "OK"


def teams(r):
    r.send("TEAMS")
    return int(recv(r).split("|")[1])


def get_bikers(r, num_livr):
    r.send(f"GETBIKERS|{num_livr}\r\n")
    return split(recv(r))


def get_map(r):
    r.send("GETMAP\r\n")
    data = recv(r).split("|")[1].translate(str.maketrans("REHS", "0312"))
    return np.array([[int(a) for a in data[i:i+31]]
                     for i in range(0, 31 * 31, 31)])


def take(r, num_livr):
    r.send("TAKE")


def start(host, port):
    r = pwn.remote(host, port)
    r.sendafter("NAME\r\n", "DogeTeam\r\n")
    teamId = int(recv(r).split("|")[1])
    return teamId, r


HOST = "127.0.0.1"
PORT = 2121

if __name__ == "__main__":

    # Parse arguments: python main.py <host> <port>
    parser = argparse.ArgumentParser()
    parser.add_argument("host", default=HOST)
    parser.add_argument("port", default=PORT, type=int)
    args = parser.parse_args()
    host = args.host
    port = args.port

    # Connect to remote server
    teamId, r = start(host, port)
    print(f"Team : {teamId}")
    print(get_bikers(r, teamId))
    print(get_map(r))