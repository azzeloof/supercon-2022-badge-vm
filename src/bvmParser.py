# bvmParser.py
# Adam Zeloof
# 3.12.2022

def pad(n:str, b:int) -> str:
    if len(n) < b:
        n = '0'*(b-len(n)) + n
    elif len(n) > b:
        pass
    return n

def bits(n:int, b:int) -> str:
    # takes an int n and int b
    # returns a string of n represented in binary with b bits
    return pad(bin(n).split('b')[1],b)


def toHexByte(n: int) -> str:
    out = hex(n)
    out = out [2:]
    if len(out) == 1:
        out = "0" + out
    return out


def parse(instruction: list) -> dict:
    print(instruction)
    #ins = instruction.split(" ")
    AB = toHexByte(instruction[0])
    CD = toHexByte(instruction[1])
    A = int(AB[0], 16) # ARG_0 or OP_1
    B = int(AB[1], 16) # ARG_1
    C = int(CD[0], 16) # UNUSED
    D = int(CD[1], 16) # OP_0
    assert(C==0)
    n = B
    x = A
    y = B
    g = int(bits(int(CD, 16),8)[4:6],2)
    f = g
    m = int(bits(int(CD, 16),8)[6:8],2)
    nn = int(AB, 16)

    if D != 0: # Four-bit opcode
        if D == 0x1:
            return {
                'op': 'ADD',
                'args': {'mode':0, 'x':x, 'y':y}              
            }
        elif D == 0x2:
            return {
                'op': 'ADC',
                'args': {'x':x, 'y':y}
            }
        elif D == 0x3:
            return {
                'op': 'SUB',
                'args': {'x':x, 'y':y}
            }
        elif D == 0x4:
            return {
                'op': 'SBB',
                'args': {'x':x, 'y':y}
            }
        elif D == 0x5:
            return {
                'op': 'OR',
                'args': {'mode':0, 'x':x, 'y':y}
            }
        elif D == 0x6:
            return {
                'op': 'AND',
                'args': {'mode':0, 'x':x, 'y':y}
            }
        elif D == 0x7:
            return {
                'op': 'XOR',
                'args': {'mode':0, 'x':x, 'y':y}
            }
        elif D == 0x8:
            return {
                'op': 'MOV',
                'args': {'mode':0, 'x':x, 'y':y}
            }
        elif D == 0x9:
            return {
                'op': 'MOV',
                'args': {'mode':1, 'x':x, 'n':n}
            }
        elif D == 0xA:
            return {
                'op': 'MOV',
                'args': {'mode':2, 'x':x, 'y':y}
            }
        elif D == 0xB:
            return {
                'op': 'MOV',
                'args': {'mode':3, 'x':x, 'y':y}
            }
        elif D == 0xC:
            return {
                'op': 'MOV',
                'args': {'mode':4, 'nn':nn}
            }
        elif D == 0xD:
            return {
                'op': 'MOV',
                'args': {'mode':5, 'nn':nn}
            }
        elif D == 0xE:
            return {
                'op': 'MOV',
                'args': {'mode':6, 'nn':nn}
            }
        elif D == 0xF:
            return {
                'op': 'JR',
                'args': {'nn':nn}
            }
    else: #Eight-bit opcode
        if A == 0x0:
            return {
                'op': 'CP',
                'args': {'n':n}
            }
        elif A == 0x1:
            return {
                'op': 'ADD',
                'args': {'mode':1, 'n':n}
            }
        elif A == 0x2:
            return {
                'op': 'INC',
                'args': {'y':n}
            }
        elif A == 0x3:
            return {
                'op': 'DEC',
                'args': {'y':n}
            }
        elif A == 0x4:
            return {
                'op': 'DSZ',
                'args': {'y':y}
            }
        elif A == 0x5:
            return {
                'op': 'OR',
                'args': {'mode':1, 'n':n}
            }
        elif A == 0x6:
            return {
                'op': 'AND',
                'args': {'mode':1, 'n':n}
            }
        elif A == 0x7:
            return {
                'op': 'XOR',
                'args': {'mode':1, 'n':n}
            }
        elif A == 0x8:
            return {
                'op': 'EXR',
                'args': {'n':n}
            }
        elif A == 0x9:
            return {
                'op': 'BIT',
                'args': {'g':g, 'm':m}
            }
        elif A == 0xA:
            return {
                'op': 'BSET',
                'args': {'g':g, 'm':m}
            }
        elif A == 0xB:
            return {
                'op': 'BCLR',
                'args': {'g':g, 'm':m}
            }
        elif A == 0xC:
            return {
                'op': 'BTG',
                'args': {'g':g, 'm':m}
            }
        elif A == 0xD:
            return {
                'op': 'RRC',
                'args': {'y':y}
            }
        elif A == 0xE:
            return {
                'op': 'RET',
                'args': {'n':n}
            }
        elif A == 0xF:
            return {
                'op': 'SKIP',
                'args': {'f':f, 'm':m}
            }
        else:
            return None

    return None
