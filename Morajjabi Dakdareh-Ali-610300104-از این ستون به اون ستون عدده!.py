def hashh(string : str) -> int:
    wholeHash = 0
    
    for i in string:
        wholeHash *= 26
        wholeHash += ord(i) - ord("A")+1
    
    return wholeHash-1

def dHash2(num:int):
    theDic = dict()
    for i in range(26):
        theDic[f"{i}"] = chr(i+65)
    flag = 0
    st = ""
    while num:
        if flag == 0:            
            r = num % 26
            num //= 26
            st = theDic[f"{r}"] + st
            flag += 1
        else:
            num -= 1
            r = num % 26
            num //= 26
            st = theDic[f"{r}"] + st
    return st

inp = input()
try:
    inp = int(inp)
    print(dHash2(inp))
except:
    print(hashh(inp))