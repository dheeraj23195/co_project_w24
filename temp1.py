import sys

# Program memory size and ranges
memory_size_program = 256
memory_range_program = range(0, memory_size_program)

# Stack memory size and ranges
memory_size_stack = 128
memory_range_stack = range(256, 256 + memory_size_stack)

# Data memory size and ranges
memory_size_data = 128
memory_range_data = range(4096, 4096 + memory_size_data)

op_codes = {
    "r_type_instructions": "0110011",
    "lw": "0000011",
    "sltiu": "0010011",
    "jalr": "1100111",
    "sw": "0100011",
    "blt": "1100011",
    "auipc": "0010111",
    "jal": "0010111"
}

# r-type-instructions data
r_type_instruction = ["add", "slt", "sltu", "xor", "sll", "srl", "or", "and", "sub"]
r_type_func3 = {"add": "000", "sub": "000", "sll": "001", "slt": "010", "sltu": "011", "xor": "100", "srl": "101",
                "or": "110", "and": "111"}

# i-type-instructions data
i_type_instruction = ["lw", "addi", "sltiu", "jalr"]
i_type_opcodes = {"lw": "0000011", "addi": "0010011", "sltiu": "0010011", "jalr": "1100111"}
i_type_func3 = {"lw": "010", "addi": "000", "sltiu": "011", "jalr": "000"}

# s-type-instructions data
s_type_instruction = ["sw"]

# b-type-instructions data
b_type_instruction = ["beq", "bne", "blt", "bge", "bltu", "bgeu"]
b_type_func3 = {"beq": "000", "bne": "001", "blt": "100", "bge": "101", "bltu": "110", "bgeu": "111"}

# u-type-instructions data
u_type_instruction = ["lui", "auipc"]
u_type_opcode = {"lui": "0110111", "auipc": "0010111"}

# j-type-instructions data
j_type_instruction = ["jal"]

# registers data
register_code= {
    "zero": "00000",
    "ra": "00001",
    "sp": "00010",
    "gp": "00011",
    "tp": "00100",
    "t0": "00101",
    "t1": "00110",
    "t2": "00111",
    "s0": "01000",
    "fp": "01000",
    "s1": "01001",
    "a0": "01010",
    "a1": "01011",
    "a2": "01100",
    "a3": "01101",
    "a4": "01110",
    "a5": "01111",
    "a6": "10000",
    "a7": "10001",
    "s2": "10010",
    "s3": "10011",
    "s4": "10100",
    "s5": "10101",
    "s6": "10110",
    "s7": "10111",
    "s8": "11000",
    "s9": "11001",
    "s10": "11010",
    "s11": "11011",
    "t3": "11100",
    "t4": "11101",
    "t5": "11110",
    "t6": "11111"
}

def binary_decimal(decimal_num, num_bits):
    range_bin = (2**num_bits)/2
    binary_str = ''
    if (decimal_num > range_bin-1 or decimal_num < -1*range_bin):
        return 'Out of range'
    elif decimal_num == 0:
        return '0' * num_bits
    elif decimal_num > 0:
        while decimal_num > 0:
            remainder = decimal_num % 2
            binary_str = str(remainder) + binary_str
            decimal_num //= 2
        binary_str = '0' + binary_str
        if len(binary_str) < num_bits:
            binary_str = binary_str[0] * (num_bits - len(binary_str)) + binary_str
        return binary_str
    elif decimal_num < 0:
        decimal_num = -1 * decimal_num
        while decimal_num > 0:
            remainder = decimal_num % 2
            binary_str = str(remainder) + binary_str
            decimal_num //= 2
        binary_str = '0' + binary_str
        if len(binary_str) < num_bits:
            binary_str = binary_str[0] * (num_bits - len(binary_str)) + binary_str
        return twos_complement(ones_complement(binary_str))
    else:
        binary_string = binary_decimal(decimal_num+1, num_bits)
        binary_string = binary_string[0:len(binary_string)-1]+"0"
        return binary_string

def ones_complement(binary_str):
    length_binary = len(binary_str)
    new_binary = ""
    for i in range(length_binary):
        if binary_str[i] == "0":
            new_binary += "1"
        elif binary_str[i] == "1":
            new_binary += "0"
    return new_binary

def twos_complement(ones_complement_str):
    if ones_complement_str[len(ones_complement_str) - 1] == "0":
        return ones_complement_str[0:len(ones_complement_str) - 1] + "1"
    else:
        len_ones_compl_str = len(ones_complement_str)
        add_str = ""
        for i in range(len_ones_compl_str-1, -1, -1):
            if (ones_complement_str[i] == "0"):
                return ones_complement_str[0:i] + "1" + add_str
            add_str += "0"

def is_binary_positive(binary_str):
    if binary_str[0] == '1':
        return False
    return True

def b_type_convert(instruction):
    operation, registers = instruction.split()
    rs1, rs2, imm = registers.split(",")
    imm = int(imm)
    imm_bin = binary_decimal(imm, 12)
    imm_bin=imm_bin[::-1]
    return imm_bin[11] + imm_bin[9:3:-1] + register_code[rs2] + register_code[rs1] + b_type_func3[operation] + imm_bin[3:0:-1] +imm_bin[0] + imm_bin[10] + "1100011"

i1 = "beq s0,s1,12"

print(b_type_convert(i1))

#0 000000 01001 01000 00001 1001 100011
#0 000000 01001 01000 00001 100011

#00000000100101000000011001100011
#00000000100101000000110001100011