#turns assembly code into machine code

#updating the provided information in useable format
op_codes = { #add the opcodes
    "r_type_instructions": "0110011", "lw": "0000011", "sltiu": "0010011", "jalr": "1100111","sw": "0100011","blt": "1100011","auipc": "0010111",
    "jal": "0010111",
}

#r-type-instructions data
r_type_instruction=["add", "slt", "sltu", "xor", "sll", "srl", "or", "and", "sub"]
r_type_func3={}

#i-type-instructions data
i_type_instruction=["lw", "addi", "sltiu", "jalr"]

s_type_instruction=["sw"]

b_type_instruction=["beq", "bne", "blt", "bge", "bltu", "bgeu"]

u_type_instruction=["lui", "auipc"]

j_type_instruction=["jal"]

bonus_instruction=["mul", "rst", "halt", "rvrs"]

def binary_decimal(binary):
    binary_str = str(binary)
    length_binary = len(binary_str)
    decimal = 0
    if binary_str[0] == 0:
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

input_data=[]
f=open("input.txt","r")
for x in f:
    input_data.append(x)
f.close()

output_data=[]
#loop to work on input and convert to output
#for i in input_data:
#   output_data.append(func(i)+"\n")

f1=open("output.txt","a")
f1.writelines(output_data)
f1.close()
