class Simulator:
    def __init__(self):
        self.pc = 0
        self.registers = [0] * 32
        self.memory = [0] * (2 ** 10)
        self.instructions = []
    
    def load_program(self, program):
        self.instructions = program
    
    def fetch(self):
        instruction = self.instructions[self.pc]
        self.pc += 1
        return instruction
    
    def decode(self, instruction):
        opcode = instruction[:7]
        rd = int(instruction[7:12], 2)
        rs1 = int(instruction[12:17], 2)
        rs2 = int(instruction[17:22], 2)
        imm = int(instruction[20:], 2)
        return opcode, rd, rs1, rs2, imm
    
    def execute(self, opcode, rd, rs1, rs2, imm):
        if opcode == "0000000":  # LUI
            self.registers[rd] = imm << 12
        elif opcode == "0000000":  # AUIPC
            self.registers[rd] = self.pc + (imm << 12)
        elif opcode == "0000000":  # JAL
            self.registers[rd] = self.pc + 4
            self.pc += imm
        elif opcode == "0000000":  # JALR
            self.registers[rd] = self.pc + 4
            self.pc = self.registers[rs1] + imm
        elif opcode == "0000000":  # BEQ
            if self.registers[rs1] == self.registers[rs2]:
                self.pc += imm
        elif opcode == "0000000":  # BNE
            if self.registers[rs1] != self.registers[rs2]:
                self.pc += imm
        elif opcode == "0000000":  # BLT
            if self.registers[rs1] < self.registers[rs2]:
                self.pc += imm
        elif opcode == "0000000":  # BGE
            if self.registers[rs1] >= self.registers[rs2]:
                self.pc += imm
        elif opcode == "0000000":  # BLTU
            if self.registers[rs1] < self.registers[rs2]:
                self.pc += imm
        elif opcode == "0000000":  # BGEU
            if self.registers[rs1] >= self.registers[rs2]:
                self.pc += imm
        elif opcode == "0000000":  # LB
            address = self.registers[rs1] + imm
            self.registers[rd] = self.memory[address]
        elif opcode == "0000000":  # LH
            address = self.registers[rs1] + imm
            self.registers[rd] = (self.memory[address] << 8) | self.memory[address + 1]
        elif opcode == "0000000":  # LW
            address = self.registers[rs1] + imm
            self.registers[rd] = (self.memory[address] << 24) | (self.memory[address + 1] << 16) | (self.memory[address + 2] << 8) | self.memory[address + 3]
        elif opcode == "0000000":  # LBU
            address = self.registers[rs1] + imm
            self.registers[rd] = self.memory[address]
        elif opcode == "0000000":  # LHU
            address = self.registers[rs1] + imm
            self.registers[rd] = (self.memory[address] << 8) | self.memory[address + 1]
        elif opcode == "0000000":  # SB
            address = self.registers[rs1] + imm
            self.memory[address] = self.registers[rs2] & 0xFF
        elif opcode == "0000000":  # SH
            address = self.registers[rs1] + imm
            self.memory[address] = (self.registers[rs2] >> 8) & 0xFF
            self.memory[address + 1] = self.registers[rs2] & 0xFF
        elif opcode == "0000000":  # SW
            address = self.registers[rs1] + imm
            self.memory[address] = (self.registers[rs2] >> 24) & 0xFF
            self.memory[address + 1] = (self.registers[rs2] >> 16) & 0xFF
            self.memory[address + 2] = (self.registers[rs2] >> 8) & 0xFF
            self.memory[address + 3] = self.registers[rs2] & 0xFF
        elif opcode == "0000000":  # ADDI
            self.registers[rd] = self.registers[rs1] + imm
        elif opcode == "0000000":  # SLTI
            self.registers[rd] = 1 if self.registers[rs1] < imm else 0
        elif opcode == "0000000":  # SLTIU
            self.registers[rd] = 1 if self.registers[rs1] < imm else 0
        elif opcode == "0000000":  # XORI
            self.registers[rd] = self.registers[rs1] ^ imm
        elif opcode == "0000000":  # ORI
            self.registers[rd] = self.registers[rs1] | imm
        elif opcode == "0000000":  # ANDI
            self.registers[rd] = self.registers[rs1] & imm
        elif opcode == "0000000":  # SLLI
            self.registers[rd] = self.registers[rs1] << imm
        elif opcode == "0000000":  # SRLI
            self.registers[rd] = self.registers[rs1] >> imm
        elif opcode == "0000000":  # SRAI
            self.registers[rd] = self.registers[rs1] >> imm
        elif opcode == "0000000":  # ADD
            self.registers[rd] = self.registers[rs1] + self.registers[rs2]
        elif opcode == "0000000":  # SUB
            self.registers[rd] = self.registers[rs1] - self.registers[rs2]
        elif opcode == "0000000":  # SLL
            self.registers[rd] = self.registers[rs1] << self.registers[rs2]
        elif opcode == "0000000":  # SLT
            self.registers[rd] = 1 if self.registers[rs1] < self.registers[rs2] else 0
        elif opcode == "0000000":  # SLTU
            self.registers[rd] = 1 if self.registers[rs1] < self.registers[rs2] else 0
        elif opcode == "0000000":  # XOR
            self.registers[rd] = self.registers[rs1] ^ self.registers[rs2]
        elif opcode == "0000000":  # SRL
            self.registers[rd] = self.registers[rs1] >> self.registers[rs2]
        elif opcode == "0000000":  # SRA
            self.registers[rd] = self.registers[rs1] >> self.registers[rs2]
        elif opcode == "0000000":  # OR
            self.registers[rd] = self.registers[rs1] | self.registers[rs2]
        elif opcode == "0000000":  # AND
            self.registers[rd] = self.registers[rs1] & self.registers[rs2]

    def run(self):
        while self.pc < len(self.instructions):
            instruction = self.fetch()
            opcode, rd, rs1, rs2, imm = self.decode(instruction)
            self.execute(opcode, rd, rs1, rs2, imm)
        self.print_state()

    def print_state(self):
        print("Program Counter:", self.pc)
        print("Registers:")
        for i in range(len(self.registers)):
            print(f"x{i}: {self.registers[i]}")

simulator = Simulator()

# Load the program into the simulator's memory
program = [
    "00000000001000000000000010011011",  # LUI x1, 10
    "00000000010000000000000010011011",  # LUI x2, 20
    "00000000000000100001000110110011"   # ADD x3, x1, x2
]

simulator.load_program(program)

# Run the program
simulator.run()