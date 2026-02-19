# Natural Language → Code Converter (Python/C++/Java/MATLAB)

This is a small CLI tool that turns **very plain English** into starter code in:
- Python
- C++
- Java
- MATLAB

It’s **rule-based** (regex patterns), so it works best for common beginner intents:
loops, prints, variables, classes, file write, try/open file, nested loops.

## Files
- `code_generator.py` — the main program
- `examples.txt` — example prompts you can copy/paste
- `USER_MANUAL.md` — beginner-friendly instructions

## Requirements
- Python 3.9+ recommended

## Run
```bash
python code_generator.py
```

Pick a language, then type prompts. Press **Enter on a blank line** to generate code.
Type `exit` to quit.

## Notes
- “Execution mode” is only implemented for **Python** inside this tool.
  For C++/Java/MATLAB, copy the generated code into your environment and run it there.
