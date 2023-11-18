magic =  {1: 1, 2: 1}
def hes(n):
    if n in magic:
        return magic[n]
    else:
        magic[n] = hes(n-1) + hes(n-2)
        return magic[n]
    
hes(10)