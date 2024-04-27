class Stack:
    def __init__(self):
        self.stack_size_limit = 5
        self.stack = []
            
    def size(self):
        return len(self.stack)

    def is_full(self):
        if self.size() == self.stack_size_limit:
            return True
        return False      

    def push(self,item):
        if not self.is_full():        
            self.stack.append(item)
        else:
            return print("The stack is full!")

    def is_empty(self):
        if self.size() == 0:
            return "Yes"
        return "No"

    def pop(self):
        if self.is_empty()== "No":
            return self.stack.pop()
        return "The stack is empty!"

    def top(self):
        if self.is_empty()== "No":
            return self.stack[-1]
        return None
