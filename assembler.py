#turns assembly code into machine code

#updating the provided information in useable format
op_codes = { #add the opcodes
    "r_type_instructions": "0110011", "lw": "0000011", "sltiu": "0010011", "jalr": "1100111","sw": "0100011","blt": "1100011","auipc": "0010111",
    "jal": "0010111",
}

r_type_instruction=["add", "slt", "sltu", "xor", "sll", "srl", "or", "and", "sub"]
r_type_func3={}

i_type_instruction=["lw", "addi", "sltiu", "jalr"]

s_type_instruction=["sw"]

b_type_instruction=["beq", "bne", "blt", "bge", "bltu", "bgeu"]

u_type_instruction=["lui", "auipc"]

j_type_instruction=["jal"]

bonus_instruction=["mul", "rst", "halt", "rvrs"]


input_data=[]
f=open("input.txt","r")
for x in f:
    input_instructions.append(x)
f.close()

output_data=[]
#loop to work on input and convert to output
#for i in input_instructions:
#   output_data.append(func(i)+"\n")

f1=open("output.txt","a")
f1.writelines(output_data)
f1.close()