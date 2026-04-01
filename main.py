# Yeast - a bread transpiler
import os

_vars = {}

___path_sep  = "\\" if os.name == "nt" else "/"

__input_file = "example.yeast"
__output_file= "output.bin"

__is_yeast   = __input_file.endswith(".yeast")

def error(string) -> None:
	print(string)
	exit(67420)

def __file2abs_dir(file) -> str:
	expanded = os.path.expanduser(file)
	absolute = os.path.abspath(expanded)
	directory = os.path.dirname(absolute)

	return directory

def to_c(string) -> str:
	string = string.strip()
	_string = string.split("/")

	command = _string[0]
	args    = _string[1:]

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
		elif command == "@":
			command = "print"

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
				error("Compiler Error: Only 1-2 int arguments, "+str(command))
		case "bol":
			_vars[arg] = "bol"
			if len(args) == 1:
				return f'bool {arg};'
			elif len(args) == 2:
				return f'bool {args[0]} = {args[1]};'
			else:
				error("Compiler Error: Only 1-2 bol/bool arguments, "+str(command))
		case "str":
			_vars[arg] = "str"
			if len(args) == 1:
				return f'string {arg};'
			elif len(args) == 2:
				return f'string {args[0]} = {args[1]};'
			else:
				error("Compiler Error: Only 1-2 str/string arguments, "+str(command))
		case "exit":
			if len(args) == 1:
				return f'exit({arg});'
			elif len(args) == 0:
				return f'exit(0);'
			else:
				error("Compiler Error: Only 0-1 exit arguments, "+str(command))
		case "if":
			if len(args) != 3:
				error("Compiler Error: if requires 3 arguments, "+str(command))
			ops = {"equals": "==", "notequals": "!=", "greater": ">", "less": "<"}
			if args[1] not in ops:
				error(f"Compiler Error: Unknown operator '{args[1]}'")
			op = ops[args[1]]
			return f'if ({args[0]} {op} {args[2]}) {{'
		case "endif":
			return '}'
		case "while":
			if len(args) == 1:
				if arg not in _vars or _vars[arg] != "bol":
					error(f"Compiler Error: '{arg}' is not a bool")
				return f'while ({arg}) {{'
			elif len(args) == 3:
				ops = {"equals": "==", "notequals": "!=", "greater": ">", "less": "<"}
				if args[1] not in ops:
					error(f"Compiler Error: Unknown operator '{args[1]}'")
				op = ops[args[1]]
				return f'while ({args[0]} {op} {args[2]}) {{'
			else:
				error("Compiler Error: while takes 1 or 3 arguments")
		case "endwhile":
			return '}'
		case "add":
			# add / xxx / 1
			# cmd / arg / args[1]

			if len(args) == 1:
				if not __is_yeast:
					error("Compiler Error: Only 2 add arguments, "+str(command))
				else:
					return f'{arg}++;'
			elif len(args) == 2:
				if arg in _vars and _vars[arg] == "int":
					return f'{arg} += {args[1]};'
				else:
					error("Compiler Error: Cannot add non-ints (or nonexistants!), "+str(command))
			else:
				error("Compiler Error: Only 1-2 add arguments, "+str(command))
		case "sub":
			if len(args) == 1:
				if not __is_yeast:
					error("Compiler Error: Only 2 subtract arguments, "+str(command))
				else:
					return f'{arg}--;'
			elif len(args) == 2:
				if arg in _vars and _vars[arg] == "int":
					return f'{arg} -= {args[1]};'
				else:
					error("Compiler Error: Cannot subtract non-ints (or nonexistants!), "+str(command))
			else:
				error("Compiler Error: Only 1-2 sub/subtract arguments, "+str(command))
		case "mul":
			if len(args) == 1:
				error("Compiler Error: Only 2 mul arguments, "+str(command))
			elif len(args) == 2:
				if arg in _vars and _vars[arg] == "int":
					return f'{arg} *= {args[1]};'
				else:
					error("Compiler Error: Cannot mul non-ints (or nonexistants!), "+str(command))
			else:
				error("Compiler Error: Only 1-2 mul/multiply arguments, "+str(command))
		case "div":
			if len(args) == 1:
				error("Compiler Error: Only 2 div arguments, "+str(command))
			elif len(args) == 2:
				if arg in _vars and _vars[arg] == "int":
					return f'{arg} /= {args[1]};'
				else:
					error("Compiler Error: Cannot div non-ints (or nonexistants!), "+str(command))
			else:
				error("Compiler Error: Only 1-2 div/divide arguments, "+str(command))
		case "mod":
			if len(args) == 1:
				error("Compiler Error: Only 2 mod arguments, "+str(command))
			elif len(args) == 2:
				if arg in _vars and _vars[arg] == "int":
					return f'{arg} = {arg} % {args[1]};'
				else:
					error("Compiler Error: Cannot mod non-ints (or nonexistants!), "+str(command))
			else:
				error("Compiler Error: Only 1-2 mod/modulus arguments, "+str(command))
		case "wait":
			if arg in _vars or arg.isdigit():
				return f'wait({arg});'
			else:
				error("Compiler Error: Only 1 wait argument, "+str(command))
		case "shrtct": 
			pass # NI
		case _:
			error("Compiler Error: Unknown Command, "+str(command))

def gen_boilerplate(path):
	with open(path, "wt") as source:
		source.write("""
// Generated with the Yeast Programming Language
// https://github.com/SoftPankek7/Yeast. Based on the Bread programming language, see:
// https://github.com/angrypig555/bread.
// Compiler is MIT Licensed!!!

#include "yeast.h"
int main() {
""")
	
	with open(f"{__file2abs_dir(path)}{___path_sep}yeast.h", "wt") as header:
		header.write("""
// Generated with the Yeast Programming Language
// https://github.com/SoftPankek7/Yeast. Based on the Bread programming language, see:
// https://github.com/angrypig555/bread.
// Compiler is MIT Licensed!!!
			   
#ifndef YEAST_RUNTIME_H
#define YEAST_RUNTIME_H
					 
#include <stdio.h>
#include <stdbool.h>
#include <unistd.h>

typedef char* string;

#define print_str(x)  printf("%s\n", x)
#define print_int(x)  printf("%d\n", x)
#define print_bol(x)  printf("%d\n", x)

#define input(x)      fgets(x, 65536, stdin);

#define wait(x)       sleep(x)

#endif
""")

def _compile_file(path, out):
	gen_boilerplate(out)

	with open(path, 'rt') as _input_file, open(out, "at") as _output_file:
		if __is_yeast: # Bread requires you to define True/False. I made sure it is defined.
			_output_file.write(to_c("bool/True/true")+"\n")
			_output_file.write(to_c("bool/False/false")+"\n")
				
		for line in _input_file:
			if line.strip() == "":
				continue
				
			if line[0:2] == ";;" and __is_yeast: # Bread doesnt allow comments
				continue
				
			_output_file.write(to_c(line)+"\n")

		_output_file.write("return 0;\n")
		_output_file.write("}\n")

if __name__ == "__main__":
	_compile_file(__input_file, __output_file)