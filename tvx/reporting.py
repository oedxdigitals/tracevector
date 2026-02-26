import os
from datetime import datetime


def generate_html(scan_data: dict, risk_data: dict, filename: str) -> str:
    """
    Generate simple HTML fraud investigation report.
    """

    if not filename.endswith(".html"):
        filename += ".html"

    html_content = f"""
    <html>
    <head>
        <title>TraceVector Fraud Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f4f4f4;
            }}
            h1 {{
                color: #222;
            }}
            .box {{
                background: white;
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0,0,0,0.05);
            }}
            .high {{ color: red; }}
            .medium {{ color: orange; }}
            .low {{ color: green; }}
        </style>
    </head>
    <body>
        <h1>TraceVector Fraud Investigation Report</h1>
        <p><strong>Generated:</strong> {datetime.utcnow().isoformat()} UTC</p>

        <div class="box">
            <h2>Scan Result</h2>
            <pre>{scan_data}</pre>
        </div>

        <div class="box">
            <h2>Risk Assessment</h2>
            <p><strong>Score:</strong> {risk_data.get("score")}</p>
            <p><strong>Level:</strong> 
                <span class="{risk_data.get("level", "").lower()}">
                    {risk_data.get("level")}
                </span>
            </p>
            <p><strong>Flags:</strong></p>
            <ul>
                {''.join(f'<li>{flag}</li>' for flag in risk_data.get("flags", []))}
            </ul>
        </div>
    </body>
    </html>
    """

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    return os.path.abspath(filename)
