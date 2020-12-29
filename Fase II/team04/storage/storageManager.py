from storage.avl import avlMode
from storage.b import BMode
def createDatabase(database: str, mode: string, encoding: string) -> int:
    if mode = "avl":
        avlMode.createDatabase(database)
    pass

def alterDatabaseMode(database: str, mode: str) -> int:
    # database = "base1"
    base1 = lista_bases.search("base1")
    
    if mode = "b":
        BMode.createDatabase("base1")
        tablas_temp = avlMode.showTables("base1")

        for nombre in tablas_temp:
            BMode.createTable(nombre, "base1")
            tuplas = avlMode.extractTable("base1", "tabla1")
            
            for tupla in tuplas:
                BMode.insert("base1", "tabla1", tupla)
        


    pass

# NODO
nombre = "base1"
tipo = "avl"
base = avlMode