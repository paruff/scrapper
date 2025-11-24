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

# Security: Require secret key in production; fail fast if not set in non-dev mode
if os.environ.get("FLASK_ENV") == "production" and not os.environ.get("FLASK_SECRET_KEY"):
    raise RuntimeError(
        "FLASK_SECRET_KEY environment variable must be set in production. "
        "Generate one with: python -c 'import secrets; print(secrets.token_hex())'"
    )
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

    # Validate states - only allow exact matches from AVAILABLE_STATES
    # This ensures no malicious input can reach the subprocess command
    validated_states = [s for s in selected_states if s in AVAILABLE_STATES]

    if not validated_states:
        flash("Please select valid states to scrape.", "error")
        return redirect(url_for("index"))

    if len(validated_states) != len(selected_states):
        invalid_count = len(selected_states) - len(validated_states)
        flash(f"Skipped {invalid_count} invalid state(s). Processing valid selections.", "warning")

    # Prepare command using only validated states
    # Security: states are whitelisted from AVAILABLE_STATES, not directly from user input
    states_arg = ",".join(validated_states)
    cmd = ["scrapy", "crawl", "vrm", "-a", f"states={states_arg}"]

    # Add optional page limit for testing - validate it's numeric
    page_limit = request.form.get("page_limit", "").strip()
    if page_limit:
        # Security: ensure page_limit is purely numeric before using it
        if page_limit.isdigit() and 1 <= int(page_limit) <= 1000:
            cmd.extend(["-s", f"CLOSESPIDER_PAGECOUNT={page_limit}"])
        else:
            flash("Invalid page limit. Must be a number between 1 and 1000.", "warning")

    try:
        # Run scraper in background
        # Security: Using list format for cmd prevents shell injection
        # For production, consider using Celery or similar task queue for async processing
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600,  # 10 minute timeout
            shell=False,  # Explicit: never use shell to prevent injection
            check=False,  # Don't raise on non-zero exit
        )

        if result.returncode == 0:
            flash(
                f"Successfully scraped states: {', '.join(validated_states)}. "
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

    # Additional security: reject filenames with path separators
    if "/" in filename or "\\" in filename or ".." in filename:
        flash("Invalid file requested.", "error")
        return redirect(url_for("index"))

    output_dir = Path("output").resolve()
    file_path = (output_dir / filename).resolve()

    # Ensure the resolved path is within the output directory (prevent path traversal)
    try:
        file_path.relative_to(output_dir)
    except ValueError:
        flash("Invalid file requested.", "error")
        return redirect(url_for("index"))

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
    # Development server - not for production use
    # For production, use a WSGI server like Gunicorn:
    #   gunicorn -w 4 -b 0.0.0.0:8000 web_app:app
    debug_mode = os.environ.get("FLASK_DEBUG", "1") == "1"
    host = os.environ.get("FLASK_HOST", "127.0.0.1")  # Localhost by default for security
    port = int(os.environ.get("FLASK_PORT", "5000"))

    if debug_mode and host == "0.0.0.0":
        print(
            "WARNING: Running in debug mode with host 0.0.0.0 is insecure. "
            "Only use this in trusted development environments."
        )

    app.run(debug=debug_mode, host=host, port=port)
