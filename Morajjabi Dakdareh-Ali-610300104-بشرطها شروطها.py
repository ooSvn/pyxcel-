import re

def eval2(string:str):
    def hashh(string : str) -> int:
        try:
            return int(string)
        except:
            wholeHash = 0
            
            for i in string[1:-1]:
                wholeHash *= 26
                wholeHash += ord(i) - ord("A")+1
            
            return wholeHash-1

    def dHash(num:int) -> str:
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
                    return f'"{dHash(hashh(splittedS[0])+int(splittedS[1]))}"' , sPrime 
                
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
                    return f'"{dHash(hashh(splittedS[0])-int(splittedS[1]))}"' , sPrime
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
                        flag2 = 1
                        return ("unsupported operand")
                if flag == 0 and flag2 == 0:
                    return (s)
            else:
                return (s)
        else:
            return ("unsupported operand")
    
    return analyzer(string)

def typeFinder2(x:str):
    flag = False
    for item in x:
        if not "0" <= item <= "9":
            flag = True
    if flag:
        return "nondigit"
    else:
        return "digit"

def comparer(s:str):
    if s == "true":
        return "true"
    elif s == "false":
        return "false"
    else:
        sp_pattern = re.compile(r"(==|>|<)")
        x = sp_pattern.split(s)
        for i in range(len(x)):
            x[i] = x[i].strip()
        ans = []
        typesItem = []
        try:
            for i in range(0,3,2):
                ans.append(eval2(x[i]))
            for i in range(2):
                typesItem.append(typeFinder2(ans[i]))
            if "digit" in typesItem and "nondigit" in typesItem:
                return "unsupported"
            elif "digit" in typesItem:
                if "==" in s:
                    if int(ans[0]) == int(ans[1]):
                        return "true"
                    else:
                        return "false"
                elif ">" in s:
                    if int(ans[0]) > int(ans[1]):
                        return "true"
                    else:
                        return "false"
                elif "<" in s:
                    if int(ans[0]) < int(ans[1]):
                        return "true"
                    else:
                        return "false"
            else:
                if "==" in s:
                    if (ans[0]) == (ans[1]):
                        return "true"
                    else:
                        return "false"
                elif ">" in s:
                    if (ans[0]) > (ans[1]):
                        return "true"
                    else:
                        return "false"
                elif "<" in s:
                    if (ans[0]) < (ans[1]):
                        return "true"
                    else:
                        return "false"
        except:
            return "unsupported"

def operators_runner(x,op,y):
    if op == "or":
        if x == "true" == y:
            return "true"
        elif x == "false" == y:
            return "false"
        elif x == "true" and y == "false":
            return "true"
        elif x == "false" and y == "true":
            return "true"
    elif op == "and":
        if x == "true" == y:
            return "true"
        elif x == "false" == y:
            return "false"
        elif x == "true" and y == "false":
            return "false"
        elif x == "false" and y == "true":
            return "false"

def itemChecker():
    i = input()
    splitPattern = re.compile(r"(or|and)")
    splitedInput = re.split(splitPattern,i)
    for i in range(len(splitedInput)):
        splitedInput[i] = splitedInput[i].strip()
    items = splitedInput[::2]
    operators = splitedInput[1::2]
    for i in range(len(items)):
        items[i] = comparer(items[i])
    if not "unsupported" in items:
        while len(items) > 1:
            newValue = operators_runner(items[0],operators[0],items[1])
            items.pop(0)
            items.pop(0)
            operators.pop(0)
            items.insert(0,newValue)
        print(*items)
    else:
        print("typeError")

itemChecker()