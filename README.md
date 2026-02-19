# NL-to-code-converter
A rule-based command-line tool that translates plain English instructions  into code across 4 programming languages.
## Overview

This tool is designed to make code generation accessible to beginners by 
accepting natural, conversational input and converting it into working code. 
No AI or external APIs required — fully rule-based and offline.

## Supported Languages

- Python
- C++
- Java
- MATLAB

## What It Can Generate

- Loops (`"repeat 5 times"`, `"loop around 5 times"`)
- Variables (`"set x to 10"`)
- Print statements (`"print hello"`, `"show x"`)
- Classes (`"create a class named Person with attributes name and age"`)
- File writing (`"write 'hello' into a file called out.txt"`)
- Error handling (`"try to open file, if it fails print error"`)
- Nested loops (`"for each row in matrix"`)

## How to Use

1. Clone the repo and navigate to the folder
2. Run the program:
```bash
python code_generator.py
```
3. Choose your language (`python`, `c++`, `java`, `matlab`)
4. Type one instruction per line
5. Press Enter on an empty line to generate code

## Example
```
Choose language: python
Enter instructions (empty line to generate):
> set x to 10
> repeat 5 times
> print hello
>

Generated Python code:
x = 10
for i in range(5):
    pass
print("hello")
```

## Files

| File | Description |
|------|-------------|
| `code_generator.py` | Main program |
| `README.md` | Quick start guide |
| `USER_MANUAL.md` | Beginner-friendly full manual |
| `examples.txt` | Copy-paste prompts to try |

## Features

- Execution mode: generated Python code can be run immediately
- No internet connection or API keys required
- Beginner friendly — conversational input accepted

## Tools

- Python 3.x
- Standard library only (no dependencies)
