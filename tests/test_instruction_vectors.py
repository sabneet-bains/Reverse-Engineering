import subprocess
import sys
from pathlib import Path

import pytest

from mips_tool.decoder import decode_instruction
from mips_tool.encoder import assemble_instruction, assemble_program
from mips_tool.encoding import EncodedInstruction
from mips_tool.tables import ALL_SPECS
from tools.generate_instruction_inventory import build_markdown


# Fixed vectors exercise MIPS opcode/funct field layouts; see
# docs/vector-provenance.md for source scope and coverage notes.
R_TYPE_VECTORS = [
    ("add $t0, $t1, $t2", "0x012A4020", "add $t0, $t1, $t2"),
    ("subu $s0, $s1, $s2", "0x02328023", "subu $s0, $s1, $s2"),
    ("and $t3, $t4, $t5", "0x018D5824", "and $t3, $t4, $t5"),
    ("sll $t0, $t1, 3", "0x000940C0", "sll $t0, $t1, 3"),
    ("sllv $t0, $t1, $t2", "0x01494004", "sllv $t0, $t1, $t2"),
    ("jr $ra", "0x03E00008", "jr $ra"),
    ("jalr $t0, $ra", "0x03E04009", "jalr $t0, $ra"),
    ("mflo $v0", "0x00001012", "mflo $v0"),
    ("mult $t0, $t1", "0x01090018", "mult $t0, $t1"),
    ("syscall 7", "0x000001CC", "syscall 7"),
    ("teq $t0, $t1, 3", "0x010900F4", "teq $t0, $t1, 3"),
]

I_TYPE_VECTORS = [
    ("addiu $t0, $zero, -1", "0x2408FFFF", "addiu $t0, $zero, -1"),
    ("andi $t0, $t1, 255", "0x312800FF", "andi $t0, $t1, 255"),
    ("lui $at, 4660", "0x3C011234", "lui $at, 4660"),
    ("beq $t0, $t1, -2", "0x1109FFFE", "beq $t0, $t1, -2"),
    ("blez $t0, 5", "0x19000005", "blez $t0, 5"),
    ("bltz $t0, -1", "0x0500FFFF", "bltz $t0, -1"),
    ("lw $t1, 8($t2)", "0x8D490008", "lw $t1, 8($t2)"),
]

J_TYPE_VECTORS = [
    ("j 0x10", "0x08000010", "j 0x10"),
    ("jal 0x20", "0x0C000020", "jal 0x20"),
]

MIPS64_VECTORS = [
    ("daddu $t0, $t1, $t2", "0x012A402D", "daddu $t0, $t1, $t2"),
    ("dsll32 $t0, $t1, 4", "0x0009413C", "dsll32 $t0, $t1, 4"),
    ("ddivu $t0, $t1", "0x0109001F", "ddivu $t0, $t1"),
    ("sd $t0, -16($sp)", "0xFFA8FFF0", "sd $t0, -16($sp)"),
]

COPROCESSOR_VECTORS = [
    ("add.d $f2, $f4, $f6", "0x46262080", "add.d $f2, $f4, $f6"),
    ("mtc1 $t0, $f4", "0x44882000", "mtc1 $t0, $f4"),
    ("mfc0 $t0, $status", "0x40086000", "mfc0 $t0, $status"),
    ("eret", "0x42000018", "eret"),
]

ENCODING_VECTORS = (
    R_TYPE_VECTORS
    + I_TYPE_VECTORS
    + J_TYPE_VECTORS
    + MIPS64_VECTORS
    + COPROCESSOR_VECTORS
)

SAMPLE_OPERANDS_BY_KIND = {
    "r3": "$t0, $t1, $t2",
    "shift": "$t0, $t1, 3",
    "shiftv": "$t0, $t1, $t2",
    "rs": "$ra",
    "rd": "$v0",
    "rs_rt": "$t0, $t1",
    "jalr": "$t0, $ra",
    "code20": "7",
    "trap_r": "$t0, $t1, 3",
    "i_rt_rs_imm": "$t0, $t1, 123",
    "lui": "$at, 4660",
    "branch2": "$t0, $t1, -2",
    "branch1": "$t0, 5",
    "regimm": "$t0, -1",
    "mem": "$t1, 8($t2)",
    "trap_i": "$t0, 3",
    "jump": "0x10",
    "fpu3": "$f2, $f4, $f6",
    "cop1_move": "$t0, $f4",
    "cop0_move": "$t0, $status",
    "eret": "",
}


@pytest.mark.parametrize(("assembly", "expected_hex", "expected_disassembly"), ENCODING_VECTORS)
def test_instruction_vectors_encode_and_decode(assembly, expected_hex, expected_disassembly):
    encoded = assemble_instruction(assembly)[0]
    assert encoded.hex == expected_hex
    assert decode_instruction(expected_hex).assembly == expected_disassembly


def test_supported_instruction_forms_round_trip_through_decoder():
    for mnemonic, instruction_spec in ALL_SPECS.items():
        operands = SAMPLE_OPERANDS_BY_KIND[instruction_spec.kind]
        assembly = f"{mnemonic} {operands}".strip()

        encoded = assemble_instruction(assembly)[0]
        decoded = decode_instruction(encoded.hex)
        reencoded = assemble_instruction(decoded.assembly)[0]

        assert reencoded.word == encoded.word, assembly


def test_generated_instruction_inventory_is_checked_in():
    expected = build_markdown()
    actual = Path("docs/instruction-set.md").read_text(encoding="utf-8")
    assert actual == expected


def test_vector_provenance_document_is_checked_in():
    provenance = Path("docs/vector-provenance.md").read_text(encoding="utf-8")
    assert "assembly -> expected hex word -> canonical disassembly" in provenance
    assert "MIPS32 Architecture For Programmers" in provenance


def test_module_cli_success_and_failure_exit_codes():
    assemble = subprocess.run(
        [sys.executable, "-m", "mips_tool", "assemble", "addi $v0, $zero, 4"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert assemble.returncode == 0
    assert "0x20020004" in assemble.stdout

    disassemble = subprocess.run(
        [sys.executable, "-m", "mips_tool", "disassemble", "00100000000000100000000000000100"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert disassemble.returncode == 0
    assert disassemble.stdout.strip() == "addi $v0, $zero, 4"

    explain = subprocess.run(
        [sys.executable, "-m", "mips_tool", "explain", "ld $t0, 16($sp)"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert explain.returncode == 0
    assert "assembly: ld $t0, 16($sp)" in explain.stdout

    walkthrough = subprocess.run(
        [sys.executable, "-m", "mips_tool", "walkthrough", "addi $v0, $zero, 4"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert walkthrough.returncode == 0
    assert "form:      I-type / i_rt_rs_imm" in walkthrough.stdout

    bad = subprocess.run(
        [sys.executable, "-m", "mips_tool", "assemble", "mul $t0, $t1, $t2"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert bad.returncode == 2
    assert "unsupported instruction: mul" in bad.stderr


def test_cli_file_input_assembles_example_program():
    result = subprocess.run(
        [sys.executable, "-m", "mips_tool", "assemble", "examples/tutorial.asm", "--format", "hex"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "0x20020004" in result.stdout
    assert "0x8D490008" in result.stdout
    assert "0xDFAA0010" in result.stdout


def test_public_api_return_shape_and_pseudo_metadata():
    encoded = assemble_instruction("addi $v0, $zero, 4")
    assert isinstance(encoded, list)
    assert isinstance(encoded[0], EncodedInstruction)
    assert encoded[0].assembly == "addi $v0, $zero, 4"
    assert encoded[0].binary == "00100000000000100000000000000100"
    assert encoded[0].hex == "0x20020004"
    assert encoded[0].fields

    expanded = assemble_instruction("li $t0, 0x12345678")
    assert [item.expanded_from for item in expanded] == ["li $t0, 0x12345678", "li $t0, 0x12345678"]
    assert [item.assembly for item in expanded] == ["lui $at, 4660", "ori $t0, $at, 22136"]


def test_branch_offsets_account_for_pseudo_expansion():
    encoded = assemble_program(
        """
start:
    li $t0, 0x12345678
    b start
"""
    )
    assert [item.assembly for item in encoded] == [
        "lui $at, 4660",
        "ori $t0, $at, 22136",
        "beq $zero, $zero, -3",
    ]
    assert encoded[-1].hex == "0x1000FFFD"


def test_benchmark_quick_smoke():
    result = subprocess.run(
        [sys.executable, "tools/benchmark.py", "--quick"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "encode" in result.stdout
    assert "decode" in result.stdout
    assert "explain" in result.stdout
    assert "program" in result.stdout
