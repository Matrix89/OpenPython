import os
import sys
import time
import traceback
from collections import Container
from pathlib import Path
from subprocess import check_call, DEVNULL, CalledProcessError
from typing import TypeVar, Generic

from dataclasses import dataclass
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection, Section, Symbol
import shutil

FOLDER = Path(__file__).parent
OPMOD_PATH = FOLDER.parent / "opmod"
TARGET_FOLDER = OPMOD_PATH / "src/main/resources/assets/openpie/firmwares/debug"  # TODO: place version


@dataclass
class SymbolInfo:
    bind: str
    type: str


@dataclass
class SimpleSymbol:
    name: str
    st_name: int
    st_value: int
    st_size: int
    st_info: SymbolInfo
    st_other: Container
    st_shndx: int

    @classmethod
    def from_symbol(cls, symbol_obj: Symbol):
        return SimpleSymbol(
            symbol_obj.name,
            st_info=SymbolInfo(**symbol_obj.entry.pop("st_info")),
            **symbol_obj.entry,
        )


@dataclass
class SimpleSection:
    name: str
    sh_name: int
    sh_type: str
    sh_flags: int
    sh_addr: int
    sh_offset: int
    sh_size: int
    sh_link: int
    sh_info: int
    sh_addralign: int
    sh_entsize: int


@dataclass
class SimpleSegment:
    p_type: str
    p_offset: int
    p_vaddr: int
    p_paddr: int
    p_filesz: int
    p_memsz: int
    p_flags: int
    p_align: int


T = TypeVar("T")


def find_section(elf: ELFFile, cls: Generic[T]) -> T:
    return list(s for s in elf.iter_sections() if type(s) == cls)


def pretty_addr(addr: int, size=8) -> str:
    return "0x" + hex(addr)[2:].zfill(size)


def process_elf(elf: ELFFile, map_file: Path):
    assert elf.get_machine_arch() == "ARM"

    if False:
        print(">", "section")
        for section_obj in find_section(elf, Section):  # type: Section
            section = SimpleSection(section_obj.name, **section_obj.header)
            if not section.sh_addr:
                continue

            print(
                pretty_addr(section.sh_addr),
                pretty_addr(section.sh_size, size=6),
                section.sh_flags,
                section.sh_type,
                section.name,
                sep="\t"
            )

    with map_file.open('w') as fp:
        type2typ = {
            "STT_OBJECT": "OBJECT",
            "STT_FUNC": "FUNC",
        }
        for symbol_table in find_section(elf, SymbolTableSection):
            symbols = [SimpleSymbol.from_symbol(obj) for obj in symbol_table.iter_symbols()
                       if (obj['st_info']['type'] == "STT_FUNC" or
                           obj['st_info']['type'] == "STT_OBJECT") and
                       obj['st_info']['bind'] == "STB_GLOBAL"]

            for symbol in sorted(symbols, key=lambda x: x.st_value):
                print(
                    pretty_addr(symbol.st_value),
                    pretty_addr(symbol.st_size, size=4),
                    # symbol.st_info.bind,
                    type2typ[symbol.st_info.type],
                    symbol.name,
                    sep="\t",
                    file=fp,
                )


def build(folder: Path = FOLDER, target_folder: Path = TARGET_FOLDER):
    build_path: Path = folder / "build"

    check_call(
        ["wsl", "make", "-j8"],
        cwd=str(folder),
        shell=True,
        stdin=DEVNULL
    )

    target_folder.mkdir(parents=True, exist_ok=True)

    with (build_path / "firmware.elf").open('rb') as fp:
        elf = ELFFile(fp)
        process_elf(elf, target_folder / "firmware.map")

    shutil.copyfile(str(build_path / "firmware.bin"), str(target_folder / "firmware.bin"))
    shutil.copyfile(str(build_path / "firmware.elf"), str(target_folder / "firmware.elf"))
    shutil.copyfile(str(build_path / "firmware.elf.map"), str(target_folder / "firmware.elf.map"))
    print(target_folder / "firmware.bin")


def main():
    try:
        build()
        return 0
    except CalledProcessError as e:
        traceback.print_exc()
        raise SystemExit(e.returncode)


if __name__ == '__main__':
    main()
