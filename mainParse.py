from itertools import chain
import re
from timeit import default_timer as timer
start = timer()

number_regex_1="-?(?:0|\d+)(?:\.\d+)?" #это часть регулярки говорит что число может быть нулем целым или дробным
number_regex_2="(?:[eE][+-]?\d+)" #Это часть отвечает за эекспоненциальную форму числа
regex_for_all="\s(.*)" #\r\n\t\f\v - это делает \s* а .* означает любой символ
number_regex = re.compile(r"(-?(?:0|\d+)(?:\.\d+)?(?:[eE][+-]?\d+)?)\s*(.*)", re.DOTALL)
string_regex_1='[^\\"]' #не встречаются символы закрывающую строку
string_regex_2='\\["\\/bfnrt]' #/ один из следющих символов
string_regex_3="\\u[0-9a-fA-F]{4}" #это нкжно для 4hex \u
string_regex_4="*?" #так называемое lazy выражение озночает как можно меньшне повторений
string_regex = re.compile(r'("(?:[^\\"]|\\["\\/bfnrt]|\\u[0-9a-fA-F]{4})*?")\s*(.*)', re.DOTALL)

#послденяя часстьь для того чтобы работала нижняя штука
def parse_number(src):
    match = number_regex.match(src)
    if match is not None:
        number, src = match.groups()
        yield eval(number), src


def parse_string(src):
    match = string_regex.match(src)
    if match is not None:
        string, src = match.groups()
        yield eval(string), src

def parse_word_generator(word, value=None):
    l = len(word)
    def result(src):
        if src.startswith(word)==True:
            yield value, src[l:].lstrip()
    return result

parse_true = parse_word_generator("true", True)
parse_false = parse_word_generator("false", False)
parse_null = parse_word_generator("null", None)

def parse_value(src):
    for match in chain(
        parse_string(src),
        parse_number(src),
        parse_true(src),
        parse_false(src),
        parse_null(src),
        parse_object(src),

    ):
        yield match

parse_comma = parse_word_generator(",")
parse_left_curly_bracket = parse_word_generator("{")
parse_right_curly_bracket = parse_word_generator("}")


def parse_object(src):
    for _, src in parse_left_curly_bracket(src):
        for items, src in parse_comma_separated_keyvalues(src):
            for _, src in parse_right_curly_bracket(src):
                yield items, src


parse_colon = parse_word_generator(":")

def parse_keyvalue(src):
    for key,src in parse_string(src):
        for _,src in parse_colon(src):
            for value,src in parse_value(src):
                yield {key: value}, src


def parse_comma_separated_keyvalues(src):
    for keyvalue,ssrc in parse_keyvalue(src):
        for _,ssrc in parse_comma(ssrc):
            for keyvalues,ssrc in parse_comma_separated_keyvalues(ssrc):

                keyvalue.update(keyvalues)

                yield keyvalue, ssrc

    for keyvalue, src in parse_keyvalue(src):

        yield keyvalue, src

def parse(s):
    match = list(parse_value(s))
    result, a = match[0]
    return result

f = open('lol.json', 'r', encoding = "utf-8")
string=""
lines=f.readlines()
lines = [line.rstrip() for line in lines]
for line in lines:
    string1="".join(line)
    string=string+string1
print(parse(string))


end = timer()
print("--- %s seconds ---" % (end - start))