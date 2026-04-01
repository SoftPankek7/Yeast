# Yeast - a bread transpiler
import os

_vars = {}

# Expected:
#
# {
#     "foo": "int"
# }

___path_sep  = "\\" if os.name == "nt" else "/"

__input_file = "example.bread"
__output_file= "output.bin"

__is_yeast   = __input_file.endswith(".yeast")


def __file2abs_dir(file):
	expanded = os.path.expanduser(file)
	absolute = os.path.abspath(expanded)
	directory = os.path.dirname(absolute)

	return directory

def to_c(string):
	_string = string.split("/")

	command = _string[0]
	arg     = _string[1]

	match command:
		case "print":
			return f'printf({arg[1]});'
		case _:
			print("Compiler Error: Unknown Command, "+str(command))

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
#define print_str(x)  printf("%d\n", x)

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