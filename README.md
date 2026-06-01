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
