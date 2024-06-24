from abc import ABC
from typing import Optional
import random

DEBUG = False

WHITE:int = 7
BLACK:int = 8
RED:int = 9
YELLOW:int = 10
BLUE:int = 11

COLOR_OPTS:list[int] = [WHITE, BLACK, RED, YELLOW, BLUE]

TEXT_OPTS:list[str] = ["Abort", "Detonate", "Hold", "Press"]
INDICATOR_OPTS:list[str] = ["CAR", "FRK"]

class Module(ABC):
    def __init__(self):
        pass


class Wires(Module):
    sn: str
    strikes: int
    num_wires: int
    wires: list[int]
    correct_sequence:list[int]
    moves: int
    deactivated: bool
    def __init__(self, sn:str = "W00000", strikes:int = 2):
        self.sn = sn
        self.strikes = strikes
        self.num_wires = random.randint(3,6)
        self.wires = []

        for _ in range(self.num_wires):
            self.wires.append(random.choice(COLOR_OPTS))
        
        self.correct_sequence = []
        self.moves = 1
        self.deactivated = False
    
    
    def present_wires(self) -> None:
        print(f"Original number of wires: {self.num_wires}")
        for i, wire in enumerate(self.wires):
            wire = self.num_to_color(wire)
            print(f"Wire {i+1}: {wire}")


    def num_to_color(self, wire_n:int) -> str:
        wire_s:str = ""
        match wire_n:
            case 7:
                wire_s = "WHITE"
            case 8:
                wire_s = "BLACK"
            case 9:
                wire_s = "RED"
            case 10:
                wire_s = "YELLOW"
            case 11:
                wire_s = "BLUE"
        return wire_s
    
    def color_to_num(self, wire_s:str) -> int:
        wire_n:int = 0
        match wire_s:
            case "WHITE":
                wire_n = WHITE
            case "BLACK":
                wire_n = BLACK
            case "RED":
                wire_n = RED
            case "YELLOW":
                wire_n = YELLOW
            case "BLUE":
                wire_n = BLUE
        return wire_n


    def get_correct_sequence(self) -> list[int]:
        serial_last:int = int(self.sn[-1])
        if DEBUG:
            print(f"WIRES CHECK: {self.wires}")
            print(f"SERIAL NUMBER: {self.sn}")
            print(f"The last digit of the serial is {serial_last}.")
        match self.num_wires:
            case 3:
                if RED not in self.wires:
                    self.correct_sequence.append(self.wires[1])
                if self.wires[-1] == WHITE:
                    self.correct_sequence.append(self.wires[-1])
                if self.wires.count(BLUE) > 1:
                    self.correct_sequence.append(BLUE)
                self.correct_sequence.append(self.wires[-1])
            case 4:
                if self.wires.count(RED) > 1 and \
                    serial_last % 2 != 0:
                    self.correct_sequence.append(RED)
                if self.wires[-1] == YELLOW and RED not in self.wires:
                    self.correct_sequence.append(self.wires[0])
                if self.wires.count(BLUE) == 1:
                    self.correct_sequence.append(self.wires[0])
                if self.wires.count(YELLOW) > 1:
                    self.correct_sequence.append(self.wires[-1])
                self.correct_sequence.append(self.wires[1])
            case 5:
                if self.wires[-1] == BLACK and \
                    serial_last % 2 != 0:
                    self.correct_sequence.append(self.wires[3])
                if self.wires.count(RED) == 1 and self.wires.count(YELLOW) > 1:
                    self.correct_sequence.append(self.wires[0])
                if BLACK not in self.wires:
                    self.correct_sequence.append(self.wires[1])
                self.correct_sequence.append(self.wires[0])
            case 6:
                if YELLOW not in self.wires and \
                    serial_last % 2 != 0:
                    self.correct_sequence.append(self.wires[2])
                if self.wires.count(YELLOW) == 1 and self.wires.count(WHITE) > 1:
                    self.correct_sequence.append(self.wires[3])
                if RED not in self.wires:
                    self.correct_sequence.append(self.wires[-1])
                self.correct_sequence.append(self.wires[3])




class Button(Module):
    strikes: int
    button_color: int
    button_text: str
    num_batteries:int
    correct_sequence:list[int]
    moves: int
    deactivated: bool
    lit_indicator:int
    indicator_label:str
    def __init__(self, num_batteries:int = 1, strikes:int = 2):
        self.strikes = strikes
        self.button_color = random.choice(COLOR_OPTS)
        self.button_text = random.choice(TEXT_OPTS)
        self.num_batteries = num_batteries
        self.correct_sequence = []
        self.moves = 1
        self.deactivated = False
        self.lit_indicator = BLACK
        while self.lit_indicator == BLACK:
            self.lit_indicator = random.choice(COLOR_OPTS)
        self.indicator_label = random.choice(INDICATOR_OPTS)


    def present_button(self) -> None:
        print(f"Color of Button: {self.num_to_color(self.button_color)}")
        print(f"Text on Button: {self.button_text}")
        print(f"Indicator Color: {self.num_to_color(self.lit_indicator)}")
        print(f"Indicator Label: {self.indicator_label}")
        print(f"Number of Batteries: {self.num_batteries}")
        print()


    def num_to_color(self, wire_n:int) -> str:
        wire_s:str = ""
        match wire_n:
            case 7:
                wire_s = "WHITE"
            case 8:
                wire_s = "BLACK"
            case 9:
                wire_s = "RED"
            case 10:
                wire_s = "YELLOW"
            case 11:
                wire_s = "BLUE"
        return wire_s
    

    def releasing_a_button(self) -> tuple[str, int]:
        result:list[str, Optional[int]] = []
        match self.lit_indicator:
            case 7:
                result = ["HOLD", 1]
            case 9:
                result = ["HOLD", 1]
            case 10:
                result = ["HOLD", 5]
            case 11:
                result = ["HOLD", 4]
        return result
    

    def correct_action(self) -> tuple[str, Optional[int]]:
        result:list[str, Optional[int]] = []
        if self.button_color == BLUE and self.button_text == "Abort":
            result = self.releasing_a_button()
        elif self.num_batteries > 1 and self.button_text == "Detonate":
            result = ["PRESS", None]
        elif self.button_color == WHITE and self.indicator_label == "CAR":
            result = self.releasing_a_button()
        elif self.num_batteries > 2 and self.indicator_label == "FRK":
            result = ["PRESS", None]
        elif self.button_color == YELLOW:
            result = self.releasing_a_button()
        elif self.button_color == RED and self.button_text == "Hold":
            result = ["PRESS", None]
        else:
            result = self.releasing_a_button()
        return tuple(result)
    

    def button_deactivate(self) -> None:
        print(f"Button deactivated!")
        print()
        print()
        self.deactivated = True
        

class Keypad(Module):
    moves: int
    def __init__(self):
        self.moves = 1
        #print("this is a Keypad module")

class SimonSays(Module):
    moves: int
    def __init__(self):
        self.moves = 1
        #print("this is a SimonSays module")

class WhosOnFirst(Module):
    moves: int
    def __init__(self):
        self.moves = 1
        #print("this is a WhosOnFirst module")

class Memory(Module):
    moves: int
    def __init__(self):
        self.moves = 1
        #print("this is a Memory module")

class MorseCode(Module):
    moves: int
    def __init__(self):
        self.moves = 1
        #print("this is a MorseCode module")

class ComplicatedWires(Module):
    moves: int
    def __init__(self):
        self.moves = 1
        #print("this is a ComplicatedWires module")

class WireSequences(Module):
    moves: int
    def __init__(self):
        self.moves = 1
        #print("this is a WireSequences module")

class Mazes(Module):
    moves: int
    def __init__(self):
        self.moves = 1
        #print("this is a Mazes module")

class Passwords(Module):
    moves: int
    def __init__(self):
        self.moves = 1
        #print("this is a Passwords module")
