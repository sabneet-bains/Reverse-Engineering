# Reverse Engineering - MIPS

A repository of Python-based assemblers and disassemblers for a variety of CPU architectures.

![](https://github.com/sabneet95/Reverse-Engineering/blob/master/output.jpg)

→ `Currently, the main focus is on MIPS32/64 architecture, soon ARM-64 and x86 will be added.`

## Requirements

[Python 3.9.1 (64-bit) or above](https://www.python.org/downloads/)

[MIPS Assembler and Runtime Simulator (Optional)](https://courses.missouristate.edu/KenVollmar/MARS/)

## Build Tested

Visual Studio Code
* Version: 1.52.1 (system setup)
* Commit: ea3859d4ba2f3e577a159bc91e3074c5d85c0523
* Electron: 9.3.5
* Chrome: 83.0.4103.122
* Node.js: 12.14.1
* V8: 8.3.110.13-electron.0
* OS: Windows_NT x64 10.0.19042
* Memory: 1981M
* Cores: 8

## Usage

1)	Open the project in **Visual Studio Code** > _predefine_ the MIPS instructions in assembler.py

```python

instructions = [['addi', '$v0', '$zero', '0'], ['lw', '$t9', '0', '$a0']]

.
..
...

```

2)	Then, in a terminal tab, _run_ the assembler.py

```
    >>  assembler.py █
```

3)	Likewise, specify the instructions in disassembler.py

```python

instructions = ['00000001101011100101100000100100', '10001101010010010000000000001000']

.
..
...

```

4)	Then, in a terminal tab, _run_ the disassembler.py

```
    >>  disassembler.py █
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


## License
[MIT](https://choosealicense.com/licenses/mit/)
