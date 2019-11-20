import mainParse
from timeit import default_timer as timer
start = timer()
f = open('lol.json', 'r', encoding = "utf-8")

string=""
lines=f.readlines()
lines = [line.rstrip() for line in lines]
for line in lines:
    string1="".join(line)
    string=string+string1


for i in range(0,10):
    mainParse.parse(string)
end=timer()
print("--- %s seconds ---" % (end - start))