import mainParse
f = open('lol.json', 'r', encoding = "utf-8")
objects='message '
all_value='required'
tip1='string'
tip2='uint32'
newline=''
def types(s):
    if isinstance(s,str):
        l='string'
        return l
    else:
        l='uint32'
        return l

string=""
lines=f.readlines()
lines = [line.rstrip() for line in lines]
for line in lines:
    string1="".join(line)
    string=string+string1
w=open('kek.proto', 'w', encoding="utf-8")
s=mainParse.parse(string)

keysdouble2=[]
def cinvert(dic,t,h):
    keys = []
    for key in dic:
        keys.append(key)
    for i in range(0,len(keys)):
        if isinstance(dic[keys[i]],dict)==True:
            w.write('\t'*t+objects+keys[i]+' {'+'\n')
            if len(keys)==1:
                t+=1
            cinvert(dic[keys[i]],t,h)
            w.write('\t'*t+'}'+'\n')
        elif isinstance(dic[keys[i]],dict) == False:
            h+=1
            w.write('\t'*(t+1)+'required'+' '+types(dic[keys[i]])+' '+ keys[i]+'='+str(h)+';'+'\n')


print(s)
cinvert(s,0,0)