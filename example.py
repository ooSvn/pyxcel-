import re
### <<<<<<<<<<<<<<<<<<<<<<<<<<<<< global variants >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
variants = {}
currentTableFlag = None
tables = dict()
tablesList = list()
setFuncs = list()
### >>>>>>>>>>>>>>>>>>>>>>>>>>>>> global variants <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< functions >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def hashh(string: str) -> int:
    wholeHash = 0
    for i in string:
        wholeHash *= 26
        wholeHash += ord(i) - ord("A") + 1
    return wholeHash - 1
def dHash(num: int):
    theDic = dict()
    for i in range(26):
        theDic[f"{i}"] = chr(i + 65)
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
def eval3(string:str):
    def typeFinder(x):
        splitPattern = re.compile(r"[+\-*/]")
        splittedX = re.split(splitPattern, x)
        for i in range(2):
            splittedX[i] = splittedX[i].strip()
        numPattern = re.compile(r"[0-9]+")
        textNum_textPatt = re.compile(r" *\".+\" *")
        items_types = []  # types - ["text_num","text","num"]
        for i in splittedX:
            flag = True
            if re.findall(textNum_textPatt, i):
                for char in i[1:-1]:
                    if not "A" <= char <= "Z":
                        flag = False
                if flag == True:
                    items_types.append("text_num")
                else:
                    items_types.append("text")
            elif re.findall(numPattern, i):
                items_types.append("num")
            else:
                items_types.append("unsupported")
        return (items_types, splittedX)
    def cal_div_mul(s: str):
        items_types, splittedS = typeFinder(s)
        if "unsupported" not in items_types:
            if "*" in s:
                if "text_num" in items_types or "text" in items_types:
                    return "unsupported"
                i = s.find("*")
                return (str(int(splittedS[0]) * int(splittedS[1])), (s[:i] + "\\*" + s[i + 1:]))

            elif "/" in s:
                if "text_num" in items_types or "text" in items_types:
                    return "unsupported"
                return (str(int(splittedS[0]) // int(splittedS[1])), s)
        else:
            return "unsupported"
    def cal_sum_minus(s: str):
        items_types, splittedS = typeFinder(s)
        if "unsupported" not in items_types:
            if "+" in s:
                i = s.find("+")
                sPrime = s[:i] + "\\" + s[i:]
                if (items_types[0] == "text" or items_types[0] == "text_num") and (
                        items_types[1] == "text" or items_types[1] == "text_num"):
                    return splittedS[0][:-1] + splittedS[1][1:], sPrime

                elif items_types[0] == "text_num" and items_types[1] == "num":
                    return f'"{dHash(hashh(splittedS[0][1:-1]) + int(splittedS[1]))}"', sPrime

                elif items_types[0] == "num" and items_types[1] == "text":
                    return "unsupported"

                elif items_types[0] == "num" and items_types[1] == "text_num":
                    return str(int(splittedS[0]) + hashh(splittedS[1][1:-1])), sPrime

                elif items_types[0] == "num" and items_types[1] == "num":
                    try:
                        return str(int(splittedS[0]) + int(splittedS[1])), sPrime
                    except:
                        return "unsupported"
                else:
                    return "unsupported"
            elif "-" in s:
                sPrime = s
                if "text" in items_types:
                    return "unsupported"
                elif items_types[0] == "text_num" and items_types[1] == "text_num":
                    return "unsupported"
                elif items_types[0] == "text_num" and items_types[1] == "num":
                    return f'"{dHash(hashh(splittedS[0][1:-1]) - int(splittedS[1]))}"', sPrime
                elif items_types[0] == "num" and items_types[1] == "num":
                    return str(int(splittedS[0]) - int(splittedS[1])), sPrime
                elif items_types[0] == "num" and items_types[1] == "text_num":
                    return str(int(splittedS[0]) - hashh(splittedS[1])), sPrime
                else:
                    return "unsupported"
        else:
            return "unsupported"
    def analyzer(string: str):
        s = string
        p = re.compile(r" *\"?[A-Za-z0-9]+\"? *[/*] *\"?[A-Za-z0-9]+\"? *")
        blankStringPatt2 = re.compile(r"^ *\"\" *\+ *")
        blankStringPatt23 = re.compile(r"[+\-] *\"\" *")
        s = re.sub(blankStringPatt2, "", s)
        s = re.sub(blankStringPatt23, "", s)
        # numPattern = re.compile(r"[0-9]+")
        # textNum_textPatt = re.compile(r" *\".+\" *")
        match = re.findall(p, s)
        # flagg = True
        # if len(match) == 0:
        #     if re.findall(numPattern, s):
        #         flagg = False
        #     elif re.findall(textNum_textPatt, s):
        #         flagg = False

        flag = 0
        while match:
            if cal_div_mul(match[0]) != "unsupported":
                sub, selff = cal_div_mul(match[0])
                s = re.sub(selff, sub, s)
                match = re.findall(p, s)
            else:
                # unsupported operand
                flag = 1
                break
        flag2 = 0
        if flag == 0:
            p2 = re.compile(r" *\"?[A-Za-z0-9,.% \^&*!;:><#@`~{}]+\"? *[\-+] *\"?[A-Za-z;0-9,.% \^&*!:><#@`~{}]+\"? *")
            match2 = re.findall(p2, s)
            if match2:
                while match2:
                    if cal_sum_minus(match2[0]) != "unsupported":
                        sub, selff = cal_sum_minus(match2[0])
                        s = re.sub(selff, sub, s)
                        match2 = re.findall(p2, s)
                    else:
                        return "unsupported operand"
                if flag == 0 and flag2 == 0:
                    return s
            else:
                return s
        else:
            return "unsupported operand"
    def analyzer3(string: str):
        try:
            flag = True
            chartData = dict()
            varients = variants
            s = string
            itemsList = []
            signs = []
            bracketFlag = 0
            st = ""
            signsList = ["+", "-", "/", "*"]
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
            if currentTableFlag != None:
                lis = list(enumerate(tables[currentTableFlag].table[1:],1))
                for i in range(len(lis)):
                    for j in range(len(lis[i][1])):
                        chartData[f'{dHash(j)}{lis[i][0]}'] = str(lis[i][1][j])
                for i in range(len(itemsList)):
                    itemsList[i] = itemsList[i].strip()
                for index in range(len(itemsList)):
                    if itemsList[index] in varients.keys():
                        itemsList[index] = varients[itemsList[index]]
                    elif itemsList[index] in chartData.keys():
                        itemsList[index] = chartData[itemsList[index]]
                for index in range(len(itemsList)):
                    if "[" in itemsList[index]:
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
                        if sub == None:
                            flag = False
                            break
                        itemsList[index] = sub
                if flag == False:
                    return "Error"
                newS = ""
                for i in range(len(itemsList) - 1):
                    newS += itemsList[i]
                    newS += signs[i]
                newS += itemsList[-1]
                x = analyzer(newS)
                return x if x != "unsupported operand" else "Error" 
            else:
                for i in range(len(itemsList)):
                    itemsList[i] = itemsList[i].strip()
                for index in range(len(itemsList)):
                    if itemsList[index] in varients.keys():
                        itemsList[index] = varients[itemsList[index]]
                for index in range(len(itemsList)):
                    if "[" in itemsList[index]:
                        innersPatt = re.compile(r"\[([^\]]+)\] *\[([^\[\]]+)\]")
                        innersList = innersPatt.findall(itemsList[index])
                        itemCol = innersList[0][0]
                        itemRow = innersList[0][1]
                        if itemCol in varients.keys():
                            itemCol = varients[itemCol]
                        if itemRow in varients.keys():
                            itemRow = varients[itemRow]
                        itemCol = analyzer(itemCol)
                        itemRow = analyzer(itemRow)
                        sub = chartData[f"{itemCol[1:-1]}{itemRow}"]
                        if sub == "None":
                            flag = False
                            break
                        itemsList[index] = sub
                    if flag == False:
                        return "Error"
                newS = ""
                for i in range(len(itemsList) - 1):
                    newS += itemsList[i]
                    newS += signs[i]
                newS += itemsList[-1]
                x = analyzer(newS)
                return x if x != "unsupported operand" else "Error" 
        except:
            return("Error")
    return analyzer3(string)

### to find out is the input a chartItem or a variant
def tttypeFinder(i : str):
    i = i.strip()
    if "a" <= i[0] <= "z":
        return "var"
    elif "A" <= i[0] <= "Z":
        index = 0
        while "A" <= i[index] <= "Z":
            index += 1
        return  (i[:index], i[index:])
    else:
        x = list(re.findall(r'\[\"(.+)\"\]\[(.+)\]',i)[0])
        for index in range(len(x)):
            if x[index] in variants.keys():
                x[index] = variants[x[index]]
        col = x[0]
        row = x[1]
        return (col, eval3(row))

### to display the table the client wants
def display(inp : str): ###<inp> : display(<tableName>)
    inp = inp.strip()
    if inp in tables.keys():
        tables[inp].display()
    else:
        print("Error")
        exit()

### setting the currentTableFlag the table which the client wants
def currentTableFunc(inp : str): ### <inp> : context(<tableName>)
    global currentTableFlag
    inp = inp.strip()
    if inp in tables.keys():
        currentTableFlag = inp
    else:
        print("Error")
        exit()

### making an instance of <class table>
def create(inp : str): ### <inp> : create(<name,colCount,rowCount>)
    name, colCount, rowCount = re.split(r",",inp)
    name, colCount, rowCount = name.strip(), colCount.strip(), rowCount.strip()
    tables[name] = Table(int(colCount),int(rowCount))

### to print the value which the client wants
def printer(inp : str): ### <inp> : print(<inp>)
    inp = inp.strip()
    res = eval3(inp)
    print("out:",res,sep="")

### to detect that we are making a variant or setting value of a table
def assignment(i : str, val : str): ### <inp> : (variant = x) or (chartItem = x)
    i = i.strip()
    res = tttypeFinder(i)
    value = eval3(val)
    if res == "var":
        variants[i] = value
    else:
        if currentTableFlag != None:
            col = res[0]
            row = res[1]
            tables[currentTableFlag].setValue(int(hashh(col)), int(row), value)
            if tables[currentTableFlag].setFuncs:
                for item in tables[currentTableFlag].setFuncs:
                    if item[0] == col+row:
                        tables[currentTableFlag].setFuncs.remove(item)
        else:
            print("Error")
            exit()
def setFunc(toBeSet, exp): # <inp> : setFunc(<toBeSet,exp>) to add new setFuncs to the table object
    col, row = tttypeFinder(toBeSet)
    if currentTableFlag != None:
        tables[currentTableFlag].add_setFuncs(col+row,exp)
        tables[currentTableFlag].setValue(int(hashh(col)),int(row),exp)
    else:
        print("Error")
        exit()
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> functions <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
class Table:
    def __init__(self, colCount:int, rowCount:int): # to set a "self.table" for the items which is saved in this table
        self.table = []
        row1 = []
        for i in range(colCount):
            row1.append(chr(65+i))
        self.table.append(row1)
        for i in range(rowCount):
            self.table.append([None for _ in range(colCount)])
        self.setFuncs = list()
    def display(self):
        mat = list()
        for i in range(len(self.table)):
            r = []
            for j in range(len(self.table[i])):
                r.append(self.getValue(j,i))
            mat.append(r.copy())
        lens = [max(map(len, col)) for col in zip(*mat)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in mat]
        for i in  range(len(table)):
            print(f"{i}   \t" + table[i])
    def context(self):
        global currentTableFlag
        currentTableFlag = tables[self]
    def getValue(self, col_hashed, row):
        x = str(eval3(str(self.table[row][col_hashed])))
        return x if x != "Error" else "None" 
    def setValue(self, col_hashed, row, value):
        try:
            self.table[row][col_hashed] = value
        except:
            print("Error")
            exit()

    def add_setFuncs(self, toBeSet, exp): # just add the <col-row> of the item which is set with setFunc & will be set with setValue method
        self.setFuncs.append((toBeSet, exp))
    def handle_setFuncs(self): # should be called in every operation a loop does
        if self.setFuncs:
            for item in self.setFuncs:
                col, row = tttypeFinder(item[0])
                x = eval3(item[1])
                if x != "Error":
                    self.setValue(int(hashh(col)) , int(row), eval3(item[1]))
### <<<<<<<<<<<<<<<<<<<<<<<< patterns >>>>>>>>>>>>>>>>>>>>>>>>>
printPatt = re.compile(r'print\((.+)\)')
createPatt = re.compile(r'create\((.+)\)')
contextPatt = re.compile(r'context\((.+)\)')
assignmentPatt = re.compile(r'([^=]+)=([^=]+)')
displayPatt = re.compile(r'display\((.+)\)')
setFuncPatt = re.compile(r'setFunc\( *([^,]+) *, *([^,]+) *\)')
### >>>>>>>>>>>>>>>>>>>>>>>> patterns <<<<<<<<<<<<<<<<<<<<<<<<<<<

### <<<<<<<<<<<<<<<<<<<<<<<<< operation >>>>>>>>>>>>>>>>>>>>>>>>>>>
n = int(input())
runCount = 0
while runCount != n:
    inp = input().strip()
    if printPatt.findall(inp):
        printer(printPatt.findall(inp)[0])
    elif createPatt.findall(inp):
        create(createPatt.findall(inp)[0])
    elif contextPatt.findall(inp):
        currentTableFunc(contextPatt.findall(inp)[0])
    elif assignmentPatt.findall(inp):
        i , v = assignmentPatt.findall(inp)[0]
        assignment(i, v)
    elif displayPatt.findall(inp):
        display(displayPatt.findall(inp)[0])
    elif setFuncPatt.findall(inp):
        setFunc(setFuncPatt.findall(inp)[0][0],setFuncPatt.findall(inp)[0][1])
    else:
        print("Error")
        exit()
    if currentTableFlag != None:
        tables[currentTableFlag].handle_setFuncs()
    runCount += 1
### >>>>>>>>>>>>>>>>>>>>>>>>>>>> opertion <<<<<<<<<<<<<<<<<<<<<<<<<<<<<