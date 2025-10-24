# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
from helper_functions import evaluate_staging, save_text_to_file
from get_assessment import staging_assessment
import json

app = Flask(__name__)

with open("parameters.json", "r", encoding="utf-8") as file:
    parameters_dict = json.load(file)


@app.route("/", methods=["GET", "POST"])
def index():
    results = {}
    text = ""

    if request.method == "POST":
        text = (request.form.get("input_text") or "").strip()

        if text:
            save_text_to_file(text)  

        for staging_parameter in ["T", "N", "EMVI", "MRF"]:
            average, _, recommendation_1 = staging_assessment(
                text, staging_parameter, parameters_dict
            )
            cutoffs = parameters_dict[f"{staging_parameter}_cutoff"]

            stage_text, status = evaluate_staging(
                staging_parameter, average, recommendation_1, cutoffs
            )

            results[f"{staging_parameter.lower()}_stage"] = {
                "text": stage_text.lstrip(),
                "status": status,
            }

    return render_template("index.html", result=results, input_text=text)


@app.route("/evaluate/<stage>", methods=["POST"])
def evaluate_stage(stage: str):
    text = (request.json.get("text", "") if request.is_json else "").strip()

    if text:
        save_text_to_file(text)

    average, _, recommendation_1 = staging_assessment(
        text, stage, parameters_dict
    )
    cutoffs = parameters_dict[f"{stage}_cutoff"]
    stage_text, status = evaluate_staging(stage, average, recommendation_1, cutoffs)

    return jsonify({"stage": stage, "text": stage_text.lstrip(), "status": status})


@app.route("/save", methods=["POST"])
def save():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()

    if text:
        save_text_to_file(text)
        return jsonify({"status": "saved"}), 200

    return jsonify({"status": "no text"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=False)
