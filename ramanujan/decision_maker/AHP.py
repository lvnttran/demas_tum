def normalize_table(series, n):
    '''Receive U-table in form of series and convert it into AHP farmiliar form'''
    res = [[0] * n for i in range(0, n)]
    p = 0
    for i in range(n):
        for j in range(n):
            if i == j:
                res[i][j] = 1
            elif i < j:
                if series[p] < 0:
                    res[i][j] = 1 / (-series[p])
                else:
                    res[i][j] = series[p]
                p += 1
            else:
                # i > j
                res[i][j] = 1 / res[j][i]
    return res


def ahp(table):
    '''Convert pair-comparision table to ahp vector'''
    n = len(table)
    res = [0] * n
    for i in range(n):
        for row in range(n):
            res[i] += table[row][i]

    for i in range(n):
        for j in range(n):
            table[i][j] = table[i][j] / res[j]

    for row in range(n):
        res[row] = sum(table[row]) / n

    return res
