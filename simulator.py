import sys
import os

check=0

def decimaltobinaryreal(num):
    num=int(num)
    if num < 0:
        z = abs(num)
        cnt = 1
        s = ""
        temp = z
        while temp != 0:
            cnt += 1
            temp = temp//2
        a = (2**cnt) - z
        while a != 0:
            b = a%2
            a = a//2
            s = s + str(b)
        s = s[::-1]
        filler = 32 - len(s)
        if filler <= 0:
            #print("Number out of Range")
            s='-1'
            return s
        s = filler*"1" + s
        return s
        
    else:
        s = ""
        a = num
        while a != 0:
            b = a%2
            a = a//2
            s = s + str(b)
        s = s[::-1]
        filler = 32 - len(s)
        if filler <= 0:
            s='-1'
            check=1
            #print("number out of Range")
            return s
        s = filler*"0" + s
        return s

def sext(imm):
    if imm[0] == '0':
        while len(imm)<32 :
            imm = '0' + imm
        return imm
    while len(imm) < 32:
        imm = '1' + imm
    return imm

    
def bintodecu(binary):
    s,c=[0,0]
    while(c<len(binary)):
        c=c+1
        s=s+((2**(c))*int(binary[len(binary)-1-c]))    
    return s
    
def bintodecs(binary):
    is_neg = binary[0] == '1'

    if is_neg:
        #Checkifcorrect
        pos = ''.join('1' if bit == '0' else '0' for bit in binary)
        pos = "00" + bin(int(pos, 2) + 1)[2:]
    else:
        pos = binary

    decimal = int(pos, 2)
    if is_neg:
        decimal = -decimal

    return decimal



#check=0

def R_type(code,pc,check=0):
    rs1=code[-20:-15]
    rd=code[-12:-7]
    opcode=code[-32:-25]
    rs2=code[-25:-20]
    funct3=code[-15:-12]
    if(opcode=="0100000"):
        return sub(rd,rs1,rs2,pc)
    else:
        if(funct3=="111"):
            return and_func(rd,rs1,rs2,pc)
        elif(funct3=="000"):
            return add(rd,rs1,rs2,pc)
        elif(funct3=="010"):
            return slt(rd,rs1,rs2,pc)
        elif(funct3=="001"):
            return sll(rd,rs1,rs2,pc)
        elif(funct3=="100"):
            return xor(rd,rs1,rs2,pc)
        elif(funct3=="011"):
            return sltu(rd,rs1,rs2,pc)
        elif(funct3=="110"):
            return or_func(rd,rs1,rs2,pc)
        elif(funct3=="101"):
            return srl(rd,rs1,rs2,pc)
        else:
            return pc

def add(rd,rs1,rs2,pc,check=0):
    n1 = bintodecs(registers[rs1])
    pc+=4
    n2 = bintodecs(registers[rs2])
    x = (n1 + n2)
    y = decimaltobinaryreal(x)
    #Check the func
    check=1
    length=len(y)
    if length > 32:
        registers[rd] = y[-32:]
    else:
        registers[rd] = y
    return(pc)

def slt(rd,rs1,rs2,pc):
    y=registers[rs2]
    y=bintodecs(y)
    pc+=4
    x=registers[rs1]
    x=bintodecs(x)
    if(x<y):
        registers[rd]=decimaltobinaryreal(1)
    return pc

def sub(rd,rs1,rs2,pc,check=0):
    pc+=4
    x=registers[rs1]
    x=bintodecs(x)
    y=registers[rs2]
    y=bintodecs(y)
    z=x-y
    registers[rd]=decimaltobinaryreal(z)
    return pc

def xor(rd,rs1,rs2,pc):
    pc+=4
    x=bintodecs(registers[rs1])
    y=bintodecs(registers[rs2])
    registers[rd]=decimaltobinaryreal(x^y)
    return pc

def sltu(rd,rs1,rs2,pc):
    y=registers[rs2]
    y=bintodecu(x)
    x=registers[rs1]
    x=bintodecu(y)
    pc+=4
    if(x<y):
        registers[rd]=decimaltobinaryreal(1)
    return pc

def and_func(rd,rs1,rs2,pc):
    pc+=4
    x = bintodecs(registers[rs1])
    y = bintodecs(registers[rs2])
    registers[rd]=decimaltobinaryreal(x & y)
    return pc

def srl(rd,rs1,rs2,pc):
    x=bintodecs(registers[rs1])
    y=bintodecu(registers[rs2][-5:])
    pc+=4
    registers[rd]=decimaltobinaryreal(x//(2**y))
    return pc

def or_func(rd,rs1,rs2,pc):
    pc+=4
    x=bintodecs(registers[rs1])
    y=bintodecs(registers[rs2])
    registers[rd]=decimaltobinaryreal(x|y)
    return pc



def sll(rd,rs1,rs2,pc):
    pc+=4
    x=bintodecs(registers[rs1])
    y=bintodecu(registers[rs2][-5:])
    registers[rd]=decimaltobinaryreal(x*(2**y))
    return pc



#I Type

def jalr(code,pc):
    imm = code[-32:-20]
    rd = code[-12:-7]
    imm = sext(imm)
    y=bintodecs(imm)
    rs1 = code[-20:-15]
    x=bintodecs(registers[rs1])
    temp = decimaltobinaryreal(pc + 4)
    registers[rd] = temp   
    pc = x + y
    if pc%2==1:
        pc = pc - 1
    return pc


def lw(code,pc):
    pc+=4
    rs1 = code[-20:-15]
    x=bintodecs(registers[rs1])
    imm = code[-32:-20]
    y=bintodecs(sext(imm))
    rd = code[-12:-7]
    add = hex(x + y)
    length = len(add)
    while(len(add)<10):
        add = "0x" + "0" + add[2:]
    registers[rd] = memory[add]
    return pc



def addi(code,pc):
    pc+=4
    rs1 = code[-20:-15]
    x = bintodecs(registers[rs1])
    rd = code[-12:-7]
    imm = sext(code[-32:-20])
    y = bintodecs(imm)
    value = x + y
    registers[rd] = decimaltobinaryreal(value)
    return pc




#B Type
def B_type(code,pc):
    funct3 = code[-15:-12]
    imm = code[-32] + code[-8] + code[-31:-25] + code[-12:-8] + '0'
    rs1 = code[-20:-15]
    rs2 = code[-25:-20]
    imm = sext(imm)
    imm = bintodecs(imm)

    if funct3 == "000":
        return beq(rs1,rs2,imm,pc)
    elif funct3 == "001":
        return bne(rs1,rs2,imm,pc)
    elif funct3 == "100":
        return blt(rs1,rs2,imm,pc)
    elif funct3 == "101":
        return bge(rs1,rs2,imm,pc)
    else:
        return pc

def bne(rs1,rs2,imm,pc):
    x=bintodecs(registers[rs1])
    y=bintodecs(registers[rs2])
    if x!=y:
        return pc + imm
    else:
        return pc + 4

def bge(rs1,rs2,imm,pc):
    x=bintodecs(registers[rs1])
    y=bintodecs(registers[rs2])
    if x>=y:
        return pc + imm
    else:
        return pc + 4

def beq(rs1,rs2,imm,pc):
    val1=bintodecs(registers[rs1])
    val2=bintodecs(registers[rs2])
    if val1==val2:
        return pc + imm
    else:
        return pc + 4


def blt(rs1,rs2,imm,pc):
    x=bintodecs(registers[rs1])
    y=bintodecs(registers[rs2])
    if x<y:
        return pc + imm
    else:
        return pc + 4



#S Type
def sw(code,pc):
    imm = code[-32:-25] + code[-12:-7]
    imm=sext(imm)
    rs1 = code[-20:-15]
    pc+=4
    val1=bintodecs(registers[rs1])
    rs2 = code[-25:-20]
    val2= bintodecs(imm)
    add = val1 + val2
    add = hex(add)
    length=len(add)
    while(length<10):
        add = "0x" + "0" + add[2:]
        length=len(add)
    memory[add] = registers[rs2]
    return pc


#J Type
def jal(code,pc):
    imm = code[-32] + code[-20:-12] + code[-21] + code[-31:-21] + "0"
    imm = sext(imm)
    rd = code[-12:-7]
    temp = pc + 4
    imm = bintodecs(imm)
    temp = decimaltobinaryreal(temp)
    registers[rd] = temp
    pc = pc + imm
    if pc%2==1:
        pc = pc - 1
    return pc

#U Type
def auipc(code,pc):
    filler="000000000000"
    imm = code[-32:-12] + filler
    imm = bintodecs(imm)
    temp = pc + imm
    temp = decimaltobinaryreal(temp)
    pc+=4
    rd = code[-12:-7]
    registers[rd] = temp

    return pc

def lui(code,pc):
    filler="000000000000"
    imm = code[-32:-12] + filler
    pc+=4
    rd = code[-12:-7]
    registers[rd] = imm
    return pc



#Reg print and main
def RegPrint(l):
    s=""
    s1=""
    for i in registers.keys():
        s1="0b"+registers[i]+" "
        s=s+s1
    s+="\n"
    l.append(s)

def Main(registers,memory,pc_dic):
    pc=0
    while True:
        OpCode=pc_dic[pc][-7:]

        if pc_dic[pc] == "00000000000000000000000001100011":
            RegPrint(l)
            break
        
        #J Type
        if(OpCode=="1101111"):
            pc=jal(pc_dic[pc],pc)
            check=1
            registers['pc']=decimaltobinaryreal(pc)
        #S Type
        elif(OpCode=="0100011"):
            pc=sw(pc_dic[pc],pc)
            check=-1
            registers['pc']=decimaltobinaryreal(pc)    
        #R Type
        elif(OpCode=="0110011"):
            pc=R_type(pc_dic[pc],pc)
            registers['pc']=decimaltobinaryreal(pc)
        #B Type
        elif(OpCode=="1100011"):
            pc=B_type(pc_dic[pc],pc)
            registers['pc']=decimaltobinaryreal(pc)    
        #I Type
        elif(OpCode=="0000011"):
            pc=lw(pc_dic[pc],pc)
            registers['pc']=decimaltobinaryreal(pc)
        elif(OpCode=="0010011"):
            pc=addi(pc_dic[pc],pc)
            registers['pc']=decimaltobinaryreal(pc)
        elif(OpCode=="1100111"):
            pc=jalr(pc_dic[pc],pc)
            registers['pc']=decimaltobinaryreal(pc)
        #U Type
        elif(OpCode=="0110111"):
            pc=lui(pc_dic[pc],pc)
            registers['pc']=decimaltobinaryreal(pc)
        elif(OpCode=="0010111"):
            pc=auipc(pc_dic[pc],pc)
            registers['pc']=decimaltobinaryreal(pc)
        
        RegPrint(l)

def read_file_and_create_dict(input_file):
    pc_dic = {}
    var = 0

    with open(input_file, "r") as f:
        while True:
            line = f.readline().strip()  # Read and remove leading/trailing whitespaces
            if not line:
                break  # Exit loop if an empty line is encountered
            pc_dic[var] = line
            var += 4

    if not pc_dic:
        sys.exit("Input file is empty")

    return pc_dic

# Example usage:
if len(sys.argv) < 3:
    sys.exit("Input file path and output file path are required")

input = sys.argv[1]
output = sys.argv[2]

if not os.path.exists(input):
    sys.exit("Input file does not exist")

pc_dic = read_file_and_create_dict(input)
registers={
    'pc':'00000000000000000000000000000100',
    '00000':'00000000000000000000000000000000',
    '00001':'00000000000000000000000000000000',
    '00010':'00000000000000000000000100000000',
    '00011':'00000000000000000000000000000000',
    '00100':'00000000000000000000000000000000',
    '00101':'00000000000000000000000000000000',
    '00110':'00000000000000000000000000000000',
    '00111':'00000000000000000000000000000000',
    '01000':'00000000000000000000000000000000',
    '01001':'00000000000000000000000000000000',
    '01010':'00000000000000000000000000000000',
    '01011':'00000000000000000000000000000000',
    '01100':'00000000000000000000000000000000',
    '01101':'00000000000000000000000000000000',
    '01110':'00000000000000000000000000000000',
    '01111':'00000000000000000000000000000000',
    '10000':'00000000000000000000000000000000',
    '10001':'00000000000000000000000000000000',
    '10010':'00000000000000000000000000000000',
    '10011':'00000000000000000000000000000000',
    '10100':'00000000000000000000000000000000',
    '10101':'00000000000000000000000000000000',
    '10110':'00000000000000000000000000000000',
    '10111':'00000000000000000000000000000000',
    '11000':'00000000000000000000000000000000',
    '11001':'00000000000000000000000000000000',
    '11010':'00000000000000000000000000000000',
    '11011':'00000000000000000000000000000000',
    '11100':'00000000000000000000000000000000',
    '11101':'00000000000000000000000000000000',
    '11110':'00000000000000000000000000000000',
    '11111':'00000000000000000000000000000000'}

l=[]

memory= {
    "0x00010000": "00000000000000000000000000000000",
    "0x00010004": "00000000000000000000000000000000",
    "0x00010008": "00000000000000000000000000000000",
    "0x0001000c": "00000000000000000000000000000000",
    "0x00010010": "00000000000000000000000000000000",
    "0x00010014": "00000000000000000000000000000000",
    "0x00010018": "00000000000000000000000000000000",
    "0x0001001c": "00000000000000000000000000000000",
    "0x00010020": "00000000000000000000000000000000",
    "0x00010024": "00000000000000000000000000000000",
    "0x00010028": "00000000000000000000000000000000",
    "0x0001002c": "00000000000000000000000000000000",
    "0x00010030": "00000000000000000000000000000000",
    "0x00010034": "00000000000000000000000000000000",
    "0x00010038": "00000000000000000000000000000000",
    "0x0001003c": "00000000000000000000000000000000",
    "0x00010040": "00000000000000000000000000000000",
    "0x00010044": "00000000000000000000000000000000",
    "0x00010048": "00000000000000000000000000000000",
    "0x0001004c": "00000000000000000000000000000000",
    "0x00010050": "00000000000000000000000000000000",
    "0x00010054": "00000000000000000000000000000000",
    "0x00010058": "00000000000000000000000000000000",
    "0x0001005c": "00000000000000000000000000000000",
    "0x00010060": "00000000000000000000000000000000",
    "0x00010064": "00000000000000000000000000000000",
    "0x00010068": "00000000000000000000000000000000",
    "0x0001006c": "00000000000000000000000000000000",
    "0x00010070": "00000000000000000000000000000000",
    "0x00010074": "00000000000000000000000000000000",
    "0x00010078": "00000000000000000000000000000000",
    "0x0001007c": "00000000000000000000000000000000"}

Main(registers, memory, pc_dic)

with open(output, "w") as f:
    for line in l:
        f.write(line)
    for i in memory.keys():
        f.write(i+":0b"+memory[i]+"\n")
sys.exit()