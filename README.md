# PYSM 🚀
**Python-Powered Assembly-Style Language**

PYSM is a lightweight, procedural, assembly-themed scripting language built in roughly 200 lines of Python. It combines the low-level feel of assembly (opcodes, labels, jumps) with high-level features like file I/O and strict string piping.

## ✨ Features
* **Procedural Logic**: Full support for subroutines using `CAL` and `RET`.
* **File System**: Open, read, write, and append to files with 3-letter opcodes.
* **VS Code Ready**: Custom syntax highlighting included for a professional dev experience.
* **Lightweight**: The entire interpreter is a single, readable Python file.
* **Labels**: Labels so that your programs functionality is not determined by your ability to count from 0

## 🛠️ Installation
1. Clone this repo.
2. Add the folder containing `pysm.bat` to your **System PATH** (Windows).
3. Install the [PYSM Syntax Highlighting](vscode:extension/pixelkc.pysm-syntax) Vscode Extension

## 🚀 Quick Start: Countdown
```asm
SET INT i 10

:LOOP
CLR
OUT i <- "\n"
SLP 1
DEC i
JNZ i LOOP

CLR
OUT "Happy New Year!"
HLT
```
# Opcode Table

| Opcode | Description | Example |
| :--- | :--- | :--- |
| `SET` | Declare a variable (INT, FLT, STR, ARR, FILE) | `SET INT x 10` |
| `OUT` | Print to console with piping | `OUT "Val: " <- x` |
| `INP` | Take user input into a variable | `INP x` |
| `ADD` | Addition (Src1, Src2, Dest) | `ADD x 5 x` |
| `SUB` | Subtraction (Src1, Src2, Dest) | `SUB x 1 x` |
| `MUL` | Multiplication (Src1, Src2, Dest) | `MUL x 2 x` |
| `DIV` | Division (Src1, Src2, Dest) | `DIV x 2 x` |
| `MOD` | Modulo (Src1, Src2, Dest) | `MOD x 3 x` |
| `INC` | Increment a variable by 1 | `INC x` |
| `DEC` | Decrement a variable by 1 | `DEC x` |
| `JMP` | Jump to a label or line number | `JMP LOOP` |
| `JZ`  | Jump if variable is zero (Var, Target) | `JZ x WIN` |
| `JNZ` | Jump if variable is not zero (Var, Target) | `JNZ x LOOP` |
| `CAL` | Call a subroutine | `CAL MY_FUNC` |
| `RET` | Return from a subroutine | `RET` |
| `SLP` | Pause execution (seconds) | `SLP 1.5` |
| `RNG` | Generate random int (Min, Max, Dest) | `RNG 1 100 x` |
| `OPN` | Open a file (R, W, A) | `OPN f "file.txt" A` |
| `RED` | Read file lines into an ARR | `RED f my_list` |
| `WRT` | Write to a file with piping | `WRT f <- "Data"` |
| `CLS` | Close a file handle | `CLS f` |
| `CLR` | Clear the console screen | `CLR` |
| `HLT` | Terminate the program | `HLT` |
## Created by PixelKc