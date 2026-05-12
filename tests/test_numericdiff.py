import json
import subprocess
import sys

from pytest import approx


def test_cli_numeric_diff(sample_csv_files):
    old_csv, new_csv = sample_csv_files

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "dift.cli",
            str(old_csv),
            str(new_csv),
            "--key",
            "customer_id",
            "--report",
            "json",
        ],
        capture_output=True,
        text=True,
    )

    numeric_report = json.loads(result.stdout)["numeric"]

    assert result.returncode == 0
    assert numeric_report[0]["new_outliers"] == []
    assert numeric_report[0]["old_outliers"] == []
    assert numeric_report[0]["delta_outliers"] == "Number of outliers did not change"
    assert numeric_report[2]["new_outliers"] == approx([1350.0, 120.0])
    assert numeric_report[2]["old_outliers"] == []
    assert numeric_report[2]["delta_outliers"] == "More outliers detected"
