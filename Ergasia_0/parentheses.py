class Stack:
    def __init__(self):
        self.stackNodes=[]
        print("Stack Initialized!")

    def empty(self):
        if len(self.stackNodes):
            return 0;
        else:
            return 1

    def push(self,char):
        self.stackNodes.append(char)
        print("Item pushed!")

    def pop(self):
        if(self.empty()):
            return
        print("Item popped!")
        temp=self.stackNodes.pop()

myStack=Stack()
parantheses=["[","(","(",")","(",")",")","]"]
for i in parantheses:
    if(i=="[" or i=="(" or i=="{"):
        myStack.push(i)
    else:
        myStack.pop()
if(myStack.empty()):
    print("Parenthesis well balanced!")
    print(len(myStack.stackNodes))
else:
    print("Parentheses are not well balanced")
    print(len(myStack.stackNodes))