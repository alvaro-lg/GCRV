if __name__ == '__main__':

    n = 4
    m = 2

    total = n

    for x in range(1, m):
        for y in range(1, n):
            for z in range(1, total):
                total = total + 1
                
    print(total)