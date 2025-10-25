# 🔍 Reverse Engineering — MIPS Assembler & Disassembler  

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/)
[![Architecture](https://img.shields.io/badge/Focus-MIPS32%2F64-lightgrey?logo=microchip&logoColor=white)](#)
[![Reverse Engineering](https://img.shields.io/badge/Domain-Reverse_Engineering-orange?logo=github&logoColor=white)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

<br>

**A Python-based educational toolkit for exploring instruction encoding, decoding, and ISA (Instruction Set Architecture) design.**  

This repository provides modular **assemblers and disassemblers** for **MIPS32/64**, enabling students, engineers, and researchers to visualize how **assembly maps to binary machine code**—and how CPUs interpret and execute those bit fields.  

Planned extensions will introduce **ARM-64** and **x86-64** modules for comparative ISA analysis.

<img src="https://github.com/sabneet95/Reverse-Engineering/blob/master/output.jpg" alt="Output Screenshot" width="800">

> *Note: This repository is designed for educational and research exploration and may require adaptation for production environments.*


## 🧭 Table of Contents
- [Overview](#overview)
- [Learning Objectives](#learning-objectives)
- [Technical Background](#technical-background)
- [Architecture](#architecture)
- [Directory Structure](#directory-structure)
- [Requirements](#requirements)
- [Usage](#usage)
- [Testing](#testing)
- [Contributing](#contributing)
- [Future Work](#future-work)
- [Author](#author)
- [License](#license)


## 🧩 Overview

This repository implements **assembler and disassembler tools** for **MIPS32/64** architectures.  
Each Python script demonstrates how instructions are parsed, encoded, and reconstructed, serving as a foundation for understanding instruction sets, binary translation, and reverse engineering.

**Modules**
- **`assembler.py`** → Encodes assembly mnemonics into binary machine code.  
- **`disassembler.py`** → Decodes binary words into readable assembly.  

Both emphasize clarity and modularity to make ISA study reproducible and extensible.


## 🎓 Learning Objectives

By using this toolkit, learners can:

- Translate **assembly instructions** into binary encodings at the bit level.  
- Understand **R, I, and J instruction formats** within MIPS32/64.  
- Explore **opcode, function code, and register field extraction**.  
- Gain insight into **data paths, control signals, and pipeline instruction flow**.  
- Extend assembler logic to **new opcodes** or **custom ISAs**, reinforcing hardware-software co-design concepts.


## 🧮 Technical Background

MIPS instructions are fixed-length (32-bit) and partitioned into fields depending on the instruction format:

| Format | Bits | Example | Description |
|---------|------|----------|--------------|
| **R-Type** | `[31-26]=opcode`, `[25-21]=rs`, `[20-16]=rt`, `[15-11]=rd`, `[10-6]=shamt`, `[5-0]=funct` | `add $rd,$rs,$rt` | Register-to-register operations |
| **I-Type** | `[31-26]=opcode`, `[25-21]=rs`, `[20-16]=rt`, `[15-0]=immediate` | `addi $rt,$rs,imm` | Immediate arithmetic / memory ops |
| **J-Type** | `[31-26]=opcode`, `[25-0]=address` | `j target` | Jump instructions |

The assembler script constructs binary encodings by packing these bit fields using bitwise shifts and masks, while the disassembler unpacks them through right-shifts and logical AND operations.  

Both modules rely on **opcode dictionaries** and **function tables** for efficient lookup and validation.


## ⚙️ Architecture

The project is structured for modular experimentation:

- **Opcode Dictionaries** — Mnemonics mapped to opcode and function values.  
- **Encoding Layer** — Converts tokenized assembly into 32-bit binary strings using bit shifting.  
- **Decoding Layer** — Extracts fields and resolves mnemonics using dictionary lookups.  
- **Pipeline Context (educational)** — Demonstrates how these encodings would propagate through *IF → ID → EX → MEM → WB* stages in a MIPS pipeline, aiding instruction-level reasoning.  
- **Extensibility** — Adding a new architecture requires defining its instruction formats and opcode tables.


## 📂 Directory Structure

```
Reverse-Engineering/
├── assembler.py
├── disassembler.py
├── output.jpg
├── LICENSE
└── README.md
```


## 🧰 Requirements

- **Python 3.9.1 or later (64-bit)**  
  [Download Python](https://www.python.org/)  
- *(Optional)* **MIPS Simulator / Runtime Environment**  
  [MARS](https://courses.missouristate.edu/) — for testing assembled code.


## 🚀 Usage

### **Running the Assembler**
1. Edit `assembler.py` to define your instructions:
   ```python
   instructions = [
       ['addi', '$v0', '$zero', '0'],
       ['lw', '$t9', '0', '$a0']
   ]
   ```
2. Execute:
   ```bash
   python assembler.py
   ```

### **Running the Disassembler**
1. Edit `disassembler.py`:
   ```python
   instructions = [
       '00000001101011100101100000100100',
       '10001101010010010000000000001000'
   ]
   ```
2. Execute:
   ```bash
   python disassembler.py
   ```

**Educational Tip:**  
Modify an instruction and observe how specific bit segments change — this reveals how **register IDs, immediates, and opcodes** interact at the binary level.


## 🧪 Testing

<details>
<summary>Testing Status</summary>

Automated testing is not yet integrated.  
Planned tests include verifying instruction encodings, bit-field accuracy, and round-trip assembler ↔ disassembler equivalence.  
A **pytest** suite will validate sample instructions across multiple architectures.
</details>


## 🤝 Contributing

1. Open an issue before implementing new features or ISAs.  
2. Follow **PEP-8** and document encoding logic with inline bit masks.  
3. Submit pull requests with example test cases and expected encodings.

> 💡 Contributions adding **ARM-64/x86 modules**, **bit-field visualizers**, or **pipeline simulators** are especially encouraged.


## 🔮 Future Work

- Integrate an automated testing framework.  
- Extend support for **ARM-64** and **x86-64** architectures.  
- Add **graphical visualization** for bit-field and control path mapping.  
- Provide **Jupyter notebooks** with step-through assembly examples.  
- Expand documentation with **opcode tables and timing diagrams**.


## 👤 Author

**Sabneet Bains** — *Quantum × AI × Scientific Computing*  
[LinkedIn](https://www.linkedin.com/in/sabneet-bains/) • [GitHub](https://github.com/sabneet-bains)


## 📄 License

This repository is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

