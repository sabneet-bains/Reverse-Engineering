import pytest

from mips_tool.decoder import decode_instruction
from mips_tool.errors import MipsError


@pytest.mark.parametrize(
    "word",
    [
        "0x70000000",  # unsupported opcode
        "0x00000005",  # unsupported SPECIAL funct
        "0x40400000",  # unsupported COP0 rs selector
        "0x44400000",  # unsupported COP1 rs selector
        "0x4600003F",  # unsupported COP1 funct
    ],
)
def test_unsupported_machine_words_fail_clearly(word):
    with pytest.raises(MipsError):
        decode_instruction(word)
