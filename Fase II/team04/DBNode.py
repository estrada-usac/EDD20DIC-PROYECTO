# Package:      Storage Manager
# License:      Released under MIT License
# Notice:       Copyright (c) 2020 TytusDB Team
# Developer:    Alexis Peralta

# Nodos utilizados en las listas DBList
class DBNode:
    def __init__(self, name, mode):
        self.name = name
        self.mode = mode
        self.next = None