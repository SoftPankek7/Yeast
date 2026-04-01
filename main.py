# Yeast - a bread transpiler
import os

_vars = {}

# Expected:
#
# {
#     "foo": "int",
#	  "bar": "str",
# 	  "baz": "bol"         # (Or bool too, if on yeast)
# }

___path_sep  = "\\" if os.name == "nt" else "/"

__input_file = "example.bread"
__output_file= "output.bin"

__is_yeast   = __input_file.endswith(".yeast")


def error(string):
	print(string)
	exit(67420)

def __file2abs_dir(file):
	expanded = os.path.expanduser(file)
	absolute = os.path.abspath(expanded)
	directory = os.path.dirname(absolute)

	return directory

def to_c(string):
	_string = string.split("/")

	command = _string[0]
	args    = _string[1:]

	if len(args) == 0:
		arg = ""
	else:
		arg = args[0]

	if command == "bool" and __is_yeast: # Bread doesnt like bool, it wants bol.
		command = "bol"
	elif command == "string" and __is_yeast:# Same with string & str
		command = "str"

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
			pass # Not Implemented (NI)
		case "while":
			pass # NI
		case "add":
			pass # Soon to be implemented
		case "sub":
			pass # Soon to be implemented
		case "mul":
			pass # Soon to be implemented
		case "div":
			pass # Soon to be implemented
		case "mod":
			pass # Soon to be implemented
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
		for line in _input_file:
			if line.strip() == "":
				continue
				
			if line[0:2] == ";;" and __is_yeast: # Bread doesnt allow comments
				continue

			print(to_c(line))

		print("}")

if __name__ == "__main__":
	_compile_file(__input_file, __output_file)