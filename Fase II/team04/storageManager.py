# Package:      Storage Manager
# License:      Released under MIT License
# Notice:       Copyright (c) 2020 TytusDB Team
# Developers:   Alexis Peralta

from storage.avl import avlMode
from storage.b import BMode
from storage.bplus import BPlusMode
from storage.hash import HashMode
from storage.isam import ISAMMode
from storage.json_mode import jsonMode
from storage.dict import DictMode
from storage.b import Serializable
from DBList import DBList

MODES = ['avl', 'b', 'bplus', 'dict', 'isam', 'json', 'hash']

try:
    databases = Serializable.rollback("lista_bases_de_datos")
except FileNotFoundError:
    databases = DBList()
    Serializable.commit(databases, "lista_bases_de_datos")

def createDatabase(database: str, mode: str, encoding: str) -> int:
    if databases.search(database) != None:
        return 2
    if mode == "avl":
        code = avlMode.createDatabase(database)
    elif mode == "b":
        code = BMode.createDatabase(database)
    elif mode == "bplus":
        code = BPlusMode.createDatabase(database)
    elif mode == "dict":
        code = DictMode.createDatabase(database)
    elif mode == "isam":
        code = ISAMMode.createDatabase(database)
    elif mode == "json":
        code = jsonMode.createDatabase(database)
    elif mode == "hash":
        code = HashMode.createDatabase(database)
    else:
        return 3
    if code == 0:
        databases.create(database, mode)
        try:
            for i in range(5):
                try:
                    Serializable.commit(databases, "lista_bases_de_datos")
                except:
                    continue
        except:
            code_drop = dropDatabase(database)
            if code_drop == 0:
                databases.delete(database)
                return 1
            else:
                for i in range(4):
                    code_drop = dropDatabase(database)
                    if code_drop == 0:
                        databases.delete(database)
                        break
                return 1
    return code

def createTable(database: str, table: str, numberColumns: int) -> int:
    db = databases.search(database)
    if db == None:
        return 2
    if db.mode == "avl":
        result = avlMode.createTable(database, table, numberColumns)
    elif db.mode == "b":
        result = BMode.createTable(database, table, numberColumns)
    elif db.mode == "bplus":
        result = BPlusMode.createTable(database, table, numberColumns)
    elif db.mode == "dict":
        result = DictMode.createTable(database, table, numberColumns)
    elif db.mode == "isam":
        result = ISAMMode.createTable(database, table, numberColumns)
    elif db.mode == "json":
        result = jsonMode.createTable(database, table, numberColumns)
    elif db.mode == "hash":
        result = HashMode.createTable(database, table, numberColumns)
    return result

def showTables(database: str) -> list:
    db = databases.search(database)
    if db == None:
        return None
    if db.mode == "avl":
        result = avlMode.showTables(database)
    elif db.mode == "b":
        result = BMode.showTables(database)
    elif db.mode == "bplus":
        result = BPlusMode.showTables(database)
    elif db.mode == "dict":
        result = DictMode.showTables(database)
    elif db.mode == "isam":
        result = ISAMMode.showTables(database)
    elif db.mode == "json":
        result = jsonMode.showTables(database)
    elif db.mode == "hash":
        result = HashMode.showTables(database)
    return result

def codificar(texto, condificacion):
    pass

def insert(database: str, table: str, register: list):
    db = databases.search(database)
    if db == None:
        return 2
    for x in range(0, len(register)):
        register[x] = codificar(register[x], db.encoding)
    if db.mode == "avl":
        result = avlMode.insert(database, table, register)
    pass