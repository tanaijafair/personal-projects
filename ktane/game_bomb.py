import random
from abc import ABC
from modules import Wires, Button, Keypad, SimonSays, WhosOnFirst, \
    Memory, MorseCode, ComplicatedWires, WireSequences, Mazes, Passwords

DEBUG = True

class Module(ABC):
    def __init__(self):
        pass

SERIAL_OPTS:list[str | int] = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", 
                               "K", "L", "M","N", "P", "Q", "R", "S", "T", "U", 
                               "V", "W", "X", "Y", "Z", 0, 1, 2, 3, 4, 5, 6, 7, 
                               8, 9]

WIRES:Wires = Wires()
BUTTON:Button = Button()
KEYPAD:Keypad = Keypad()
SIMONSAYS:SimonSays = SimonSays()
WHOSONFIRST:WhosOnFirst = WhosOnFirst()
MEMORY:Memory = Memory()
MORSECODE:MorseCode = MorseCode()
COMPLICATEDWIRES:ComplicatedWires = ComplicatedWires()
WIRESEQUENCES:WireSequences = WireSequences()
MAZES:Mazes = Mazes()
PASSWORDS:Passwords = Passwords()

MODULE_OPTS: list[Module] = [WIRES, BUTTON, KEYPAD, SIMONSAYS, WHOSONFIRST,
MEMORY, MORSECODE, COMPLICATEDWIRES, WIRESEQUENCES, PASSWORDS]

TEMP_OPTS:list[Module] = [WIRES, BUTTON, KEYPAD]

class Bomb:
    num_modules: int
    num_batteries: int
    moves_allowed: int
    moves_left:int
    strikes_left: int
    serial_number: str
    modules: list[Module]
    exploded:bool
    def __init__(self, num_modules, num_strikes):
        self.num_modules = num_modules
        self.num_batteries = random.randint(1, 3)
        self.strikes_left = num_strikes
        self.serial_number = ""

        for _ in range(6):
            self.serial_number += str(random.choice(SERIAL_OPTS))

        self.serial_number += str(random.randint(0, 9))
        self.modules = []

        for _ in range(self.num_modules):
            if DEBUG:
                self.modules.append(random.choice(TEMP_OPTS))
            else:
                self.modules.append(random.choice(MODULE_OPTS))
            

        self.moves_allowed = 0

        for mod in self.modules:
            self.moves_allowed += mod.moves

        self.moves_allowed += self.strikes_left
        self.moves_left = self.moves_allowed
        self.exploded = False


    def bomb_stats(self) -> None:
        print("BOMB STATS:")
        print(f"serial number: {self.serial_number}")
        print(f"number of batteries: {self.num_batteries}")
        print(f"number of modules: {self.num_modules}")
        if DEBUG:    
            print(f"(DEBUG) modules: {self.modules}")
        print(f"number of moves: {self.moves_allowed}")
        print(f"number of strikes: {self.strikes_left}")
        print()