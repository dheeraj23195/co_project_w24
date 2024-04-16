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
    "jal": "1101111"
}

# r-type-instructions data
r_type_instruction = ["add", "sub", "slt", "sltu", "xor", "sll", "srl", "or", "and"]
r_type_func3 = {"add": "000", "sub": "000", "slt": "010", "sltu": "011", "xor": "100", "sll": "001", "srl": "101",
                "or": "110", "and": "111"}

# i-type-instructions data
i_type_instruction = ["lw", "addi", "sltiu", "jalr"]
i_type_opcodes = {"lw": "0000011", "addi": "0010011", "sltiu": "0010011", "jalr": "1100111"}
i_type_func3 = {"lw": "010", "addi": "000", "sltiu": "011", "jalr": "000"}

# s-type-instructions data
s_type_instruction = ["sw"]
s_type_func3 = {"sw": "010"}

# b-type-instructions data
b_type_instruction = ["beq", "bne", "blt", "bge", "bltu", "bgeu"]
b_type_func3 = {"beq": "000", "bne": "001", "blt": "100", "bge": "101", "bltu": "110", "bgeu": "111"}

# u-type-instructions data
u_type_instruction = ["lui", "auipc"]
u_type_opcode = {"lui": "0110111", "auipc": "0010111"}

# j-type-instructions data
j_type_instruction = ["jal"]
j_type_opcode = {"jal": "1101111"}

# bonus instructions
bonus_instruction = ["mul", "rst", "halt", "rvrs"]

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

# Register file
registers = [0] * 32

# Program Counter
pc = 0

# Memory
memory = [0] * (memory_size_program + memory_size_stack + memory_size_data)

def binary_to_assembly(binary_instruction):
    opcode = binary_instruction[-7:]
    if opcode == op_codes["r_type_instructions"]:
        funct7 = binary_instruction[:7]
        rs2 = binary_instruction[12:17]
        rs1 = binary_instruction[17:22]
        funct3 = binary_instruction[17:20]
        rd = binary_instruction[20:25]
        if funct7 == "0000000":
            instruction = list(r_type_func3.keys())[list(r_type_func3.values()).index(funct3)]
            return f"{instruction} x{int(rd, 2)}, x{int(rs1, 2)}, x{int(rs2, 2)}"
    elif opcode == op_codes["lw"]:
        imm = binary_instruction[:12]
        rs1 = binary_instruction[12:17]
        funct3 = binary_instruction[17:20]
        rd = binary_instruction[20:25]
        if opcode == i_type_opcodes["lw"]:
            instruction = "lw"
            return f"{instruction} x{int(rd, 2)}, {int(imm, 2)}(x{int(rs1, 2)})"
    elif opcode == op_codes["sltiu"]:
        imm = binary_instruction[:12]
        rs1 = binary_instruction[12:17]
        funct3 = binary_instruction[17:20]
        rd = binary_instruction[20:25]
        if opcode == i_type_opcodes["sltiu"]:
            instruction = "sltiu"
            return f"{instruction} x{int(rd, 2)}, x{int(rs1, 2)}, {int(imm, 2)}"
    elif opcode == op_codes["jalr"]:
        imm = binary_instruction[:12]
        rs1 = binary_instruction[12:17]
        funct3 = binary_instruction[17:20]
        rd = binary_instruction[20:25]
        if opcode == i_type_opcodes["jalr"]:
            instruction = "jalr"
            return f"{instruction} x{int(rd, 2)}, {int(imm, 2)}(x{int(rs1, 2)})"
    elif opcode == op_codes["sw"]:
        imm = binary_instruction[:7] + binary_instruction[20:25]
        rs2 = binary_instruction[7:12]
        rs1 = binary_instruction[12:17]
        funct3 = binary_instruction[17:20]
        if opcode == "0100011":
            instruction = "sw"
            return f"{instruction} x{int(rs2, 2)}, {int(imm, 2)}(x{int(rs1, 2)})"
    elif opcode == op_codes["blt"]:
        imm = binary_instruction[:1] + binary_instruction[24:31] + binary_instruction[1:7] + binary_instruction[20:24]
        rs2 = binary_instruction[7:12]
        rs1 = binary_instruction[12:17]
        funct3 = binary_instruction[17:20]
        if opcode == "1100011":
            instruction = "blt"
            return f"{instruction} x{int(rs1, 2)}, x{int(rs2, 2)}, {int(imm, 2)}"
    elif opcode == op_codes["auipc"]:
        imm = binary_instruction[:20]
        rd = binary_instruction[20:25]
        if opcode == u_type_opcode["auipc"]:
            instruction = "auipc"
            return f"{instruction} x{int(rd, 2)}, {int(imm, 2)}"
    elif opcode == op_codes["jal"]:
        imm = binary_instruction[:1] + binary_instruction[12:20] + binary_instruction[11:12] + binary_instruction[1:11]
        rd = binary_instruction[20:25]
        if opcode == j_type_opcode["jal"]:
            instruction = "jal"
            return f"{instruction} x{int(rd, 2)}, {int(imm, 2)}"

    return "Unknown instruction"

def execute_instruction(binary_instruction):
    opcode = binary_instruction[-7:]
    if opcode == op_codes["r_type_instructions"]:
        funct7 = binary_instruction[:7]
        rs2 = int(binary_instruction[12:17], 2)
        rs1 = int(binary_instruction[17:22], 2)
        funct3 = binary_instruction[17:20]
        rd = int(binary_instruction[20:25], 2)
        if funct7 == "0000000":
            instruction = list(r_type_func3.keys())[list(r_type_func3.values()).index(funct3)]
            if instruction == "add":
                registers[rd] = (registers[rs1] + registers[rs2]) & 0xFFFFFFFF
            elif instruction == "sub":
                registers[rd] = (registers[rs1] - registers[rs2]) & 0xFFFFFFFF
            elif instruction == "slt":
                registers[rd] = 1 if (registers[rs1] < registers[rs2]) else 0
            elif instruction == "sltu":
                registers[rd] = 1 if (registers[rs1] < registers[rs2]) else 0
            elif instruction == "xor":
                registers[rd] = (registers[rs1] ^ registers[rs2]) & 0xFFFFFFFF
            elif instruction == "sll":
                shift_amount = registers[rs2] & 0x1F
                registers[rd] = (registers[rs1] << shift_amount) & 0xFFFFFFFF
            elif instruction == "srl":
                shift_amount = registers[rs2] & 0x1F
                registers[rd] = (registers[rs1] >> shift_amount) & 0xFFFFFFFF
            elif instruction == "or":
                registers[rd] = (registers[rs1] | registers[rs2]) & 0xFFFFFFFF
            elif instruction == "and":
                registers[rd] = (registers[rs1] & registers[rs2]) & 0xFFFFFFFF
    elif opcode == op_codes["lw"]:
        imm = int(binary_instruction[:12], 2)
        rs1 = int(binary_instruction[12:17], 2)
        funct3 = binary_instruction[17:20]
        rd = int(binary_instruction[20:25], 2)
        address = (registers[rs1] + imm) & 0xFFFFFFFF
        if address in memory_range_data:
            registers[rd] = memory[address]
    elif opcode == op_codes["sltiu"]:
        imm = int(binary_instruction[:12], 2)
        rs1 = int(binary_instruction[12:17], 2)
        funct3 = binary_instruction[17:20]
        rd = int(binary_instruction[20:25], 2)
        registers[rd] = 1 if (registers[rs1] < imm) else 0
    elif opcode == op_codes["jalr"]:
        imm = int(binary_instruction[:12], 2)
        rs1 = int(binary_instruction[12:17], 2)
        funct3 = binary_instruction[17:20]
        rd = int(binary_instruction[20:25], 2)
        registers[rd] = (pc + 4) & 0xFFFFFFFF
        pc_new = (registers[rs1] + imm) & 0xFFFFFFFF
        pc_new &= 0xFFFFFFFE  # Ensure LSB is 0
        global pc
        pc = pc_new
    elif opcode == op_codes["sw"]:
        imm = int(binary_instruction[:7] + binary_instruction[20:25], 2)
        rs2 = int(binary_instruction[7:12], 2)
        rs1 = int(binary_instruction[12:17], 2)
        funct3 = binary_instruction[17:20]
        address = (registers[rs1] + imm) & 0xFFFFFFFF
        if address in memory_range_data:
            memory[address] = registers[rs2]
    elif opcode == op_codes["blt"]:
        imm = int(binary_instruction[:1] + binary_instruction[24:31] + binary_instruction[1:7] + binary_instruction[20:24] + "0", 2)
        rs2 = int(binary_instruction[7:12], 2)
        rs1 = int(binary_instruction[12:17], 2)
        funct3 = binary_instruction[17:20]
        if (registers[rs1] < registers[rs2]):
            global pc
            pc = (pc + imm) & 0xFFFFFFFF
    elif opcode == op_codes["auipc"]:
        imm = int(binary_instruction[:20] + "000000000000", 2)
        rd = int(binary_instruction[20:25], 2)
        registers[rd] = (pc + imm) & 0xFFFFFFFF
    elif opcode == op_codes["jal"]:
        imm = int(binary_instruction[:1] + binary_instruction[12:20] + binary_instruction[11:12] + binary_instruction[1:11] + "0", 2)
        rd = int(binary_instruction[20:25], 2)
        registers[rd] = (pc + 4) & 0xFFFFFFFF
        global pc
        pc = (pc + imm) & 0xFFFFFFFF
    else:
        print(f"Unknown instruction: {binary_instruction}")

def run_simulation(input_file, output_file):
    with open(input_file, "r") as file:
        binary_instructions = [line.strip() for line in file]

    with open(output_file, "w") as file:
        global pc
        pc = 0
        for binary_instruction in binary_instructions:
            # Print register state
            file.write(" ".join(f"{reg:08b}" for reg in registers) + "\n")

            # Execute instruction
            execute_instruction(binary_instruction)

            # Update PC
            pc += 4

        # Print final memory state
        for i in range(0, len(memory), 1):
            file.write(f"{0x00010000 + i * 4:08x}:{memory[i]:08b}\n")

def main():
    if len(sys.argv) != 3:
        print("Usage: python <filename>.py <inputname>.txt <outputname>.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    run_simulation(input_file, output_file)

if __name__ == "_main_":
    main()