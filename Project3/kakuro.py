from csp import *
import time  # for time calculation


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#           class Kakuro represents the kakuro problem
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class Kakuro(CSP):

    def __init__(self, variables, domains, neighbors, constraints, numberOfBlankSquares):
        #self.blankValues = None   # this is the number that the blank square is gonna take.
        self.elapsedTime = None  # this is the total time needed from blank square to take a value.
        self.numberOfBlankSquares = numberOfBlankSquares
        self.Result = None

        CSP.__init__(self, variables, domains, neighbors, constraints)  # initializing CSP.

    #=======================================================================
    #           *** MAC + MRV + LCV ***
    #=======================================================================

    def MAC_MRV_LCV(self):
       
        start_time = (time.time() * 1000)

        btResult = backtracking_search(self, select_unassigned_variable=mrv,order_domain_values=lcv,inference=mac) # infernce is MAC here.

        self.elapsedTime = (time.time() * 1000) - start_time     # keeping the elapsed time in miliseconds.

        if not btResult:
            self.Result = "Sorry, there is not any solution\n"
        else:
            self.Result = "MAC + MRV + LCV SOLUTION\n-----------------------------------------------\n"
            self.Result += "These are the blank squares and their values:\n"

        for i in range(self.numberOfBlankSquares):
            self.Result += "Blank Square no"
            self.Result += str(i+1)
            self.Result += " -> "
            self.Result += str(btResult[i+1])
            self.Result += "\n\n"

        self.Result += "Elapsed Time: "
        self.Result += str(self.elapsedTime)
        self.Result += " miliseconds\n\n"

    #=======================================================================
    #           *** FC + MRV + LCV ***
    #=======================================================================


    def FC_MRV_LCV(self):
    
        start_time = (time.time() * 1000)
    
        btResult = backtracking_search(self, select_unassigned_variable=mrv,order_domain_values=lcv,inference=forward_checking) # inference is FC (forward_checking) here.
        
        self.elapsedTime = (time.time() * 1000) - start_time     # keeping the elapsed time in miliseconds.
        
        if not btResult:
            self.Result = "Sorry, there is not any solution\n"
        else:
            self.Result = "FC + MRV + LCV SOLUTION\n-----------------------------------------------\n"
            self.Result += "These are the blank squares and their values:\n"
    
        for i in range(self.numberOfBlankSquares):
            self.Result += "Blank Square no"
            self.Result += str(i+1)
            self.Result += " -> "
            self.Result += str(btResult[i+1])
            self.Result += "\n\n"
        
        self.Result += "Elapsed Time: "
        self.Result += str(self.elapsedTime)
        self.Result += " miliseconds\n\n"

    #=======================================================================

    def printBlankSquareValues(self):
        print (self.Result)

    def getElapsedTime(self):
        return (self.elapsedTime)
    def getNassigns(self):
        return self.nassigns

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#           class Puzzle represents the frid of kakuro puzzle
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


 #this conversts a list of lists to its cartesian product
# ex. [[1,2], [3,4]] -> [ (1,3), (1,4), (2,3), (2,4)]
def cartesianProduct(listOfLists):
    if listOfLists == []:
         return [()]
    newList = []
    for x in cartesianProduct(listOfLists[:-1]):
        for y in listOfLists[-1]:
            newList.append(x + (y,))
    return newList



class Puzzle():

    def __init__(self,numberOfBlankSquares, sums):
        self.sums = sums # sums represent the sums of line (or column) (ex. [["x2", "x4", 4], ["x1", "x3", 5]] )
        self.numberOfBlankSquares = numberOfBlankSquares # this is the number of white squares

        self.setVariables()
        self.setDomains()
        self.setNeighbors()
        self.constraints = self.setConstraints
        
        
    def getNumberOfBlankSquares(self):
        return self.numberOfBlankSquares

    def getVariables(self):
         return self.variables

    def getDomains(self):
        return self.domains

    def getNeighbors(self):
       return self.neighbors

    def getConstraints(self):
         return self.constraints

    # creating a list of all variables needed
    # example: ["x1", "x2", 5] -> [1, 2, 3]
    def setVariables(self):
        newList = []
        for i in range(len(self.sums) + self.numberOfBlankSquares):
            newList.append(i+1)
        self.variables = newList
    #--------------------------------------------------
    # returns a list(a) of list(b) of lists(c).
    # Last element of list(b) is the list(c) of blank squares of a specific sum
    # The rest elements of list (b) are lists(b) of all the possible values that give the sum-goal
    def setDomains(self):
        possibleValues = [1,2,3,4,5,6,7,8,9]
        domains = {}

        # creating domains of variables which represent blank squares
        for i in range(self.numberOfBlankSquares):
            domains[i+1] = []
            for j in possibleValues:
                domains[i+1].append(j)
        # creating domains of each sum
        for i in range(len(self.sums)):
                
            #twicePossibleValues is: [[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]]
            twicePossibleValues = []
            for item in self.sums[i]:
                if not isinstance(item, int): # skips the x1/x2...which are the last item of list
                    twicePossibleValues.append(possibleValues)

            combinations = cartesianProduct(twicePossibleValues)
            okValues = []

            for  item in combinations:
                cntr = 0
                for aValue in item:
                    cntr += aValue
                if cntr == self.sums[i][-1]:
                    newItem = []
                    newItem = list(item)
                    newItem.append((self.sums[i][0:len(self.sums[i])- 1])) # adding the x name of variables of sum
                    okValues.append(newItem)
            domains[i + (self.numberOfBlankSquares + 1)] = okValues
        self.domains = domains
    #--------------------------------------------------

    def setNeighbors(self):
        neighbors = {}
            
        # creating neighbors of variables which represent blank squares
        for i in range(self.numberOfBlankSquares):
            currentNeighbors = []

            cntr = 0 # this keeps the number of sum
            for item in self.sums:
                if  "x" + str(i + 1) in item: # if the variable Xi exists in item
                    for aValue in item: # for each value in item
                        if (not isinstance(aValue,int)) and (aValue != "x" + str(i + 1)): # skips the value of summary and its own variable Xi
                            currentNeighbors.append(int (aValue[1:]))
                    currentNeighbors.append(self.numberOfBlankSquares+1+cntr)
                cntr += 1
            currentNeighbors.sort() # in order to keep current neighbors sorted
            neighbors[i+1] = currentNeighbors
            
        # creating neighbors of each sum
        for i in range(len(self.sums)):
            currentNeighbors = [] # neighbors of i
            for aValue in self.sums[i]:
                if not isinstance(aValue,int): #skips the value of summary
                    currentNeighbors.append(int(aValue[1:])) # adds a new neighbor

            currentNeighbors.sort() # keeping neighbors sorted
            neighbors[self.numberOfBlankSquares+1+i] = currentNeighbors

        self.neighbors = neighbors
    #--------------------------------------------------

    def setConstraints(self,X,x,Y,y):

        # if X, Y are variables which represent blank squares
        if isinstance(x,int) and isinstance(y,int):
            return x != y #  neighbors must be different

        if isinstance(y,int):
            temp = x[-1]
            # going to find the position of Y in X
            position = 0
            for item in temp:
                if Y == int(item[1:]):
                    if x[position] == y:
                        #self.constraints =  True
                        return True
                position += 1

        if isinstance(x,int):
            temp = y[-1]
            # going to find the position of Y in X
            position = 0
            for item in temp:
                if X == int(item[1:]):
                    if y[position] == x:
                        self.constraints = True
                        #return
                        return True
                position += 1

        self.constraints = False
        #return
        return False


















#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
print("==========================================================")
print("*** This is the solution of question 2 of Project ***")
print("==========================================================\n")

#easy puzzle 4x5
puzzle1 = [ ["x1","x2",3], ["x3","x4","x5","x6",10], ["x7","x8",3], ["x3","x7",4],
            ["x4","x8",3], ["x1","x5",6], ["x2","x6",3] ]
numberOfBlankSquares1 = 8

aPuzzle = Puzzle(numberOfBlankSquares1,puzzle1)
aProblem = Kakuro(aPuzzle.getVariables(), aPuzzle.getDomains(), aPuzzle.getNeighbors(), aPuzzle.getConstraints(), aPuzzle.getNumberOfBlankSquares())

# Calling and printing MAC + MRV + LCV METHOD
aProblem.MAC_MRV_LCV()
aProblem.printBlankSquareValues()

# Calling and printing FC + MRV + LCV METHOD
aProblem.FC_MRV_LCV()
aProblem.printBlankSquareValues()


print("==========================================================")
print("*** This is the solution of question 3 of Project ***")
print("==========================================================\n")

#easy puzzle 4x5
puzzle1 = [ ["x1","x2",3], ["x3","x4","x5","x6",10], ["x7","x8",3], ["x3","x7",4],
            ["x4","x8",3], ["x1","x5",6], ["x2","x6",3] ]
numberOfBlankSquares1 = 8

# expert 4x4 puzzle
puzzle2 = [ ["x1","x2",16],["x3","x4","x5","x6",10],
            ["x7","x8","x9","x10",21], ["x11","x12",9],
            ["x1","x3","x7",13],["x2","x4","x8",10],
            ["x5","x9","x11",21], ["x6","x10","x12",12]
]
numberOfBlankSquares2 = 12


# easy 9x11 puzzle
puzzle3 = [ ["x1","x2",14], ["x3","x4",11], ["x5","x6",4],
            ["x7","x8","x9","x10","x11",30], ["x12","x13","x14",12],
            ["x15","x16",4], ["x17","x18","x19",23], ["x20","x21",9],
            ["x22","x23",10], ["x24","x25",11], ["x26","x27","x28","x29","x30",25],
            ["x31","x32","x33",22], ["x34","x35",4], ["x36","x37",12],
            ["x38","x39","x40",24], ["x41","x42","x43","x44","x45",16],
            ["x46","x47",17], ["x48","x49",3], ["x50","x51",4],
            ["x52","x53","x54",6], ["x55","x56",4], ["x57","x58","x59",6],
            ["x60","x61","x62","x63","x64",26], ["x65","x66",11], ["x67", "x68",11],
            ["x69","x70",14], ["x1","x7",14], ["x20","x26",13], ["x38","x46",17],
            ["x57","x65",5], ["x2","x8","x15","x21","x27",16],
            ["x39","x47","x52","x58","x66",28], ["x9","x16",8], ["x28","x34","x40",12],
            ["x53","x59",3], ["x3","x10",16], ["x29","x35",8], ["x48","x54",3],
            ["x4","x11",12], ["x22","x30",16], ["x41","x49",3], ["x60","x67",12],
            ["x17","x23",9], ["x36","x42",12], ["x61","x68",16], ["x12","x18",10],
            ["x31","x37","x43",17], ["x55","x62",3],
            ["x5","x13","x19","x24","x32",17], ["x44","x50","x56","x63","x69",15],
            ["x6","x14",12], ["x25","x33",17], ["x45","x51",7], ["x64","x70",12]
        ]
numberOfBlankSquares3 = 70

# intermidiate 9x11 puzzle
puzzle4 = [ ["x1","x2",9], ["x3","x4",9], ["x5","x6",16], ["x7","x8","x9",14],
            ["x10","x11","x12","x13","x14",24], ["x15","x16","x17","x18",10], ["x19","x20",8],
            ["x21","x22",12], ["x23","x24",5], ["x25","x26","x27",15], ["x28","x29",8],
            ["x30","x31","x32","x33","x34",31], ["x35","x36","x37","x38","x39",30],
            ["x40","x41","x42","x43","x44",30], ["x45","x46", 15], ["x47","x48","x49",20],
            ["x50","x51",14], ["x52","x53",13], ["x54","x55",16], ["x56","x57","x58","x59",12],
            ["x60","x61","x62","x63","x64",32], ["x65","x66","x67",24], ["x68","x69",13],
            ["x70","x71",14], ["x72","x73",16], ["x7","x15","x21","x28",11], ["x40","x47",14],
            ["x60","x68",17], ["x1","x8","x16","x22","x29",19],
            ["x41","x48","x54","x61","x69",17], ["x2","x9","x17",21],
            ["x35","x42","x49","x55","x62",35], ["x18","x23",3], ["x36","x43",9],
            ["x63","x70",17], ["x3","x10",7], ["x24","x30","x37","x44","x50",34],
            ["x64","x71",13], ["x4","x11",14], ["x31","x38",8], ["x51","x56",14],
            ["x12","x19","x25","x32","x39",32], ["x57","x65","x72",20],
            ["x5","x13","x20","x26","x33",34], ["x45","x52","x58","x66","x73",28],
            ["x6","x14",10], ["x27","x34",7], ["x46","x53","x59","x67",26]
        ]
numberOfBlankSquares4 = 73

# hard 9x11 puzzle
puzzle5 = [ ["x1","x2",6], ["x3","x4",14], ["x5","x6",10], ["x7","x8",8],
            ["x9","x10","x11","x12","x13",34], ["x14","x15","x16","x17",13],
            ["x18","x19",8], ["x20","x21","x22","x23",20], ["x24","x25","x26","x27",13],
            ["x28","x29",12], ["x30","x31","x32","x33","x34",29],
            ["x35","x36","x37","x38","x39",15], ["x40","x41","x42","x43","x44",28],
            ["x45","x46",12], ["x47","x48","x49","x50",10], ["x51","x52","x53","x54",21],
            ["x55","x56",5], ["x57","x58","x59","x60",14],  ["x61","x62","x63","x64","x65",19],
            ["x66","x67",11], ["x68","x69",5], ["x70","x71",9], ["x72","x73",9],
            ["x1","x7",7], ["x20","x28",8], ["x40","x47",9], ["x61","x68",3],
            ["x2","x8","x14","x21","x29",15], ["x41","x48","x55","x62","x69",15],
            ["x15","x22",12], ["x35","x42","x49","x56","x63",17], ["x16","x23",10],
            ["x36","x43","x50",10], ["x64","x70",3], ["x3","x9","x17",20],
            ["x30","x37","x44",21], ["x57","x65","x71",19], ["x4","x10",16],
            ["x24","x31","x38",19], ["x51","x58",11], ["x11","x18","x25","x32","x39",15],
            ["x52","x59",17], ["x5","x12","x19","x26","x33",16],
            ["x45","x53","x60","x66","x72",28], ["x6","x13",15], ["x27","x34",10],
            ["x46","x54",6], ["x67","x73",3]
        ]
numberOfBlankSquares5 = 73


listOfPuzzles = [puzzle1, puzzle2, puzzle3, puzzle4, puzzle5]
listOfNumberOfBlankSquares = [numberOfBlankSquares1, numberOfBlankSquares2, numberOfBlankSquares3, numberOfBlankSquares4, numberOfBlankSquares5]
listOfPuzzleNames = ["Easy 3x4", "Expert 4x4", "Easy 9x11", "Intermidiate 9x11", "Hard 9x11"]

# here we are going to take each one of the five puzzles
# and try to solve it 10 repetitive times
# in order to keep average values of total time need and
# total number of assignments for a solution
for i in range(5): # for each one of the five possible puzzles

    totalMacTime = 0.0
    totalFcTime = 0.0

    totalMacAssigns = 0
    totalFcAssigns = 0
    for j in range(10): # solving each puzzle 10 times in order to get statistics
        aPuzzle = Puzzle(listOfNumberOfBlankSquares[i],listOfPuzzles[i])
        aKakuro = Kakuro(aPuzzle.getVariables(), aPuzzle.getDomains(), aPuzzle.getNeighbors(), aPuzzle.getConstraints(), aPuzzle.getNumberOfBlankSquares())

        # Calling  MAC + MRV + LCV METHOD
        aKakuro.MAC_MRV_LCV()
        totalMacTime += aKakuro.getElapsedTime() # getting the elapsed time
        totalMacAssigns  += aKakuro.getNassigns() # getting the number of assignments

        # Calling  FC + MRV + LCV METHOD
        aKakuro.FC_MRV_LCV()
        totalFcTime += aKakuro.getElapsedTime() # getting the elapsed time
        totalFcAssigns += aKakuro.getNassigns() # getting the number of assignments


        del aKakuro
        del aPuzzle

    # calculating average elapsed times after 10 recursions
    totalMacTime = totalMacTime / float(10)
    totalFcTime = totalFcTime / float(10)
    # calculating average number of assignments after 10 recursions
    totalMacAssigns = totalMacAssigns // 10
    totalFcAssigns = totalFcAssigns // 10

    print(listOfPuzzleNames[i] ,"- TotalMac->", totalMacTime, "miliseconds and ",totalMacAssigns, "assignments.")
    print(listOfPuzzleNames[i], "- TotalFC->", totalFcTime, "miliseconds and ", totalFcAssigns, "assignments.\n")



























