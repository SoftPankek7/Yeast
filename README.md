![Yeast Logo](docs/logo.png)

# Yeast

A faster, better, and more generally improved version of [Bread programming language](https://github.com/angrypig555/bread).

> Also, instead of **C++** (that Bread compiles to), **Yeast compiles to C**
----

## Usage

```bash
python yeast.py <file> [options]
```

### Options

| Flag | Description |
|------|-------------|
| `-o=<name>` | Set output binary name (default: `./output`) |
| `--comp=<compiler>` | Force a specific compiler (`gcc`, `clang`, `cc`, `cl`, `eccp`, `ibm-clang`, `dont`) |
| `--keep-temp-c` | Keep the generated `tmp.c` file |
| `--force-yeast` | Treat the file as `.yeast` regardless of extension |
| `--force-bread` | Treat the file as `.bread` regardless of extension |

### Example

```bash
python main.py hello.yeast -o=hello
./hello
```

---

## Language Reference

### Variables

```
int/foo/5        -- integer with value
int/foo          -- empty integer
str/foo/hello    -- string with value
str/foo          -- empty string
bol/foo/true     -- boolean (true/false)
bol/foo          -- empty boolean
```

### Yeast aliases (`.yeast` only)

`bool` = `bol`, `string` = `str`, `func`/`function` = `shrtct`, `@` = `print`

### Print

```
print/Hello World!   -- print a literal string
print/foo            -- print a variable
```

### Input

```
in/foo    -- read input into string foo (auto-declares if needed)
```

### Math

```
add/foo/5    -- foo += 5
sub/foo/5    -- foo -= 5
mul/foo/5    -- foo *= 5
div/foo/5    -- foo /= 5
mod/foo/5    -- foo %= 5
```

Yeast only: `add/foo` (foo++) and `sub/foo` (foo--)

### Control Flow

```
if/foo/equals/bar
    ...
endif/
```

Operators: `equals`, `notequals`, `greater`, `less`

```
while/foo/equals/10
    ...
endwhile/
```

Or with a bool: `while/var` (loops while var is true)

### Functions (shortcuts)

```
shrtct/greet
    print/Hello!
endshrtct/

greet
```

Must be defined before use. Cannot take arguments.

### Other

```
wait/5      -- sleep for 5 seconds
exit/0      -- exit with code
exit        -- exit with 0
```

### Comments (`.yeast` only)

```
;; this is a comment
```

---

## Yeast vs Bread

| Feature | Bread | Yeast |
|---------|-------|-------|
| Comments | ❌ | ✅ (`;;`) |
| `bool` keyword | ❌ | ✅ |
| `string` keyword | ❌ | ✅ |
| `func`/`function` keyword | ❌ | ✅ |
| `@` for print | ❌ | ✅ |
| `add/foo` (++) | ❌ | ✅ |
| `sub/foo` (--) | ❌ | ✅ |
| `True`/`False` built-in | ❌ | ✅ |

---

## Requirements

- Python 3.10+
- A C compiler: `gcc`, `clang`, `cc`, `cl`, `eccp`, or `ibm-clang` (Supported with no compiler, using ``--comp=dont``)

## License

MIT — based on [Bread](https://github.com/angrypig555/bread) by angrypig555, also MIT licensed.
