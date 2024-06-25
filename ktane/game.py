from game_bomb import Bomb
from modules import Module, Wires, Button, Keypad, SimonSays, WhosOnFirst, \
    Memory, MorseCode, ComplicatedWires, WireSequences, Mazes, Passwords
from game_bomb import WIRES, BUTTON, KEYPAD, SIMONSAYS, WHOSONFIRST, \
MEMORY, MORSECODE, COMPLICATEDWIRES, WIRESEQUENCES, PASSWORDS
import sys
from typing import Optional

DEBUG = True

def main():
    bomb:Bomb = gen_bomb()
    for module in bomb.modules:
        run_module(bomb, module)
    return fin_game(bomb)


def gen_bomb(num_modules:int = 3, num_strikes:int = 2) -> Bomb:
    bomb:Bomb = Bomb(num_modules, num_strikes)
    bomb.bomb_stats()
    return bomb

def run_module(bomb:Bomb, module:Module) -> None:
    if module == WIRES:
        wires_mod:Wires = Wires(bomb.serial_number, bomb.strikes_left)
        run_wires(bomb, wires_mod)
    elif module == BUTTON:
        button_mod:Button = Button(bomb.num_batteries, bomb.strikes_left)
        run_button(bomb, button_mod)
    elif module == KEYPAD:
        keypad_mod:Keypad = Keypad(bomb.strikes_left)
        run_keypad(bomb, keypad_mod)


def wrong_action(bomb:Bomb):
    bomb.strikes_left -= 1
    if bomb.strikes_left < 0:
        bomb.exploded = True
        sys.exit("YOU BLEW UP")
    print(f"Strikes left: {bomb.strikes_left}")
    print()


def run_wires(bomb:Bomb, wires_mod:Wires) -> None:
    print("This is a Wires Module")
    print()
    num_wires:int = wires_mod.num_wires
    wires_mod.get_correct_sequence()
    while not wires_mod.deactivated and not bomb.exploded and \
        num_wires > 0 and bomb.moves_left > 0:
        print(f"Moves left: {bomb.moves_left}")
        wires_mod.present_wires()
        if DEBUG:
            print(f"correct sequence: {wires_mod.correct_sequence}")
        while 1:
            wire_cut_s:str = input("Which wire will you cut? ").upper()
            print()
            wire_cut_n:int = wires_mod.color_to_num(wire_cut_s)
            if wire_cut_n in wires_mod.wires:
                break
        bomb.moves_left -= 1
        i:int = 0
        if wire_cut_n == wires_mod.correct_sequence[i]:
            print(f"Wires deactivated!")
            print()
            print()
            wires_mod.deactivated = True
        else:
            i+=1
            print(f"WRONG WIRE!!!")
            wrong_action(bomb)
            num_wires -= 1
            if wires_mod.wires.count(wire_cut_n) > 1:
                for wire in wires_mod.wires:
                    if wire == wire_cut_n:
                        wires_mod.wires.remove(wire_cut_n)
                        break
            else:
                wires_mod.wires.remove(wire_cut_n)
            if wire_cut_n in wires_mod.correct_sequence:
                wires_mod.correct_sequence.remove(wire_cut_n)
            

def run_button(bomb:Bomb, button_mod:Button) -> None:
    print("This is a Button module")
    print()
    button_mod.present_button()
    while not button_mod.deactivated and not bomb.exploded and \
        bomb.moves_left > 0:
        print(f"Moves left: {bomb.moves_left}")
        while 1:
            action:str = input("Press or Hold? ").upper()
            print()
            if action == "PRESS" or action == "HOLD":
                break
        answer:tuple[str, Optional[int]] = button_mod.correct_action()
        if action == answer[0]:
            match action:
                case "PRESS":
                    print(f"Button deactivated!")
                    print()
                    print()
                    button_mod.button_deactivate()
                case "HOLD":
                    timer_count:int = int(input("What timer position will you release on? "))
                    print()
                    if timer_count == answer[1]:
                        print(f"Button deactivated!")
                        print()
                        print()
                        button_mod.button_deactivate()
                    else:
                        print(f"WRONG ACTION!!!")
                        wrong_action(bomb)
        else:
            print(f"WRONG ACTION!!!")
            wrong_action(bomb)


def run_keypad(bomb:Bomb, keypad_mod:Keypad):
    print("This is a Keypad module")
    keypad_mod.present_keypad()
    answer:list[str] = keypad_mod.correct_sequence()
    while not keypad_mod.deactivated and not bomb.exploded and \
        bomb.moves_left > 0:
        print(f"Moves left: {bomb.moves_left}")
        """
        Try to make this less ugly... Could you have one loop to take care of 
        each round?
        """
        count:int = 0
        while count < 4:
            for _ in range(4):
                while 1:
                    symbol:str = input("Which symbol next? ").lower()
                    print()
                    if symbol in keypad_mod.get_symbol_opts():
                        break
                bomb.moves_left -= 1
                
                if symbol == answer[count]:
                    print(f"'{symbol}' activated correctly")
                    print()
                    count += 1
                    if count == 4:
                        print(f"Keypad deactivated!")
                        print()
                        print()
                        keypad_mod.deactivated = True
                        print()

                else:
                    print(f"Wrong symbol!!!")
                    count = 0
                    wrong_action(bomb)
        

def fin_game(bomb:Bomb) -> bool:
    print("CONGRATS, YOU DEFUSED THE BOMB!")
    print(f"You finished with {bomb.moves_left} moves left and {bomb.strikes_left} strikes left")
    return True

main()