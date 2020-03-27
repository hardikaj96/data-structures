from .node import Node

class LinkedList:
    """Linked List definition"""
    def __init__(self):
        self.head = None

    def insert_start(self, data):
        self.head = Node(data, self.head)

    def insert_after(self, prev_node, data):
        prev_node.next = Node(data, prev_node.next)

    def insert_end(self, data):
        node = Node(data)
        if not self.head:
            self.head = node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = node

    def __repr__(self):
        curr = self.head
        nodes = []
        while curr:
            nodes.append(str(curr.data))
            curr = curr.next
        return '->'.join(nodes)

    def delete_node(self, key):
        curr = self.head
        if curr and curr.data == key:
            self.head = curr.next
            curr = None
            return

        while curr:
            if curr.data == key:
                break
            prev = curr
            curr = curr.next
        if curr == None:
            return
        prev.next = curr.next
        curr = None

    def __len__(self):
        curr = self.head
        length = 0
        while curr:
            length += 1
            curr = curr.next
        return length