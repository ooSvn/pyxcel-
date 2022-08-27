import re

# "AB"            -> text-num
# "adm1245a"      -> text 
# 2               -> num
# "ABdk"          -> unSupported

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
    # blankStringPatt = re.compile(r"[+\-] *\"\" *$")
    blankStringPatt2 = re.compile(r"^ *\"\" *\+ *")
    blankStringPatt23 = re.compile(r"[+\-] *\"\" *")
    # s = re.sub(blankStringPatt,"",s)
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
                    print("unsupported operand")
                    flag2 = 1
                    break
            if flag == 0 and flag2 == 0:
                print(s)
        else:
            if flagg == False:
                print(s)            
            else:
                print("unsupported operand")
    else:
        print("unsupported operand")
n = input().strip()
analyzer(n)

# 1+" "
# "A" - "C" 
# 2 - "A"
# "A1" + 3 *12/4
# "1"+"AA"+1


# "" + 2 -> unsupported
# "" + "A" -> "A"
# "AB" + 2 + 3 = "AG"
# 2 + "AB" + 3 = 33 relatively
# "AB"+2 + "kc" = "ADkc"
# "AB" + "a" + "k" = "ABak"
# 2+6*50/25
# "1" + "2"