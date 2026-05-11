import pytest

from mips_tool.errors import MipsError
from mips_tool.parser import parse_int, parse_memory_operand, require_range, sign_extend
from mips_tool.registers import cop0_name, gpr_name, parse_cop0, parse_fpr, parse_gpr
from mips_tool.word import InstructionWord


def test_integer_parsing_formats():
    assert parse_int("42") == 42
    assert parse_int("0x2A") == 42
    assert parse_int("0b101010") == 42
    assert parse_int("1_024") == 1024
    assert parse_int("-16") == -16


def test_integer_range_and_sign_extension():
    assert require_range(-1, 16, signed=True, what="immediate") == 0xFFFF
    assert sign_extend(0xFFF0, 16) == -16
    with pytest.raises(MipsError):
        require_range(70000, 16, signed=False, what="immediate")


def test_register_aliases_and_names():
    assert parse_gpr("$zero") == 0
    assert parse_gpr("$0") == 0
    assert parse_gpr("$fp") == 30
    assert parse_gpr("$s8") == 30
    assert gpr_name(31) == "$ra"
    assert parse_cop0("$status") == 12
    assert cop0_name(14) == "$epc"
    assert parse_fpr("$f31") == 31


def test_register_failures_are_clear():
    with pytest.raises(MipsError):
        parse_gpr("$bad")
    with pytest.raises(MipsError):
        parse_cop0("$bad")
    with pytest.raises(MipsError):
        parse_fpr("$f32")
    with pytest.raises(MipsError):
        parse_fpr("$bad")


def test_memory_operand_parser():
    assert parse_memory_operand("8($t2)") == (8, 10)
    assert parse_memory_operand("-16($sp)") == (0xFFF0, 29)
    with pytest.raises(MipsError):
        parse_memory_operand("$sp")


def test_instruction_word_parses_supported_literal_forms():
    binary = "00100000000000100000000000000100"
    assert InstructionWord.parse(binary).value == 0x20020004
    assert InstructionWord.parse("0x20020004").opcode == 0x08
    assert InstructionWord.parse(0x20020004).immediate == 4


def test_instruction_word_rejects_bad_or_out_of_range_values():
    with pytest.raises(MipsError):
        InstructionWord.parse("not-a-word")
    with pytest.raises(MipsError):
        InstructionWord.parse(0x1_0000_0000)
