import subprocess
import sys
from pathlib import Path

from mips_tool.walkthrough import walkthrough_instruction


def _read_expected(path: str) -> str:
    text = Path(path).read_text(encoding="utf-8").rstrip("\n")
    if text.startswith("command:"):
        return text.split("\n\n", 1)[1]
    return text


def test_walkthrough_for_real_instruction_matches_expected_output():
    expected = _read_expected("examples/expected/walkthrough-addi.txt")
    assert walkthrough_instruction("addi $v0, $zero, 4") == expected


def test_walkthrough_for_pseudo_instruction_shows_expansion():
    expected = _read_expected("examples/expected/walkthrough-li.txt")
    assert walkthrough_instruction("li $t0, 0x12345678") == expected


def test_walkthrough_for_machine_word_decodes_first():
    output = walkthrough_instruction("00100000000000100000000000000100")
    assert "kind:      machine word" in output
    assert "assembly:  addi $v0, $zero, 4" in output
    assert "binary:    00100000000000100000000000000100" in output


def test_walkthrough_covers_r_type_memory_and_jump_forms():
    r_type = walkthrough_instruction("add $t0, $t1, $t2")
    assert "form:      R-type / r3" in r_type
    assert "table:     opcode=0x00, kind=r3, funct=0x20" in r_type
    assert "pack:      pack_r(opcode, rs, rt, rd, shamt, funct)" in r_type

    memory = walkthrough_instruction("lw $t1, 8($t2)")
    assert "form:      I-type / mem" in memory
    assert "table:     opcode=0x23, kind=mem" in memory
    assert "immediate  15:0   0000000000001000  8" in memory

    jump = walkthrough_instruction("j 0x10")
    assert "form:      J-type / jump" in jump
    assert "table:     opcode=0x02, kind=jump" in jump
    assert "pack:      pack_j(opcode, address)" in jump


def test_cli_walkthrough_success_and_failure():
    ok = subprocess.run(
        [sys.executable, "-m", "mips_tool", "walkthrough", "addi $v0, $zero, 4"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert ok.returncode == 0
    assert "form:      I-type / i_rt_rs_imm" in ok.stdout

    bad = subprocess.run(
        [sys.executable, "-m", "mips_tool", "walkthrough", "mul $t0, $t1, $t2"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert bad.returncode == 2
    assert "unsupported instruction: mul" in bad.stderr
