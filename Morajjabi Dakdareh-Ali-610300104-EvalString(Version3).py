import re

def hashh(string : str) -> int:
    wholeHash = 0

    for i in string:
        wholeHash *= 26
        wholeHash += ord(i) - ord("A")+1

    return wholeHash-1

def dHash(num:int):
    theDic = dict()
    for i in range(26):
        theDic[f"{i}"] = chr(i+65)
    n = num
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
    return st if n > 0 else "A"


# =================================== inputs ===================================== 
n = int(input().strip())
lis = [[i] for i in range(1,(n+1))]

for i in range(n):
    lis[i].append(list(input().strip().split(" ")))

chartData = dict()
for i in range(n):
    for j in range(len(lis[i][1])):
        chartData[f'{dHash(j)}{lis[i][0]}'] = lis[i][1][j] 

varients = dict()
var = list(input().strip().split(" "))
values = list(input().strip().split(" "))
for i in range(len(var)):
    varients[var[i]] = values[i]
# =========================== functions =============================
def typeFinder(x):
    splitPattern = re.compile(r"[+\-*/]")
    splittedX = re.split(splitPattern,x)
    for i in range(2):
        splittedX[i] = splittedX[i].strip()
    numPattern = re.compile(r"[0-9]+")
    textNum_textPatt = re.compile(r" *\".+\" *")
    items_types = []                                    # types - ["text_num","text","num"]
    for i in splittedX:
        flag = True
        if re.findall(textNum_textPatt,i):
            for char in i[1:-1]:
                if not "A" <= char <= "Z":
                    flag = False
            if flag == True:
                items_types.append("text_num")
            else:
                items_types.append("text")
        elif re.findall(numPattern,i):
            items_types.append("num")
        else:
            items_types.append("unsupported")
    return (items_types,splittedX)

def cal_div_mul(s:str):
    items_types,splittedS = typeFinder(s)
    if "unsupported" not in items_types:
        if "*" in s:
            if "text_num" in items_types or "text" in items_types:
                return "unsupported"
            i = s.find("*")
            return (str(int(splittedS[0])*int(splittedS[1])) , (s[:i] + "\\*" + s[i+1:]))

        elif "/" in s:
            if "text_num" in items_types or "text" in items_types:
                return "unsupported"
            return (str(int(splittedS[0])//int(splittedS[1])) , s)
    else:
        return "unsupported"

def cal_sum_minus(s:str):
    items_types,splittedS = typeFinder(s)
    if "unsupported" not in items_types:
        if "+" in s:
            i = s.find("+")
            sPrime = s[:i] + "\\" + s[i:]
            if (items_types[0] == "text" or items_types[0] == "text_num") and (items_types[1] == "text" or items_types[1] == "text_num"):
                return splittedS[0][:-1]+splittedS[1][1:] , sPrime

            elif items_types[0] == "text_num" and items_types[1] == "num":
                return f'"{dHash(hashh(splittedS[0][1:-1])+int(splittedS[1]))}"' , sPrime 
            
            elif items_types[0] == "num" and items_types[1] == "text":
                return "unsupported"

            elif items_types[0] == "num" and items_types[1] == "text_num":
                return str(int(splittedS[0])+hashh(splittedS[1])) , sPrime

            elif items_types[0] == "num" and items_types[1] == "num":
                try: return str(int(splittedS[0])+int(splittedS[1])) , sPrime
                except: return "unsupported"
            else:
                return "unsupported"

        elif "-" in s:
            sPrime = s
            if "text" in items_types:
                return "unsupported"
            elif items_types[0] == "text_num" and items_types[1] == "text_num":
                return "unsupported"
            elif items_types[0] == "text_num" and items_types[1] == "num":
                return f'"{dHash(hashh(splittedS[0][1:-1])-int(splittedS[1]))}"' , sPrime
            elif items_types[0] == "num" and items_types[1] == "num":
                return str(int(splittedS[0])-int(splittedS[1])) , sPrime
            elif items_types[0] == "num" and items_types[1] == "text_num":
                return str(int(splittedS[0])-hashh(splittedS[1])) , sPrime
            else:
                return "unsupported"
    else:
        return "unsupported"

def analyzer(string:str):
    s = string
    p = re.compile(r" *\"?[A-Za-z0-9]+\"? *[/*] *\"?[A-Za-z0-9]+\"? *")
    blankStringPatt2 = re.compile(r"^ *\"\" *\+ *")
    blankStringPatt23 = re.compile(r"[+\-] *\"\" *")
    s = re.sub(blankStringPatt2,"",s)
    s = re.sub(blankStringPatt23,"",s)
    numPattern = re.compile(r"[0-9]+")
    textNum_textPatt = re.compile(r" *\".+\" *")
    match = re.findall(p,s)
    flagg = True
    if len(match) == 0:
        if re.findall(numPattern,s):
            flagg = False
        elif re.findall(textNum_textPatt,s):
            flagg = False
    
    flag = 0
    while match:
        if cal_div_mul(match[0]) != "unsupported":
            sub,selff = cal_div_mul(match[0])
            s = re.sub(selff,sub,s)
            match = re.findall(p,s)
        else:
            # unsupported operand
            flag = 1
            break
    flag2 = 0
    if flag == 0:
        p2 = re.compile(r" *\"?[A-Za-z0-9,.% \^&*!;:><#@`~{}]+\"? *[\-+] *\"?[A-Za-z;0-9,.% \^&*!:><#@`~{}]+\"? *")
        match2 = re.findall(p2,s)
        if match2:
            while match2:
                if cal_sum_minus(match2[0]) != "unsupported":
                    sub,selff = cal_sum_minus(match2[0])
                    s = re.sub(selff,sub,s)
                    match2 = re.findall(p2,s)
                else:
                    return "unsupported operand"
            if flag == 0 and flag2 == 0:
                return s
        else:
            return s
    else:
        return "unsupported operand"


def analyzer3(string:str):
    try:
        s = string
        itemsList = []
        signs = []
        bracketFlag = 0
        st = ""
        signsList = ["+","-","/","*"]
        for item in s:
            if item == "[":
                bracketFlag += 1
                st += "["
                continue
            elif item == "]":
                bracketFlag -= 1
                st += "]"
                continue
            else:
                if item in signsList and bracketFlag == 0:
                    itemsList.append(st)
                    signs.append(item)
                    st = ""
                else:
                    st += item
        itemsList.append(st)
        for i in range(len(itemsList)):
            itemsList[i] = itemsList[i].strip()
        for index in range(len(itemsList)):
            if itemsList[index] in varients.keys():
                itemsList[index] = varients[itemsList[index]]
            elif itemsList[index] in chartData.keys():
                itemsList[index] = chartData[itemsList[index]]
        for index in range(len(itemsList)):
            if "["  in itemsList[index]:
                innersPatt = re.compile(r"\[([^\]]+)\] *\[([^\[\]]+)\]")
                innersList = innersPatt.findall(itemsList[index])
                itemCol = innersList[0][0]
                itemRow = innersList[0][1]
                if itemCol in varients.keys():
                    itemCol = varients[itemCol]
                elif itemCol in chartData.keys():
                    itemCol = chartData[itemCol]
                if itemRow in varients.keys():
                    itemRow = varients[itemRow]
                elif itemRow in chartData.keys():
                    itemRow = chartData[itemRow]
                itemCol = analyzer(itemCol)
                itemRow = analyzer(itemRow)
                sub = chartData[f"{itemCol[1:-1]}{itemRow}"]
                itemsList[index] = sub
        for i in range(len(itemsList)-1):
            newS += itemsList[i]
            newS += signs[i]
        newS += itemsList[-1]
        return analyzer(newS)
    except:
        return "unsupported operand"


i = input()
print(analyzer3(i))
