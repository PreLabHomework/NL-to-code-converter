import re

def parse_line(nl_line, language):
    """
    Converts a single line of vague natural language into a code snippet for the specified language.
    The regex patterns have been broadened to capture more casual phrasing.
    """
    original_line = nl_line.strip()
    line = original_line.lower().strip()
    if not line:
        return ""

    # ----------------------------
    # Helpers
    # ----------------------------
    def comment(text: str) -> str:
        if language == "python":
            return f"# {text}"
        if language in ["c++", "java"]:
            return f"// {text}"
        return f"% {text}"

    # ----------------------------
    # Comments
    # ----------------------------
    m = re.match(r'(?:comment|add comment)\s*:\s*(.+)', line, re.IGNORECASE)
    if m:
        return comment(m.group(1))

    # ----------------------------
    # Vague For Loop (repeat N times)
    # Examples:
    #   "can i have a for loop that loops around 5 times"
    #   "make a loop that repeats 10 times"
    #   "loop 3 times"
    # ----------------------------
    m = re.search(
        r'(?:can i have|please give me|i need|i want|make|create|give me)?\s*'
        r'(?:a\s+)?(?:for\s+loop|loop)\s*'
        r'(?:that\s+)?(?:loops\s+around|repeats|runs|iterates|goes\s+through)?\s*'
        r'(\d+)\s*(?:times?)',
        line,
        re.IGNORECASE
    )
    if m:
        count = m.group(1)
        if language == "python":
            return f"for i in range({count}):\n    print(i)"
        if language == "c++":
            return f"for (int i = 0; i < {count}; i++) {{\n    std::cout << i << std::endl;\n}}"
        if language == "java":
            return f"for (int i = 0; i < {count}; i++) {{\n    System.out.println(i);\n}}"
        return f"for i = 1:{count}\n    disp(i)\nend"

    # ----------------------------
    # Nested loops (matrix / rows / columns)
    # Example:
    #   "for each row in matrix, for each column in row, print value"
    # ----------------------------
    m = re.search(
        r'for each row in (\w+)\s*,?\s*for each (\w+)\s*in row\s*,?\s*print\s+(.+)',
        line, re.IGNORECASE
    )
    if m:
        collection = m.group(1)
        inner_var = m.group(2)
        print_val = m.group(3).strip()
        if print_val.lower() == "value":
            print_val = inner_var

        if language == "python":
            return f"for row in {collection}:\n    for {inner_var} in row:\n        print({print_val})"
        if language == "c++":
            return (
                f"for (auto row : {collection}) {{\n"
                f"    for (auto {inner_var} : row) {{\n"
                f"        std::cout << {print_val} << std::endl;\n"
                f"    }}\n"
                f"}}"
            )
        if language == "java":
            # Assumes a 2D array. For collections, users can adjust.
            return (
                f"for (int i = 0; i < {collection}.length; i++) {{\n"
                f"    for (int j = 0; j < {collection}[i].length; j++) {{\n"
                f"        System.out.println({collection}[i][j]);\n"
                f"    }}\n"
                f"}}"
            )
        # MATLAB matrix iteration
        return (
            f"for i = 1:size({collection}, 1)\n"
            f"    for j = 1:size({collection}, 2)\n"
            f"        disp({collection}(i,j))\n"
            f"    end\n"
            f"end"
        )

    # ----------------------------
    # Vague Function Definition
    # Examples:
    #   "i need a function called add that takes two numbers and returns a + b"
    #   "make a function called greet that takes name and prints 'hi'"
    # ----------------------------
    m = re.search(
        r'(?:can i have|i need|please give me|create|make|write)?\s*'
        r'(?:a\s+)?function\s*(?:called\s+|named\s+)?(\w+)\s*'
        r'(?:that\s+)?(?:takes|accepts|with)?\s*(.*?)'
        r'(?:\s+and\s+(?:returns|gives|outputs|prints)\s+(.+))?$',
        line,
        re.IGNORECASE
    )
    if m and "function" in line:
        func_name = m.group(1)
        params_str = (m.group(2) or "").strip()
        action = (m.group(3) or "").strip()

        # Light normalization for common phrases
        params = ""
        if params_str:
            if "two numbers" in params_str:
                params = "a, b"
            elif "one number" in params_str:
                params = "a"
            else:
                # Replace words like "and" with comma in params, then clean
                params = re.sub(r'\band\b', ',', params_str)
                params = re.sub(r'\s+', ' ', params).strip()
        # Default behavior if not specified
        if not action:
            action = f"print('{func_name} called')"

        if language == "python":
            return f"def {func_name}({params}):\n    {action}"
        if language == "c++":
            return f"void {func_name}({params}) {{\n    {action};\n}}"
        if language == "java":
            return f"public void {func_name}({params}) {{\n    {action};\n}}"
        return f"function {func_name}({params})\n    {action}\nend"

    # ----------------------------
    # Vague Class Definition
    # Examples:
    #   "create a class named Person with attributes name and age"
    #   "make a class called Car with attributes brand, year"
    # ----------------------------
    m = re.search(
        r'(?:can i have|please create|make|create|write)?\s*'
        r'(?:a\s+)?class\s*(?:called|named)\s+(\w+)'
        r'(?:\s+with\s+attributes?\s+(.+))?',
        line,
        re.IGNORECASE
    )
    if m and "class" in line:
        class_name = m.group(1)
        attributes = (m.group(2) or "").strip()

        # Parse attributes "name and age" / "name, age"
        attrs = []
        if attributes:
            attrs = [a.strip() for part in attributes.split("and") for a in part.split(",")]
            attrs = [a for a in attrs if a]

        if language == "python":
            if attrs:
                init_params = ", ".join(attrs)
                assignments = "\n        ".join([f"self.{a} = {a}" for a in attrs])
                return f"class {class_name}:\n    def __init__(self, {init_params}):\n        {assignments}"
            return f"class {class_name}:\n    pass"

        if language == "c++":
            if attrs:
                decls, params, inits = [], [], []
                for a in attrs:
                    t = "int" if a.lower() == "age" else "std::string" if a.lower() == "name" else "auto"
                    decls.append(f"    {t} {a};")
                    params.append(f"{t} {a}")
                    inits.append(f"{a}({a})")
                params_str = ", ".join(params)
                init_list = " : " + ", ".join(inits) if inits else ""
                return (
                    f"class {class_name} {{\n"
                    f"public:\n"
                    f"{chr(10).join(decls)}\n"
                    f"    {class_name}({params_str}){init_list} {{}}\n"
                    f"}};"
                )
            return f"class {class_name} {{\n}};"

        if language == "java":
            if attrs:
                decls, params, assigns = [], [], []
                for a in attrs:
                    t = "int" if a.lower() == "age" else "String" if a.lower() == "name" else "Object"
                    decls.append(f"    {t} {a};")
                    params.append(f"{t} {a}")
                    assigns.append(f"        this.{a} = {a};")
                return (
                    f"public class {class_name} {{\n"
                    f"{chr(10).join(decls)}\n\n"
                    f"    public {class_name}({', '.join(params)}) {{\n"
                    f"{chr(10).join(assigns)}\n"
                    f"    }}\n"
                    f"}}"
                )
            return f"public class {class_name} {{\n}}"

        # MATLAB
        if attrs:
            props = "\n       ".join(attrs)
            params = ", ".join(attrs)
            assigns = "\n           ".join([f"obj.{a} = {a};" for a in attrs])
            return (
                f"classdef {class_name}\n"
                f"   properties\n"
                f"       {props}\n"
                f"   end\n"
                f"   methods\n"
                f"       function obj = {class_name}({params})\n"
                f"           {assigns}\n"
                f"       end\n"
                f"   end\n"
                f"end"
            )
        return f"classdef {class_name}\nend"

    # ----------------------------
    # Exception handling: try open file, else print error
    # Examples:
    #   "try to open a file named data.txt, if it fails print Error"
    #   "try opening data.txt, if it fails print 'Error'"
    # ----------------------------
    m = re.search(
        r'try\s+(?:to\s+)?open(?:ing)?\s+(?:a\s+)?file(?:\s+named\s+|\s+called\s+)?(\S+)?\s*,?\s*'
        r'(?:and\s+)?(?:if it fails|if it doesn\'t work|on error|if error)\s+print\s+["\']?([^"\']+)["\']?',
        line, re.IGNORECASE
    )
    if m:
        filename = m.group(1) or "file.txt"
        msg = m.group(2)

        if language == "python":
            return f"try:\n    f = open('{filename}', 'r')\nexcept Exception:\n    print('{msg}')"
        if language == "c++":
            return (
                "#include <iostream>\n#include <fstream>\n#include <stdexcept>\n\n"
                "try {\n"
                f"    std::ifstream file(\"{filename}\");\n"
                "    if (!file) {\n"
                f"        throw std::runtime_error(\"{msg}\");\n"
                "    }\n"
                "} catch (const std::exception &e) {\n"
                "    std::cout << e.what() << std::endl;\n"
                "}"
            )
        if language == "java":
            return (
                "try {\n"
                f"    java.io.FileReader fr = new java.io.FileReader(\"{filename}\");\n"
                "} catch (Exception e) {\n"
                f"    System.out.println(\"{msg}\");\n"
                "}"
            )
        return (
            "try\n"
            f"    fid = fopen('{filename}', 'r');\n"
            "    if fid == -1, error('File error'); end\n"
            "catch\n"
            f"    disp('{msg}')\n"
            "end"
        )

    # ----------------------------
    # Vague file write
    # Examples:
    #   "create a file named notes.txt and write hello"
    #   "write hello into a file called out.txt"
    # ----------------------------
    m = re.search(
        r'(?:write|put|save|store)\s+["\']?([^"\']+)["\']?\s+'
        r'(?:into|to|in)\s+(?:a\s+)?(?:text\s+)?file\s*(?:named|called)?\s*(\S+)?',
        line, re.IGNORECASE
    )
    if m:
        text = m.group(1)
        filename = m.group(2) or "output.txt"
        if language == "python":
            return f"with open('{filename}', 'w') as f:\n    f.write(\"{text}\")"
        if language == "c++":
            return (
                "#include <fstream>\n\n"
                f"std::ofstream file(\"{filename}\");\n"
                f"file << \"{text}\";\n"
                "file.close();"
            )
        if language == "java":
            return (
                "try {\n"
                f"    java.io.FileWriter fw = new java.io.FileWriter(\"{filename}\");\n"
                f"    fw.write(\"{text}\");\n"
                "    fw.close();\n"
                "} catch (Exception e) {\n"
                "    System.out.println(e);\n"
                "}"
            )
        return (
            f"fid = fopen('{filename}', 'w');\n"
            f"fprintf(fid, '{text}');\n"
            "fclose(fid);"
        )

    # ----------------------------
    # If / If-Else (some vague phrasing)
    # Examples:
    #   "if x > 10 then print 'big' else print 'small'"
    #   "if x is bigger than 10 then print big"
    # ----------------------------
    m = re.search(r'if\s+(.+?)\s*(?:,?\s*then\s+|\s+then\s+)(.+?)\s+else\s+(.+)$', line, re.IGNORECASE)
    if m:
        cond = m.group(1).strip()
        t_action = m.group(2).strip()
        f_action = m.group(3).strip()
        if language == "python":
            return f"if {cond}:\n    {t_action}\nelse:\n    {f_action}"
        if language in ["c++", "java"]:
            return f"if ({cond}) {{\n    {t_action};\n}} else {{\n    {f_action};\n}}"
        return f"if {cond}\n    {t_action}\nelse\n    {f_action}\nend"

    m = re.search(r'if\s+(.+?)\s*(?:,?\s*then\s+|\s+then\s+)(.+)$', line, re.IGNORECASE)
    if m:
        cond = m.group(1).strip()
        action = m.group(2).strip()
        if language == "python":
            return f"if {cond}:\n    {action}"
        if language in ["c++", "java"]:
            return f"if ({cond}) {{\n    {action};\n}}"
        return f"if {cond}\n    {action}\nend"

    # ----------------------------
    # Variable assignment (casual)
    # Examples:
    #   "set x to 5"
    #   "make x equal 5"
    # ----------------------------
    m = re.search(r'(?:set|make)\s+(\w+)\s+(?:to|equal|equals)\s+(.+)$', line, re.IGNORECASE)
    if m:
        var = m.group(1)
        val = m.group(2).strip()
        if language == "python":
            return f"{var} = {val}"
        if language == "c++":
            return f"auto {var} = {val};"
        if language == "java":
            return f"var {var} = {val};"
        return f"{var} = {val};"

    # ----------------------------
    # Print / display (casual)
    # Examples:
    #   "print hello"
    #   "show x"
    # ----------------------------
    m = re.search(r'(?:print|show|display)\s+(.+)$', line, re.IGNORECASE)
    if m:
        content = m.group(1).strip()
        if language == "python":
            return f"print({content})"
        if language == "c++":
            return f"std::cout << {content} << std::endl;"
        if language == "java":
            return f"System.out.println({content});"
        return f"disp({content})"

    # ----------------------------
    # Fallback
    # ----------------------------
    return comment(f"Could not parse: {original_line}")

def natural_to_code(nl_input, language):
    """
    Converts multi-line natural language input into code for the selected language.
    """
    lines = nl_input.strip().split("\n")
    return "\n".join(parse_line(line, language) for line in lines if line.strip())

def execute_code(code, language):
    """
    Executes generated code only for Python.
    """
    if language != "python":
        print("Execution is only supported for Python in this tool. Copy the output to your C++/Java/MATLAB environment.")
        return
    try:
        print("Executing the following code:")
        print("-" * 40)
        print(code)
        print("-" * 40)
        exec(code, {}, {})
    except Exception as e:
        print(f"Execution error: {e}")

def main():
    print("Select a language (Python, C++, Java, MATLAB):")
    lang_choice = input("> ").strip().lower()
    if lang_choice not in ["python", "c++", "java", "matlab"]:
        print("Unsupported language. Defaulting to Python.")
        lang_choice = "python"
    print(f"Language set to {lang_choice}.")
    print("Enter your natural language description (type 'exit' to quit).")
    print("Submit a blank line to process your multi-line input.")
    full_input = ""
    while True:
        user_input = input("> ")
        if user_input.strip().lower() == "exit":
            break
        if user_input.strip() == "":
            if not full_input.strip():
                continue
            generated_code = natural_to_code(full_input, lang_choice)
            print("\nGenerated Code:\n")
            print(generated_code)
            print("\n-----------------\n")
            if lang_choice == "python":
                run = input("Execute the generated code? (y/n): ").strip().lower()
                if run.startswith("y"):
                    execute_code(generated_code, lang_choice)
            else:
                print("Execution is not available for this language here. Copy/paste into your IDE/compiler.")
            full_input = ""
        else:
            full_input += user_input + "\n"

if __name__ == "__main__":
    main()
