def generate_html(scan_result, risk_result, output_file="report.html"):
    html = f"""
    <html>
    <head>
        <title>TraceVector Report</title>
    </head>
    <body>
        <h1>TraceVector Investigation Report</h1>

        <h2>Scan Result</h2>
        <pre>{scan_result}</pre>

        <h2>Risk Assessment</h2>
        <pre>{risk_result}</pre>
    </body>
    </html>
    """

    with open(output_file, "w") as f:
        f.write(html)

    return output_file
