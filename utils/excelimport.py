import openpyxl
from pathlib import Path

class ExcelUtils:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"Excel file not found: {self.file_path}")

    def get_all_test_data(self, sheet_name: str) -> list[dict]:
        """Return all rows as a list of dictionaries (for parametrize)."""
        workbook = openpyxl.load_workbook(self.file_path)
        sheet = workbook[sheet_name]

        headers = [cell.value for cell in sheet[1]]  # first row = headers
        all_data = []

        for row in sheet.iter_rows(min_row=2, values_only=True):
            row_dict = {}
            for idx, header in enumerate(headers):
                value = row[idx]
                if header.lower() == "run_flag" and value:
                    value = str(value).upper().strip()  # normalize flag
                row_dict[header] = value
            all_data.append(row_dict)

        workbook.close()
        return all_data

    def get_test_data(self, sheet_name: str, test_case_id: str) -> dict:
        """Return data for a single TestCaseID."""
        all_data = self.get_all_test_data(sheet_name)
        for row in all_data:
            if str(row.get("TestCaseID")).strip() == test_case_id:
                return row
        raise ValueError(f"TestCaseID '{test_case_id}' not found in sheet '{sheet_name}'")
