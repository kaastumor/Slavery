"""Minimal read-only XLSX reader for the atlas migration tools.

This intentionally uses only the Python standard library. It supports the cell
representations used by the canonical v0.6.1 workbook and preserves source
values without modifying the workbook.
"""
from __future__ import annotations

from pathlib import Path
import re
import zipfile
import xml.etree.ElementTree as ET

_NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
_NS_REL_DOC = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
_NS_REL_PKG = "http://schemas.openxmlformats.org/package/2006/relationships"


def _col_index(cell_ref: str) -> int:
    m = re.match(r"([A-Z]+)", cell_ref)
    if not m:
        raise ValueError(f"Invalid XLSX cell reference: {cell_ref}")
    n = 0
    for ch in m.group(1):
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def _numeric(value: str):
    try:
        if re.fullmatch(r"[-+]?\d+", value):
            return int(value)
        return float(value)
    except ValueError:
        return value


class XlsxReader:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self._zip = zipfile.ZipFile(self.path)
        self._shared_strings = self._load_shared_strings()
        self._sheet_paths = self._load_sheet_paths()

    def close(self):
        self._zip.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    def _load_shared_strings(self) -> list[str]:
        try:
            data = self._zip.read("xl/sharedStrings.xml")
        except KeyError:
            return []
        root = ET.fromstring(data)
        strings: list[str] = []
        for si in root.findall(f"{{{_NS_MAIN}}}si"):
            text = "".join((t.text or "") for t in si.iter(f"{{{_NS_MAIN}}}t"))
            strings.append(text)
        return strings

    def _load_sheet_paths(self) -> dict[str, str]:
        workbook = ET.fromstring(self._zip.read("xl/workbook.xml"))
        rels = ET.fromstring(self._zip.read("xl/_rels/workbook.xml.rels"))
        rel_map = {
            rel.attrib["Id"]: rel.attrib["Target"]
            for rel in rels.findall(f"{{{_NS_REL_PKG}}}Relationship")
        }
        out: dict[str, str] = {}
        sheets = workbook.find(f"{{{_NS_MAIN}}}sheets")
        if sheets is None:
            return out
        for sheet in sheets.findall(f"{{{_NS_MAIN}}}sheet"):
            name = sheet.attrib["name"]
            rid = sheet.attrib[f"{{{_NS_REL_DOC}}}id"]
            target = rel_map[rid]
            if target.startswith("/"):
                path = target.lstrip("/")
            elif target.startswith("xl/"):
                path = target
            else:
                path = "xl/" + target.lstrip("./")
            out[name] = path
        return out

    @property
    def sheet_names(self) -> list[str]:
        return list(self._sheet_paths)

    def rows(self, sheet_name: str) -> list[list[object | None]]:
        if sheet_name not in self._sheet_paths:
            raise KeyError(f"Worksheet not found: {sheet_name}")
        root = ET.fromstring(self._zip.read(self._sheet_paths[sheet_name]))
        sheet_data = root.find(f"{{{_NS_MAIN}}}sheetData")
        if sheet_data is None:
            return []
        rows: list[list[object | None]] = []
        for row in sheet_data.findall(f"{{{_NS_MAIN}}}row"):
            values: dict[int, object | None] = {}
            max_col = -1
            for cell in row.findall(f"{{{_NS_MAIN}}}c"):
                ref = cell.attrib.get("r")
                if not ref:
                    continue
                col = _col_index(ref)
                max_col = max(max_col, col)
                cell_type = cell.attrib.get("t")
                if cell_type == "inlineStr":
                    inline = cell.find(f"{{{_NS_MAIN}}}is")
                    value = "" if inline is None else "".join(
                        (t.text or "") for t in inline.iter(f"{{{_NS_MAIN}}}t")
                    )
                else:
                    v = cell.find(f"{{{_NS_MAIN}}}v")
                    raw = None if v is None else v.text
                    if raw is None:
                        value = None
                    elif cell_type == "s":
                        value = self._shared_strings[int(raw)]
                    elif cell_type == "b":
                        value = raw == "1"
                    elif cell_type in ("str", "e"):
                        value = raw
                    else:
                        value = _numeric(raw)
                values[col] = value
            if max_col < 0:
                rows.append([])
            else:
                rows.append([values.get(i) for i in range(max_col + 1)])
        return rows


def table_dicts(rows: list[list[object | None]], first_header: str) -> list[dict[str, object | None]]:
    header_idx = None
    for i, row in enumerate(rows):
        if row and row[0] == first_header:
            header_idx = i
            break
    if header_idx is None:
        raise ValueError(f"Header row starting with {first_header!r} not found")
    headers = [str(x) if x is not None else "" for x in rows[header_idx]]
    out: list[dict[str, object | None]] = []
    for row in rows[header_idx + 1 :]:
        padded = list(row) + [None] * (len(headers) - len(row))
        if not any(v is not None and v != "" for v in padded[: len(headers)]):
            continue
        out.append({headers[i]: padded[i] for i in range(len(headers)) if headers[i]})
    return out
