# Yeast/Bread Language Support

Syntax highlighting for the [Yeast](https://github.com/SoftPankek7/Yeast) and [Bread](https://github.com/angrypig555/bread) programming languages.

## What is Yeast?

Yeast is an improved transpiler for the Bread programming language, rewritten in Python. It compiles `.yeast` or `.bread` files to C, then to a native binary.

## Features

- Syntax highlighting for `.yeast` and `.bread` files
- Comment highlighting (`;;`)
- Keyword highlighting (`print`, `int`, `str`, `bool`, `while`, `if`, `else`, etc.)
- Operator highlighting (`equals`, `notequals`, `greater`, `less`)
- Number highlighting
- Raw C escape highlighting (`\`)

## Usage

Install the extension, then open any `.yeast` or `.bread` file — highlighting will apply automatically.

## Example

```yeast
;; Hello World in Yeast

str/message/Hello World!
print/message
exit/0
```

## Links

- [Yeast on GitHub](https://github.com/SoftPankek7/Yeast)
- [Bread on GitHub](https://github.com/angrypig555/bread)
- [Yeast on the VSCode Marketplace](https://marketplace.visualstudio.com/publishers/CharlieTulip)

## License

MIT
