class Order:
    def __init__(self, qtty, customer):
        self.customer = customer
        self.qtty = qtty

    def getCustomer(self):
        return self.customer

    def getQtty(self):
        return self.qtty

    def print(self):
        print(f"     Customer: {self.getCustomer()}")
        print(f"     Quantity: {self.getQtty()}")
        print("     ------------")


class Node:
    def __init__(self, element):
        self.element = element
        self.next = None

    def getNext(self):
        return self.next

    def setNext(self, next_node):
        self.next = next_node

class Queue:
    def __init__(self):
        self.first = None
        self.last = None
        self._size = 0

    def size(self):
        return self._size

    def isEmpty(self):
        return self._size == 0

    def front(self):
        if self.isEmpty():
            return None
        return self.first.element

    def enqueue(self, info):
        new_node = Node(info)
        if self.isEmpty():
            self.first = new_node
        else:
            self.last.setNext(new_node)
        self.last = new_node
        self._size += 1

    def dequeue(self):
        if self.isEmpty():
            return None
        result = self.first.element
        self.first = self.first.getNext()
        self._size -= 1
        if self.isEmpty():
            self.last = None
        return result

    def printInfo(self):
        print("********* QUEUE DUMP *********")
        print(f"   Size: {self._size}")
        node = self.first
        count = 1
        while node is not None:
            print(f"   ** Element {count}")
            node.element.print()
            node = node.getNext()
            count += 1
        print("******************************")


if __name__ == "__main__":
    queue = Queue()


    o1 = Order(20, "cust1")
    o2 = Order(30, "cust2")
    o3 = Order(40, "cust3")
    o4 = Order(50, "cust3")

    queue.enqueue(o1)
    queue.enqueue(o2)
    queue.enqueue(o3)
    queue.enqueue(o4)

    queue.printInfo()
