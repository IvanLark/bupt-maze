from asyncio import start_server


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Stack:
    def __init__(self):
        self.head = Node(None)
        self.head.next = None

    def put(self, data):
        # 头插法
        original_top = self.head.next
        top = Node(data)
        self.head.next = top
        top.next = original_top

    def pop(self):
        # 判断是否栈空
        if self.head.next is None:
            return None
        # 头取法
        top = self.head.next
        self.head.next = top.next
        return top.data

    def empty(self):
        return self.head.next is None
