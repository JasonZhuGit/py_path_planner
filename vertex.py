#!/usr/bin/env python
# -*- coding:utf-8 -*-


class Vertex():
    def __init__(self, name=None, succ=None, prec=None, weight=0, dist=None, copied=False, visited=0, heur=0):
        self.name = name
        self.prec = prec #for tree or path
        self.succ = succ #for linking
        self.heur = heur #heuristic
        self.dist = dist
        self.weight = weight
        self.copied = copied
        self.visited = visited
        self.entry = None
        self.back = None

    def __str__(self):
        attr_dict = {'name': self.name,
                    'prec': self.prec,
                    'succ': self.succ,
                    'heur': self.heur,
                    'dist': self.dist,
                    'weight': self.weight,
                    'copied': self.copied,
                    'visited': self.visited,
                    'entry': self.entry,
                    'back': self.back}
        return str(attr_dict)

    def reset(self):
        self.dist = None
        self.visited = 0
        self.weight = 0
        self.entry = None
        self.back = None
        self.prec = None
    
    @property
    def name(self):
        return self._name

    @name.setter 
    def name(self, name):
        self._name = name
    
    @property
    def prec(self):
        return self._prec

    @prec.setter
    def prec(self, prec):
        self._prec = prec
    
    @property 
    def succ(self):
        return self._succ

    @succ.setter
    def succ(self, succ):
        self._succ = succ

    @property
    def heur(self):
        return self._heur

    @heur.setter 
    def heur(self, heur):
        self._heur = heur

    @property
    def entry(self):
        return self._entry

    @entry.setter
    def entry(self, entry):
        self._entry = entry
    
    @property
    def back(self):
        return self._back

    @back.setter
    def back(self, back):
        self._back = back

    @property 
    def weight(self):
        return self._weight

    @weight.setter 
    def weight(self, weight):
        self._weight = weight

    @property
    def dist(self):
        return self._dist

    @dist.setter 
    def dist(self, dist):
        self._dist = dist

    @property
    def copied(self):
        return self._copied

    @copied.setter 
    def copied(self, copied):
        self._copied = copied

    @property
    def visited(self):
        return self._visited

    @visited.setter
    def visited(self, visited): #0: white, 1: grey, 2: black
        self._visited = visited

    def insert(self, name, weight=0, dist=None, copied=True):
        vertex = Vertex(name, weight=weight, dist=dist, copied=copied)
        vertex.succ = self.succ
        self.succ = vertex


if __name__ == "__main__":
    pass
