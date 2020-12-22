#from graphviz import Digraph, nohtml
from Page import *


# Clase que contiene la definicón de la estructura de datos ISAM
class Isam:
    def __init__(self):
        self.root = None
        self.leftmost = None
        self.height = 0 # cambiamos None a 0 INSERTAR

    # Indica si la parte arborea de la estructura ya está llena
    # (Se encuentra llena cuando todas las páginas están llenas)
    @property
    def full(self):
        children = self.root.count_children()
        expected_children = (3**self.height)*2
        return True if children == expected_children else False

    def __full_level(self, level, page):
        if page.level == level:
            result = page.full
            aux = page
            while aux != None:
                result = result and aux.full
                aux = aux.right_sister
            return int(result)
        else:
            if page.left != None:
                return self.__full_level(level, page.left)
            else:
                return 2

    def full_level(self, level):
        return self.__full_level(level, self.root)

    def __update_level(self, level, page):
        if page.level == level:
            aux = page
            while aux != None:
                if aux.mid != None and aux.right != None:
                    aux.left_node = aux.mid.lowest_child
                    aux.right_node = aux.right.lowest_child
                aux = aux.right_sister
            return 0
        else:
            if page.left != None:
                return self.__update_level(level, page.left)
            else:
                return 1

    def update_level(self, level):
        return self.__update_level(level, self.root)

            # Inserta un nuevo nodo con información en la estructura

    def insert(self, new_node, new_raiz):
        if self.root == None:  # Si la raiz es igual a nula
            # Creamos la pagina
            new_page = Page()
            self.root = new_page
            self.leftmost = self.root
            self.root.leaf = True
            self.root.level = 0
            # Insertar Nodo En Página
            full_page = self.root.full
            self.root.insert(new_node, full_page)
        else: # La Raíz No Es Nula

            # Verificar Si Página actual Esta Llena
             #La pagina esta llena
            if new_raiz.full:
                full_page = new_raiz.full
                insert_return = new_raiz.insert(new_node,full_page)

                if inset_return == 0: #Se inserto correctamente
                    pass
                elif insert_return == 1: #Ocurrio Un Problema
                    pass
                elif insert_return == 2: #Ya Existe un Nodo con el # IDEA:
                    pass
                elif insert_return == 3: #La Pagina esta llena pero la estructura arborea no (es posible un Corrimiento)
                    
                    if new_raiz.leaf: # es hoja //FALTA HACER ESTA PARTE
                        code = self.full_level(new_raiz.level) #verifico si el nivel esta lleno
                        if code == 0: #no lleno
                            #Se va por la izquierda
                            if new_node.node_id < new_raiz.node_izq.node_id:
                                self.insert(new_node,new_raiz.left)
                            #Se va por el medio
                            elif new_node.node_id > new_raiz.node_izq.node_id and new_node.node_id < new_raiz.node_der.node_id:
                                self.insert(new_node,new_raiz.mid)
                            #Se va por la Derecha
                            elif new_node.node_id > new_raiz.node_der.node_id:
                                self.insert(new_node, new_raiz.der)

                        elif code == 1: #corrimiento especial , si el nivel esta lleno
                         # rotaciones de hojas

                    else: #la raiz no es una hoja

                       lleno_nivel = self.full_level(new_raiz.level) #verifico nivel
                        if lleno_nivel == 0: #nivel no lleno


                        elif lleno_nivel = 1:#nivel lleno

                            #Se es menor al de la izquierda
                            if new_node.node_id < new_raiz.node_izq.node_id:
                                if new_node.node_id < new_raiz.left.node_izq.node_id:#nodo menor al menor hijo izq
                                    aux = new_node.node_id
                                    new_node.node_id = new_raiz.left.node_izq.node_id#el entrante sera el menor del hijo izq
                                    new_raiz.left.node_izq.node_id = aux #el menor del hijo izq sera el que iba a entrar antes
                                    corrio = left_shift_sp(new_raiz.left.node_izq.node_id) # corro y mando la pagina con el menor del hijo izq
                                    if corrio  == 0:#corrio nodos a la izq
                                        self.insert(new_node,new_raiz.left)
                                        self.update_level(new_raiz.level) #update mando la raiz
                                    elif corrio == 1:#no corrio a la izq
                                        if new_node.node_id < new_raiz.node_izq.node_id: #manda a correr hijo izq
                                            corro = right_shift_sp(new_raiz.left.node_izq.node_id) # corro y mando la pagina con el menor del hijo izq
                                            if corro == 0:
                                                self.insert(new_node,new_raiz.left)
                                                self.update_level(new_raiz.level) #update mando la raiz

                                            elif corro == 1:
                                                #rotacion ramas

                                        elif new_node.node_id > new_raiz.node_izq.node_id: #manda correr hijo medio
                                            corro = right_shift_sp(new_raiz.mid.node_izq.node_id) # corro y mando la pagina con el menor del hijo medio
                                            if corro == 0:
                                                self.insert(new_node,new_raiz.mid)
                                                self.update_level(new_raiz.level) #update mando la raiz

                                            elif corro == 1:
                                                #rotacion ramas

                                elif new_node.node_id > new_raiz.left.node_izq.node_id:
                                    corrio = left_shift_sp(new_raiz.left.node_izq.node_id) # corro y mando la pagina con el menor del hijo izq
                                    self.insert(new_node,new_raiz.left)       
                                    #FALTA CODIGO

                            #Se va por el medio
                            elif new_node.node_id > new_raiz.node_izq.node_id and new_node.node_id < new_raiz.node_der.node_id:
                                corrio = left_shift_sp(new_raiz.mid.node_izq.node_id) # corro y mando la pagina con el menor del hijo medio
                                    if corrio  == 0:#corrio nodos a la izq
                                        self.insert(new_node,new_raiz.mid)
                                        self.update_level(new_raiz.level) #update mando la raiz
                                    elif corrio == 1:#no corrio a la izq
                                        corro = right_shift_sp(new_raiz.right.node_izq.node_id) # corro y mando la pagina con el menor del hijo izq
                                            if corro == 0:
                                                self.insert(new_node,new_raiz.right)
                                                self.update_level(new_raiz.level) #update mando la raiz
                                            elif corro == 1:
                                                #rotacion ramas

                            #Si es mayor al derecho
                            elif new_node.node_id > new_raiz.node_der.node_id:
                                corrio = left_shift_sp(new_raiz.right.node_izq.node_id) # corro y mando la pagina con el menor del hijo medio
                                    if corrio  == 0:#corrio nodos a la izq
                                        self.insert(new_node,new_raiz.right)
                                        self.update_level(new_raiz.level) #update mando la raiz
                                    elif corrio == 1:#no corrio a la izq
                                        corro = right_shift_sp(new_raiz.right.right_sister.node_izq.node_id) # corro y mando la pagina con el menor del hijo izq
                                            if corro == 0:
                                                self.insert(new_node,new_raiz.right.right_sister)
                                                self.update_level(new_raiz.level) #update mando la raiz
                                            elif corro == 1:
                                                #rotacion ramas    
                      
                elif insert_return == 4: #si hay posibilidad crear nuevos hijos
                    #print("insert_return = 4")
                    self.root.procreate() #baja los nodos tambien

                    # Busca En Que Página Insetar (Izq o Der)
                    if new_node.node_id < new_raiz.left_node.node_id:
                        # Se Va Por La izquierda
                        self.insert(new_node, new_raiz.left)
                    elif new_node.node_id > new_raiz.left_node.node_id:
                        # Se Va Por La Derecha
                        self.insert(new_node, new_raiz.right)

                    # Despues De Recursividad Regresa Al Padre Y Actualiza
                    self.update_level(new_raiz.level)
            # La Página No Está Llena TRABAJANDO ACTUALMENTE
            else: 
                if new_raiz.left_node.node_id != None:
                    if new_raiz.leaf: # es una hoja
                                
                    else: #no es una hoja
                        if full_level(new_raiz.level): # nivel esta lleno, deberia ser si nivel lleno excepto la raiz_actual
                            #supuesto error
                        else:  # el nivel no esta lleno
                                    
                                #si es menor 
                            if new_node.node_id < new_raiz.node_izq.node_id:

                                #Si nodo menor al menor hijo izq
                                if new_node.node_id < new_raiz.left.node_izq.node_id:
                                    aux = new_node.node_id
                                    new_node.node_id = new_raiz.left.node_izq.node_id#el entrante sera el menor del hijo izq
                                    new_raiz.left.node_izq.node_id = aux #el menor del hijo izq sera el que iba a entrar antes
                                    corrio = left_shift_sp(new_raiz.left.node_izq.node_id) # corro y mando la pagina con el menor del hijo izq
                                    if corrio  == 0:#corrio nodos a la izq
                                        self.insert(new_node,new_raiz.left)
                                        self.update_level(new_raiz.level) #update mando la raiz
                                    elif corrio == 1:#no corrio a la izq
                                        #vuelvo nodos como estaban antes , el menor sera el nuevo y el de la izq el valor tenia al principio
                                        aux2 = new_node.node_id
                                        new_node.node_id = new_raiz.left.node_izq.node_id
                                        new_raiz.left.node_izq.node_id = aux2 #el menor del hijo izq sera el que iba a entrar antes
                                        corro = right_shift_sp(new_raiz.left.node_izq.node_id) # corro y mando la pagina con el menor del hijo izq
                                        if corro == 0:#inserta 
                                            self.insert(new_node,new_raiz.left)
                                            self.update_level(new_raiz.level) #update mando la raiz

                                        elif corro == 1:
                                            #error
                                            
                                elif new_node.node_id > new_raiz.left.node_izq.node_id:
                                    


                                #si es mayor
                                #si es mayor
                            elif new_node.node_id > new_raiz.node_der.node_id:
                                #llamo correr izq, mando rama media
                                correr = left_shift_sp(new_raiz.mid.node_izq.node_id)
                                if correr == 0:
                                    self.insert(new_node,new.raiz.mid)
                                    self.update_level(new_raiz.level)
                                elif correr == 1:
                                    corro = right_shift_sp(new_raiz.right.node_izq.node_id)
                                    if corro == 0:
                                        self.insert(new_node,new_raiz.right)
                                        self.update_level(new_raiz.level)
                                    elif corro == 1:
                                        #error

                
                # Retorna el nodo con el id especificado 
                
    def search(self, node_id):
    	pass

        # Busca y elimina el nodo con el id especificado
    def delete(self, node_id):
    	pass

        # Busca un nodo dentro de la estructura y lo sustituye con el
        # nodo especificado. Para la búsqueda utiliza el id del nodo
        # especificado en los parametros
    def modify(self, edited_node):
    	pass

        # Edita el grafo de manera recursiva
    def __edit_graph(self, page, graph):
        if page != None:
            str1 = str(page.left_node.node_id) if page.left_node != None else "None"
            str2 = str(page.right_node.node_id) if page.right_node != None else "None"
            str3 = "<f0> |<f1> {0}|<f2> |<f3> {1}|<f4>".format(str1, str2)
            graph.node(page.name, nohtml(str3))
            if page.left != None:
                graph = self.__edit_graph(page.left, graph)
                graph.edge("{0}:f0".format(page.name), "{0}:f2".format(page.left.name), tailport="sw")
            if page.mid != None:
                graph = self.__edit_graph(page.mid, graph)
                graph.edge("{0}:f2".format(page.name), "{0}:f2".format(page.mid.name), tailport="s")
            if page.right != None:
                graph = self.__edit_graph(page.right, graph)
                graph.edge("{0}:f4".format(page.name), "{0}:f2".format(page.right.name), tailport="se")
            if page.overflow_page != None:
                graph = self.__edit_graph(page.overflow_page, graph)
                graph.edge("{0}:f2".format(page.name), "{0}:f2".format(page.overflow_page.name), tailport="s")
        return graph

        # Muestra la estructura de forma gráfica
    def show(self):
        graph = Digraph("graph", node_attr={"shape": "record"}, graph_attr={"nodesep": ".5", "ranksep": "2", "splines": "line"})
        graph = self.__edit_graph(self.root, graph)
        graph.render("graph", format="png", view=True)

        # Crea un nuevo nivel de páginas hijo para todas las páginas
        # en el último nivel. Aplica sólo cuando el árbol tiene menos de
        # 3 niveles.
    def procreate(self):
        if self.full and self.height < 2:
            if self.root.procreate() == 0:
                self.height += 1
                self.leftmost = self.root.leftmost()
                return 0
            else:
                return 1

    # Contrae un nivel del árbol en caso de ser posible.
    def contract(self):
        if self.root.contract() == 0:
            self.height -= 1
            self.leftmost = self.root.leftmost()
            return 0
        else:
            return 1

    # Mueve una posición a la derecha a la página que contenga el nodo
    # con el node_id indicado
    def __right_shift_sp(node_id):
        pass

        # Mueve una posición a la derecha a la página que contenga el nodo
        # con el node_id indicado
    def right_shift_sp(node_id):
        pass

    # Mueve una posición a la izquierda a la página que contenga el nodo
    # con el node_id indicado
    def __left_shift_sp(node_id, page):
        pass

    # Mueve una posición a la izquierda a la página que contenga el nodo
    # con el node_id indicado
    def left_sifht_sp(node_id):
        pass

    # Mueve una posición a la derecha al nodo con el node_id indicado
    def __right_shift(node_id):
        pass

        # Mueve una posición a la derecha al nodo con el node_id indicado
    def right_shift(node_id):
        pass

    # Mueve una posición a la izquierda al nodo con el node_id indicado
    def __left_shift(node_id, page):
        pass

    # Mueve una posición a la izquierda al nodo con el node_id indicado
    def left_shift(node_id):
        pass
