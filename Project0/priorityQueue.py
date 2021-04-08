class Stack:

    MAXSTACKSIZE = 100 	# this contains the maximun number of items the stack can have

    # Constructor
    def __init__(self):
	self.items = []

    # Returns true if stack is empty and false if not
    def isEmpty(self):
	return self.items == []	 # uses logical == to return true or false

    # Returns true if stack is full and false if not
    def isFull(self):
	return len(self.items) == self.MAXSTACKSIZE


    # Push item on the top of the stack
    def push(self, item):
	self.items.append(item)

    # Pop item from the top of the stack
    def pop(self):
	return self.items.pop()


# Returns true when two parethenses are matched and false when they are not
def Match(c1, c2):
    if c2 == "[" :
	return c1 == "]" 
    if c2 == "(" :
	return c1 == ")"
    if c2 == "{" :
	return c1 == "}"

# Checks if a string of parentheses is balanced
def ParenMatch(string):
    stack = Stack()	# creating a stack 
    for c in string:	# iterating through string
	if c == "[" or c == "(" or c == "{" :
	    stack.push(c) # if we have an opening parentheses, we push it to stack
	elif c == "]" or c == ")" or c == "}" :
	    if stack.isEmpty(): # if we have a closing parentheses we first look if stack is empty. At this case, no opening parentheses would have been stored earlier.
		return("Unbalanced: More right parentheses then left parentheses.")
	    else: # if the stack is not empty
	        temp = stack.pop() # take the top item of the stack
		if not Match(c, temp) : #if the closing parentheses and the item poped from the top of the stack do not match
		    return("Unbalanced: Mismatched Parentheses.")
    if stack.isEmpty() : #everything is fine
        return("Balanced.")
    else:
	return("Unbalanced: More left parentheses than right parentheses.")







# Code to check our program

string = raw_input("Please give a string with parentheses to check whether is balances or not: ") # Program asks for a string of parentheses
print "You gave: " +  string # Printing the string given
print(ParenMatch(string)) # Printing balanced or not
