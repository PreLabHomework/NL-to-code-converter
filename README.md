# Natural Language to Code Converter

A rule based command line tool that translates simple English programming requests into starter code across Python, C++, Java, and MATLAB.

This project was built to reduce basic syntax lookup for beginner programming tasks. It is not an LLM or full code assistant. Instead, it uses structured parsing and regex based intent detection to generate predictable starter code for common programming patterns.

## Supported languages

- Python
- C++
- Java
- MATLAB

## What it can generate

The converter supports common beginner programming intents, including:

- print statements
- variables
- loops
- nested loops
- classes
- file writing
- file opening
- try and except blocks
- simple reusable code templates

## How it works

The tool takes a plain English prompt, detects the likely programming intent, then maps that intent to a language specific code template.

Example prompts:

```text
make a for loop from 1 to 10
print hello world
create a class called Student
write text to a file
open a file with error handling

Files
File	Description
code_generator.py	Main command line program
examples.txt	Example prompts to test the generator
USER_MANUAL.md	Beginner friendly usage guide
Requirements
Python 3.9 or newer
Running the tool
python code_generator.py

After starting the program:

Pick a target language.
Type a plain English prompt.
Press Enter on a blank line to generate code.
Type exit to quit.
Execution mode

Python execution is supported inside the tool.

For C++, Java, and MATLAB, copy the generated code into the correct environment and run it there.

Skills demonstrated
Python command line development
Rule based NLP
Regex pattern matching
Intent parsing
Code generation
Multi language syntax mapping
Beginner focused software tooling
Limitations

This tool is designed for simple programming requests. It does not understand complex project context, external libraries, multi file applications, or ambiguous prompts. The goal is to generate clear starter code, not replace a full programming assistant.
