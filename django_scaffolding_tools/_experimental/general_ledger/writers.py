from pathlib import Path
from typing import Dict, Any, List

from openpyxl.utils import get_column_letter
from openpyxl.workbook import Workbook

from django_scaffolding_tools._experimental.general_ledger.parsers import get_default_mappings


def write_transactions(target_file: Path, transactions: Dict[str, List[Dict[str, str]]], start_row: int = 6,
                       column_mappings: Dict[int, Dict[str, Any]] = get_default_mappings()):
    wb = Workbook()
    for account_id in transactions.keys():
        sheet = wb.create_sheet(account_id)
        ## Setting column widths
        for col_num, column_mapping in column_mappings.items():
            column_letter = get_column_letter(col_num)
            sheet.column_dimensions[column_letter].width = column_mapping.get('width', 20)
        row = start_row
        transaction_list = transactions[account_id]
        for transaction in transaction_list:
            for col_num, col_mapping in column_mappings.items():
                sheet.cell(column=col_num, row=row, value=transaction[col_mapping['name']])
                if col_mapping.get('number_format') is not None:
                    sheet.cell(column=col_num, row=row).number_format = col_mapping.get('number_format')
            row += 1
    wb.save(target_file)
