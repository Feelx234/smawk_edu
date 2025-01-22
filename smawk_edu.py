import numpy as np
import functools

A = None

def arr_lookup(M, i, j):
    return M[i,j]

def smawk_arr_edu(M):
    global A
    A = M.copy()
    lookup = functools.partial(arr_lookup, M)
    m, n = M.shape
    results = np.zeros(m, dtype=int)
    rows = np.arange(m)
    cols = np.arange(n)
    _smawk_edu(rows, cols, lookup, results)
    return results



def _smawk_edu(rows, cols, lookup, result):
    if len(rows)==0:
        return

    _cols = reduce_edu(rows, cols, lookup)
    result[rows[0]]=_cols[0]


    odd_rows = rows[1::2]
    print(odd_rows, cols)

    _smawk_edu(odd_rows, _cols, lookup, result)
    if len(rows)>2:
        print(result)
        interpolate_edu(rows, _cols, lookup, result)


def reduce_edu(rows, cols, lookup):
    # https://courses.engr.illinois.edu/cs473/sp2016/notes/06-sparsedynprog.pdf
    print("begin_reduce")
    print(rows, cols)
    with np.printoptions(linewidth=200):
        print(A[np.ix_(rows, cols)])
    m = len(rows)
    n = len(cols)
    S = np.empty(m,dtype=int)
    S[0]=0
    r = 0
    for k in cols:
        while r >= 0:
            print(f"comparing row {rows[r]} col {S[r]} with col {k} ({lookup(rows[r], S[r])} vs {lookup(rows[r], k)})",)
            if lookup(rows[r], S[r]) > lookup(rows[r], k):
                A[rows[r]:,S[r]]=0
                r-=1
            else:
                A[:rows[r]+1, k]=0
                break
        with np.printoptions(linewidth=200):
            print(A[np.ix_(rows, cols)])
        if r < m-1:
            r+=1
            S[r]=k
    print("end_reduce")
    print(A)
    print("reduce_result", S[:r+1])
    return S[:r+1]



def interpolate_edu(rows, cols, lookup, result):
    print("begin interpolate")
    curr=0
    for i in range(2, len(rows), 2):
        start_col = result[rows[i-1]]
        if i+1 < len(rows):
            stop_col = result[rows[i+1]]
        else:
            stop_col = cols[len(cols)-1]
        while cols[curr] < start_col:
            curr+=1
        print(rows[i],start_col,stop_col)
        best = curr
        best_val = lookup(rows[i], cols[best])
        while cols[curr] < stop_col:
            tmp = lookup(rows[i], cols[curr+1])
            print(f"comparing row {rows[i]} col {cols[curr]} with col {cols[curr+1]} ({best_val} vs {tmp})",)
            if best_val > tmp:
                A[rows[i]:,cols[best]]=0
                best = curr+1
                best_val = tmp
            else:
                A[rows[i],cols[curr+1]]=0

            curr+=1
        result[rows[i]]=cols[best]
    print("end_interpolate")
    print(A)