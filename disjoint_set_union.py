class DSU:
    def __init__(self, total: int):
        self.father = [index for index in range(total)]

    def find(self, index: int):
        if index == self.father[index]:
            return index
        leader = self.find(self.father[index])
        self.father[index] = leader
        return leader

    def join(self, index_a: int, index_b: int):
        a_leader = self.find(index_a)
        b_leader = self.find(index_b)
        if a_leader != b_leader:
            self.father[a_leader] = b_leader
