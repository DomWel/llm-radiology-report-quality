## Open-Source LLM for Radiology Report Quality Assessment (Rectal Cancer Staging)

This repository hosts the code and resources for the paper "Utilizing an Open-Source LLM to Assess and Improve Radiology Report Quality for Tumor Staging."

We developed a workflow-compatible method using a locally run, open-source Large Language Model (**Llama 3.3-70B-Instruct**) to systematically assess the clarity and completeness of free-text radiology reports, focusing on rectal cancer MRI staging.

### Project Highlights:

* **Quality Assessment:** The LLM generates a certainty score (1–10) for four key staging parameters: **T stage, N stage, Mesorectal Fascia (MRF), and Extramural Vascular Invasion (EMVI)**. This scoring demonstrated excellent discrimination performance (AUCs 0.90 to 0.97).
* **Workflow Integration:** We created a Flask-based user interface to deliver color-coded, LLM-generated feedback directly to radiology residents.
* **Impact:** A reader study confirmed the utility of this approach, showing that LLM-guided revisions significantly improved the explicit documentation of N stage, MRF, and EMVI in the reports.

This method offers a practical solution for clinical quality assurance and enables the scalable curation of high-quality training datasets for AI development, functioning as a valuable complement to structured reporting.

**The code used for the LLM evaluation and the reader study interface is publicly available here.**
