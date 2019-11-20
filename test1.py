#Мой парсер основан на том что все в JSON это объект

import re
from timeit import default_timer as timer
start = timer()

number_regex_1="-?(?:0|\d+)(?:\.\d+)?" #это часть регулярки говорит что число может быть нулем целым или дробным
number_regex_2="(?:[eE][+-]?\d+)" #Это часть отвечает за эекспоненциальную форму числа
number_regex = re.compile(r"(-?(?:0|\d+)(?:\.\d+)?(?:[eE][+-]?\d+)?)", re.DOTALL)
string_regex_1='[^\\"]' #не встречаются символы закрывающую строку
string_regex_2='\\["\\/bfnrt]' #/ один из следющих символов
string_regex_3="\\u[0-9a-fA-F]{4}" #это нкжно для 4hex \u
string_regex_4="*?" #так называемое lazy выражение озночает как можно меньшне повторений
string_regex = re.compile(r'("(?:[^\\"]|\\["\\/bfnrt]|\\u[0-9a-fA-F]{4})*?")', re.DOTALL)

#послденяя часстьь для того чтобы работала нижняя штука
def parse_number(src):
    match = number_regex.search(src)
    if match is not None:
        number= match.group()
        return eval(number) #делаю стринг числом

def parse_string(src):
    match = string_regex.search(src)
    if match is not None:
        string= match.group()
        return eval(string) #для ковычек

def parse_word(word, value=None):
    def result(src):
        if src.startswith(word)==True:  #Возвращает флаг, указывающий на то, начинается ли строка с указанного префикса
            return value
    return result

def parse_all(src):
    ahaha=parse_string(src)
    if ahaha is not None:
        return ahaha
    ahaha=parse_number(src)
    if ahaha is not None:
        return ahaha
    ahaha=parse_false(src)
    if ahaha is not None:
        return ahaha
    ahaha=parse_true(src)
    if ahaha is not None:
        return ahaha
    ahaha=parse_null(src)
    if ahaha is not None:
        return ahaha

parse_true = parse_word("true", True)
parse_false = parse_word("false", False)
parse_null = parse_word("null", None)
parse_comma = ","
parse_left_curly_bracket = "{"
parse_right_curly_bracket = "}"
parse_colon =":"


def pase_object(src):
    left_curly_bracket=[]
    right_curly_bracket=[]
    objects=[]
    res=[]

    for i in range(0,len(src)):
        if src[i]==parse_left_curly_bracket:
            left_curly_bracket.append(i)
        elif src[i]==parse_right_curly_bracket:
            right_curly_bracket.append(i)
#получаем массив с границами объектов от внешнего к внутреннему
    for i in range(0,len(right_curly_bracket)):
        if i==0:
            objects.append(left_curly_bracket[i])
            objects.append(right_curly_bracket[len(right_curly_bracket)-i-1])
        else:
            objects.append(left_curly_bracket[i])
            objects.append(right_curly_bracket[i-1])
    #objects=[0, 30,5,29, 8, 19, 11, 27, 23, 28]
    objects_a=[]
    objects_a.append(objects[0])
    objects_a.append(objects[1])

    i=2
    while i<(len(objects)-2):
        if (objects[i]<objects[i+2]) and (objects[i+1]<objects[i+2]):
            print('объекты однородны')
        else:

            per=objects[i]
            objects[i]=objects[i+2]#если они друг в друге то надо поменять границы
            objects[i+2]=per
        i=i+2
    objects_b=[]#зависимые в главном
    #не большая проблема после подгонки коффициентов они смещаются
    for i in range(0,len(objects)):
        for j in range(0,len(objects)):
            if (i%2==0)and(j%2==0):
                if objects[i]<objects[j]:
                    k1=objects[i]
                    k2=objects[i+1]
                    objects[i]=objects[j]
                    objects[i+1]=objects[j+1]
                    objects[j]=k1
                    objects[j+1]=k2

    i=2
    while i < (len(objects) - 2):
        if (objects[i] < objects[i + 2]) and (objects[i + 1] < objects[i + 2]):
            print('объекты однородны')
        else:
            objects_a.append(objects[i+2])
            objects_a.append(objects[i + 1])
        i = i + 2

    print(objects)
    print(objects_a)

    objects_b=[item for item in objects if item not in objects_a]
    a =[]
    for i in range(2, int(len(objects_a))):
        if i % 2 == 0:
            a.append(src[objects_a[i]:objects_a[i + 1]])

    for j in range(0,int(len(objects_b)/2)):
        if j%2==0:
            work_str=src[objects_b[j]:objects_b[j+1]]
    for i in range(0,len(a)):
        work_str=work_str.replace(a[i],'')

    work_str=work_str.replace('}','')
    work_str=work_str.replace('{','')
    work_str=work_str.replace(',','')
    l1=work_str.split(':')

    print(l1[:len(l1)-1])

    for i in range(0,int(len(objects_a))):
        if i%2==0:

            work_str=src[objects_a[i]:objects_a[i+1]]
            t=0
            for j in range(0,len(work_str)):

                if work_str[j] == '{':
                    t=t+1
            if t==1:
                work_str=work_str.replace(',','`')
            l=work_str.split('`')
            if i==0:
                if (work_str.find('{',1)==work_str.find(':')+1 and (objects[3]==objects[1]-1)):

                    res.append('d')
                    res.append(parse_all(l[0]))

                else:
                    #разработка
                    print("2:17-я считаю это экономически не выгодно")
            else:
                work_str = work_str.replace('}', '')
                work_str = work_str.replace('{', '')
                work_str = work_str.replace(',', '')

            print(l)

def key_value(key,values):
    result={key : values}
    return result


f = open('lol.json', 'r', encoding = "utf-8")
string=""
lines=f.readlines()
lines = [line.strip() for line in lines]
for line in lines:
    string1="".join(line)
    string=string+string1
pase_object('{1:{9:{e:{d:d,s:s}}}}')