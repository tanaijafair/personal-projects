from game_bomb import Bomb
from modules import Module, Wires, Button, Keypad, SimonSays, WhosOnFirst, \
    Memory, MorseCode, ComplicatedWires, WireSequences, Mazes, Passwords
from game_bomb import WIRES, BUTTON, KEYPAD, SIMONSAYS, WHOSONFIRST, \
MEMORY, MORSECODE, COMPLICATEDWIRES, WIRESEQUENCES, PASSWORDS
import sys
from typing import Optional

DEBUG = False

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
            bomb.strikes_left -= 1
            if bomb.strikes_left < 0:
                bomb.exploded = True
                sys.exit("YOU BLEW UP")
            else:
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
                print(f"Strikes left: {bomb.strikes_left}")
                print()
    

def run_button(bomb:Bomb, button_mod:Button) -> None:
    print("This is a Button module")
    print()
    button_mod.present_button()
    while not button_mod.deactivated and not bomb.exploded and \
        bomb.moves_left > 0:
        while 1:
            action:str = input("Press or Hold? ").upper()
            if action == "PRESS" or action == "HOLD":
                break
        answer:tuple[str, Optional[int]] = button_mod.correct_action()
        if action == answer[0]:
            match action:
                case "PRESS":
                    button_mod.button_deactivate()
                case "HOLD":
                    timer_count:int = int(input("What timer position will you release on? "))
                    if timer_count == answer[1]:
                        button_mod.button_deactivate()
                    else:
                        print(f"WRONG ACTION!!!")
                        bomb.strikes_left -= 1
                        if bomb.strikes_left < 0:
                            bomb.exploded = True
                            sys.exit("YOU BLEW UP")
                        else:
                            print(f"Strikes left: {bomb.strikes_left}")
                            print()
        else:
            print(f"WRONG ACTION!!!")
            bomb.strikes_left -= 1
            if bomb.strikes_left < 0:
                bomb.exploded = True
                sys.exit("YOU BLEW UP")
            else:
                print(f"Strikes left: {bomb.strikes_left}")
                print()
            


def fin_game(bomb:Bomb) -> bool:
    print("CONGRATS, YOU DEFUSED THE BOMB!")
    print(f"You finished with {bomb.moves_left} moves left and {bomb.strikes_left} strikes left")
    return True

main()