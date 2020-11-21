import math

class BNode:
    def __init__(self, m):
        self.data = [None] * (m+1)
        self.children = [None] * (m+2)
        self.count = 0
        self.m = m

    def insert_into(self, value, index):
        j = self.count
        #print(self.data)
        while j > index:
            self.data[j] = self.data[j-1]
            self.children[j+1] = self.children[j]
            j -= 1
        self.data[index] = value
        self.children[index+1] = self.children[index]
        #print(self.data)
        self.count += 1


    def split(self, index):
        print("split node")
        ptr = self.children[index]
        child0 = BNode(ptr.m)
        child1 = BNode(ptr.m)
        i = 0
        print(math.ceil(ptr.m / 2))
        while i < math.ceil(ptr.m / 2):
            child0.children[i] = ptr.children[i]
            print("ptr.data[i]",ptr.data[i])
            child0.data[i] = ptr.data[i]
            child0.count += 1
            i += 1
        child0.children[i] = ptr.children[i]
        mid = i

        j = 0
        print("ptr.count",ptr.count)
        while i < ptr.count:
            child1.children[j] = ptr.children[i]
            print("ptr.data[i]",ptr.data[i])
            child1.data[j] = ptr.data[i]
            child1.count += 1
            j += 1
            i += 1
        child1.children[j] = ptr.children[i]
        self.insert_into(ptr.data[mid], index)
        self.children[index] = child0
        self.children[index + 1] = child1
        print("mid "+str(mid))
        print("index "+str(index))
        print("self.children[index] "+str(self.children[index].data))
        print("self.children[index+1] "+str(self.children[index+1].data))
        print("ptr.data[mid] "+str(ptr.data[mid]))


    def insert(self,value):
        index = 0
        while index < self.count and self.data[index] <= value:
            index += 1

        if self.children[index] == None:
            #print("insert into ", value, index)
            self.insert_into(value, index)
        else:
            state = self.children[index].insert(value)
            if state == -1:
                self.split(index)
        return -1 if self.count >= self.m else 1


    def retirar(self, value, level):
        print(self.data[:self.count])
        if value in self.data: #si el valor a eliminar se encuentra en un Nodo u Hoja
            index = self.data.index(value)
            print("index "+str(index))
            print("level "+str(level))
            if self.children[index+1] != None:
                nivel, dato = self.children[index+1].retirar(value, level+1)
            else: # en caso de que se nodo hoja
                print(self.data)
                self.data.remove(value)
                self.count -= 1
                print(self.data)
                return level, self.data[0]
            print("level vs nivel", level, nivel)
            if level < nivel:
                print(self.data)
                self.data[index] = dato
                print(self.data)
                return nivel, self.data[0]
        else: #si el valor no se encuentra en un nodo
            print("no se encuentra en este nivel")
            index=0
            for i in range(0, self.count):
                if value < self.data[i]:
                    index = i-1
            print("index "+str(index))
            print("level "+str(level))
            if self.children[index] != None:
                nivel, dato = self.children[index+1].retirar(value, level+1)
            else: # en caso de que se nodo hoja
                print("Nodo no encontrado, revisar  valor")
                return 0, 0
            return nivel, dato



def find(ptr, value):
    if ptr != None:
        print("ptr.count "+str(ptr.count))
        i = 0
        while i < ptr.count:
            print("ptr.data["+str(i)+"] "+str(ptr.data[i]))
            if value == ptr.data[i]:
                return True
            elif value < ptr.data[i]:
                return True if find(ptr.children[i], value) == True else False
            else:
                i += 1
        if i == ptr.count:
            print("final")
            return True if find(ptr.children[i], value) == True else False
    else:
        print("Not Found")





def print_rec(ptr, level):
    if ptr != None:
        i = ptr.count - 1
        while i >= 0:
            print_rec(ptr.children[i+1], level + 1)
            for j in range(level):
                print("\t\t", end = "")
            print(ptr.data[i])
            i -= 1
        print_rec(ptr.children[0], level + 1)

def split_root(ptr):
    print("split root")
    child0 = BNode(ptr.m)
    child1 = BNode(ptr.m)
    i = 0
    print(math.ceil(ptr.m / 2))
    while i < math.ceil(ptr.m / 2):
        child0.children[i] = ptr.children[i]
        print("ptr.data[i]",ptr.data[i])
        child0.data[i] = ptr.data[i]
        child0.count += 1
        i += 1
    child0.children[i] = ptr.children[i]
    mid = i
    #i += 1  # skip
    j = 0
    while i < ptr.count:
        child1.children[j] = ptr.children[i]
        print("ptr.data[i]",ptr.data[i])
        child1.data[j] = ptr.data[i]
        child1.count += 1
        j += 1
        i += 1
    child1.children[j] = ptr.children[i]
    ptr.data[0] = ptr.data[mid]
    ptr.children[0] = child0
    ptr.children[1] = child1
    ptr.count = 1
    print("mid",mid)
    print("ptr.children[0].data",ptr.children[0].data)
    print("ptr.children[1].data",ptr.children[1].data)
    print("ptr.count ",ptr.count)

class BTree:
    def __init__(self, m=4):
        self.m = m
        self.root = BNode(m)

    def insert(self, value):
        print("insertando valor ",value)
        state = self.root.insert(value)
        if state == -1:
            #print("Split Root")
            split_root(self.root)

    def encontrar(self, value):
        print("\nBuscando ************** "+str(value))
        print(find(self.root, value))


    def print(self):
        print("\nMostrando Arbol *****************************************")
        print_rec(self.root, 0)

    def quitar(self, value):
        print("\nRemoviendo *************** "+str(value))
        level = 0
        state = self.root.retirar(value, level)
        if state == -1:
            pass


#Creando B+ Tree
bplustree = BTree(4)
#insertando valores al B+ Tree
for i in range(1, 26):
    bplustree.insert(i)
    bplustree.print()
#viendo el Arbol de forma gráfica
bplustree.print()

#~buscando un valor existente
bplustree.encontrar(5)
#buscando un valor no existente
bplustree.encontrar(105)

#quitando un valor existente
bplustree.quitar(53)
#quitando un valor que no existe
bplustree.quitar(53)
#volviendo a mostrar B+ tree para demostrar borrados.
bplustree.print()
