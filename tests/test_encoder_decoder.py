from pathlib import Path

import pytest

from mips_tool.decoder import decode_instruction
from mips_tool.encoder import assemble_instruction, assemble_program
from mips_tool.errors import MipsError
from mips_tool.explain import explain_instruction
from mips_tool.parser import parse_memory_operand


def one(text):
    encoded = assemble_instruction(text)
    assert len(encoded) == 1
    return encoded[0]


def test_mips32_r_i_j_encoding():
    assert one("add $t0, $t1, $t2").binary == "00000001001010100100000000100000"
    assert one("addi $v0, $zero, 4").binary == "00100000000000100000000000000100"
    assert one("j 0x10").binary == "00001000000000000000000000010000"


def test_memory_operands_are_encoded_and_decoded_canonically():
    encoded = one("lw $t1, 8($t2)")
    assert encoded.binary == "10001101010010010000000000001000"
    assert decode_instruction(encoded.binary).assembly == "lw $t1, 8($t2)"
    assert parse_memory_operand("-16($sp)") == (0xFFF0, 29)


def test_mips64_integer_subset():
    assert one("daddiu $t0, $zero, 42").hex == "0x6408002A"
    assert one("ld $t1, 16($sp)").hex == "0xDFA90010"
    assert decode_instruction("0xDFA90010").assembly == "ld $t1, 16($sp)"


def test_fpu_and_cop0_representative_instructions():
    assert decode_instruction(one("add.s $f6, $f4, $f8").word).assembly == "add.s $f6, $f4, $f8"
    assert decode_instruction(one("mfc0 $t2, $status").word).assembly == "mfc0 $t2, $status"
    assert decode_instruction(one("eret").word).assembly == "eret"


def test_labels_use_two_pass_branch_offsets():
    program = """
start:
    addi $t0, $zero, 1
    beq $t0, $zero, done
    addi $t0, $t0, 1
done:
    jr $ra
"""
    encoded = assemble_program(program)
    assert encoded[1].assembly == "beq $t0, $zero, 1"
    assert encoded[1].binary.endswith("0000000000000001")


def test_pseudo_instructions_expand_and_track_source():
    encoded = assemble_program("""
    li $t0, 0x12345678
    move $t1, $t0
    nop
""")
    assert [item.assembly for item in encoded] == [
        "lui $at, 4660",
        "ori $t0, $at, 22136",
        "addu $t1, $t0, $zero",
        "sll $zero, $zero, 0",
    ]
    assert encoded[0].expanded_from == "li $t0, 0x12345678"


def test_bitfield_explainer_is_deterministic():
    output = explain_instruction("ld $t0, 16($sp)")
    assert "assembly: ld $t0, 16($sp)" in output
    assert "opcode" in output
    assert "immediate" in output


def test_bitfield_explainer_matches_golden_output():
    text = Path("examples/expected/explain-ld.txt").read_text(encoding="utf-8").rstrip("\n")
    expected = text.split("\n\n", 1)[1] if text.startswith("command:") else text
    assert explain_instruction("ld $t0, 16($sp)") == expected


@pytest.mark.parametrize(
    "text",
    [
        "madeup $t0, $t1",
        "add $bad, $t0, $t1",
        "addi $t0, $t1, 70000",
        "lw $t0, $sp",
    ],
)
def test_clear_failures_for_unsupported_or_malformed_input(text):
    with pytest.raises(MipsError):
        assemble_instruction(text)
