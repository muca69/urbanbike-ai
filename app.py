from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlsplit
import html

import joblib
import pandas as pd

from config.common import ROOT, FEATURES, read_splits


# ============================================================
# 1. LOAD MACHINE LEARNING MODEL
# ============================================================

MODEL_PATH = ROOT / "models" / "regression.joblib"
FIGURE_PATH = ROOT / "reports" / "figures" / "04_predictions.png"
METRICS_PATH = ROOT / "reports" / "regression_metrics.csv"

bundle = joblib.load(MODEL_PATH)

selected = bundle["selected"]
model = bundle["models"][selected]

_, _, test = read_splits()

test = test.copy()
test["date"] = pd.to_datetime(test["date"])
test = test.sort_values("date")
test["date_label"] = test["date"].dt.strftime("%Y-%m-%d")

metrics = pd.read_csv(METRICS_PATH)


# ============================================================
# 2. MODEL PERFORMANCE
# ============================================================

def get_metrics():
    test_metrics = metrics.loc[
        metrics["split"] == "test"
    ]

    result = {}

    for _, row in test_metrics.iterrows():
        result[row["model"]] = {
            "MAE": float(row["MAE"]),
            "RMSE": float(row["RMSE"]),
            "R2": float(row["R2"])
        }

    return result


# ============================================================
# 3. HTML PAGE
# ============================================================

def render_page(date_value=None, submitted=False):

    dates = test["date_label"].tolist()

    if not dates:
        raise ValueError("Test dataset is empty")

    if date_value not in dates:
        date_value = dates[0]
        submitted = False

    prediction = None
    actual = None
    error = None

    if submitted:
        row = test.loc[
            test["date_label"] == date_value
        ].iloc[[0]]

        prediction = max(
            0.0,
            float(model.predict(row[FEATURES])[0])
        )

        actual = float(row["rentals"].iloc[0])
        error = abs(actual - prediction)

    options = ""

    for date in dates:
        selected_option = (
            "selected" if date == date_value else ""
        )

        options += (
            f'<option value="{date}" {selected_option}>'
            f'{date}</option>'
        )

    if submitted:
        prediction_value = f"{prediction:,.0f}"
        actual_value = f"{actual:,.0f}"
        error_value = f"{error:,.0f}"
        result_message = (
            f"Prediction for {html.escape(date_value)}"
        )
    else:
        prediction_value = "—"
        actual_value = "—"
        error_value = "—"
        result_message = (
            "Choose a historical date to generate a prediction."
        )

    performance = get_metrics()

    selected_metrics = performance[selected]

    model_rows = ""

    for name, values in performance.items():

        active_class = (
            "active-row" if name == selected else ""
        )

        model_rows += f"""
        <tr class="{active_class}">
            <td>{html.escape(name)}</td>
            <td>{values['MAE']:,.2f}</td>
            <td>{values['RMSE']:,.2f}</td>
            <td>{values['R2']:.3f}</td>
        </tr>
        """

    return f"""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1">

    <title>UrbanBike AI | Demand Intelligence</title>

    <style>

        :root {{
            --background: #0B1720;
            --surface: #142733;
            --surface-light: #1B3441;
            --mint: #8FE5B2;
            --white: #F4FAFC;
            --muted: #A9BAC4;
            --border: #29434D;
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            background: var(--background);
            color: var(--white);
            font-family:
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                Arial,
                sans-serif;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1180px;
            margin: auto;
            padding: 30px 24px 80px;
        }}

        /* HEADER */

        header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 15px 0 35px;
            border-bottom: 1px solid var(--border);
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 14px;
        }}

        .brand-icon {{
            width: 48px;
            height: 48px;
            display: grid;
            place-items: center;
            border-radius: 14px;
            background: #173B36;
            font-size: 26px;
        }}

        .brand-name {{
            font-size: 23px;
            font-weight: 800;
            letter-spacing: -0.7px;
        }}

        .brand-subtitle {{
            font-size: 10px;
            letter-spacing: 2px;
            color: var(--muted);
        }}

        .badge {{
            background: #173B36;
            border: 1px solid #306B54;
            color: var(--mint);
            padding: 8px 16px;
            border-radius: 30px;
            font-size: 13px;
            font-weight: 700;
        }}

        /* HERO */

        .hero {{
            padding: 65px 0 35px;
        }}

        .eyebrow {{
            color: var(--mint);
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 2px;
            text-transform: uppercase;
        }}

        h1 {{
            font-size: clamp(34px, 5vw, 62px);
            line-height: 1.1;
            letter-spacing: -2px;
            margin: 18px 0;
        }}

        .hero p {{
            color: var(--muted);
            font-size: 17px;
            max-width: 650px;
        }}

        /* PANELS */

        .panel {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 22px;
            padding: 30px;
            margin-top: 28px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.12);
        }}

        .panel-title {{
            font-size: 21px;
            font-weight: 750;
            margin: 0 0 8px;
        }}

        .panel-description {{
            color: var(--muted);
            font-size: 14px;
            margin-bottom: 25px;
        }}

        /* FORM */

        .prediction-form {{
            display: flex;
            align-items: flex-end;
            gap: 18px;
            flex-wrap: wrap;
        }}

        .field {{
            flex: 1;
            min-width: 220px;
        }}

        label {{
            display: block;
            font-size: 13px;
            font-weight: 700;
            margin-bottom: 10px;
        }}

        select {{
            width: 100%;
            background: var(--surface-light);
            border: 1px solid var(--border);
            color: var(--white);
            border-radius: 12px;
            padding: 16px;
            font-size: 15px;
            cursor: pointer;
        }}

        button {{
            border: none;
            background: var(--mint);
            color: #0B1720;
            padding: 17px 30px;
            border-radius: 12px;
            font-size: 15px;
            font-weight: 800;
            cursor: pointer;
            transition: 0.2s ease;
        }}

        button:hover {{
            background: #B4F5CD;
            transform: translateY(-2px);
        }}

        button:active {{
            transform: translateY(0);
        }}

        button:focus-visible,
        select:focus-visible {{
            outline: 3px solid var(--mint);
            outline-offset: 3px;
        }}

        /* RESULT CARDS */

        .section-heading {{
            margin: 45px 0 18px;
            font-size: 24px;
            font-weight: 800;
        }}

        .result-info {{
            color: var(--muted);
            font-size: 14px;
            margin-bottom: 20px;
        }}

        .cards {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 18px;
        }}

        .card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 28px;
            min-height: 175px;
            transition: 0.2s ease;
        }}

        .card:hover {{
            border-color: #467966;
            transform: translateY(-3px);
        }}

        .card-icon {{
            color: var(--mint);
            font-size: 25px;
            margin-bottom: 15px;
        }}

        .card-label {{
            color: var(--muted);
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
        }}

        .card-value {{
            font-size: clamp(28px, 3vw, 42px);
            font-weight: 850;
            margin-top: 12px;
            letter-spacing: -1px;
        }}

        .card:first-child .card-value {{
            color: var(--mint);
        }}

        /* METRICS */

        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-top: 20px;
        }}

        .metric {{
            background: var(--surface-light);
            padding: 22px;
            border-radius: 14px;
        }}

        .metric-label {{
            color: var(--muted);
            font-size: 12px;
        }}

        .metric-value {{
            font-size: 27px;
            font-weight: 800;
            margin-top: 8px;
        }}

        /* CHART */

        .chart-container {{
            background: white;
            border-radius: 15px;
            padding: 15px;
            margin-top: 22px;
        }}

        .chart-container img {{
            width: 100%;
            height: auto;
            display: block;
        }}

        /* TABLE */

        .table-wrapper {{
            overflow-x: auto;
            margin-top: 25px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }}

        th {{
            color: var(--muted);
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        th, td {{
            padding: 17px;
            border-bottom: 1px solid var(--border);
        }}

        td {{
            font-size: 14px;
        }}

        .active-row {{
            background: rgba(143,229,178,0.08);
            color: var(--mint);
            font-weight: 700;
        }}

        /* FOOTER */

        footer {{
            margin-top: 60px;
            padding-top: 25px;
            border-top: 1px solid var(--border);
            color: var(--muted);
            font-size: 13px;
            display: flex;
            justify-content: space-between;
            gap: 15px;
        }}

        /* RESPONSIVE */

        @media (max-width: 800px) {{

            .cards,
            .metrics-grid {{
                grid-template-columns: 1fr;
            }}

            .hero {{
                padding-top: 45px;
            }}

            .prediction-form {{
                flex-direction: column;
                align-items: stretch;
            }}

            button {{
                width: 100%;
            }}
        }}

        @media (max-width: 480px) {{

            .container {{
                padding: 20px 15px 50px;
            }}

            .panel {{
                padding: 20px;
            }}

            .brand-name {{
                font-size: 19px;
            }}

            .brand-subtitle {{
                font-size: 8px;
            }}

            .badge {{
                font-size: 11px;
                padding: 7px 10px;
            }}

            footer {{
                flex-direction: column;
            }}
        }}

    </style>
</head>

<body>

<div class="container">

    <!-- HEADER -->

    <header>

        <div class="brand">

            <div class="brand-icon" aria-hidden="true">
                🚲
            </div>

            <div>
                <div class="brand-name">
                    urbanbike.ai
                </div>

                <div class="brand-subtitle">
                    DEMAND INTELLIGENCE
                </div>
            </div>

        </div>

        <div class="badge">
            ● {html.escape(selected)} ML
        </div>

    </header>


    <!-- HERO -->

    <section class="hero">

        <div class="eyebrow">
            Smart Mobility Analytics
        </div>

        <h1>
            Predict the city<br>
            in motion.
        </h1>

        <p>
            AI-powered bike rental demand prediction.
            Explore historical daily rental patterns
            and evaluate machine learning performance.
        </p>

    </section>


    <!-- PREDICTION FORM -->

    <section class="panel">

        <h2 class="panel-title">
            Demand Prediction
        </h2>

        <p class="panel-description">
            Select a historical date from the test dataset
            to generate a one-day rental prediction.
        </p>

        <form class="prediction-form" method="GET">

            <div class="field">

                <label for="date">
                    Select Date
                </label>

                <select id="date" name="date" required>
                    {options}
                </select>

            </div>

            <input type="hidden" name="predict" value="1">

            <button type="submit">
                ✨ Predict Demand
            </button>

        </form>

    </section>


    <!-- RESULTS -->

    <section>

        <h2 class="section-heading">
            Prediction Results
        </h2>

        <p class="result-info" aria-live="polite">
            {result_message}
        </p>

        <div class="cards">

            <article class="card">

                <div class="card-icon" aria-hidden="true">
                    ↗️
                </div>

                <div class="card-label">
                    Predicted Rentals
                </div>

                <div class="card-value">
                    {prediction_value}
                </div>

            </article>

            <article class="card">

                <div class="card-icon" aria-hidden="true">
                    🚲
                </div>

                <div class="card-label">
                    Actual Rentals
                </div>

                <div class="card-value">
                    {actual_value}
                </div>

            </article>

            <article class="card">

                <div class="card-icon" aria-hidden="true">
                    ◎
                </div>

                <div class="card-label">
                    Absolute Error
                </div>

                <div class="card-value">
                    {error_value}
                </div>

            </article>

        </div>

    </section>


    <!-- MODEL PERFORMANCE -->

    <section class="panel">

        <h2 class="panel-title">
            Model Performance
        </h2>

        <p class="panel-description">
            Evaluation results on the historical test dataset.
            The selected model was chosen using validation MAE.
        </p>

        <div class="metrics-grid">

            <div class="metric">

                <div class="metric-label">
                    Test MAE
                </div>

                <div class="metric-value">
                    {selected_metrics['MAE']:,.2f}
                </div>

            </div>

            <div class="metric">

                <div class="metric-label">
                    Test RMSE
                </div>

                <div class="metric-value">
                    {selected_metrics['RMSE']:,.2f}
                </div>

            </div>

            <div class="metric">

                <div class="metric-label">
                    Test R²
                </div>

                <div class="metric-value">
                    {selected_metrics['R2']:.3f}
                </div>

            </div>

        </div>

        <div class="chart-container">

            <img
                src="/predictions.png"
                alt="Actual versus predicted bike rentals
                     on the historical test dataset"
            >

        </div>

    </section>


    <!-- MODEL COMPARISON -->

    <section class="panel">

        <h2 class="panel-title">
            Model Comparison
        </h2>

        <p class="panel-description">
            Performance of all regression models
            on the test dataset.
            Lower MAE and RMSE indicate smaller errors.
        </p>

        <div class="table-wrapper">

            <table>

                <thead>
                    <tr>
                        <th>Model</th>
                        <th>Test MAE</th>
                        <th>Test RMSE</th>
                        <th>Test R²</th>
                    </tr>
                </thead>

                <tbody>
                    {model_rows}
                </tbody>

            </table>

        </div>

    </section>


    <!-- FOOTER -->

    <footer>

        <span>
            ©️ UrbanBike AI — Academic Machine Learning Project
        </span>

        <span>
            Powered by {html.escape(selected)} Regression
        </span>

    </footer>

</div>

</body>
</html>
"""


# ============================================================
# 4. HTTP SERVER
# ============================================================

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):

        parsed = urlsplit(self.path)

        if parsed.path == "/predictions.png":

            if not FIGURE_PATH.exists():
                self.send_error(
                    404,
                    "Prediction chart not found"
                )
                return

            content = FIGURE_PATH.read_bytes()

            self.send_response(200)
            self.send_header("Content-Type", "image/png")
            self.send_header(
                "Content-Length",
                str(len(content))
            )
            self.end_headers()

            self.wfile.write(content)
            return

        if parsed.path != "/":
            self.send_error(404)
            return

        params = parse_qs(parsed.query)

        date_value = params.get(
            "date", [None]
        )[0]

        submitted = (
            params.get("predict", ["0"])[0] == "1"
        )

        content = render_page(
            date_value=date_value,
            submitted=submitted
        ).encode("utf-8")

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8"
        )

        self.send_header(
            "Content-Length",
            str(len(content))
        )

        self.end_headers()
        self.wfile.write(content)


# ============================================================
# 5. START APPLICATION
# ============================================================

if __name__ == "__main__":

    server = HTTPServer(
        ("127.0.0.1", 8000),
        Handler
    )

    print("=" * 50)
    print("UrbanBike AI Dashboard")
    print("Selected model:", selected)
    print("Open: http://127.0.0.1:8000")
    print("=" * 50)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()