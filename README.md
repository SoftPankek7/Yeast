<p align="center">
    <img src="docs/icon_x128.png" alt="Yeast Logo">
</p>

<h1 align="center">Yeast</h1>

A faster, better, and more generally improved version of [Bread programming language](https://github.com/angrypig555/bread).

> Also, instead of **C++** (that Bread compiles to), **Yeast compiles to C**.
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

----

## Yeast vs Bread

| Feature | Bread | Yeast |
|---------|-------|-------|
| Variables | ✅ | ✅ |
| Compilation | ✅ | ✅ |
| Developer Suite | ✅ | *WIP* |
| Comments | ❌ | ✅ |
| `bool` keyword | ❌ | ✅ |
| `string` keyword | ❌ | ✅ |
| `func`/`function` keyword | ❌ | ✅ |
| `@` for print | ❌ | ✅ |
| `add/foo` (++) | ❌ | ✅ |
| `sub/foo` (--) | ❌ | ✅ |
| `True`/`False` built-in | ❌ | ✅ |
| **Raw** C editing | ❌ | ✅ |

Literally does everything bread can **+ more**
Also, note that Yeast *is backwards compatible by design*. To force bread, rename your file from ``example.yeast`` to ``example.bread``, *or* use the compiler's ``--force-bread`` flag. 

---

## Requirements

- Python 3.10+
- A C compiler: `gcc`, `clang`, `cc`, `cl`, `eccp`, or `ibm-clang` (Supported with no compiler, using ``--comp=dont``)

## License

MIT — based on [Bread](https://github.com/angrypig555/bread) by angrypig555, [also MIT licensed](https://github.com/angrypig555/bread/blob/main/LICENSE).
