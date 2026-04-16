"""Excel export for CVision: assembles DataFrames from plain data and writes an .xlsx with an embedded chart."""

import numpy as np
import pandas as pd


def export_to_excel(filename, x, raw_y1, raw_y2, y1, y2, smoothing_active,
                    deriv_y1, deriv_y2, second_deriv_y1, second_deriv_y2,
                    table_data, deriv_intersections, second_deriv_intersections,
                    e_half_value, measurement_type,
                    calibration_settings=None, calibration_unit_label="μA"):
    """
    Write CV analysis results to an .xlsx file with an embedded line chart.

    All arguments are plain Python/NumPy types — no Qt references.
    Raises on failure; the caller is responsible for catching and displaying errors.
    """
    df = pd.DataFrame({
        "x": x,
        "y_ox": raw_y1 if raw_y1 is not None else np.nan,
        "y_red": raw_y2 if raw_y2 is not None else np.nan,
    })

    if smoothing_active:
        df["smoothed_y_ox"] = y1
        df["smoothed_y_red"] = y2

    if deriv_y1 is not None:
        df["deriv_ox"] = deriv_y1
    if deriv_y2 is not None:
        df["deriv_red"] = deriv_y2
    if second_deriv_y1 is not None:
        df["second_deriv_ox"] = second_deriv_y1
    if second_deriv_y2 is not None:
        df["second_deriv_red"] = second_deriv_y2

    df_params = pd.DataFrame(table_data) if table_data else pd.DataFrame()

    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    df.to_excel(writer, sheet_name="Dane", index=False)
    df_params.to_excel(writer, sheet_name="Parametry", index=False)

    if calibration_settings is not None:
        params_sheet = writer.sheets["Parametry"]
        start_row = len(df_params) + 2
        params_sheet.write(start_row, 0, "Kalibracja")
        params_sheet.write(start_row + 1, 0, "electrode_area [cm²]")
        params_sheet.write(start_row + 1, 1, calibration_settings.electrode_area)
        params_sheet.write(start_row + 2, 0, "concentration [mM]")
        params_sheet.write(start_row + 2, 1, calibration_settings.concentration)
        params_sheet.write(start_row + 3, 0, "normalize_by_area")
        params_sheet.write(start_row + 3, 1, bool(calibration_settings.normalize_by_area))
        params_sheet.write(start_row + 4, 0, "normalize_by_concentration")
        params_sheet.write(start_row + 4, 1, bool(calibration_settings.normalize_by_concentration))
        params_sheet.write(start_row + 5, 0, "jednostka wynikowa")
        params_sheet.write(start_row + 5, 1, calibration_unit_label)

    if deriv_intersections:
        pd.DataFrame(deriv_intersections, columns=["x", "y"]).to_excel(
            writer, sheet_name="Przecięcia Pochodnej", index=False
        )
    if second_deriv_intersections:
        pd.DataFrame(second_deriv_intersections, columns=["x", "y"]).to_excel(
            writer, sheet_name="Przecięcia Drugiej Pochodnej", index=False
        )

    e_half_export = e_half_value if e_half_value is not None else 0.0
    n = len(x)
    workbook = writer.book
    worksheet = writer.sheets["Dane"]

    chart = workbook.add_chart({'type': 'line'})
    chart.add_series({
        'name': '=Dane!$B$1',
        'categories': f"=Dane!$A$2:$A${n + 1}",
        'values': f"=Dane!$B$2:$B${n + 1}",
        'line': {'color': 'red'},
    })
    chart.add_series({
        'name': '=Dane!$C$1',
        'categories': f"=Dane!$A$2:$A${n + 1}",
        'values': f"=Dane!$C$2:$C${n + 1}",
        'line': {'color': 'blue'},
    })

    y_min = df[["y_ox", "y_red"]].min().min()
    y_max = df[["y_ox", "y_red"]].max().max()
    worksheet.write(n + 1, 3, e_half_export)
    worksheet.write(n + 1, 4, y_min)
    worksheet.write(n + 2, 3, e_half_export)
    worksheet.write(n + 2, 4, y_max)
    chart.add_series({
        'name': 'E1/2',
        'categories': f"=Dane!$D${n + 2}:$D${n + 3}",
        'values': f"=Dane!$E${n + 2}:$E${n + 3}",
        'line': {'color': 'green', 'dash_type': 'dash'},
    })

    chart.set_x_axis({
        'name': 'E [mV]',
        'name_font': {'name': 'Verdana', 'bold': True, 'size': 14},
        'num_font': {'name': 'Calibri', 'size': 10},
        'crossing': 'min' if measurement_type == 0 else 'max',
    })
    chart.set_y_axis({
        'name': f'I [{calibration_unit_label}]',
        'name_font': {'name': 'Verdana', 'bold': True, 'size': 14},
        'num_font': {'name': 'Calibri', 'size': 10},
    })
    chart.set_size({'width': 600, 'height': 600})
    worksheet.insert_chart('G2', chart)

    writer.close()
