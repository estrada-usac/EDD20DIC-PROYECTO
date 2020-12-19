from graphviz import Digraph, nohtml

# Clase que contiene la definición de los nodos que almacenarán
# la información dentro de la estructura.
class Node:
    def __init__(self, info):
        self.node_id = str(info[0])
        self.secret_pk = "0"
        self.primary_keys = []
        self.columns = len(info)
        self.info = info

# Clase que contiene la definción de las páginas que se utilizarán
# en la estructura para contener a los nodos con información.
class Page:
    def __init__(self):
        self.level = 0
        self.leaf = False
        self.overflow = False
        self.left = None
        self.mid = None
        self.right = None
        self.left_node = None
        self.right_node = None
        self.next_page = None
        self.left_sister = None
        self.right_sister = None
        self.overflow_page = None

    # Indica si la página está vacía o no
    @property
    def empty(self):
        if self.left_node == None and self.right_node == None:
            return True
        else:
            return False

    # Indica si una página tiene ocupados ambos slots
    @property
    def full(self):
        if self.left_node == None or self.right_node == None:
            return False
        else:
            return True

    # El nodo hijo más pequeño (sin tomar en cuenta las páginas de desborde)
    @property
    def lowest_child(self):
        if self.left != None and not self.left.empty:
            return self.left.lowest_child
        elif self.mid != None and not self.mid.empty:
            return self.mid.lowest_child
        elif self.right != None and not self.right.empty:
            return self.right.lowest_child
        else:
            return self.left_node if self.left_node != None else self.right_node

    # El nodo hijo más grande (sin tomar en cuenta las páginas de desborde)
    @property
    def highest_child(self):
        if self.right != None and not self.right.empty:
            return self.right.highest_child
        elif self.mid != None and not self.mid.empty:
            return self.mid.highest_child
        elif self.left != None and not self.left.empty:
            return self.left.highest_child
        else:
            return self.right_node if self.right_node != None else self.left_node

    # Indica si puede contraer sus hijos para volverse una sola página
    @property
    def can_contract(self):
        if self.left != None and self.mid != None and self.right != None:
            if self.left.leaf or self.mid.leaf or self.right.leaf:
                return True if self.count_children() <= 2 else False
            else:
                return self.left.can_contract and self.mid.can_contract and self.right.can_contract
        else:
            return True
        
    # Cuenta la cantidad de nodos hijo que tiene una página
    def count_children(self):
        if self.left != None and self.mid != None and self.right != None:
            return self.left.count_children() + self.mid.count_children() + self.right.count_children()
        else:
            if self.empty:
                return 0
            if self.full:
                return 2
            else:
                return 1

    # Inserta un nodo en la página
    def insert(self, new_node, full_tree):
        same_left_node = self.left_node != None and self.left_node.node_id == new_node.node_id
        same_right_node = self.right_node != None and self.right_node.node_id == new_node.node_id
        if same_left_node or same_right_node:
            # Ya está almacenado un nodo con ese id
            return 2
        elif self.left_node == None:
            # Si el slot izquierdo de la página está vacío
            self.left_node = new_node
            return 0
        elif self.right_node == None:
            # Si el slot derecho de la página está vacío
            if new_node.node_id > self.left_node.node_id:
                self.right_node = new_node
            else:
                self.right_node = self.left_node
                self.left_node = new_node
            return 0
        elif self.level < 2:
            # La página está llena pero aún queda espacio
            if not full_tree:
                return 3
            else:
                return 4
        elif not full_tree:
            return 3
        elif self.level == 2 and (new_node.node_id > self.right_node.node_id or new_node.node_id < self.left_node.node_id):
            if new_node.node_id > self.right_node.node_id:
                aux = self.right_node
                self.right_node = new_node
                self.insert(aux, full_tree)
            elif new_node.node_id < self.left_node.node_id:
                aux = self.left_node
                self.left_node = new_node
                self.insert(aux, full_tree)
        elif self.overflow_page == None:
            # Si la página ya está llena y no tiene página de overflow
            new_page = Page()
            new_page.level = self.level + 1
            new_page.overflow = True
            new_page.insert(new_node, full_tree)
            new_page.next_page = self.next_page
            self.next_page = new_page
            self.overflow_page = new_page
            return 0
        elif self.overflow_page != None:
            # Si la página ya está llena y tiene una página de overflow
            return self.overflow_page.insert(new_node, full_tree)

    # Extrae uno de los nodos de la página dándole prioridad al de la izquierda
    def __extract(self):
        if self.left_node != None:
            # Devolver el nodo izquierdo
            aux = self.left_node
            self.left_node = self.right_node
            self.right_node = aux
            self.delete(self.right_node.node_id)
            return aux
        elif self.right_node != None:
            # Devolver el nodo derecho
            aux = self.right_node
            self.delete(self.right_node.node_id)
            return aux

    # Elimina la página de desborde en caso de estar vacía
    def __clean_overflow(self):
        if self.overflow_page != None and self.overflow_page.empty:
            self.next_page = self.overflow_page.next_page
            self.overflow_page = None

    # Busca el nodo con el id especificado entre la página y sus
    # páginas de desborde (en caso de tenerlas) y lo elimina de la
    # estructura
    def delete(self, node_id):
        if self.left_node != None and self.left_node.node_id == node_id:
            if self.leaf:
                # Eliminar nodo de página hoja
                self.left_node = None
                # Obtener el nodo con el id más bajo
                temp = self.lowest()
                if temp != None and temp.node_id == self.right_node.node_id:
                    # El nodo con el id más pequeño es el derecho de la página hoja
                    self.left_node = self.right_node
                    if self.overflow_page != None:
                        self.right_node = self.overflow_page.highest()
                        self.overflow_page.delete(self.right_node.node_id)
                    else:
                        self.right_node = None
                else:
                    # El nodo con el id más pequeño es de una página de desborde
                    if self.overflow_page != None:
                        self.overflow_page.delete(temp.node_id)
                    self.left_node = temp
            else:
                # Eliminar nodo de página de desborde
                # Eliminar nodo izquierdo de la página
                self.left_node = self.right_node
                if self.overflow_page != None:
                    # Sustituir nodo eliminado
                    self.right_node = self.overflow_page.__extract()
                    if self.right_node.node_id < self.left_node.node_id:
                        aux = self.left_node
                        self.left_node = self.right_node
                        self.right_node = aux
                else:
                    # Dejar espacio vacío
                    self.right_node = None
            self.__clean_overflow()
            return 0
        elif self.right_node != None and self.right_node.node_id == node_id:
            if self.leaf:
                # Eliminar nodo de página hoja
                self.right_node = None
                # Obtener el nodo con el id más alto
                temp = self.highest()
                if temp != None and temp.node_id == self.left_node.node_id:
                    # El nodo con el id más alto es el izquierdo de la página hoja
                    if self.overflow_page != None:
                        self.right_node = self.left_node
                        self.left_node = self.overflow_page.lowest()
                    else:
                        self.right_node = None
                else:
                    # El nodo con el id más alto es de una página de desborde
                    if self.overflow_page != None:
                        self.overflow_page.delete(temp.node_id)
                    self.right_node = temp
            else:
                # Eliminar nodo de página de desborde
                # Eliminar nodo derecho de la página
                if self.overflow_page != None:
                    # Sustituir nodo eliminado
                    self.right_node = self.overflow_page.__extract()
                    if self.right_node.node_id < self.left_node.node_id:
                        aux = self.left_node
                        self.left_node = self.right_node
                        self.right_node = aux
                else:
                    # Dejar espacio vacío
                    self.right_node = None
            self.__clean_overflow()
            return 0
        elif self.overflow_page != None:
            # Eliminar nodo de la página de desborde
            code = self.overflow_page.delete(node_id)
            self.__clean_overflow()
            return code
        else:
            # No se encontró ningún nodo con ese id
            return 2        

    # Devuelve el nodo con el id más bajo de entre la página y sus
    # páginas de desborde (en caso de tenerlas)
    def lowest(self):
        aux = self
        temp = self.left_node if self.left_node != None else self.right_node
        while aux != None:
            if aux.left_node != None and aux.left_node.node_id < temp.node_id:
                temp = aux.left_node
            if aux.right_node != None and aux.right_node.node_id < temp.node_id:
                temp = aux.right_node
            aux = aux.overflow_page
        return temp

    # Devuelve el nodo con el id más alto de entre la página y sus
    # páginas de desborde (en caso de tenerlas)
    def highest(self):
        aux = self
        temp = self.left_node if self.left_node != None else self.right_node
        while aux != None:
            if aux.left_node != None and aux.left_node.node_id > temp.node_id:
                temp = aux.left_node
            if aux.right_node != None and aux.right_node.node_id > temp.node_id:
                temp = aux.right_node
            aux = aux.overflow_page
        return temp

    # Devuelve la página hijo más a la derecha de una página
    # si la página no tiene hijos, devuelve la página misma
    def rightmost(self):
        if self.right != None:
            return self.right.rightmost()
        else:
            return self

    # Devuelve la página hijo más a la izquierda de una página
    # si la página no tiene hijos, devuelve la página misma
    def leftmost(self):
        if self.left != None:
            return self.left.leftmost()
        else:
            return self

    # Identificación de la página
    @property
    def name(self):
        left_id = str(self.left_node.node_id) if self.left_node != None else "none{0}".format(self.level)
        right_id = str(self.right_node.node_id) if self.right_node != None else "none{0}".format(self.level)
        extra = str(self.next_page.name) if self.next_page != None else "extra"
        return left_id + right_id + extra

    # Procrea un nuevo nivel de páginas hijo
    def procreate(self):
        code = 1
        if self.leaf and self.left == self.mid == self.right == None:
            self.leaf = False
            self.left = Page()
            self.mid = Page()
            self.right = Page()
            self.left.leaf = True
            self.mid.leaf = True
            self.right.leaf = True
            self.left.level = self.level + 1
            self.mid.level = self.level + 1
            self.right.level = self.level + 1
            self.left.left_node = self.left_node
            self.mid.left_node = self.right_node
            self.left_node = self.right_node
            self.right_node = None
            self.left.next_page = self.mid
            self.mid.next_page = self.right
            self.next_page = None
            self.left.right_sister = self.mid
            self.mid.right_sister = self.right
            self.right.left_sister = self.mid
            self.mid.left_sister = self.left
            code = 0
        else:
            self.left.procreate()
            self.mid.procreate()
            self.right.procreate()
            lft_rightmost = self.left.rightmost()
            mid_rightmost = self.mid.rightmost()
            rgt_leftmost = self.right.leftmost()
            mid_leftmost = self.mid.leftmost()
            lft_rightmost.next_page = mid_leftmost
            mid_rightmost.next_page = rgt_leftmost
            lft_rightmost.right_sister = mid_leftmost
            mid_rightmost.right_sister = rgt_leftmost
            rgt_leftmost.left_sister = mid_rightmost
            mid_leftmost.left_sister =  lft_rightmost
            code = 0
        return code

    # Contrae las páginas hijo en caso de ser posible.
    def contract(self):
        if self.can_contract and self.left != None and self.mid != None and self.right != None:
            if self.left.leaf and self.mid.leaf and self.right.leaf:
                low = self.lowest_child
                high = self.highest_child
                self.next_page = self.right_sister
                self.left = None
                self.mid = None
                self.right = None
                self.left_node = low
                self.right_node = high
                self.leaf = True
            else:
                self.left.contract()
                self.mid.contract()
                self.right.contract()
            return 0
        else:
            return 1

# Clase que contiene la definicón de la estructura de datos ISAM
class Isam:
    def __init__(self):
        self.root = None
        self.leftmost = None
        self.height = None
    
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
                    aux.left_node = aux.mid.leftmost().left_node
                    aux.right_node = aux.right.leftmost().left_node
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
    def insert(self, new_node):
    	pass

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
    def draw(self, name="graph", show=False):
        graph = Digraph(name, node_attr={"shape": "record"}, graph_attr={"nodesep": ".5", "ranksep": "1", "splines": "line"})
        graph = self.__edit_graph(self.root, graph)
        graph.render(name, format="png", view=show)

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

    def __right_shift_sp(self, node_id, page):
        if not page.leaf:
            if node_id < page.left_node.node_id:
                code = self.__right_shift_sp(node_id, page.left)
            elif page.right_node != None:
                if node_id >= page.left_node.node_id and node_id < page.right_node.node_id:
                    code = self.__right_shift_sp(node_id, page.mid)
                if node_id >= page.right_node.node_id:
                    code = self.__right_shift_sp(node_id, page.right)
            else:
                code = self.__right_shift_sp(node_id, page.mid)
            self.update_level(page.level)
            return code
        else:
            if page.left_node != None and page.left_node.node_id == node_id:
                if page.right_sister != None:
                    code = self.__right_shift_sp(node_id, page.right_sister)
                    if code == 0:
                        page.left_node = None
                        self.update_level(page.level)
                        return 0
                    else:
                        return 1
                else:
                    return 1
            elif page.left_node != None and page.left_node.node_id != node_id:
                if page.right_sister != None:
                    code = self.__right_shift_sp(node_id, page.right_sister)
                    if code == 0:
                        page.left_node = page.left_sister.left_node
                        return 0
                    else:
                        return 1
                else:
                    return 1
            elif page.empty:
                page.left_node = page.left_sister.left_node
                return 0
            else:
                return 1

    # Mueve una posición a la derecha a la página que contenga el nodo
    # con el node_id indicado
    def right_shift_sp(self, node_id):
        return self.__right_shift_sp(node_id, self.root)

    def __left_shift_sp(self, node_id, page):
        if not page.leaf:
            if node_id < page.left_node.node_id:
                code = self.__left_shift_sp(node_id, page.left)
            elif page.right_node != None:
                if node_id >= page.left_node.node_id and node_id < page.right_node.node_id:
                    code = self.__left_shift_sp(node_id, page.mid)
                if node_id >= page.right_node.node_id:
                    code = self.__left_shift_sp(node_id, page.right)
            else:
                code = self.__left_shift_sp(node_id, page.mid)
            self.update_level(page.level)
            return code
        else:
            is_left_node = page.left_node != None and page.left_node.node_id == node_id
            is_right_node = page.right_node != None and page.right_node.node_id == node_id
            if is_left_node or is_right_node:
                aux = self.leftmost
                count = 1
                shift = False
                while aux != None:
                    if aux.empty:
                        shift = True
                        if aux.right_sister != None and not aux.right_sister.empty:
                            aux.left_node = aux.right_sister.left_node
                            aux.right_sister.left_node = None
                            aux.right_node = aux.right_sister.right_node
                            aux.right_sister.right_node = None
                        elif aux.right_sister != None and aux.right_sister.empty:
                            if count % 3 != 0:
                                aux.left_node = aux.right_sister.right_sister.left_node
                                aux.right_sister.right_sister.left_node = None
                                aux.right_node = aux.right_sister.right_sister.right_node
                                aux.right_sister.right_sister.right_node = None
                    is_left_node = aux.left_node != None and aux.left_node.node_id == node_id
                    is_right_node = aux.right_node != None and aux.right_node.node_id == node_id
                    if is_left_node or is_right_node:
                        return int(not shift)
                    self.update_level(1)
                    self.update_level(0)
                    aux = aux.right_sister
                    count += 1
                return 1
            else:
                return 1

    # Mueve una posición a la izquierda a la página que contenga el nodo
    # con el node_id indicado
    def left_shift_sp(self, node_id):
        return self.__left_shift_sp(node_id, self.root)

    def __right_shift(self, node_id, page):
        if not page.leaf:
            if node_id < page.left_node.node_id:
                code = self.__right_shift(node_id, page.left)
            elif page.right_node != None:
                if node_id >= page.left_node.node_id and node_id < page.right_node.node_id:
                    code = self.__right_shift(node_id, page.mid)
                if node_id >= page.right_node.node_id:
                    code = self.__right_shift(node_id, page.right)
            else:
                code = self.__right_shift(node_id, page.mid)
            self.update_level(page.level)
            return code
        else:
            is_left_node = page.left_node != None and page.left_node.node_id == node_id
            is_right_node = page.right_node != None and page.right_node.node_id == node_id
            if is_left_node or is_right_node:
                if page.right_sister != None:
                    code = self.__right_shift(node_id, page.right_sister)
                    if code == 0:
                        page.right_sister.left_node = page.right_node
                        page.right_node = None
                        if is_left_node:
                            page.right_node = page.left_node
                            page.left_node = None
                        return 0
                    else:
                        pass
                else:
                    return 1
            else:
                if page.full:
                    code = self.__right_shift(node_id, page.right_sister)
                    if code == 0:
                        page.right_sister.left_node = page.right_node
                        page.right_node = page.left_node
                        page.left_node = None
                    return code
                else:
                    page.right_node = page.left_node
                    page.left_node =  None
                    return 0

    # Mueve una posición a la derecha al nodo con el node_id indicado
    def right_shift(self, node_id):
        return self.__right_shift(node_id, self.root)

    def __left_shift(self, node_id, page):
        if not page.leaf:
            if node_id < page.left_node.node_id:
                code = self.__left_shift(node_id, page.left)
            elif page.right_node != None:
                if node_id >= page.left_node.node_id and node_id < page.right_node.node_id:
                    code = self.__left_shift(node_id, page.mid)
                if node_id >= page.right_node.node_id:
                    code = self.__left_shift(node_id, page.right)
            else:
                code = self.__left_shift(node_id, page.mid)
            self.update_level(page.level)
            return code
        else:
            is_left_node = page.left_node != None and page.left_node.node_id == node_id
            is_right_node = page.right_node != None and page.right_node.node_id == node_id
            if is_left_node or is_right_node:
                aux = self.leftmost
                while aux != None:
                    if aux.empty:
                        aux.left_node = aux.right_sister.left_node
                        aux.right_sister.left_node = None
                        if aux.left_node.node_id == node_id:
                            return 0
                    elif aux.full:
                        if aux.left_node.node_id == node_id or aux.right_node.node_id == node_id:
                            return 0
                    else:
                        aux.right_node = aux.right_sister.left_node
                        aux.right_sister.left_node = None
                        if aux.left_node.node_id == node_id or aux.right_node.node_id == node_id:
                            return 0
                    self.update_level(1)
                    self.update_level(0)
                    aux = aux.right_sister
                return 1
            else:
                return 1

    # Mueve una posición a la izquierda al nodo con el node_id indicado
    def left_shift(self, node_id):
        return self.__left_shift(node_id, self.root)

    # Devuelve una lista con todos los nodos de la estructura
    def get_all(self):
        nodes = []
        aux = self.leftmost
        while aux != None:
            if aux.left_node != None:
                nodes.append(aux.left_node)
            if aux.right_node != None:
                nodes.append(aux.right_node)
            aux = aux.next_page
        return nodes