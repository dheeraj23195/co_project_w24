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
    "r_type": "0110011",
    "lw": "0000011",
    "addi": "0010011",
    "sltiu": "0010011",
    "jalr": "1100111",
    "sw": "0100011",
    "beq": "1100011",
    "blt": "1100011",
    "auipc": "0010111",
    "jal": "1101111",
    "lui": "0110111"
}

# r-type-instructions data
r_type_instruction = ["add", "slt", "sltu", "xor", "sll", "srl", "or", "and", "sub"]
r_type_func3 = {"add": "000", "sub": "000", "sll": "001", "slt": "010", "sltu": "011", "xor": "100", "srl": "101", "or": "110", "and": "111"}

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

#bonus instructions
bonus_instruction = ["mul", "rst", "halt", "rvrs"]

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

def binary_to_assembly(binary_instruction):
    opcode = binary_instruction[-7:]
    if opcode == op_codes["r_type_instructions"]:
        funct7 = binary_instruction[:7]
        rs2 = binary_instruction[17:22]
        rs1 = binary_instruction[12:17]
        funct3 = binary_instruction[17:20]
        rd = binary_instruction[20:25]
        for instr, f3 in r_type_func3.items():
            if funct3 == f3:
                return f"{instr} x{int(rd, 2)}, x{int(rs1, 2)}, x{int(rs2, 2)}"
       # if funct7 == "0000000":
        #    instruction = list(r_type_func3.keys())[list(r_type_func3.values()).index(funct3)]
         #   return f"{instruction} x{int(rd, 2)}, x{int(rs1, 2)}, x{int(rs2, 2)}"
   # elif opcode == op_codes["lw"]:
     elif opcode in [op_codes["lw"], op_codes["sltiu"], op_codes["jalr"], op_codes["addi"]]:
        imm = binary_instruction[:12]
        rs1 = binary_instruction[12:17]
        funct3 = binary_instruction[17:20]
        rd = binary_instruction[20:25]
        #if opcode == i_type_opcodes["lw"]:
         #   instruction = "lw"
          #  return f"{instruction} x{int(rd, 2)}, {int(imm, 2)}(x{int(rs1, 2)})"
        if funct3 == "010" and opcode == op_codes["lw"]:
            return f"lw x{int(rd, 2)}, {int(imm, 2)}(x{int(rs1, 2)})"
        elif funct3 == "011" and opcode == op_codes["sltiu"]:
            return f"sltiu x{int(rd, 2)}, x{int(rs1, 2)}, {int(imm, 2)}"
        elif funct3 == "000" and opcode == op_codes["jalr"]:
            return f"jalr x{int(rd, 2)}, x{int(rs1, 2)}, {int(imm, 2)}"
    elif opcode == op_codes["sw"]:
        imm = binary_instruction[:7] + binary_instruction[20:25]
        rs2 = binary_instruction[12:17]
        rs1 = binary_instruction[17:22]
        funct3 = binary_instruction[17:20]
        if funct3 == s_type_func3["sw"]:
            return f"sw x{int(rs2, 2)}, {int(imm, 2)}(x{int(rs1, 2)})"
      #  if opcode == s_type_opcodes["sw"]:
       #     instruction = "sw"
        #    return f"{instruction} x{int(rs2, 2)}, {int(imm, 2)}(x{int(rs1, 2)})"
    elif opcode == op_codes["blt"]:
        imm = binary_instruction[:1] + binary_instruction[24:31] + binary_instruction[1:7] + binary_instruction[20:24]
        rs2 = binary_instruction[12:17]
        rs1 = binary_instruction[17:22]
        funct3 = binary_instruction[17:20]
        if funct3 == b_type_func3["blt"]:
            return f"blt x{int(rs1, 2)}, x{int(rs2, 2)}, {int(imm, 2)}"
        #if opcode == b_type_opcodes["blt"]:
         #   instruction = "blt"
          #  return f"{instruction} x{int(rs1, 2)}, x{int(rs2, 2)}, {int(imm, 2)}"
    elif opcode == op_codes["auipc"]:
        imm = binary_instruction[:20]
        rd = binary_instruction[20:25]
        return f"auipc x{int(rd, 2)}, {int(imm, 2)}"
        #if opcode == u_type_opcode["auipc"]:
         #   instruction = "auipc"
          #  return f"{instruction} x{int(rd, 2)}, {int(imm, 2)}"
    elif opcode == op_codes["jal"]:
        imm = binary_instruction[:1] + binary_instruction[12:20] + binary_instruction[11:12] + binary_instruction[1:11]
        rd = binary_instruction[20:25]
        return f"jal x{int(rd, 2)}, {int(imm, 2)}"
        #if opcode == j_type_opcode["jal"]:
         #   instruction = "jal"
          #  return f"{instruction} x{int(rd, 2)}, {int(imm, 2)}"
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

    return "Unknown instruction"
assembly_instruction = binary_to_assembly(binary_instruction)
print(assembly_instruction)
