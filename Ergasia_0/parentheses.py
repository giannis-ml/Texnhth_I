class Stack:
    def __init__(self):
        self.stackNodes=[] #in init function i create a list, which will implement the stack 
        print("Stack Initialized!")     #and i print a message for this

    def empty(self):
        if len(self.stackNodes):    #in empty function i check the length of list and if this 
            return 0;       #is zero stack is empty
        else:
            return 1

    def push(self,char):
        self.stackNodes.append(char)    #in push function i use append(char) to put an element into stack
        print("Item pushed!")

    def pop(self):
        if(self.empty()):   #in pop function if stack is empty i don't do anything
            return          #in other case i use pop()
        temp=self.stackNodes.pop()
        print("Item popped!")

myStack=Stack()
parantheses=["[","(","(",")","(",")",")","]"]
for i in parantheses:
    if(i=="[" or i=="(" or i=="{"):
        myStack.push(i)
    elif(i=="]" or i==")" or i=="}"):
        if(myStack.empty()):  #this is the case that i want to use pop() in an empty list
            print("Parentheses are not well balanced")
            exit()
        else:
            myStack.pop()
    else:
        print("Unauthorized character!")
        exit()
if(myStack.empty()):
    print("Parenthesis well balanced!")
else:
    print("Parentheses are not well balanced")