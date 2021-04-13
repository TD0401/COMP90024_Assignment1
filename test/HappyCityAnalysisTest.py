from HappyCityAnalysis import  find_cell_id

def test_find_grid_cell2():
    map = {}
    map['C1'] = {'id': 'C1', 'xmin': -3.0, 'xmax': -1.5, 'ymin': 0, 'ymax': 1.5, 'score': 0}
    map['C7'] = {'id': 'C7', 'xmin': 0.0, 'xmax': 1.5, 'ymin': -1.5, 'ymax': 0, 'score': 0}
    map['C4'] = {'id': 'C4', 'xmin': 1.5, 'xmax': 3.0, 'ymin': 0, 'ymax': 1.5, 'score': 0}
    map['C10'] = {'id': 'C10', 'xmin': -1.5, 'xmax': 0.0, 'ymin': -3.0, 'ymax': -1.5, 'score': 0}
    map['C5'] = {'id': 'C5', 'xmin': -3.0, 'xmax': -1.5, 'ymin': -1.5, 'ymax': 0, 'score': 0}
    map['C8'] = {'id': 'C8', 'xmin': 1.5, 'xmax': 3.0, 'ymin': -1.5, 'ymax': 0, 'score': 0}
    map['C3'] = {'id': 'C3', 'xmin': 0.0, 'xmax': 1.5, 'ymin': 0, 'ymax': 1.5, 'score': 0}
    map['C2'] = {'id': 'C2', 'xmin': -1.5, 'xmax': 0, 'ymin': 0, 'ymax': 1.5, 'score': 0}
    map['C9'] = {'id': 'C9', 'xmin': -3.0, 'xmax': -1.5, 'ymin': -3.0, 'ymax': -1.5, 'score': 0}
    map['C11'] = {'id': 'C11', 'xmin': 0, 'xmax': 1.5, 'ymin': -3.0, 'ymax': -1.5, 'score': 0}
    map['C6'] = {'id': 'C6', 'xmin': -1.5, 'xmax': 0.0, 'ymin': -1.5, 'ymax': 0, 'score': 0}
    map['C12'] = {'id': 'C12', 'xmin': 1.5, 'xmax': 3.0, 'ymin': -3.0, 'ymax': -1.5, 'score': 0}
    map['C13'] = {'id': 'C13', 'xmin': -1.5, 'xmax': 0, 'ymin':  1.5, 'ymax': 3, 'score': 0}
    map['C14'] = {'id': 'C14', 'xmin': 0, 'xmax': 1.5, 'ymin': -4.5, 'ymax': -3.0, 'score': 0}
    map['C15'] = {'id': 'C15', 'xmin': -1.5, 'xmax': 0, 'ymin': -4.5, 'ymax': -3.0, 'score': 0}

    '''points on outer boundary of grids which means
        a. either left is null between left and right 
        b. either right is null between right and left
        c. either top is null between top and bottom
        d. either bottom is null between top and bottom 
        all passed
    '''
    A = [ -3 , 1.2]
    B = [-2.7 , 1.5]
    F = [ -3 , -2.8]
    G = [ -1.8, -3.0]
    H = [2.1, -3.0]
    I = [3, -2.1]
    J = [ 3, 1.1]
    K = [2.0, 1.5]

    #points inside the grid sharing boundaries - correct
    C = [-2.2, 0]
    D = [0, 1.1]
    E = [-0.8, 0]
    Y = [-1.1, 1.5]

    #point at intersection of 4 cells inside grid - correct
    L = [1.5,0]

    #points at boundary corners of grids - correct
    M = [-3, -3]
    N = [3, -3]
    O = [3, 1.5]
    P = [-3, 1.5]
    W = [-1.5,-4.5]
    Z = [0, 3]

    '''points at boundary cells intersection which means
    a. top bottom exists at but either of lefts or rights are empty
    b. left right exists but either of tops or bottoms are empty
    '''
    Q = [-3, 0]
    R = [0, -3]
    S = [3, -1.5]
    T = [1.5, 1.5]
    X = [0, -4.5]

    #points inside cells -- fine
    U = [1.2, -1.2]
    V = [-0.8, -2.2]

    assert find_cell_id(A[1],A[0] , map) == 'C1'
    assert find_cell_id(B[1], B[0], map) == 'C1'
    assert find_cell_id(C[1], C[0], map) == 'C5'
    assert find_cell_id(D[1], D[0], map) == 'C2'
    assert find_cell_id(E[1], E[0], map) == 'C6'
    assert find_cell_id(F[1], F[0], map) == 'C9'
    assert find_cell_id(G[1], G[0], map) == 'C9'
    assert find_cell_id(H[1], H[0], map) == 'C12'
    assert find_cell_id(I[1], I[0], map) == 'C12'
    assert find_cell_id(J[1], J[0], map) == 'C4'
    assert find_cell_id(K[1], K[0], map) == 'C4'
    assert find_cell_id(L[1], L[0], map) == 'C3'
    assert find_cell_id(M[1], M[0], map) == 'C9'
    assert find_cell_id(N[1], N[0], map) == 'C12'
    assert find_cell_id(O[1], O[0], map) == 'C4'
    assert find_cell_id(P[1], P[0], map) == 'C1'
    assert find_cell_id(Q[1], Q[0], map) == 'C5'
    assert find_cell_id(R[1], R[0], map) == 'C10'
    assert find_cell_id(S[1], S[0], map) == 'C8'
    assert find_cell_id(T[1], T[0], map) == 'C3'
    assert find_cell_id(U[1], U[0], map) == 'C7'
    assert find_cell_id(V[1], V[0], map) == 'C10'
    assert find_cell_id(W[1], W[0], map) == 'C15'
    assert find_cell_id(X[1], X[0], map) == 'C15'
    assert find_cell_id(Y[1], Y[0], map) == 'C13'
    assert find_cell_id(Z[1], Z[0], map) == 'C13'

    #outside grid
    assert find_cell_id(-7,8, map) == ''



