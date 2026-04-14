from typing import Callable
import shlex
import sys
import time
import random
import os
import io

def main() -> None:
    program_scope: dict[str, dict[str, Callable | None]] = {"__builtins__": {
        "PrT22E": print,
        "InP22E": input,
        "SlP22E": time.sleep,
        "RnG22E": random.randint,
        "OpN22E": open,
        "str": str,
        "int": int,
        "flt": float,
        "list": list,
        "dict": dict,
        "file": io.TextIOWrapper,
        "null": None,
    }}

    call_stack: list[int] = []

    program_counter: int = 0

    class OpcodeError(Exception):
        def __init__(self, opcode):
            super().__init__(f"OPCODE: '{opcode}' was not found")

    try:
        with open(sys.argv[1]) as PYSMSCRIPT:
            lines: list[str] = [line.strip() for line in PYSMSCRIPT.readlines()]
    except IndexError:
        print("PYSM Error: Please pass a file name as a command line argument")
        sys.exit()
    except FileNotFoundError:
        print(f"PYSM Error: File Not Found {sys.argv[1]}")
        sys.exit()

    labels: dict[str, int] = {}
    for i, line in enumerate(lines):
        if line.startswith(":"):
            label_name = line[1:].strip().upper()
            labels[label_name] = i

    # Variable Declaration
    def setd(program_split: list) -> None:
        type_hint = program_split[1].lower()
        if type_hint == "list" or type_hint == "dict":
            raise NameError(f"name '{type_hint}' is not defined")
        if type_hint == "arr":
            value = program_split[3]
            if value.startswith("{"):
                type_hint = "dict"
            else:
                type_hint = "list"
        value = ' '.join(program_split[3:])
        if value.upper() == "NULL":
            value = value.lower()
        exec(f"{program_split[2]}: {type_hint} = {value}", program_scope)

    # I/O
    def out(command_split: list) -> None:
        args = command_split[1:]
        for i in range(len(args) - 1):
            if args[i] != "<-" and args[i+1] != "<-":
                raise SyntaxError("Multiple string literals were passed without string concatenation")
        
        for part in args:
            if part != "<-":
                exec(f"PrT22E({part}, end='', sep='')", program_scope)


    def inp(command_split: list) -> None:
        if command_split[1] not in program_scope:
            raise NameError(f"name '{command_split[1]}' is not defined")
        try:
            exec(f"{command_split[1]} = {type(program_scope[command_split[1]]).__name__}(InP22E())", program_scope)
        except ValueError:
            raise ValueError(f"invalid input for type '{type(program_scope[command_split[1]]).__name__}'")

    # Jumps
    def jmp(command_split: list) -> int:
        target: str = command_split[1]
        return labels[target.upper()] if target.upper() in labels else int(target)

    def jz(command_split: list) -> int | None:
        target = command_split[2]
        if command_split[1] not in program_scope:
            raise NameError(f"name '{command_split[1]}' is not defined")
        if program_scope[command_split[1]] == 0:
            return labels[target.upper()] if target.upper() in labels else int(target)
        return None

    def jnz(command_split: list) -> int | None:
        target = command_split[2]
        if command_split[1] not in program_scope:
            raise NameError(f"name '{command_split[1]}' is not defined")
        if not program_scope[command_split[1]] == 0:
            return labels[target.upper()] if target.upper() in labels else int(target)
        return None

    def cal(command_split: list) -> int:
        target = command_split[1]
        call_stack.append(program_counter + 1) 
        return labels[target.upper()] if target.upper() in labels else int(target)

    def ret(command_split: list) -> int:
        if not call_stack:
            raise IndexError("Stack Underflow: Attempted to RET with an empty stack!")
        return call_stack.pop()

    def slp(command_split: list) -> None:
        exec(f"SlP22E({command_split[1]})", program_scope)

    # Arithmetic
    def add(command_split: list) -> None:
        if command_split[3] not in program_scope:
            raise NameError(f"name '{command_split[3]}' is not defined")
        exec(f"{command_split[3]} = {command_split[1]} + {command_split[2]}", program_scope)

    def sub(command_split: list) -> None:
        if command_split[3] not in program_scope:
            raise NameError(f"name '{command_split[3]}' is not defined")
        exec(f"{command_split[3]} = {command_split[1]} - {command_split[2]}", program_scope)

    def mul(command_split: list) -> None:
        if command_split[3] not in program_scope:
            raise NameError(f"name '{command_split[3]}' is not defined")
        exec(f"{command_split[3]} = {command_split[1]} * {command_split[2]}", program_scope)

    def div(command_split: list) -> None:
        if command_split[3] not in program_scope:
            raise NameError(f"name '{command_split[3]}' is not defined")
        exec(f"{command_split[3]} = {command_split[1]} / {command_split[2]}", program_scope)

    def mod(command_split: list) -> None:
        if command_split[3] not in program_scope:
            raise NameError(f"name '{command_split[3]}' is not defined")
        exec(f"{command_split[3]} = {command_split[1]} % {command_split[2]}", program_scope)

    def inc(command_split: list) -> None:
        if command_split[1] not in program_scope:
            raise NameError(f"name '{command_split[1]}' is not defined")
        exec(f"{command_split[1]} += 1", program_scope)

    def dec(command_split: list) -> None:
        if command_split[1] not in program_scope:
            raise NameError(f"name '{command_split[1]}' is not defined")
        exec(f"{command_split[1]} -= 1", program_scope)

    # Misc
    def rng(command_split: list) -> None:
        if command_split[3] not in program_scope:
            raise NameError(f"name '{command_split[3]}' is not defined")
        exec(f"{command_split[3]} = RnG22E({command_split[1]}, {command_split[2]})", program_scope)
    def clr(command_split: list) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
    
    # File Handling
    def opn(command_split: list) -> None:
        if command_split[1] not in program_scope:
            raise NameError(f"name '{command_split[1]}' is not defined")
        exec(f"{command_split[1]} = OpN22E({command_split[2]}, '{command_split[3].lower()}')", program_scope)

    def red(command_split: list) -> None:
        if command_split[1] not in program_scope:
            raise NameError(f"name '{command_split[1]}' is not defined")
        lines: list[str] = []
        for line in program_scope[command_split[1]].readlines():
            lines.append(line.strip())
        exec(f"{command_split[2]} = {lines}", program_scope)

    def wrt(command_split: list) -> None:
        args = command_split[2:]
        for i in range(len(args) - 1):
            if args[i] != "<-" and args[i+1] != "<-":
                raise SyntaxError("Multiple string literals were passed without string concatenation")
        for part in args:
            if part != "<-":
                exec(f"{command_split[1]}.write(str({part}))", program_scope)

    def clsd(command_split: list) -> None:
        if command_split[1] not in program_scope:
            raise NameError(f"name '{command_split[1]}' is not defined")
        exec(f"{command_split[1]}.close()", program_scope)

    opcodes: dict[str, Callable] = {
        "SET": setd,
        "OUT": out,
        "INP": inp,
        "JMP": jmp,
        "JZ": jz,
        "JNZ": jnz,
        "CAL": cal,
        "RET": ret,
        "SLP": slp,
        "ADD": add,
        "SUB": sub,
        "MUL": mul,
        "DIV": div,
        "MOD": mod,
        "INC": inc,
        "DEC": dec,
        "RNG": rng,
        "CLR": clr,
        "OPN": opn,
        "RED": red,
        "WRT": wrt,
        "CLS": clsd,
    }

    if "HLT" not in lines:
        print("PYSM Error: PYSM script must end with 'HLT'")
        sys.exit()

    try:
        while lines[program_counter].upper() != "HLT":
            if not lines[program_counter] or lines[program_counter].startswith("#") or lines[program_counter].startswith(":"):
                program_counter += 1
                continue
            command_split: list = shlex.split(lines[program_counter], posix=False)
            if command_split[0].upper() in opcodes:
                result = opcodes[command_split[0].upper()](command_split)
                program_counter = result if result is not None else program_counter + 1
            else:
                raise OpcodeError(command_split[0].upper())
    except Exception as e:
        line_display = lines[program_counter] if program_counter < len(lines) else "unknown"
        print(f"PYSM Error on line {program_counter+1}: {e} \n{line_display}")
        sys.exit()

if __name__ == "__main__":
    main()