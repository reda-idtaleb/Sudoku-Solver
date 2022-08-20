from pysat.solvers import Minisat22

# For sudoku, variables represent triplets (i,j,k) with i, j and k in [0,8].
# These triples have the following meaning: the variable (i,j,k) is true iff
# in the sudoku solution, the coordinate box (i,j) contains the number k+1.

# We define l to be the digits in [0, 8]
l = list(range(0, 9))

# pos contains all possible triples (i,j,k)
pos = [(i,j,k) for i in l for j in l for k in l]


def encode(i,j,k):
    """
    The encode function takes a triple (i,j,k) of pos as an argument 
    and returns a number that indicates the variable corresponding to this triple.
    """
    return 1 + i + j* 9 + k * 81

def decode(n):
    """
    Decode takes as argument takes a number between 1 and 729 which represents 
    a variable representing a triplet (i,j,k) and returns the corresponding triplet.
    """
    m = n-1
    i = m % 9
    m= m//9
    j = m % 9
    k = m//9
    return (i,j,k)

# Instantiate the variable phi1 by the constraint SAT which indicates 
# that any box contains a value
phi1 = [[encode(i, j, k) for k in l] for i in l for j in l]

# Instantiate the variable phi2 by the constraint SAT which indicates 
# that a box contains at most one value
phi2 = [[-encode(i, j, k), -encode(i, j, m)] for i in l for j in l for k in l for m in l if k < m]

# Instantiate the variable phi3 by the constraint SAT which indicates 
# that on a line at most once each value.
phi3 = [[-encode(i, j, k), -encode(i, j2, k)] for i in l for j in l for j2 in l for k in l if j < j2]

# Instantiate the variable phi4 by the constraint SAT which indicates 
# that on a column at most once each value
phi4 = [[-encode(i, j, k), -encode(i2, j, k)] for i in l for j in l for i2 in l for k in l if i<i2]

# Instantiate the variable phi5 by the constraint SAT which indicates 
# that on a square at most once each value.

# For this we can (it is not necessary) write a square function 
# corresponding to the following specification:

def square(i1, j1, i2, j2):
    """
    Indicates whether boxes (i1,j1) and (i2,j2) belong to the same square.

    The result is indifferent (i.e. can be True or False) 
    when (i1,j1) and (i2,j2) are on the same row or the same column.
    """
    x0, x1 = i1//3, i2//3
    y0, y1 = j1//3, j2//3
    if (i1, j1) != (i2, j2):
        return (x0 == x1 and y0 == y1)
    else:
        return False
        

phi5 = [[-encode(i1, j1, k), -encode(i2, j2, k)] 
        for i1 in l 
            for j1 in l 
                for i2 in l 
                    for j2 in l 
                        for k in l 
                            if square(i1, j1, i2, j2)] 

# Instantiate the variable phi6 by the constraint SAT 
# which represents the statement grid.
phi6 =[ [encode(0, 4, 1)], [encode(0, 7, 0)], [encode(0, 8, 6)], 
        [encode(1, 1, 2)], [encode(1, 5, 6)], [encode(1, 8, 7)],
        [encode(2, 4, 8)], [encode(2, 6, 5)],
        [encode(3, 1, 7)], [encode(3, 3, 8)], [encode(3, 5, 1)], [encode(3, 7, 5)],
        [encode(4, 0, 3)], [encode(4, 2, 5)], [encode(4, 6, 2)], [encode(4, 8, 1)],
        [encode(5, 1, 1)], [encode(5, 3, 5)], [encode(5, 5, 2)], [encode(5, 7, 6)],
        [encode(6, 2, 6)], [encode(6, 4, 5)], 
        [encode(7, 0, 7)], [encode(7, 3, 6)], [encode(7, 7, 4)],   
        [encode(8, 0, 1)], [encode(8, 1, 4)], [encode(8, 4, 2)] ]

# This part of the program launches the SAT solver with the conjunction of the constraints, 
# ie the concatenation of the lists representing them.
with Minisat22(bootstrap_with=phi1+phi2+phi3+phi4+phi5+phi6) as m:
    # if we found a solution
    if m.solve():
        # We retrieve the variables that are true in the solution found.
        model = [decode(v) for v in m.get_model() if v >0]
        # We display the solution
        r = [[0 for i in l] for j in l]
        for (i,j,k) in model:
            r[i][j] += k+1
        print("\n")
        for ligne in r:
            print(ligne)

    else:
        print("No solution")
