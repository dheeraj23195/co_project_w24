#turns assembly code into machine code

#updating the provided information in useable format
op_codes = { #add the opcodes
    "r_type_instructions": "0110011",
    "lw": "0000011",
    "sltiu": "0010011",
    "jalr": "1100111",
    "sw": "0100011",
    "blt": "1100011",
    "auipc": "0010111",
    "jal": "0010111"
}

#r-type-instructions data
r_type_instruction = ["add", "slt", "sltu", "xor", "sll", "srl", "or", "and", "sub"]
r_type_func3 = {"add":"000", "sub":"000", "sll":"001", "slt":"010", "sltu":"011", "xor":"100", "srl":"101", "or":"110", "and":"111"}

#i-type-instructions data
i_type_instruction = ["lw", "addi", "sltiu", "jalr"]
i_type_opcodes = {"lw":"0000011", "addi":"0010011", "sltiu":"0010011", "jalr":"1100111"}
i_type_func3 = {"lw":"010", "addi":"000", "sltiu":"011", "jalr":"000"}

#s-type-instructions data
s_type_instruction = ["sw"]

#b-type-instructions data
b_type_instruction = ["beq", "bne", "blt", "bge", "bltu", "bgeu"]
b_type_func3 = {"beq":"000", "bne":"001", "blt":"100", "bge":"101", "bltu":"110", "bgeu":"111"}

#u-type-instructions data
u_type_instruction = ["lui", "auipc"]
u_type_opcode = {"lui":"0110111", "auipc":"0010111"}

#j-type-instructions data
j_type_instruction = ["jal"]

bonus_instruction = ["mul", "rst", "halt", "rvrs"]

def binary_decimal(binary):
    binary_str = str(binary)
    length_binary = len(binary_str)
    decimal = 0
    if binary_str[0] == '0':
        for i in range (length_binary):
            a = int(binary_str[i])
            power = length_binary - 1 - i
            decimal += a*(2**power)
    return decimal

def ones_complement(binary):
    binary_str = str(binary)
    length_binary = len(binary_str)
    new_binary = ""
    for i in range(length_binary):
        if binary_str[i] == "0":
            new_binary += "1"
        elif binary_str[i] == "1":
            new_binary += "0"
    return int(new_binary)

def r_type_convert(instruction):
    operation, registers = instruction.split()
    rd,rs1,rs2=registers.split(",")
    if(operation == "sub"):
        return("0100000" + rs2 + rs1 + "000" + rd + op_codes["r_type_instructions"])
    return("0000000"+ rs2 +rs1 + r_type_func3(operation) + rd + op_codes["r_type_instructions"])

def b_type_convert(instruction):
    operation, registers = instruction.split()
    rs1,rs2,imm=registers.split(",")
    return(imm[11] + imm[9:4:-1] + rs2 + rs1 + b_type_func3[operation] + imm[4:0:-1] + imm[10] + "1100011")

def u_type_convert(instruction):
    operation, registers = instruction.split()
    rd,imm = registers.split(",")
    return(imm + rd + u_type_opcode[operation])

input_data = []
with open("input.txt", "r") as f:
    for line in f:
        input_data.append(line.strip())

output_data=[]

for instruction in input_data:
    if instruction.split()[0] in r_type_instruction:
        output_data.append(r_type_convert(instruction) + "\n")
    elif instruction.split()[0] in b_type_instruction:
        output_data.append(b_type_convert(instruction) + "\n")
    elif instruction.split()[0] in u_type_instruction:
        output_data.append(u_type_convert(instruction) + "\n")

with open("output.txt", "a") as f1:
    f1.writelines(output_data)
