import sys

# Program memory size and ranges
memory_size_program = 4096
memory_range_program = range(0, memory_size_program)

# Stack memory size and ranges
memory_size_stack = 128
memory_range_stack = range(4096, 4096 + memory_size_stack)

# Data memory size and ranges
memory_size_data = 128
memory_range_data = range(8192, 8192 + memory_size_data)

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
register_code = {
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
    binary_str = bin(decimal_num & int("1"*num_bits, 2))[2:]
    return binary_str.zfill(num_bits)

def ones_complement(binary_str):
    return ''.join('1' if bit == '0' else '0' for bit in binary_str)

def twos_complement(binary_str):
    binary_str = ones_complement(binary_str)
    return bin(int(binary_str, 2) + 1)[2:]

def r_type_convert(instruction):
    operation, registers = instruction.split()
    rd, rs1, rs2 = registers.split(",")
    if operation == "sub":
        return "0100000" + register_code[rs2] + register_code[rs1] + "000" + register_code[rd] + op_codes["r_type_instructions"]
    return ("0000000" + register_code[rs2] + register_code[rs1] + r_type_func3[operation] + register_code[rd] + op_codes["r_type_instructions"])

def b_type_convert(instruction):
    operation, registers = instruction.split()
    rs1, rs2, imm = registers.split(",")
    imm = int(imm)
    offset = imm - 4  # Adjust offset for bytes, subtracting 4 because PC has already moved past this instruction
    imm_bin = binary_decimal(offset, 12)
    return imm_bin[11] + imm_bin[1:11] + register_code[rs2] + register_code[rs1] + b_type_func3[operation] + imm_bin[0] + imm_bin[12:][::-1] + "1100011"

def u_type_convert(instruction):
    operation, registers = instruction.split()
    rd, imm = registers.split(",")
    imm = binary_decimal(int(imm), 20)
    imm = imm[::-1]
    return imm + register_code[rd] + u_type_opcode[operation]

def j_type_convert(instruction):
    operation, registers = instruction.split()
    rd, imm = registers.split(",")
    imm = binary_decimal(int(imm), 20)
    return (imm[19] + imm[9:0:-1] + imm[0] + imm[10] + imm[18:10:-1] + register_code[rd] + "1101111")

def i_type_convert(instruction):
    op, registers = instruction.split()
    if op == 'lw':
        rd, temp = registers.split(",")
        imm, rstemp = temp.split("(")
        rs1 = rstemp[0:len(rstemp)-1]
    elif op == 'addi' or op == 'sltiu':
        rd, rs1, imm = registers.split(",")
    else:
        rd, rs1, imm = registers.split(",")
    imm = binary_decimal(int(imm), 12)
    return imm + register_code[rs1] + i_type_func3[op] + register_code[rd] + i_type_opcodes[op]

def s_type_convert(instruction):
    op, registers = instruction.split()
    rs2, temp = registers.split(",")
    imm, rstemp = temp.split("(")
    rs1 = rstemp[0:len(rstemp)-1]
    imm = binary_decimal(int(imm), 12)
    return imm[11:4:-1] + register_code[rs2] + register_code[rs1] + "010" + imm[4:0:-1] + imm[0] + "0100011"

def assemble(instruction):
    op, temp = instruction.split(maxsplit=1)
    if ':' in op:  # Label definition
        return None
    if op in r_type_instruction:
        return r_type_convert(instruction)
    elif op in i_type_instruction:
        return i_type_convert(instruction)
    elif op in s_type_instruction:
        return s_type_convert(instruction)
    elif op in b_type_instruction:
        return b_type_convert(instruction)
    elif op in u_type_instruction:
        return u_type_convert(instruction)
    elif op in j_type_instruction:
        return j_type_convert(instruction)
    else:
        print(f"Error: Unknown instruction '{op}'")
        return None

def assemble_code(assembly_code):
    program_memory = {}
    current_address = 0

    for line_number, line in enumerate(assembly_code):
        line = line.strip()
        if not line or line.startswith("#"):  # Ignore empty lines and comments
            continue
        if ':' in line:
            label, instruction = line.split(':')
            instruction = instruction.strip()
            if label.strip() in program_memory:
                print(f"Error: Duplicate label '{label.strip()}' at line {line_number + 1}")
                return None
            program_memory[label.strip()] = current_address
            line = instruction
        binary_instruction = assemble(line)
        if binary_instruction is None:
            print(f"Error: Invalid instruction at line {line_number + 1}")
            return None
        program_memory[current_address] = binary_instruction
        current_address += 4

    if current_address % memory_size_program != 0:
        virtual_halt_address = current_address
        while virtual_halt_address % memory_size_program != 0:
            virtual_halt_address += 4
        program_memory[virtual_halt_address] = '00000000000000000000000000000000'

    if current_address == 0:
        print("Error: No instructions found")
        return None

    return program_memory

def main():
    if len(sys.argv) < 3:
        print("Usage: python assembler.py <assembly_file> <output_file>")
        return

    assembly_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        with open(assembly_file, 'r') as f:
            assembly_code = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{assembly_file}' not found")
        return

    program_memory = assemble_code(assembly_code)
    if program_memory is not None:
        with open(output_file, 'w') as f:
            for address in sorted(program_memory.keys()):
                if address in memory_range_program:  # Check if the address is within the program memory range
                    instruction = program_memory[address]
                    f.write(instruction + '\n')

if __name__ == "__main__":
    main()