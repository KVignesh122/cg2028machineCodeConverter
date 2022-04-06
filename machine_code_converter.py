X_4BIT = "0000"
X_3BIT = "000"
X_1BIT = '0'
SEPARATOR = '\n' + "=" * 50

CG2028 = """ ________  ________    _______  ________    _______  ________     
|\   ____\|\   ____\  /  ___  \|\   __  \  /  ___  \|\   __  \    
\ \  \___|\ \  \___| /__/|_/  /\ \  \|\  \/__/|_/  /\ \  \|\  \   
 \ \  \    \ \  \  __|__|//  / /\ \  \\\  \__|//  / /\ \   __  \  
  \ \  \____\ \  \|\  \  /  /_/__\ \  \\\  \  /  /_/__\ \  \|\  \ 
   \ \_______\ \_______\|\________\ \_______\|\________\ \_______\\
    \|_______|\|_______| \|_______|\|_______| \|_______|\|_______|
                                                                  """

TITLE = """                   _     _                ___          _          ___                          _            
  /\/\   __ _  ___| |__ (_)_ __   ___    / __\___   __| | ___    / __\___  _ ____   _____ _ __| |_ ___ _ __ 
 /    \ / _` |/ __| '_ \| | '_ \ / _ \  / /  / _ \ / _` |/ _ \  / /  / _ \| '_ \ \ / / _ | '__| __/ _ | '__|
/ /\/\ | (_| | (__| | | | | | | |  __/ / /__| (_) | (_| |  __/ / /__| (_) | | | \ V |  __| |  | ||  __| |   
\/    \/\__,_|\___|_| |_|_|_| |_|\___| \____/\___/ \__,_|\___| \____/\___/|_| |_|\_/ \___|_|   \__\___|_|   
                                                                                                            """

NAME = """ _  __                                         _  __     ___                      _     
 | |/ _   _ _ __ ___   __ _ _ __ __ ___   _____| | \ \   / (_) __ _ _ __   ___ ___| |__  
 | ' | | | | '_ ` _ \ / _` | '__/ _` \ \ / / _ | |  \ \ / /| |/ _` | '_ \ / _ / __| '_ \ 
 | . | |_| | | | | | | (_| | | | (_| |\ V |  __| |   \ V / | | (_| | | | |  __\__ | | | |
 |_|\_\__,_|_| |_| |_|\__,_|_|  \__,_| \_/ \___|_|    \_/  |_|\__, |_| |_|\___|___|_| |_|
                                                              |___/                      """

DP_INSTR = {
    "mov": "1101", 
    "sub": "0010",
    "and": "0000",
    "eor": "0001",
    "rsb": "0011",
    "add": "0100",
    "adc": "0101",
    "sbc": "0110",
    "rsc": "0111",
    "tst": "1000",
    "teq": "1001",
    "cmp": "1010",
    "cmn": "1011",
    "orr": "1100",
    "bic": "1110",
    "mvn": "1111"
}

MUL_INSTR = {
    "mul": "0000",
    "mla": "0001"
}

MEM_INSTR = {
    "ldr": '1',
    "str": '0'
}

PW = {
    "preindex": "11",
    "postindex": "00",
    "offset": "10",
}

BRANCH_MSG = """
    This may be a branch instruction, so compute the instruction set mannualy.
    Format: <4b_condition> <op:10> <00> <1b_U> <15b_0s> <8b_imm8>

    Common 4b_cond values are:-
    EQ: 0000
    NE: 0001
    GE: 1010
    LT: 1011
    LE: 1101
    GT: 1100"""

def convert_dp(cmd_word, rd, rn, rm):
    op = "00"
    cmd = DP_INSTR[cmd_word[:3]]

    if rm.startswith('#'):
        imm = '1'
    elif rm.startswith('r'):
        imm = X_1BIT
    else:
        print("ERROR: Rm value is neither register nor 8-bit integer.")
        return 0
    rm = int(rm[1:])

    if type(rd) == str and rd.startswith('r'):
        rd = int(rd[1:])
    elif rd != 0:
        print("ERROR: Rd value is not a register.")
        return 0

    if type(rn) == str and rn.startswith('r'):
        rn = int(rn[1:])
    elif rn != 0:
        print("ERROR: Rn value is not a register.")
        return 0
    
    s = X_1BIT
    if cmd_word.endswith('s') or cmd_word == "cmp":
        s = '1'
    
    rn = "{0:04b}".format(rn)
    rd = "{0:04b}".format(rd)
    rm = "{0:08b}".format(rm)

    print(f"""
    This is a data-processing instruction.
    op: {op}
    I: {imm}
    cmd: {cmd}
    S: {s}
    Rn: {rn}
    Rd: {rd}
    M: 0
    Rm/imm8: {rm}
    """)

    binary = X_4BIT + op + imm + cmd + s + rn + rd + X_4BIT + rm
    return binary


def get_dp_values(user_input, cmd_word):
    user_input = ''.join(ch for ch in user_input[len(cmd_word)+1:].strip().split())
    user_input = user_input.split(',')
    if len(user_input) == 3:
        rd, rn, rm = user_input
    elif len(user_input) == 2 and "mov" in cmd_word:
        rd, rm = user_input
        rn = 0
    elif len(user_input) == 2:
        rn, rm = user_input
        rd = rn
        if cmd_word[:3] in ["cmp", "cmn", "tst", "teq"]:
            rd = 0
    else:
        print("ERROR: Missing/Extra input values detected.")
        return 0
    return (rd, rn, rm)


def get_mul_values(user_input, cmd_word):
    user_input = ''.join(ch for ch in user_input[len(cmd_word)+1:].strip().split())
    user_input = user_input.split(',')
    if len(user_input) == 3:
        rd, rm, rs = user_input
        rn = 0
    elif len(user_input) == 2:
        rm, rs = user_input
        rd = rm
        rn = 0
    elif len(user_input) == 4:
        rd, rm, rs, rn = user_input
    else:
        print("ERROR: Missing/Extra input values detected.")
        return 0
    return (rd, rm, rs, rn)


def convert_mul_or_mla(cmd_word, rd, rm, rs, rn):
    op = "00"
    cmd = MUL_INSTR[cmd_word[:3]]
    m = '1'
    imm = X_1BIT
    s = X_1BIT

    if (rn == 0 or rn.startswith('r')) and rd.startswith('r') and rm.startswith('r') and rs.startswith('r'):
        if rn != 0:
            rn = int(rn[1:])
        rd, rm, rs = int(rd[1:]), int(rm[1:]), int(rs[1:])
    else:
        print("ERROR: Invalid register(s).")
        return 0
    
    rn = "{0:04b}".format(rn)
    rd = "{0:04b}".format(rd)
    rm = "{0:04b}".format(rm)
    rs = "{0:04b}".format(rs)

    print(f"""
    This is a data-processing instruction.
    op: {op}
    I: {imm}
    cmd: {cmd}
    S: {s}
    Rn: {rn}
    Rd: {rd}
    Rs: {rs}
    M: {m}
    Rm: {rm}
    """)

    binary = X_4BIT + op + imm + cmd + s + rn + rd + rs + X_3BIT + m + rm
    return binary


def get_mem_values(user_input, cmd_word):
    if user_input.endswith(']'):
        pw = "offset"
    elif user_input.endswith('!'):
        pw = "preindex"
    else:
        pw = "postindex"
    
    user_input = user_input.replace('[', '')
    user_input = user_input.replace(']', '')
    user_input = user_input.replace('!', '')
    user_input = user_input.replace('#', '')
    user_input = ''.join(ch for ch in user_input[len(cmd_word)+1:].strip().split())
    user_input = user_input.split(',')

    if len(user_input) == 3:
        rd, rn, os = user_input
    elif len(user_input) == 2:
        rd, rn = user_input
        os = 0
    else:
        print("ERROR: Missing/Extra input values detected.")
        return 0
    return (rd, rn, os, pw)


def convert_mem_values(cmd_word, rd, rn, os, pw):
    op = "01"
    l = MEM_INSTR[cmd_word[:3]]
    p, w = list(PW[pw])
    os = int(os)

    if os <= 0:
        u = X_1BIT
        os *= -1
    elif os > 0:
        u = '1'
    else:
        print("ERROR: Invalid offset immediate value.")
        return 0

    if rn.startswith('r') and rd.startswith('r'):
        rd, rn = int(rd[1:]), int(rn[1:])
    else:
        print("ERROR: Invalid register(s).")
        return 0
    
    rn = "{0:04b}".format(rn)
    rd = "{0:04b}".format(rd)
    os = "{0:08b}".format(os)

    print(f"""
    This is a memory instruction.
    op: {op}
    P: {p}
    U: {u}
    W: {w}
    L: {l}
    Rn: {rn}
    Rd: {rd}
    imm8: {os}
    """)

    binary = X_4BIT + op + X_1BIT + p + u + X_1BIT + w + l + rn + rd + X_4BIT + os
    return binary


def run():
    input_instr = input("\nInsert asm instruction: ")
    while input_instr != "end":
        full_binary = 0
        if input_instr == "":
            print("ERROR: Empty instruction!")
        else:
            input_instr = input_instr.strip().lower()
            cmd_word = input_instr.split()[0]
            base_cmd = cmd_word[:3]
            if base_cmd in DP_INSTR:
                values = get_dp_values(input_instr, cmd_word)
                if values != 0:
                    rd, rn, rm = values
                    full_binary = convert_dp(cmd_word, rd, rn, rm)
            elif base_cmd in MUL_INSTR:
                values = get_mul_values(input_instr, cmd_word)
                if values != 0:
                    rd, rm, rs, rn = values
                    full_binary = convert_mul_or_mla(cmd_word, rd, rm, rs, rn)
            elif base_cmd in MEM_INSTR:
                values = get_mem_values(input_instr, cmd_word)
                if values != 0:
                    rd, rn, os, pw = values
                    full_binary = convert_mem_values(cmd_word, rd, rn, os, pw)
            elif base_cmd != "bic" and base_cmd.startswith('b'):
                print(BRANCH_MSG)
            else:
                print("ERROR: Invalid instruction!")
            
            if full_binary != 0:
                formated_hex = "{0:#0{1}x}".format(int(full_binary, 2), 10)
                full_binary = " ".join(full_binary[i:i+4] for i in range(0, 32, 4))

                print(f"Binary layout: {full_binary}")
                print(f"Hex layout: {formated_hex}")
        
        print(SEPARATOR)
        input_instr = input("\nInsert asm instruction: ")


def print_menu():
    print(CG2028)
    print(TITLE)
    print("Type in your asm code to convert to hexadecimal machine code.")
    print("Type 'end' to quit program.")
    print("\n* Note: This program only supports the more popular and frequently used instructions, \nso complete reliability is not guaranteed. Pls do your own self-checks of the outputs.\n")
    print("[PC relative memory instructions are currently not supported.]")
    print(SEPARATOR)


def print_close():
    print("Program created in April 2022 by: ")
    print(NAME)
    print("<<< Program Ended >>>\n")


if __name__ == "__main__":
    print_menu()
    run()
    print_close()
    