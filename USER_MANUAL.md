# User Manual (Beginner)

## 1) Start the program
Open a terminal in the folder where `code_generator.py` is saved, then run:

```bash
python code_generator.py
```

## 2) Choose a language
Type one of:
- python
- c++
- java
- matlab

Press Enter.

## 3) Type what you want (very simple English is OK)
Type one instruction per line. When you’re done, press **Enter on a blank line**.
That tells the tool: “generate code now.”

### Common things it understands

#### A) Loop N times
- “can i have a for loop that loops around 5 times”
- “make a loop that repeats 10 times”
- “loop 3 times”

#### B) Print / show something
- “print 'hello'”
- “show x”
- “display result”

#### C) Set a variable
- “set x to 5”
- “make total equal 10”

#### D) Make a class with attributes
- “create a class named Person with attributes name and age”

#### E) Write text to a file
- “write hello into a file called out.txt”
- “save 'hi' to a file named notes.txt”

#### F) Try to open a file and print error if it fails
- “try to open a file named data.txt, if it fails print Error”

#### G) Nested loops over a matrix
- “for each row in matrix, for each column in row, print value”

## 4) If you see “Could not parse”
That means the sentence didn’t match any known pattern.

Quick fixes:
- Include a number for loops: “repeat **5** times”
- Use keywords like: loop / function / class / print / set / write / file / try open
- Keep it to one idea per line.

## 5) Execution
Only Python can be executed inside this tool:
- After code is generated, answer `y` to “Execute?”
For C++/Java/MATLAB, copy the generated code into your IDE and run normally.
