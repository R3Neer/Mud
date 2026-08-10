from __future__ import annotations

import io
import stat
import zipfile
from pathlib import PurePosixPath


MAX_PACKAGE_BYTES = 10_485_760
MAX_ENTRIES = 4_096
MAX_UNCOMPRESSED_BYTES = 33_554_432
MAX_MEMBER_BYTES = 8_388_608


class PackageSafetyError(ValueError):
    pass


def validate_zip_bytes(package: bytes) -> dict[str, int]:
    if not package or len(package) > MAX_PACKAGE_BYTES:
        raise PackageSafetyError(f"package size must be between 1 and {MAX_PACKAGE_BYTES} bytes")
    if not zipfile.is_zipfile(io.BytesIO(package)):
        raise PackageSafetyError("candidate is not a valid ZIP archive")
    total = 0
    names: set[str] = set()
    folded_names: set[str] = set()
    windows_reserved = {
        "con", "prn", "aux", "nul",
        *(f"com{index}" for index in range(1, 10)),
        *(f"lpt{index}" for index in range(1, 10)),
    }
    with zipfile.ZipFile(io.BytesIO(package), "r") as archive:
        infos = archive.infolist()
        if not infos or len(infos) > MAX_ENTRIES:
            raise PackageSafetyError(f"ZIP entry count must be between 1 and {MAX_ENTRIES}")
        for info in infos:
            raw = info.filename
            normalized = raw.replace("\\", "/")
            path = PurePosixPath(normalized)
            if (
                "\x00" in raw
                or normalized.startswith("/")
                or path.is_absolute()
                or not path.parts
                or any(part in {"", ".", ".."} for part in path.parts)
                or any(":" in part or part.endswith((" ", ".")) for part in path.parts)
            ):
                raise PackageSafetyError(f"unsafe ZIP entry path: {raw!r}")
            if any(part.split(".", 1)[0].casefold() in windows_reserved for part in path.parts):
                raise PackageSafetyError(f"Windows-reserved ZIP entry path: {raw!r}")
            canonical = path.as_posix()
            folded = canonical.casefold()
            if canonical in names or folded in folded_names:
                raise PackageSafetyError(f"duplicate or case-colliding ZIP entry: {canonical!r}")
            names.add(canonical)
            folded_names.add(folded)
            if info.flag_bits & 0x1:
                raise PackageSafetyError(f"encrypted ZIP entry: {raw!r}")
            unix_mode = (info.external_attr >> 16) & 0o170000
            if unix_mode and not (stat.S_ISREG(unix_mode) or stat.S_ISDIR(unix_mode)):
                raise PackageSafetyError(f"special ZIP entry type: {raw!r}")
            if info.file_size > MAX_MEMBER_BYTES:
                raise PackageSafetyError(f"ZIP entry exceeds {MAX_MEMBER_BYTES} bytes: {raw!r}")
            total += info.file_size
            if total > MAX_UNCOMPRESSED_BYTES:
                raise PackageSafetyError(
                    f"ZIP uncompressed size exceeds {MAX_UNCOMPRESSED_BYTES} bytes"
                )
    return {"entry_count": len(names), "uncompressed_size": total}
