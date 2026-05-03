# Yeast - an improved bread transpiler, rewritten in Python
import os
import shutil
import subprocess
import sys

version = "1.0.1"

___settings = {
	"keepTempC": False, # Whether it should keep tmp.c for future use
	"forceComp": False, # Could be a string set to the compiler (GCC, CLANG, CL, ETC.)
	"forceYeast":False, # Whether it should check if it is yeast or not
	"forceBread":False, # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑ bread ↑↑↑↑↑↑

	"inputFile": "program.yeast", # ALWAYS a str
	"outputFile":"output"         # ↑↑↑↑↑↑↑↑↑↑↑↑
}


_vars = {}
_funcs = []

___path_sep  = "\\" if os.name == "nt" else "/"

def error(string) -> None:
	print(string)
	exit(67420)

def _help():
	print(f"""Yeast v{version} Help

Flags:
	   -o=            | Set output file
	   --keep-c       | Keep the source file (C source code)
	   --comp=        | Set/remove compiler (rather than auto-select it)
	   --force-yeast  | Force yeast options - dont auto-detect it
	   --force-bread  | Force bread options - dont auto-detect it

Deafults:
	   -o=output      | Save to ./output
	   --keep-c       | False""")

if len(sys.argv) < 2:
	error("Usage: python main.py <file> [options]")

___settings["inputFile"] = sys.argv[1]

for i in sys.argv[2:]:
	if i == "--help":
		_help()
		exit(0)
	elif i.startswith("-o="):
		___settings["outputFile"] = i[len("-o="):]
	elif i == "--keep-c":
		___settings["keepTempC"] = True
	elif i.startswith("--comp="):
		___settings["forceComp"] = i[len("--comp="):]
	elif i == "--force-yeast":
		___settings["forceYeast"] = True
	elif i == "--force-bread":
		___settings["forceBread"] = True
	else:
		error(f"Unknown argument '{i}'")

if ___settings["forceBread"]:
	__is_yeast = False
elif ___settings["forceYeast"]:
	__is_yeast = True
else:
	__is_yeast = ___settings["inputFile"].endswith(".yeast")

def __file2abs_dir(file) -> str:
	expanded = os.path.expanduser(file)
	absolute = os.path.abspath(expanded)
	directory = os.path.dirname(absolute)

	return directory

from typing import Optional

def to_c(string) -> Optional[str]:
	string = string.strip()
	_string = string.split("/")

	command = _string[0]
	args    = _string[1:]

	if command == "\\":
		return string[1:]

	if len(args) == 0:
		arg = ""
	else:
		arg = args[0]

	if __is_yeast: # Speeds up non-yeast compile time by a bit
		if command == "bool": # Bread doesnt like bool, it wants bol.
			command = "bol"
		elif command == "string": # Same with string & str
			command = "str"
		elif command == "subtract":
			command = "sub"
		elif command == "multiply":
			command = "mul"
		elif command == "divide":
			command = "div"
		elif command == "modulus":
			command = "mod"
		elif command == "func" or command == "function":
			command = "shrtct"

	match command:
		case "print":
			if arg in _vars:
				return f'print_{_vars[arg]}({arg});'
			else:
				return f'print_str("{arg}");'
		case "in":
			_vars[arg] = "str"
			return f'input({arg});'
		case  "int":
			_vars[arg] = "int"
			if len(args) == 1:
				return f'int {arg};'
			elif len(args) == 2:
				return f'int {args[0]} = {args[1]};'
			else:
				___to_c_err("Only 1-2 int arguments, "+str(command))
		case "bol":
			_vars[arg] = "bol"
			if len(args) == 1:
				return f'bool {arg};'
			elif len(args) == 2:
				return f'bool {args[0]} = {args[1]};'
			else:
				___to_c_err("Only 1-2 bol/bool arguments, "+str(command))
		case "str":
			_vars[arg] = "str"
			if len(args) == 1:
				return f'string {arg};'
			elif len(args) == 2:
				return f'string {args[0]} = {args[1]};'
			else:
				___to_c_err("Only 1-2 str/string arguments, "+str(command))
		case "exit":
			if len(args) == 1:
				return f'exit({arg});'
			elif len(args) == 0:
				return f'exit(0);'
			else:
				___to_c_err("Only 0-1 exit arguments, "+str(command))
		case "if":
			if len(args) != 3:
				___to_c_err("if requires 3 arguments, "+str(command))
			ops = {"equals": "==", "notequals": "!=", "greater": ">", "less": "<"}
			if args[1] not in ops:
				___to_c_err(f"Unknown operator '{args[1]}'")
			op = ops[args[1]]
			return f'if ({args[0]} {op} {args[2]}) {{'
		case "else":
			if __is_yeast:
				return "} else {"
			else:
				___to_c_err(command)
		case "endif":
			return "}"
		case "while":
			if len(args) == 1:
				if arg not in _vars or _vars[arg] != "bol":
					___to_c_err(f"'{arg}' is not a bool")
				return f'while ({arg}) {{'
			elif len(args) == 3:
				ops = {"equals": "==", "notequals": "!=", "greater": ">", "less": "<"}
				if args[1] not in ops:
					___to_c_err(f"Unknown operator '{args[1]}'")
				op = ops[args[1]]
				return f'while ({args[0]} {op} {args[2]}) {{'
			else:
				___to_c_err("while takes 1 or 3 arguments")
		case "endwhile":
			return '}'
		case "add":
			if len(args) == 1:
				if not __is_yeast:
					___to_c_err("Only 2 add arguments, "+str(command))
				else:
					return f'{arg}++;'
			elif len(args) == 2:
				if arg in _vars and _vars[arg] == "int":
					return f'{arg} += {args[1]};'
				else:
					___to_c_err("Cannot add non-ints (or nonexistants!), "+str(command))
			else:
				___to_c_err("Only 1-2 add arguments, "+str(command))
		case "sub":
			if len(args) == 1:
				if not __is_yeast:
					___to_c_err("Only 2 subtract arguments, "+str(command))
				else:
					return f'{arg}--;'
			elif len(args) == 2:
				if arg in _vars and _vars[arg] == "int":
					return f'{arg} -= {args[1]};'
				else:
					___to_c_err("Cannot subtract non-ints (or nonexistants!), "+str(command))
			else:
				___to_c_err("Only 1-2 sub/subtract arguments, "+str(command))
		case "mul":
			if len(args) == 1:
				___to_c_err("Only 2 mul arguments, "+str(command))
			elif len(args) == 2:
				if arg in _vars and _vars[arg] == "int":
					return f'{arg} *= {args[1]};'
				else:
					___to_c_err("Cannot mul non-ints (or nonexistants!), "+str(command))
			else:
				___to_c_err("Only 1-2 mul/multiply arguments, "+str(command))
		case "div":
			if len(args) == 1:
				___to_c_err("Only 2 div arguments, "+str(command))
			elif len(args) == 2:
				if arg in _vars and _vars[arg] == "int":
					return f'{arg} /= {args[1]};'
				else:
					___to_c_err("Cannot div non-ints (or nonexistants!), "+str(command))
			else:
				___to_c_err("Only 1-2 div/divide arguments, "+str(command))
		case "mod":
			if len(args) == 1:
				___to_c_err("Only 2 mod arguments, "+str(command))
			elif len(args) == 2:
				if arg in _vars and _vars[arg] == "int":
					return f'{arg} = {arg} % {args[1]};'
				else:
					___to_c_err("Cannot mod non-ints (or nonexistants!), "+str(command))
			else:
				___to_c_err("Only 1-2 mod/modulus arguments, "+str(command))
		case "wait":
			if arg in _vars or arg.isdigit():
				return f'wait({arg});'
			else:
				___to_c_err("Only 1 wait argument, "+str(command))
		case "shrtct":
			if arg == "":
				___to_c_err("shortcut must have a name")
			_funcs.append(arg)
			return f"§void {arg}() {{"  # § prefix = goes to func buffer, not main

		case "endshrtct":
			return "§}"
		
		case "loop":
			if not __is_yeast:
				___to_c_err(command)
				
			if not arg.isdigit():
				___to_c_err("loop requires a number")
			if len(args) < 2:
				___to_c_err("loop requires a command")
			inner = to_c("/".join(args[1:]))
			return "\n".join([inner] * int(arg))
		case _:
			if string.strip() in _funcs:
				return f"{string.strip()}();"
			___to_c_err(f"Unknown command '{command}'")

def ___to_c_err(string):
	error(f"Compiler Error: {string}")

def gen_boilerplate(path):
	with open(path, "wt") as source:
		source.write("""
// Generated with the Yeast Programming Language
// https://github.com/SoftPankek7/Yeast.
//
// Based on the Bread programming language, see:
// https://github.com/angrypig555/bread.
//
// The whole project is MIT Licensed!!!
// This includes the compiler, generated header, and anything originating from the repository.

#include "yeast.h"
""")
	
	with open(f"{__file2abs_dir(path)}{___path_sep}yeast.h", "wt") as header:
		header.write("""
// Generated with the Yeast Programming Language
// https://github.com/SoftPankek7/Yeast. Based on the Bread programming language, see:
// https://github.com/angrypig555/bread.
// The whole project is MIT Licensed!!!
// This includes the compiler, generated header, and anything originating from the repository.

// Header v2

#ifndef YEAST_RUNTIME_H
#define YEAST_RUNTIME_H

#include <stdio.h>
#include <stdbool.h>
#include <unistd.h>
#include <stdlib.h>

typedef char* string;

#define print_str(x)  printf("%s\\n", x);
#define print_int(x)  printf("%d\\n", x);
#define print_bol(x)  printf("%d\\n", x);

#define input(x)      fgets(x, 65536, stdin);
#define wait(x)       sleep(x);

#endif
""")

def _get_compiler():
	if ___settings["forceComp"] == False:
		if shutil.which("gcc"):
			return ["gcc", "tmp.c", "-o", ___settings["outputFile"]]
		elif shutil.which("cc"):
			return ["cc", "tmp.c", "-o", ___settings["outputFile"]]
		elif shutil.which("cl"):
			return ["cl", "tmp.c", "/O2", "/Fe" + ___settings["outputFile"]]
		elif shutil.which("eccp"):
			return ["eccp", "tmp.c", "-m", "-o", ___settings["outputFile"]]
		elif shutil.which("ibm-clang"):
			return ["ibm-clang", "tmp.c", "-o", ___settings["outputFile"]] # I couldnt find any good docs - if you know how to use it & this is wrong, shoot a PR
		elif shutil.which("clang"):
			return ["clang", "tmp.c", "-o", ___settings["outputFile"]]
		else:
			___to_c_err("No compilers found. Compatibles: gcc, cc, cl, eccp, ibm-clang, clang")
	else:
		match ___settings["forceComp"].lower():
			case "gcc":
				return ["gcc", "tmp.c", "-o", ___settings["outputFile"]]
			case "cc":
				return ["cc", "tmp.c", "-o", ___settings["outputFile"]]
			case "cl":
				return ["cl", "tmp.c", "/O2", "/Fe" + ___settings["outputFile"]]
			case "eccp":
				return ["eccp", "tmp.c", "-m", "-o", ___settings["outputFile"]]
			case "ibm-clang":
				return ["ibm-clang", "tmp.c", "-o", ___settings["outputFile"]] # I couldnt find any good docs
			case "clang":
				return ["clang", "tmp.c", "-o", ___settings["outputFile"]]     # Anything but clang
			case "dont":
				___settings["keepTempC"] = True
				return [sys.executable, "-c", "pass"]
			case _:
				___to_c_err("Forced compiler is not availible.")

	return []

def _inter_compiler(file):
	result = subprocess.run(_get_compiler(), capture_output=True, text=True)
	if result.returncode != 0:
		print(result.stdout)
		print(result.stderr)
		___to_c_err("C compilation failed")

def _compile_file(path, out):
	gen_boilerplate(out)
	
	func_lines = []
	main_lines = []

	with open(path, 'rt') as _input_file:
		if __is_yeast:
			main_lines.append(to_c("bool/True/true"))
			main_lines.append(to_c("bool/False/false"))

		for line in _input_file:
			if ";;" in line: # See CHANGES.md
				line = line.split(";;", 1)[0]
			if line.strip() == "":
				continue
			if line[0:2] == ";;" and __is_yeast:
				continue
			result = to_c(line)
			if result is None:
				continue
			if result.startswith("§"):
				func_lines.append(result[1:])
			else:
				if _loop_num == 0:
					main_lines.append(result)
				else:
					while _loop_num != 0:
						main_lines.append(result)
						_loop_num -= 1

	with open(out, "at") as _output_file:
		for line in func_lines:
			_output_file.write(line + "\n")
		_output_file.write("int main(int argc, char *argv[]) {\n")
		for line in main_lines:
			_output_file.write(line + "\n")
		_output_file.write("return 0;\n}\n")

if __name__ == "__main__":
	print(f"Yeast v{version}")
	try:
		_compile_file(___settings["inputFile"], "tmp.c")
		_inter_compiler("tmp.c")
	finally:
		if os.path.exists("tmp.c"):
			if not ___settings["keepTempC"]:
				os.remove("tmp.c")