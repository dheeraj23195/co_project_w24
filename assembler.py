#turns assembly code into machine code


input_lines=[]
output_data=[]

#updating the provided information in useable format
op_codes = { #add the opcodes
    "r_type_instructions": "0110011", "lw": "0000011", "sltiu": "0010011", "jalr": "1100111","sw": "0100011","blt": "1100011","auipc": "0010111",
    "jal": "0010111",
}

r_type_instruction=[#add the instructions 
"add", "slt", "sltu", "xor", "sll", "srl", "or", "and", "sub"]

i_type_instruction=[#complete the instruction list
"lw", "addi", "sltiu", "jalr"]

s_type_instruction=["sw"]

b_type_instruction=["beq", "bne", "blt", "bge", "bltu", "bgeu"]

u_type_instruction=["lui", "auipc"]

j_type_instruction=["jal"]

bonus_instruction=["mul", "rst", "halt", "rvrs"]

