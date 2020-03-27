from linkedlists.singlylinkedlist import LinkedList
from linkedlists.linkedStack import LinkedStack

def test_singlyLinkedList():
    L = LinkedList()
    L.insert_start(5)
    L.insert_start(7)
    L.insert_start(6)
    L.insert_after(L.head.next,1)
    L.insert_end(2)
    print(L)
    L.delete_node(5)
    print(L)

def test_linkedStack():
    S = LinkedStack()
    S.push(5)
    print(S.top())
    S.push(6)
    S.push(1)
    S.push(2)
    S.push(3)
    print(len(S))
    print(S.pop())
    print(S.is_empty())
    print(S)

test_linkedStack()