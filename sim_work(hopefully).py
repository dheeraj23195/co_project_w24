def unsigned(value):
    # Check if the value is less than 0
    if value < 0:
        # Return the equivalent positive value for unsigned comparison
        return 2**32 + value
    else:
        return value


def signed_binary_to_int(signed_binary_str):
    # Check if the most significant bit is 1 (indicating a negative number)
    if signed_binary_str[0] == '1':
        # Calculate the two's complement value for negative numbers
        twos_complement = ''.join('1' if bit == '0' else '0' for bit in signed_binary_str[1:])
        # Convert the two's complement to an integer and negate it
        return -(int(twos_complement, 2) + 1)
    else:
        # If the most significant bit is 0, convert the binary string to an integer
        return int(signed_binary_str, 2)

opcode = {
    "0110011": "R",
    "0000011": "I", "0010011": "I", "0010011": "I", "1100111": "I",
    "0100011": "S",
    "1100011": "B",
    "0110111": "U", "0010111": "B",
    "1101111": "J"
}

dict = {
    'zero': 0,
    'ra': 0,
    'sp': 256,
    'gp': 0,
    'tp': 0,
    't0': 0,
    't1': 0,
    't2': 0,
    's0': 0,
    's1': 0,
    'a0': 0,
    'a1': 0,
    'a2': 0,
    'a3': 0,
    'a4': 0,
    'a5': 0,
    'a6': 0,
    'a7': 0,
    's2': 0,
    's3': 0,
    's4': 0,
    's5': 0,
    's6': 0,
    's7': 0,
    's8': 0,
    's9': 0,
    's10': 0,
    's11': 0,
    't3': 0,
    't4': 0,
    't5': 0,
    't6': 0
}

registers = {'00000': 'zero',
             '00001': 'ra',
             '00010': 'sp',
             '00011': 'gp',
             '00100': 'tp',
             '00101': 't0',
             '00110': 't1',
             '00111': 't2',
             '01000': 's0',
             '01001': 's1',
             '01010': 'a0',
             '01011': 'a1',
             '01100': 'a2',
             '01101': 'a3',
             '01110': 'a4',
             '01111': 'a5',
             '10000': 'a6',
             '10001': 'a7',
             '10010': 's2',
             '10011': 's3',
             '10100': 's4',
             '10101': 's5',
             '10110': 's6',
             '10111': 's7',
             '11000': 's8',
             '11001': 's9',
             '11010': 's10',
             '11011': 's11',
             '11100': 't3',
             '11101': 't4',
             '11110': 't5',
             '11111': 't6'}

def b_type(instruction):
    global dict
    global PC
    immediate = instruction[0] + instruction[24] + instruction[1:7] + instruction[20:24] + '0'
    rs2 = instruction[7:12]
    rs1 = instruction[12:17]
    func3 = instruction[17:20]
    opcode = instruction[25:]

    if func3 == "000":
        if registers[rs1] == 'zero' and registers[rs2] == 'zero' and signed_binary_to_int(immediate) == 0:
            print("0b"+decimal_binary_32bits(PC)+" ")
            for i in list(dict.keys()):
                print("0b"+decimal_binary_32bits(dict[i])+" ")
            return PC
        else:
            if dict[registers[rs1]] == dict[registers[rs2]]:
                PC += signed_binary_to_int(immediate)
            else:
                PC += 4
    elif func3 == "001":
        if dict[registers[rs1]] != dict[registers[rs2]]:
            PC += signed_binary_to_int(immediate)
        else:
            PC += 4
    elif func3 == "100":
        if dict[registers[rs1]] < dict[registers[rs2]]:
            PC += signed_binary_to_int(immediate)
        else:
            PC += 4
    elif func3 == "101":
        if dict[registers[rs1]] > dict[registers[rs2]]:
            PC += signed_binary_to_int(immediate)
        else:
            PC += 4
    elif func3 == "110":
        if dict[registers[rs1]] < dict[registers[rs2]]:
            PC += signed_binary_to_int(immediate)
        else:
            PC += 4
    elif func3 == "111":
        if dict[registers[rs1]] > dict[registers[rs2]]:
            PC += signed_binary_to_int(immediate)
        else:
            PC += 4

    print("0b"+decimal_binary_32bits(PC)+" ")
    for i in list(dict.keys()):
        print("0b"+decimal_binary_32bits(dict[i])+" ")
    return PC


def s_type(instruction):
    global dict, data_memory, PC

    opcode_value = instruction[25:]
    imm = instruction[0:7] + instruction[20:25]
    imm_value = signed_binary_to_int(imm)

    rs2 = registers[instruction[7:12]]
    rs1 = registers[instruction[12:17]]

    if opcode_value == '0100011':
        offset = dict[rs1] + imm_value
        data_memory[offset] = dict[rs2]

    PC += 4

    print("0b"+decimal_binary_32bits(PC)+" ")
    for i in list(dict.keys()):
        print("0b"+decimal_binary_32bits(dict[i])+" ")

    return PC


def j_type(instruction):
    global dict, PC
    rd = instruction[20:25]
    imm = instruction[0] + instruction[12:20] + instruction[11] + instruction[1:11] + '0'
    imm_value = signed_binary_to_int(imm)
    dict[registers[rd]] = int(PC) + 4

    PC += imm_value

    print("0b"+decimal_binary_32bits(PC)+" ")
    for i in list(dict.keys()):
        print("0b"+decimal_binary_32bits(dict[i])+" ")
    return PC


def u_type(instruction):
    global dict, pc
    imm = instruction[0:20]
    imm_value = signed_binary_to_int(imm)
    opcode = instruction[25:]
    rd = instruction[20:25]

    if opcode == "0110111":
        result = imm_value
    elif opcode == "0010111":
        result = int(pc) + imm_value

    dict[registers[rd]] = (result)
    pc += 4

    print("0b"+decimal_binary_32bits(pc))
    for i in list(dict.keys()):
        print("0b"+decimal_binary_32bits(dict[i]))
    return pc


def r_type(instruction):
    global dict_registers, PC
    func3 = instruction[17:20]
    func7 = instruction[0:7]
    rd = registers[instruction[20:25]]
    rs1 = registers[instruction[12:17]]
    rs2 = registers[instruction[7:12]]

    if func3 == '000' and func7 == '0000000':
        dict[rd] = dict[rs1] + dict[rs2]

    elif func3 == '000' and func7 == '0100000' and rs1 == "00000":
        dict[rd] = 0 - dict[rs2]  # Two’s complement

    elif func3 == '000' and func7 == '0100000':
        dict[rd] = dict[rs1] - dict[rs2]  # signed(rs1) - signed(rs2)

    elif func3 == '001' and func7 == '0000000':
        if dict[rs1] < dict[rs2]:
            dict[rd] = 1
        else:
            dict[rd] = 0

    elif func3 == '010' and func7 == '0000000':
        if (dict[rs1]) < (dict[rs2]):
            dict[rd] = 1
        else:
            dict[rd] = 0

    elif func3 == '100' and func7 == '0000000':
        dict[rd] = int(dict[rs1]) ^ int(dict[rs2])  # Bitwise Exor

    elif func3 == '101' and func7 == '0000000':
        shift_count = (dict[rs2][0:5])
        # Ensure shift count is non-negative
        shift_count = max(shift_count, 0)
        dict[rd] = dict[rs1] << shift_count  # Left shift rs1 by the non-negative value in lower 5 bits of rs2

    elif func3 == '101' and func7 == '0100000':
        shift_count = (dict[rs2][0:5])
        # Ensure shift count is non-negative
        shift_count = max(shift_count, 0)
        dict[rd] = dict[rs1] >> shift_count  # Right shift rs1 by the non-negative value in lower 5 bits of rs2

    elif func3 == '110' and func7 == '0000000':
        dict[rd] = int(dict[rs1]) | int(dict[rs2])  # Bitwise logical or.

    elif func3 == '111' and func7 == '0000000':
        dict[rd] = int(dict[rs1]) & int(dict[rs2])  # Bitwise logical and.

    PC += 4

def i_type(instruction):
    global dict, data_memory, PC

    opcode_value = instruction[25:]
    imm = instruction[0:12]
    imm_value = signed_binary_to_int(imm)

    rd = registers[instruction[20:25]]
    rs1 = registers[instruction[12:17]]

    if opcode_value == '0000011':
        offset = dict[rs1] + imm_value
        dict[rd] = data_memory[offset]

    elif opcode_value == '0010011':
        dict[rd] = dict[rs1] + imm_value

    elif opcode_value == '1100111':
        dict[rd] = PC + 4
        PC = (dict['t1'] + imm_value) & 0xFFFFFFFE

    PC += 4

def complement(binarynumber):
    ans = ""
    while binarynumber and binarynumber[-1] != "1":
        ans = binarynumber[-1] + ans
        binarynumber = binarynumber[0:-1]
    ans = binarynumber[-1] + ans
    binarynumber = binarynumber[0:-1]

    while binarynumber:
        if binarynumber[-1] == "0":
            ans = "1" + ans
        elif binarynumber[-1] == "1":
            ans = "0" + ans
        binarynumber = binarynumber[0:-1]
    return ans

def decimal_binary_32bits(b):
    a = int(b)
    if a > 0:
        ans = ""
        cnt = 0
        while a != 0:
            ans = str(a % 2) + ans
            a = a // 2
            cnt += 1
        ans = "0" * (32 - cnt) + ans
        return ans
    elif a == 0:
        answer = 32 * "0"
        return answer
    elif a < 0:
        a = abs(a)
        ans = ""
        cnt = 0
        while a != 0:
            ans = str(a % 2) + ans
            a = a // 2
            cnt += 1
        ans = "1" * (32 - cnt) + ans
        ans = complement(ans)
    return ans

l1=[]
l2=[]
dict1={}
with open(r'C:\Users\HP\OneDrive\Desktop\c++\project_co\co_simulator\text.txt',"r") as f:
    data=f.readlines()
    for lines in data:
        l1.append(lines.strip())
        lines=(lines.strip())
        dict1[l1.index(lines)*4]=lines
        lines=int(lines)
        l2.append(f'0x{lines:0>8X}')

program_memory = {}
stack_memory = {}
data_memory = {}

for i in range(32):
    address = f'0x{int(256 + i * 4):04X}'  # Stack memory starts at address 0x0000 0100
    stack_memory[address] = '0x00000000'  # Initialize stack memory locations to zeros

for i in range(32):
    address = f'0x{int(0x00100000 + i * 4):08X}'  # Data memory starts at address 0x001 0000
    data_memory[address] = '0x00000000'  # Initialize data memory locations to zeros

PC = 0

while PC <= (len(l1) - 1) * 4:
    instruction = dict1[PC]
    print(instruction)
    opcode_value = instruction[0:7]
    print(opcode_value)
    if opcode[opcode_value] == "R":
        r_type(instruction)
    elif opcode[opcode_value] == "I":
        i_type(instruction)
    elif opcode[opcode_value] == "S":
        s_type(instruction)
    elif opcode[opcode_value] == "B":
        b_type(instruction)
    elif opcode[opcode_value] == "U" or opcode[opcode_value] == "J":
        u_type(instruction)