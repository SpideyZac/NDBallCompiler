import random
import sys
import time

class Token:
    def __init__(self, token, value = None, pos = None):
        self.token = token
        self.value = value
        self.pos = pos

    def __repr__(self):
        return "Token {} with value {}".format(self.token, self.value)

class Ball:
    def __init__(self):
        self.pos = [0]
        self.direction = 0
        self.value = 0
        self.apiforms = 0
        self.dimension = 0

    def update(self):
        while len(self.pos) < self.dimension + 1:
            self.pos.append(0)

        if self.direction == 1:
            self.pos[self.dimension] += 1
        if self.direction == -1:
            self.pos[self.dimension] -= 1

def lex(text):
    lexed = []
    singleValids = ['(', ')', '{', '}', '[', ']', '<', '>', '+', '-', 'p', 'P', '$', '%', 'E', '#', '|', 'K', 'a', 'f', 'q', 'n', 'H', 'Y', '/', 's', 'L', 'R', 'S']
    multiValids = ['St', 'ESt', 'PSt']

    i = 0
    while i < len(text):
        foundone = False
        if text[i] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            num = ""
            con = True
            while text[i] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] and con:
                num += text[i]
                if i + 1 >= len(text):
                    i += 1
                    break
                i += 1
            lexed.append(Token("INT", int(num), i))
            foundone = True
            continue
        if i + 1 < len(text):
            if text[i] + text[i + 1] in multiValids:
                lexed.append(Token("St", pos=i))
                foundone = True
                continue
        if i + 2 < len(text):
            if text[i] + text[i + 1] + text[i + 2] in multiValids:
                lexed.append(Token(text[i] + text[i + 1] + text[i + 2], pos=i))
                foundone = True
                continue
        if text[i] in singleValids:
            lexed.append(Token(text[i], pos=i))
            foundone = True

        i += 1

    return lexed

def parse_location(lexdata, text):
    _ = "{"
    if lexdata[0].token != "(" and lexdata[0].token != "{":
        exit(f"Syntax error; expected line to start with location, ( or {_}\n{text}\n^")

    cord = []
    howMany = 0

    if lexdata[0].token == "(":
        i = 1
        while lexdata[i].token != ")":
            if lexdata[i].value is not None:
                if lexdata[i].value > -1 and lexdata[i].value < 5:
                    cord.append(int(lexdata[i].value))
                else:
                    exit(f"Syntax error; Location value must be either 0, 1, 2, 3, 4\n{text}\n" + " " * i + "^")
            else:
                exit(f"Syntax error; Location value must be int and positive\n{text}\n" + " " * i + "^")
            i += 1
        howMany = i + 1
    else:
        i = 1
        while lexdata[i].token != "}":
            if lexdata[i].token == "|":
                i += 1
            if lexdata[i].value is not None:
                while len(cord) <= lexdata[i].value:
                    cord.append(0)
                if i + 1 < len(lexdata):
                    if lexdata[i + 1].value > -1 and lexdata[i + 1].value < 5:
                        cord[lexdata[i].value] = lexdata[i + 1].value
                    else:
                        exit(f"Syntax error; Location value must be either 0, 1, 2, 3, 4\n{text}\n" + " " * i + "^")
                    i += 1
                else:
                    exit(f"Need location value")
            else:
                exit(f"Syntax error; Dimension must be int and positive\n{text}\n" + " " * i + "^")
            i += 1
        howMany = i + 1

    return cord, howMany

def compile(file):
    f = open(file, "r")
    lines = f.readlines()
    f.close()

    for i in range(len(lines)):
        lines[i].strip('\n')
        lines[i].strip('\t')

    loc = []
    lexed_data = []
    howManys = []
    thelines = []

    while "" in lines:
        lines.remove("")

    res = []
    for sub in lines:
        flag = 0
        for ele in sub:
            if ele in "/":
                flag = 1
        if not flag:
            res.append(sub)

    lines = res

    for i in range(len(lines)):
        lexed_data.append(lex(lines[i]))
        loc.append(parse_location(lexed_data[i], lines[i])[0])
        howManys.append(parse_location(lexed_data[i], lines[i])[1])
        thelines.append(lines[i])
    ball = Ball()
    memoryString = ""
    useMemoryString = False
    memory = []
    loca = []

    while True:
        ball.update()
        lextorun = ""
        if 5 in ball.pos or -1 in ball.pos:
            exit("Ball crashed into wall at {} and split into a thousand pieces".format(ball.pos))
        for i in range(len(loc)):
            while len(loc[i]) < len(ball.pos):
                loc[i].append(0)
            while len(loc[i]) > len(ball.pos):
                ball.pos.append(0)
            if loc[i] == ball.pos:
                lextorun = lexed_data[i]
                use = i
                break
        
        if lextorun != "":
            torun = lextorun[howManys[use]:len(lextorun)]
            for i in range(len(torun)):
                if torun[i].token == "(" or torun[i].token == ")" or torun[i].token == "{" or torun[i].token == "}":
                    exit(f"Unexpected location identifier\n{thelines[use]}\n" + " " * torun[i].pos + "^")

            if torun[0].token == ">":
                ball.direction = 1
                if torun[1].token == "INT":
                    ball.dimension = torun[1].value
                else:
                    exit(f"Dimension must be int\n{thelines[use]}\n" + " " * torun[1].pos + "^")
                if len(torun) > 2:
                    exit(f"Unexpeted action\n{thelines[use]}\n" + " " * torun[2].pos + "^")
            elif torun[0].token == "<":
                ball.direction = -1
                if torun[1].token == "INT":
                    ball.dimension = torun[1].value
                else:
                    exit(f"Dimension must be int\n{thelines[use]}\n" + " " * torun[1].pos + "^")
                if len(torun) > 2:
                    exit(f"Unexpeted action\n{thelines[use]}\n" + " " * torun[2].pos + "^")
            elif torun[0].token == "+":
                ball.value += 1
                if len(torun) > 1:
                    exit(f"Unexpeted action\n{thelines[use]}\n" + " " * torun[1].pos + "^")
            elif torun[0].token == "-":
                ball.value -= 1
                if len(torun) > 1:
                    exit(f"Unexpeted action\n{thelines[use]}\n" + " " * torun[1].pos + "^")
            elif torun[0].token == "p":
                if not useMemoryString:
                    print(chr(ball.value))
                else:
                    memoryString += chr(ball.value) + "\n"
                if len(torun) > 1:
                    exit(f"Unexpeted action\n{thelines[use]}\n" + " " * torun[1].pos + "^")
            elif torun[0].token == "P":
                if not useMemoryString:
                    print(ball.value)
                else:
                    memoryString += str(ball.value) + "\n"
                if len(torun) > 1:
                    exit(f"Unexpeted action\n{thelines[use]}\n" + " " * torun[1].pos + "^")
            elif torun[0].token == "$":
                char = input("Input a single character >>> ")
                ball.value = ord(char)
                if len(char) > 1 or len(char) == 0:
                    exit("Character was not ONE CHARACTER")
                if len(torun) > 1:
                    exit(f"Unexpeted action\n{thelines[use]}\n" + " " * torun[1].pos + "^")
            elif torun[0].token == "%":
                try:
                    ball.value = int(input("Input a number >>> "))
                except:
                    exit("Value was not INT")
            elif torun[0].token == "E":
                exit()
            elif torun[0].token == "#":
                movdir = torun[1].token
                movdim = torun[2].token
                if loc[use] in loca:
                    rem = memory[loca.index(loc[use])]
                else:
                    if len(torun) > 3:
                        rem = torun[3].value
                        if len(torun) > 4:
                            exit(f"Unexpeted action\n{thelines[use]}\n" + " " * torun[4].pos + "^")
                    else:
                        rem = 0
                if movdir != "<" and movdir != ">":
                    exit(f"Expected movement direction < or >\n{thelines[use]}\n" + " " * torun[1].pos + "^")
                if movdim != "INT":
                    exit(f"Expected dimension to be int\n{thelines[use]}\n" + " " * torun[1].pos + "^")
                if movdir == "<":
                    movdir = -1
                else:
                    movdir = 1
                movdim = torun[2].value

                if movdim == ball.dimension and movdir == ball.direction:
                    rem = ball.value
                else:
                    ball.value = rem

                if loc[use] in loca:
                    memory[loca.index(loc[use])] = rem
                else:
                    loca.append(loc[use])
                    memory.append(rem)
            elif torun[0].token == "|":")
                ball.direction = -ball.direction
                if len(torun) > 1:
                    exit(f"Unexpeted action\n{thelines[use]}\n" + " " * torun[1].pos + "^")
            elif torun[0].token == "K":
                movdir = torun[1].token
                movdim = torun[2].token
                if movdir != "<" and movdir != ">":
                    exit(f"Expected movement direction < or >\n{thelines[use]}\n" + " " * torun[1].pos + "^")
                if movdim != "INT":
                    exit(f"Expected dimension to be int\n{thelines[use]}\n" + " " * torun[1].pos + "^")
                if movdir == "<":
                    movdir = -1
                else:
                    movdir = 1
                movdim = torun[2].value

                if ball.direction != movdir or ball.dimension != movdim:
                    ball.direction = -ball.direction
                if len(torun) > 3:
                    exit(f"Unexpeted action\n{thelines[use]}\n" + " " * torun[3].pos + "^")
            elif torun[0].token == "a":
                ball.apiforms += 1
                if len(torun) > 1:
                    exit(f"Unexpeted action\n{thelines[use]}\n" + " " * torun[1].pos + "^")
            elif torun[0].token == "f":
                ball.apiforms -= 1
                if len(torun) > 1:
                    exit(f"Unexpeted action\n{thelines[use]}\n" + " " * torun[1].pos + "^")
            elif torun[0].token == "q":
                ball.apiforms = 0
                if len(torun) > 1:
                    exit(f"Unexpeted action\n{thelines[use]}\n" + " " * torun[1].pos + "^")
            elif torun[0].token == "n":
                ball.apiforms = ball.value
                if len(torun) > 1:
                    exit(f"Unexpeted action\n{thelines[use]}\n" + " " * torun[1].pos + "^")
            elif torun[0].token == "H":
                ball.value = ball.apiforms
                if len(torun) > 1:
                    exit(f"Unexpeted action\n{thelines[use]}\n" + " " * torun[1].pos + "^")
            elif torun[0].token == "Y":
                if torun[1].token != "[":
                    exit(f"Expected [\n{thelines[use]}\n" + " " * torun[1].pos + "^")
                if torun[7].token != "]":
                    exit(f"Expected ]\n{thelines[use]}\n" + " " * torun[7].pos + "^")
                x = torun[2]
                movAdir = torun[3]
                movAdim = torun[4]
                movBdir = torun[5]
                movBdim = torun[6]
                if x.token != "INT":
                    exit(f"Expected value to be int\n{thelines[use]}\n" + " " * torun[2].pos + "^")
                if movAdir.token != ">" and movAdir.token != "<":
                    exit(f"Expected movement direction < or >\n{thelines[use]}\n" + " " * torun[3].pos + "^")
                if movAdim.token != "INT":
                    exit(f"Expected dimension to be int\n{thelines[use]}\n" + " " * torun[4].pos + "^")
                if movBdir.token != ">" and movBdir.token != "<":
                    exit(f"Expected movement direction < or >\n{thelines[use]}\n" + " " * torun[5].pos + "^")
                if movBdim.token != "INT":
                    exit(f"Expected dimension to be int\n{thelines[use]}\n" + " " * torun[6].pos + "^")
                if ball.value < x.value:
                    if movAdir.token == "<":
                        ball.direction = -1
                    else:
                        ball.direction = 1
                    ball.dimension = movAdim.value
                else:
                    if movBdir.token == "<":
                        ball.direction = -1
                    else:
                        ball.direction = 1
                    ball.dimension = movBdim.value
                if len(torun) > 8:
                    exit(f"Unexpeted action\n{thelines[use]}\n" + " " * torun[8].pos + "^")
            elif torun[0].token == "/":
                if len(torun) > 1:
                    exit(f"Unexpeted action\n{thelines[use]}\n" + " " * torun[1].pos + "^")
            elif torun[0].token == "s":
                if loc[use] in loca:
                    rem = memory[loca.index(loc[use])]
                else:
                    if len(torun) > 1:
                        rem = torun[1].value
                    else:
                        rem = 0

                toRem = ball.value
                ball.value = rem
                rem = toRem
                if loc[use] in loca:
                    memory[loca.index(loc[use])] = rem
                else:
                    loca.append(loc[use])
                    memory.append(rem)
                if len(torun) > 2:
                    exit(f"Unexpeted action\n{thelines[use]}\n" + " " * torun[2].pos + "^")
            elif torun[0].token == "L":
                if loc[use] in loca:
                    if len(memory[loca.index(loc[use])]) == 0:
                        char = input("Input some text >>> ")
                    else:
                        char = memory[loca.index(loc[use])]
                else:
                    char = input("Input some text >>> ")

                print(char[-1])
                char = char[0:len(char) - 1]
                if loc[use] in loca:
                    memory[loca.index(loc[use])] = char
                else:
                    loca.append(loc[use])
                    memory.append(char)
                if len(torun) > 1:
                    exit(f"Unexpeted action\n{thelines[use]}\n" + " " * torun[1].pos + "^")
            elif torun[0].token == "R":
                ball.value = random.randint(0, 255)
                if len(torun) > 1:
                    exit(f"Unexpeted action\n{thelines[use]}\n" + " " * torun[1].pos + "^")
            elif torun[0].token == "S":
                if loc[use] in loca:
                    timer = memory[loca.index(loc[use])]
                    time.sleep(timer / 1000)
                else:
                    if torun[1].token != "INT":
                        exit(f"Expected value to be int\n{thelines[use]}\n" + " " * torun[1].pos + "^")
                    timer = torun[1].value
                    loca.append(loc[use])
                    memory.append(timer)
                    time.sleep(timer / 1000)
                if len(torun) > 2:
                    exit(f"Unexpeted action\n{thelines[use]}\n" + " " * torun[2].pos + "^")
            elif torun[0].token == "St":
                useMemoryString = True
                if len(torun) > 1:
                    exit(f"Unexpeted action\n{thelines[use]}\n" + " " * torun[1].pos + "^")
            elif torun[0].token == "ESt":
                useMemoryString = False
                if len(torun) > 1:
                    exit(f"Unexpeted action\n{thelines[use]}\n" + " " * torun[1].pos + "^")
            elif torun[0].token == "PSt":
                print(memoryString)
                if len(torun) > 1:
                    exit(f"Unexpeted action\n{thelines[use]}\n" + " " * torun[1].pos + "^")
            else:
                exit(f"Syntax Error; No Action {torun[0].token}\n{thelines[use]}\n" + " " * torun[0].pos + "^")

compile(sys.argv[1])
