"""Generate the instruction inventory markdown from the source tables."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

PSEUDO_INSTRUCTIONS = ("li", "move", "clear", "nop", "not", "b", "beqz", "bnez")

GROUP_DESCRIPTIONS = {
    "R-type / SPECIAL": "Register arithmetic, shifts, HI/LO moves, multiply/divide, traps.",
    "I-type / REGIMM": "Immediates, branches, load/store, and trap immediates.",
    "J-type": "Absolute jump target field.",
    "FPU / COP1": "Representative floating-point arithmetic and GPR-FPR moves.",
    "COP0": "Representative system-control moves and exception return.",
    "Pseudo-instructions": "Assembler conveniences expanded into real instructions.",
}


def build_markdown() -> str:
    from mips_tool.tables import COP0_SPECS, FPU_SPECS, I_SPECS, J_SPECS, R_SPECS

    groups = (
        ("R-type / SPECIAL", R_SPECS),
        ("I-type / REGIMM", I_SPECS),
        ("J-type", J_SPECS),
        ("FPU / COP1", FPU_SPECS),
        ("COP0", COP0_SPECS),
    )
    real_count = sum(len(specs) for _, specs in groups)
    lines = [
        "# Instruction Inventory",
        "",
        "Generated from `mips_tool.tables`; do not edit by hand.",
        "",
        "Regenerate with:",
        "",
        "```bash",
        "python tools/generate_instruction_inventory.py > docs/instruction-set.md",
        "```",
        "",
        "| Count | Value |",
        "|:--|--:|",
        f"| Real supported mnemonics | {real_count} |",
        f"| Pseudo-instructions | {len(PSEUDO_INSTRUCTIONS)} |",
        f"| Total supported names | {real_count + len(PSEUDO_INSTRUCTIONS)} |",
        "",
        "| Group | Count | Role | Mnemonics |",
        "|:--|--:|:--|:--|",
    ]
    for name, specs in groups:
        mnemonics = ", ".join(f"`{mnemonic}`" for mnemonic in specs)
        lines.append(f"| {name} | {len(specs)} | {GROUP_DESCRIPTIONS[name]} | {mnemonics} |")
    pseudo = ", ".join(f"`{mnemonic}`" for mnemonic in PSEUDO_INSTRUCTIONS)
    lines.append(
        f"| Pseudo-instructions | {len(PSEUDO_INSTRUCTIONS)} | "
        f"{GROUP_DESCRIPTIONS['Pseudo-instructions']} | {pseudo} |"
    )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    print(build_markdown(), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
