def unsigned(value):
    # Check if the value is less than 0
    if value < 0:
        # Return the equivalent positive value for unsigned comparison
        return 2**32 + value
    else:
        return value

def sext(value):
    # Calculate the number of bits needed for sign extension
    num_bits = value.bit_length()

    # Sign-extend the value to 32 bits based on the calculated number of bits
    sign_bit = value & (1 << (num_bits - 1))
    mask = (1 << num_bits) - 1
    extension_bits = 32 - num_bits
    sign_extended_value = value & mask  # Extract the value's bits within the specified range
    sign_extended_value |= -(sign_bit << extension_bits)  # Apply sign extension
    return sign_extended_value

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



opcode={"0110011":"R",
        "0000011":"I","0010011":"I","0010011":"I","1100111":"I",
        "0100011":"S",
        "1100011":"B",
        "0110111":"U","0010111":"B",
        "1101111":"J"}

dict = {
    'zero': 0,
    'ra': 0,
    'sp': 0,
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


registers={'00000': 'zero',
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

program_memory = {}
stack_memory = {}
data_memory = {}


for i in range(64):
    address = f'0x{int(i):04X}'
    program_memory[address] = f'0x{l1[i]}'  # Assuming l1 contains instruction in hexadecimal format

for i in range(32):
    address = f'0x{int(256 + i * 4):04X}'  # Stack memory starts at address 0x0000 0100
    stack_memory[address] = '0x00000000'  # Initialize stack memory locations to zeros


for i in range(32):
    address = f'0x{int(0x00100000 + i * 4):08X}'  # Data memory starts at address 0x001 0000
    data_memory[address] = '0x00000000'  # Initialize data memory locations to zeros


print("Program Memory:")
for address, instruction in program_memory.items():
    print(f'{address}: {instruction}')

print("\nStack Memory:")
for address, value in stack_memory.items():
    print(f'{address}: {value}')

print("\nData Memory:")
for address, value in data_memory.items():
    print(f'{address}: {value}')

registers['zero'] = registers['x0']  # Hard-wired zero
registers['ra'] = registers['x1']    # Return address
registers['sp'] = registers['x2']    # Stack Pointer
registers['gp'] = registers['x3']    # Global Pointer
registers['tp'] = registers['x4']    # Thread Pointer
registers['t0'] = registers['x5']    # Temporary/alternate link register
registers['t1'] = registers['x6']    # Temporary register
registers['t2'] = registers['x7']    # Temporary register
registers['s0'] = registers['x8']    # Saved register/frame pointer
registers['s1'] = registers['x9']    # Saved Register
registers['a0'] = registers['x10']   # Function argument/return value
registers['a1'] = registers['x11']   # Function argument/return value
registers['a2'] = registers['x12']   # Function argument
registers['a3'] = registers['x13']   # Function argument
registers['a4'] = registers['x14']   # Function argument
registers['a5'] = registers['x15']   # Function argument
registers['a6'] = registers['x16']   # Function argument
registers['a7'] = registers['x17']   # Function argument
registers['s2'] = registers['x18']   # Saved register
registers['s3'] = registers['x19']   # Saved register
registers['s4'] = registers['x20']   # Saved register
registers['s5'] = registers['x21']   # Saved register
registers['s6'] = registers['x22']   # Saved register
registers['s7'] = registers['x23']   # Saved register
registers['s8'] = registers['x24']   # Saved register
registers['s9'] = registers['x25']   # Saved register
registers['s10'] = registers['x26']  # Saved register
registers['s11'] = registers['x27']  # Saved register
registers['t3'] = registers['x28']   # Temporary register
registers['t4'] = registers['x29']   # Temporary register
registers['t5'] = registers['x30']   # Temporary register
registers['t6'] = registers['x31']   # Temporary register



def func_B(instruction):
    global dict
    global PC
    immediate=instruction[0]*20+instruction[24]+instruction[1:7]+instruction[20:24]+'0'
    rs2=instruction[7:12]
    rs1=instruction[12:17]
    func3=instruction[17:20]
    opcode=instruction[25:]

    if(func3=="000"):
        if(dict[rs1]==dict[rs2]):
            PC+=  sext(immediate)
        else:
            PC+=4

    elif(func3=="001"):
        if(dict[rs1]!=dict[rs2]):
            PC+=  sext(immediate)
        else:
            PC+=4

    elif(func3=="100"):
        if(dict[rs1]<dict[rs2]):
            PC+=  sext(immediate)
        else:
            PC+=4

    elif(func3=="101"):
        if(dict[rs1]>dict[rs2]):
            PC+=  sext(immediate)
        else:
            PC+=4

    elif(func3=="110"):
        if(dict[rs1]<dict[rs2]):
            PC+=  sext(immediate)
        else:
            PC+=4

    elif(func3=="111"):
        if(dict[rs1]>dict[rs2]):
            PC+=  sext(immediate)
        else:
            PC+=4
    pc+=4
    #print program counter
    print("0b"+decimal_binary_32bits(pc)+" ")
    for i in list(dict.keys()):
      print("0b"+decimal_binary_32bits(dict[i])+" ")
    return PC


def s_type(instruction):
    global dict, data_memory, PC

    imm = instruction[0:7] + instruction  # Immediate value, 7 bits
    imm_value = signed_binary_to_int(imm)

    rs2 = registers[instruction[7:12]]  # Source register 2
    rs1 = registers[instruction[12:17]]  # Source register 1

    funct3 = instruction[17:20]  # Funct3 code, 3 bits

    offset = imm_value + dict[rs1]  # Calculate offset as imm + value in rs1
    data_memory[offset] = dict[rs2]  # Store rs2 value at calculated memory address

    PC += 4  # Increment program counter by 4 for next instruction

    # Print updated program counter and data memory
    print("PC:", PC)
    print("Data Memory:")
    for address, value in data_memory.items():
        print(f'{hex(address)}: {value}')

    return PC

def j_type(instruction):
    global dict, PC
    imm = instruction[0:20]


    imm_value = signed_binary_to_int(imm)


    if imm[7] == '1':
        imm_value -= 1 << 20


    target_address = int(PC) + imm_value


    target_register = instruction[20:25]
    dict[target_register] = int(PC) + 4
    pc+=4
    #print program counter
    print("0b"+decimal_binary_32bits(pc)+" ")
    for i in list(dict.keys()):
      print("0b"+decimal_binary_32bits(dict[i])+" ")
    return PC


def u_type(instruction):
    global dict, PC
    imm = instruction[0:20]


    imm_value = int(imm, 2)


    opcode = instruction[25:]
    rd = instruction[20:25]

    if opcode == "0110111":
        result = imm_value
    elif opcode == "0010111":
        result = int(PC) + imm_value
        rd = instruction[20:25]


    dict[rd] = str(result)
    pc+=4
    #print program counter
    print("0b"+decimal_binary_32bits(pc)+" ")
    for i in list(dict.keys()):
      print("0b"+decimal_binary_32bits(dict[i])+" ")

    return PC

def r_type(instruction):
    global dict
    global PC
    func3 = instruction[18:21]
    func7 = instruction[0:7]
    rd = registers[instruction[20:25]]
    rs1 = registers[instruction[12:17]]
    rs2 = registers[instruction[7:12]]

    if func3 == '000' and func7 == '0000000':
        # ADD
        dict[rd] = dict[rs1] + dict[rs2]

    elif func3 == '000' and func7 == '0100000' and rs1 == "00000":
        # SUB
        dict[rd] = 0 - dict[rs2]
    elif func3 == '000' and func7 == '0100000':
        # SUB
        dict[rd] = dict[rs1] - dict[rs2]
    elif func3 == '001' and func7 == '0000000':
        # SLL
        dict[rd] = [rs1] <<dict[rs2]
    elif func3 == '010' and func7 == '0000000':
        # SLT
        if dict[rs1] < int(dict[rs2]):
            dict[rd] = 1
        else:
            dict[rd] = 0
    elif func3 == '011' and func7 == '0000000':
        # SLTU
        if dict[rs1] < dict[rs2]:
            dict[rd] = 1
        else:
            dict[rd] = 0
    elif func3 == '100' and func7 == '0000000':
        # XOR
        dict[rd] = int(dict[rs1]) ^ int(dict[rs2])
    elif func3 == '101' and func7 == '0000000':
        # SRL
        dict[rd] = dict[rs1] >> dict[rs2]
    elif func3 == '110' and func7 == '0000000':
        # OR
        dict[rd] = dict[rs1] | int(dict[rs2])
    elif func3 == '111' and func7 == '0000000':
        # AND
        dict[rd] = int(dict[rs1]) & int(dict[rs2])

    pc+=4
    #print program counter
    print("0b"+decimal_binary_32bits(pc)+" ")
    for i in list(dict.keys()):
      print("0b"+decimal_binary_32bits(dict[i])+" ")
    return PC


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
        ans = "0" * (32 - cnt) + ans
        ans = complement(ans)
    return ans



l1=[]
dict1={}
with open(r'C:\Users\HP\OneDrive\Desktop\c++\project_co\co_simulator\text.txt',"r") as f:
    data=f.readlines()
    for lines in data:
        l1.append(lines.strip())
        dict1[data.index(lines)*4]=lines.strip()


    # dict1={0:"10000000000000",4:"010111111111111111"}
    #  l1=["10000000000000","010111111111111111"]


pc=0
while(pc<virual_halt):
    instruction=dict1[pc]
    opcode_value=instruction[25:]
    temp=opcode[opcode_value]
    if temp=="R":
        pc=r_type(instruction)
    elif temp=="S":
        pc=s_type(instruction)
    elif temp=="I":
        pc=i_type(instruction)
    elif temp=="J":
        pc=j_type(instruction)
    elif temp=="B":
        pc=b_type(instruction)
    elif temp=="U":
        pc=u_type(instruction)
