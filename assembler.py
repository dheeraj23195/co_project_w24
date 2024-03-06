#turns assembly code into machine code

#updating the provided information in useable format
op_codes = { #add the opcodes
    "r_type_instructions": "0110011", "lw": "0000011", "sltiu": "0010011", "jalr": "1100111","sw": "0100011","blt": "1100011","auipc": "0010111",
    "jal": "0010111",
}

r_type_instruction=[#add the instructions 
    "add",
                    "sub"]

i_type_instruction=[#complete the instruction list
                    "lw","addi"
]

s_type_instruction=[]

b_type_instruction=[]

u_type_instruction=[]

j_type_instruction=[]

bonus_instruction=[]