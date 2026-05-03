# How to include files in yeast

<!-- ---- -->

## General Warnings

> [!NOTE]
> Planned for v1.1.0+
> ***Do not*** expect any of this (especially yeast headers) to be **1:1 or implemented in the final version**.
> Also, ***do not*** expect this to appear on v1.1.0 specifically.

> [!CAUTION]
> The "Yeast Headers" section can be changed quickly to just include the inline code instead of generating C, as it is quicker & easier.

----

## System-wide Headers

**Examples**: *stdio.h*, *windows.h*, *stdlib.h*, *unistd.h*
To include system-wide headers, you will have to use:

```yeast
@system/lib
```

> Do not use ``.h`` in the header files. It is automatically added for you.

Using this example, including ``windows.h`` would look like:

```yeast
@system/windows
```

In the compiler, this unrolls to:

```c
#include <lib.h>
```

> [!NOTE]
> Please note that ``.h`` is intentionally hardcoded - and disallows any ``.hpp`` files.

----

## Local Headers

**Examples**: *driver.h*, *library.h*, *something.h*, *project.h*

> [!WARNING]
> Note that you cannot include "yeast.h", because it is used by the compiler.

To include local headers, you will have to use:

```yeast
@local/lib
```

> Do not use ``.h`` in the header files. It is automatically added for you.

Using this example, including ``project.h`` would look like:

```yeast
@local/project
```

In the compiler, this unrolls to:

```c
#include "lib.h"
```

> [!NOTE]
> Please note that ``.h`` is intentionally hardcoded - and disallows any ``.hpp`` files.

----

## Yeast Headers

**Examples**: *utils.yeast*, *math.yeast*, *curl.yeast*, *project.yeast*

To include yeast headers, you will have to use:

```yeast
@yeast/lib
```

> Do not use ``.yeast`` in the header files. It is automatically added for you.

Using this example, including ``project.yeast`` would look like:

```yeast
@yeast/project
```

In the compiler, this unrolls to:

```c
#include <lib.h>
```

> [!NOTE]
> Yeast files will be recognised by the compiler.
>
> This then makes the yeast header get compiled & generate headers.
> Then, it references it as a header internally, as seen above with ``#include <lib.h>``

> [!NOTE]
> Please note that ``.yeast`` is intentionally hardcoded - and disallows any ``.bread`` files.
