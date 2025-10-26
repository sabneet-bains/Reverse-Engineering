<div align="center"><a name="readme-top"></a>

# 🛠️ Reverse Engineering — MIPS Assembler & Disassembler  

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/)
[![Architecture](https://img.shields.io/badge/Focus-MIPS32%2F64-lightgrey?logo=microchip&logoColor=white)](#)
[![Domain](https://img.shields.io/badge/Reverse_Engineering-orange?logo=github&logoColor=white)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)


**Educational clarity × Professional precision**  
*A modular Python toolkit that reveals how assembly instructions become machine logic—bridging syntax, semantics, and silicon.*

<img src="https://github.com/sabneet95/Reverse-Engineering/blob/master/output.jpg" alt="Assembler Output" width="800">

<sup>Part of the <b>Foundational & Academic</b> collection: educational tools designed with engineering rigor.</sup>

---

> [!IMPORTANT]
> **Star this repository ⭐** — you'll receive release notifications and support future educational tools instantly.

---

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/sabneet95/Reverse-Engineering)

</div>

> [!TIP]
> This is some tip text.

---

<details>
<summary><kbd>📖 Table of Contents</kbd></summary>

#### TOC

- [📘 Overview](#-overview)
- [🎯 Learning Objectives](#-learning-objectives)
- [⚙️ Architecture & Design](#️-architecture--design)
- [🧩 Instruction Anatomy](#-instruction-anatomy)
- [🚀 Quick Demo](#-quick-demo)
- [🧠 Conceptual Insights](#-conceptual-insights)
- [🔄 Extend & Compare](#-extend--compare)
- [🔬 Research Extensions](#-research-extensions)
- [🧭 Educational Takeaways](#-educational-takeaways)
- [👤 Author](#-author)
- [📄 License](#-license)

---

</details>

───◉───────────────────────────────◉───

## 📘 Overview  

This repository provides assembler and disassembler modules for **MIPS32/64** architectures.  
It translates assembly instructions into binary machine code — and back — allowing you to *observe the CPU’s language at the bit level*.  

### Why It Matters
- Reveals the **data structures underlying ISA design**.  
- Provides **bitwise transparency** for students of compilers, computer architecture, and systems engineering.  
- Enables **educational visualization** of instruction encoding, ideal for self-study or teaching labs.  

[![Back to Top](https://img.shields.io/badge/-BACK_TO_TOP-151515?style=flat-square)](#readme-top)

───◉───────────────────────────────◉───

## 🎯 Learning Objectives  

- Decode and encode **R, I, and J instruction formats**.  
- Explore **opcodes, funct codes, registers, and immediate values**.  
- Understand how **binary encodings map to hardware logic**.  
- Compare multiple ISAs (MIPS, ARM, x86) using a unified schema.  
- Extend and test encoding rules programmatically.  

> 💡 *Every instruction is a design decision, not just a syntax rule.*

[![Back to Top](https://img.shields.io/badge/-BACK_TO_TOP-151515?style=flat-square)](#readme-top)

───◉───────────────────────────────◉───

## ⚙️ Architecture & Design  

```
Reverse-Engineering/
├── assembler.py        # Assembly → Binary encoder
├── disassembler.py     # Binary → Assembly decoder
├── opcode_tables/      # Mnemonics & function maps
├── examples/           # Round-trip tests and cases
└── README.md
```

**Core Components**
- **Encoding Layer:** Converts assembly mnemonics into 32-bit binary sequences.  
- **Decoding Layer:** Extracts bitfields and reconstructs readable instructions.  
- **Audit Trail:** Each operation is traceable—ideal for debugging or teaching.  
- **Extensibility:** Add new architectures by defining tables and masks.  

[![Back to Top](https://img.shields.io/badge/-BACK_TO_TOP-151515?style=flat-square)](#readme-top)

───◉───────────────────────────────◉───

## 🧩 Instruction Anatomy  

| Format | Fields | Example | Bit Mapping |
|:-------|:--------|:---------|:-------------|
| **R-Type** | opcode, rs, rt, rd, shamt, funct | `add $rd,$rs,$rt` | `000000 10001 10010 01001 00000 100000` |
| **I-Type** | opcode, rs, rt, immediate | `addi $rt,$rs,imm` | `001000 10001 01001 0000000000000100` |
| **J-Type** | opcode, address | `j target` | `000010 00000000000000000000010000` |

> 🧮 Each field is a slot in a 32-bit grammar—compact, consistent, elegant.

[![Back to Top](https://img.shields.io/badge/-BACK_TO_TOP-151515?style=flat-square)](#readme-top)

───◉───────────────────────────────◉───

## 🚀 Quick Demo  

### Assemble Instructions
```bash
python assembler.py
```

**Example**
```python
instructions = [
    ['addi', '$v0', '$zero', '4'],
    ['lw', '$t9', '0', '$a0']
]
```
**Output**
```
00100000000000100000000000000100
10001101010010010000000000001000
```

### Disassemble Binary
```bash
python disassembler.py
```

**Example**
```python
instructions = [
    '00000001101011100101100000100100',
    '10001101010010010000000000001000'
]
```
**Output**
```
and $t3, $t5, $t6
lw $t1, 8($t2)
```

> 🔍 *Single-bit changes = semantic transformations.*

[![Back to Top](https://img.shields.io/badge/-BACK_TO_TOP-151515?style=flat-square)](#readme-top)

───◉───────────────────────────────◉───

## 🧠 Conceptual Insights  

| Theme | Key Takeaway |
|:------|:--------------|
| **Bit-Level Determinism** | Machine code is structured data—minimal yet expressive. |
| **Round-Trip Verification** | Disassembly validates correctness—every mapping is bidirectional. |
| **Hardware Empathy** | Understanding encodings enhances compiler design intuition. |
| **Pedagogical Value** | Makes invisible CPU logic visible to learners. |

[![Back to Top](https://img.shields.io/badge/-BACK_TO_TOP-151515?style=flat-square)](#readme-top)

───◉───────────────────────────────◉───

## 🔄 Extend & Compare  

| Goal | Action |
|:-----|:--------|
| Add new ISA | Define opcode/function maps in `architectures/` |
| Automate Tests | Implement pytest round-trip assertions |
| Compare Architectures | Add ARM/x86 support for cross-ISA insights |
| Visualize Bitfields | Integrate ASCII/matplotlib visual encoders |

> ✨ *Turn binary patterns into stories of design trade-offs.*

[![Back to Top](https://img.shields.io/badge/-BACK_TO_TOP-151515?style=flat-square)](#readme-top)

───◉───────────────────────────────◉───

## 🔬 Research Extensions  

- Visual disassembly pipelines for compiler education.  
- Interactive Jupyter notebooks showing opcode heatmaps.  
- Integration with CPU simulators or FPGA boards.  
- Automated correctness tests for student-built encoders.  

[![Back to Top](https://img.shields.io/badge/-BACK_TO_TOP-151515?style=flat-square)](#readme-top)

───◉───────────────────────────────◉───

## 🧭 Educational Takeaways  

- Demonstrates **low-level transparency** in system design.  
- Promotes **bottom-up understanding** of language → hardware translation.  
- Provides a **codebase template** for teaching or experimentation.  

<details>
<summary><kbd>Expand for Instructor Use</kbd></summary>

- Integrates easily into computer architecture or compiler courses.  
- Supports lab demos, instruction field visualizations, and ISA comparisons.  
- Encourages modular learning — modify one field, observe the effect.  

</details>

[![Back to Top](https://img.shields.io/badge/-BACK_TO_TOP-151515?style=flat-square)](#readme-top)

───◉───────────────────────────────◉───

## 👤 Author  

**Sabneet Bains**  
*Quantum × AI × Scientific Computing*  
[LinkedIn](https://www.linkedin.com/in/sabneet-bains/) • [GitHub](https://github.com/sabneet-bains)

---

## 📄 License  
Licensed under the [MIT License](https://choosealicense.com/licenses/mit/)

---

<div align="center">
<sub>“Reverse engineering is not about undoing complexity—it’s about understanding design.”</sub>
</div>
