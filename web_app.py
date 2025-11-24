"""Web application for VRM Scraper.

A simple Flask web interface that allows users to:
- Select states to scrape
- Trigger scraping jobs
- Download results as Excel files
"""

import os
import subprocess
from datetime import datetime
from pathlib import Path

from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key-change-in-production")

# Available states (could be loaded from states.yml)
AVAILABLE_STATES = ["VA", "TX", "NC", "FL", "CA", "GA", "SC", "AL", "TN", "KY"]


@app.route("/")
def index():
    """Render the main page with state selection form."""
    output_dir = Path("output")
    output_files = []

    if output_dir.exists():
        output_files = sorted(
            [f.name for f in output_dir.glob("vrm_listings_*.xlsx")], reverse=True
        )

    return render_template("index.html", states=AVAILABLE_STATES, output_files=output_files)


@app.route("/scrape", methods=["POST"])
def scrape():
    """Trigger a scraping job with selected states."""
    selected_states = request.form.getlist("states")

    if not selected_states:
        flash("Please select at least one state to scrape.", "error")
        return redirect(url_for("index"))

    # Validate states
    invalid_states = [s for s in selected_states if s not in AVAILABLE_STATES]
    if invalid_states:
        flash(f"Invalid states selected: {', '.join(invalid_states)}", "error")
        return redirect(url_for("index"))

    # Prepare command
    states_arg = ",".join(selected_states)
    cmd = ["scrapy", "crawl", "vrm", "-a", f"states={states_arg}"]

    # Add optional page limit for testing
    page_limit = request.form.get("page_limit", "").strip()
    if page_limit and page_limit.isdigit():
        cmd.extend(["-s", f"CLOSESPIDER_PAGECOUNT={page_limit}"])

    try:
        # Run scraper in background
        # For production, consider using Celery or similar task queue
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600,  # 10 minute timeout
        )

        if result.returncode == 0:
            flash(
                f"Successfully scraped states: {', '.join(selected_states)}. "
                f"Check the output directory for results.",
                "success",
            )
        else:
            flash("Scraping completed with warnings. Check logs for details.", "warning")
    except subprocess.TimeoutExpired:
        flash("Scraping timed out after 10 minutes. Results may be partial.", "warning")
    except Exception as e:
        flash(f"Error running scraper: {str(e)}", "error")

    return redirect(url_for("index"))


@app.route("/download/<filename>")
def download(filename):
    """Download a generated Excel file."""
    # Security: validate filename to prevent directory traversal
    if not filename.startswith("vrm_listings_") or not filename.endswith(".xlsx"):
        flash("Invalid file requested.", "error")
        return redirect(url_for("index"))

    file_path = Path("output") / filename

    if not file_path.exists():
        flash("File not found.", "error")
        return redirect(url_for("index"))

    return send_file(
        file_path,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@app.route("/api/status")
def api_status():
    """API endpoint to check available files."""
    output_dir = Path("output")
    output_files = []

    if output_dir.exists():
        for f in output_dir.glob("vrm_listings_*.xlsx"):
            output_files.append(
                {
                    "filename": f.name,
                    "size": f.stat().st_size,
                    "modified": datetime.fromtimestamp(f.stat().st_mtime).isoformat(),
                }
            )

    return jsonify({"files": sorted(output_files, key=lambda x: x["modified"], reverse=True)})


if __name__ == "__main__":
    # Development server - not for production
    app.run(debug=True, host="0.0.0.0", port=5000)
