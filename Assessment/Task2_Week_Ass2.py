"""Demonstrate CSV, JSON, Excel, PDF, logging, and typed file helpers."""

import csv
import importlib
import json
import logging
import pathlib
from typing import List, Optional, Union
import openpyxl  # type: ignore[reportMissingModuleSource]

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR, format="%(levelname)s-%(message)s")

Base_dir = pathlib.Path(__file__).resolve().parent


def _load_pymupdf():
    """Load pymupdf using either its current or legacy module name."""
    for module_name in ("pymupdf", "fitz"):
        try:
            return importlib.import_module(module_name)
        except ImportError:
            continue
    raise RuntimeError(
        "PDF support requires pymupdf. Install it with: python -m pip install pymupdf"
    )


def read_employees(file_path: pathlib.Path) -> List[dict]:
    """Read employee rows from a CSV file using pathlib and DictReader."""
    with file_path.open("r", newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def write_employee_outputs(rows: List[dict], directory: pathlib.Path) -> int:
    """Write all employees to JSON and employees earning over 50,000 to CSV."""
    json_path = directory / "employees.json"
    json_path.write_text(json.dumps(rows, indent=2), encoding="utf-8")

    high_earners = [row for row in rows if int(row["salary"]) > 50000]
    csv_path = directory / "high earners.csv"
    fieldnames = list(rows[0].keys()) if rows else []
    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if fieldnames:
            writer.writeheader()
            writer.writerows(high_earners)
    return len(high_earners)


def create_and_read_salary_workbook(rows: List[dict], file_path: pathlib.Path) -> int:
    """Create a salary workbook, reopen it, and return its data row count."""
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "salaries"
    sheet.append(["name", "department", "salary"])
    for row in rows:
        sheet.append([row["name"], row["department"], int(row["salary"])])
    workbook.save(file_path)

    reopened = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
    try:
        return max(reopened["salaries"].max_row - 1, 0)
    finally:
        reopened.close()


def create_sample_pdf(file_path: pathlib.Path) -> None:
    """Create a small local PDF for the PyMuPDF extraction demonstration."""
    pymupdf = _load_pymupdf()
    document = pymupdf.open()
    try:
        page = document.new_page()
        page.insert_text(
            (72, 72),
            "Employee salary report. This sample PDF demonstrates text extraction.",
        )
        document.save(file_path)
    finally:
        document.close()


def extract_first_page_text(file_path: pathlib.Path) -> str:
    """Print and return the first 100 characters of the first PDF page."""
    pymupdf = _load_pymupdf()
    with pymupdf.open(file_path) as document:
        if len(document) == 0:
            raise ValueError(f"PDF has no pages: {file_path}")
        text = document[0].get_text()
    excerpt = text[:100]
    print(excerpt, flush=True)
    return excerpt


def read_file(path: pathlib.Path) -> Optional[dict]:
    """Read a JSON object, logging missing file and malformed JSON errors."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        LOGGER.error("file not found: %s", path.name)
        return None
    except json.JSONDecodeError as error:
        LOGGER.error("invalid JSON in %s: %s", path.name, error)
        return None
    return data


def find_employee(name: str) -> Optional[dict]:
    """Find an employee by name in the generated employees.json file."""
    try:
        employee_rows = json.loads(
            (Base_dir / "employees.json").read_text(encoding="utf-8")
        )
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    return next(
        (row for row in employee_rows if row.get("name", "").casefold() == name.casefold()),
        None,
    )


def salary_value(value: Union[int, str]) -> Union[int, str]:
    """Normalize numeric salary string while accepting already parsed integers."""
    return int(value) if isinstance(value, str) else value


def main() -> None:
    """Run the complete file processing demonstration."""
    employee_csv = Base_dir / "employees.csv"
    rows = read_employees(employee_csv)
    high_count = write_employee_outputs(rows, Base_dir)
    print(f"Rows read:{len(rows)}| High earners written:{high_count}", flush=True)

    workbook_rows = create_and_read_salary_workbook(rows, Base_dir / "salary.xlsx")
    print(f"salary.xlsx created and read back:{workbook_rows}rows", flush=True)

    pdf_path = Base_dir / "sample.pdf"
    if not pdf_path.exists():
        create_sample_pdf(pdf_path)
    extract_first_page_text(pdf_path)

    read_file(Base_dir / "missing.txt")


if __name__ == "__main__":
    main()
