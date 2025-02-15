import pandas as pd
import re
from flask import Flask, request, send_file, render_template
from io import BytesIO

app = Flask(__name__)

def safe_sum_by_template(df, prefix, suffix, year):
    """
    Sums the values of all columns in df that match the pattern:
      prefix + "EF" + year + optional underscore and extra text + suffix
    """
    # Regex pattern allows an optional underscore and alphanumerics after the year.
    pattern = re.escape(prefix) + r"EF" + str(year) + r"(?:_[A-Za-z0-9]+)?" + re.escape(suffix)
    total = 0
    for col in df.columns:
        if re.fullmatch(pattern, col):
            total += df[col].sum()
    return total

def transform_csv_data(file_data, start_year, end_year):
    # Read the uploaded CSV file (file_data is a file-like object)
    df = pd.read_csv(file_data)

    # Prepare the output data dictionary.
    output_data = {
        "Year": [],
        "Undergrad enrollment - Full Time": [],
        "Undergrad enrollment - Part Time": [],
        "Graduate Enrollment": [],
        "First-Time Freshman Enrollment": [],
        "New Transfer Enrollment (Fall)": [],
        "Total Enrollment (undergrad + grad)": []
    }

    # Loop through each year in the specified range.
    for year in range(start_year, end_year + 1):
        undergrad_full = safe_sum_by_template(
            df,
            prefix="Full time total (",
            suffix="  All students  Undergraduate total)",
            year=year
        )
        undergrad_part = safe_sum_by_template(
            df,
            prefix="Part time total (",
            suffix="  All students  Undergraduate total)",
            year=year
        )
        grad_full = safe_sum_by_template(
            df,
            prefix="Full time total (",
            suffix="  All students  Graduate and First professional)",
            year=year
        )
        grad_part = safe_sum_by_template(
            df,
            prefix="Part time total (",
            suffix="  All students  Graduate and First professional)",
            year=year
        )
        fresh_full = safe_sum_by_template(
            df,
            prefix="Full time total (",
            suffix="  All students  Undergraduate  Degree/certificate-seeking  First-time)",
            year=year
        )
        fresh_part = safe_sum_by_template(
            df,
            prefix="Part time total (",
            suffix="  All students  Undergraduate  Degree/certificate-seeking  First-time)",
            year=year
        )
        transf_full = safe_sum_by_template(
            df,
            prefix="Full time total (",
            suffix="  All students  Undergraduate  Other degree/certificate-seeking  Transfer-ins)",
            year=year
        )
        transf_part = safe_sum_by_template(
            df,
            prefix="Part time total (",
            suffix="  All students  Undergraduate  Other degree/certificate-seeking  Transfer-ins)",
            year=year
        )

        grad_total = grad_full + grad_part
        freshman_total = fresh_full + fresh_part
        transfer_total = transf_full + transf_part
        total_enrollment = undergrad_full + undergrad_part + grad_total

        output_data["Year"].append(year)
        output_data["Undergrad enrollment - Full Time"].append(undergrad_full)
        output_data["Undergrad enrollment - Part Time"].append(undergrad_part)
        output_data["Graduate Enrollment"].append(grad_total)
        output_data["First-Time Freshman Enrollment"].append(freshman_total)
        output_data["New Transfer Enrollment (Fall)"].append(transfer_total)
        output_data["Total Enrollment (undergrad + grad)"].append(total_enrollment)

    # Create a DataFrame from the dictionary.
    df_out = pd.DataFrame(output_data)
    df_out = df_out.set_index("Year")
    # Sort years in descending order (latest first)
    df_out = df_out.sort_index(ascending=False)
    # Transpose so that metrics are rows and years are columns
    df_transposed = df_out.transpose()

    # Optional: Reorder rows if needed.
    desired_order = [
        "Total Enrollment (undergrad + grad)",
        "Undergrad enrollment - Full Time",
        "Undergrad enrollment - Part Time",
        "Graduate Enrollment",
        "First-Time Freshman Enrollment",
        "New Transfer Enrollment (Fall)"
    ]
    df_transposed = df_transposed.loc[desired_order]
    return df_transposed

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        # Get start and end years from the form and convert them to integers.
        start_year = int(request.form.get("start_year"))
        end_year = int(request.form.get("end_year"))

        # Process the file using our transformation function.
        df_transposed = transform_csv_data(file, start_year, end_year)

        # Write the transformed DataFrame to an in-memory bytes buffer.
        output = BytesIO()
        df_transposed.to_csv(output)
        output.seek(0)
        return send_file(
            output,
            as_attachment=True,
            download_name="transformed.csv",
            mimetype="text/csv"
        )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
