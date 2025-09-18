import os
import pandas as pd
from flask import Flask, request, jsonify, send_file
from dotenv import load_dotenv
from services.service import rule_based_scoring, ai_based_scoring
from services.storage_handler import save_offer, load_offer, save_leads, load_leads, save_results, load_results

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Endpoint to set the offer details
@app.route("/offer", methods=["POST"])
def set_offer():
    data = request.get_json()
    save_offer(data)
    return jsonify({"message": "Offer saved", "offer": data}), 201

# Endpoint to upload leads as a CSV file
@app.route("/leads/upload", methods=["POST"])
def upload_leads():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    try:
        df = pd.read_csv(file)
        leads = df.to_dict(orient="records")
        save_leads(leads)
        return jsonify({"message": "Leads uploaded", "total": len(leads)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to score leads using rule-based and AI-based logic
@app.route("/score", methods=["POST"])
def score_leads():
    offer = load_offer()
    leads = load_leads()
    if not offer:
        return jsonify({"error": "No offer set. Call /offer first"}), 400
    if not leads:
        return jsonify({"error": "No leads uploaded. Call /leads/upload first"}), 400

    results = []
    for lead in leads:
        rule_score = rule_based_scoring(lead, offer)
        ai_result = ai_based_scoring(lead, offer)
        final_score = rule_score + ai_result["ai_points"]

        results.append({
            "name": lead.get("name"),
            "role": lead.get("role"),
            "company": lead.get("company"),
            "intent": ai_result["intent"],
            "score": final_score,
            "reasoning": ai_result["reasoning"]
        })

    save_results(results)
    return jsonify({"message": "Scoring complete", "results": results}), 200

# Endpoint to get scored results as JSON
@app.route("/results", methods=["GET"])
def get_results():
    return jsonify(load_results()), 200

# Endpoint to export scored results as a CSV file
@app.route("/results/export", methods=["GET"])
def export_results():
    results = load_results()
    if not results:
        return jsonify({"error": "No results available"}), 400

    df = pd.DataFrame(results)
    file_path = "storage/scored_results.csv"
    df.to_csv(file_path, index=False)
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    # Run the Flask app in debug mode
    app.run(debug=True)
