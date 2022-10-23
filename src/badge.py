# badge.py
# Adam Zeloof
# 9.14.2022
# requires Python 3.10 or higher

from bvmCPU import CPU
from bvmParser import parse
from timeit import default_timer as timer
from random import randint
class Badge():
    def __init__(self):
        self.cpu = CPU()
        self.initMemory()
        self.clock = 0b0
        self.oldTime = timer()
        self.newTime = timer()
        self.speed = 2 # Hz
        self.progMem = []
        self.pc = 0
        self.acc = [
            0b0000, # lower
            0b0000, # middle
            0b0000  # upper
        ]
        self.cFlag = [
            0b0, # lower
            0b0, # middle
            0b0  # upper
        ]
        self.zFlag = [
            0b0, # lower
            0b0, # middle
            0b0  # upper
        ]
        self.vFlag = [
            0b0, # lower
            0b0, # middle
            0b0  # upper
        ]
        self.userCarry = 0b0
        self.adders = [
            0b0000, # dest bits
            0b0000, # source bits
            0b0000, # carry bits
            0b0000  # sum bits
        ]
        self.page = 0b0000
    

    def initMemory(self):
        self.cpu.ram[0xf1] = 14 # Set initial clock speed to 1 Hz
        self.cpu.ram[0xff] = randint(0, 16) # Set random value at SFRFF


    def load(self, program):
        with open(program, 'rb') as f:
            prog = list(f.read())
            #print(prog)
            prog = prog[6:] # Strip the header
            lenBytes = prog[0:2]
            #print(lenBytes)
            length = (lenBytes[1]<<8) + lenBytes[0]
            prog = prog[2:]
            for i in range(0, len(prog), 2):
                ins = prog[i:i+2]
                self.progMem.append(ins)
            #print(self.progMem)
            return
            lines = f.readlines()
            for line in lines:
                #line = line.replace(" ","")
                line = line.replace("\n","")
                line = line.split('//')[0]
                if line != '':
                    self.progMem.append(line)


    def step(self):
        instruction = parse(self.progMem[self.cpu.getPC()])
        if instruction is not None:
            #print(instruction)
            getattr(self.cpu, instruction['op'])(instruction['args'])
        self.cpu.step()


    def update(self):
        self.newTime = timer()
        if self.newTime > self.oldTime + 0.5/self.speed:
            if self.clock == 0:
                # Set random value at SFRFF
                # This does not really happen every clock cycle but its good enough
                self.cpu.ram[0xff] = randint(0, 16)
                # Set the page status
                self.page = self.cpu.ram[0xf0]
                # Step through the instructions
                self.step()
                self.clock = 1
            else:
                self.clock = 0
            self.oldTime = timer()

        # Check SFR1 and set clock speed accordingly
        speeds = [250e3, 100e3, 30e3, 10e3, 3e3, 1e3, 500, 200, 100, 50, 20, 10, 5, 2, 1, .5]
        self.speed = speeds[self.cpu.ram[0xf1]]
        


