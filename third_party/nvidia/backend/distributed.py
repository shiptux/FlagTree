import os
from pathlib import Path
from dataclasses import dataclass


@dataclass
class FlagCXConfig:
    bitcode_path: str
    shared_lib_path: str

    def __init__(self):
        self.default_libdir = self._get_bitcode_path()
        self.bitcode_path = str(self.default_libdir / 'libflagcx_device.bc')
        self.shared_lib_path = str(self.default_libdir / 'libflagcx.so')
        if not os.path.exists(self.bitcode_path):
            raise FileNotFoundError(f"FlagCX bitcode not found at {self.bitcode_path}")
        if not os.path.exists(self.shared_lib_path):
            raise FileNotFoundError(f"FlagCX shared library not found at {self.shared_lib_path}")

    def _get_bitcode_path(self):
        path = Path(__file__)
        while (path.name != "FlagTree"):
            path = path.parent
            if path == path.parent:
                raise FileNotFoundError("Could not find FlagTree root directory")
        return path / "third_party" / "tle" / "third_party" / "flagcx" / 'build' / 'lib'


class Distributed:

    def __init__(self):
        self.is_use_flagcx = os.environ.get("USE_FLAGCX", "ON") == "ON"
        self.extern_libs = {}
        if self.is_use_flagcx:
            self.extern_libs["libflagcx"] = FlagCXConfig().bitcode_path

    def get_extern_libs(self):
        return self.extern_libs
