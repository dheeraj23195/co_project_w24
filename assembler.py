#turns assembly code into machine code
input_lines=[]
output_data=[]
op_codes = {
    "add": "0110011",
    "jalr": "1100111",
    "lw": "0000011",
    "sw": "0100011",
    "blt": "1100011",
    "auipc": "0010111",
    "jal": "0010111",
    "addi": "0010011",
}
