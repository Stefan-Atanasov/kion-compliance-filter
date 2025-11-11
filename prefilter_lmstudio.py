from openai import OpenAI
import json
import csv
from pathlib import Path

# Connect to local LM Studio API
client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)
# Model currently loaded in LM Studio
MODEL_NAME = "phi-3-mini-4k-instruct"


def analyze_text(text: str) -> tuple[str, str, str]:
    
    # Analyze a single article text for compliance relevance.

    # The model:
    # - Identifies the main company (if any)
    # - Classifies the text as Relevant or Irrelevant
    # - Provides a short reason for the decision

    # Returns:
    #     (company, decision, reason)
    
    
    prompt = f"""
You are a corporate compliance relevance filter.

Your task for the GIVEN TEXT:
1. Identify the MAIN company or organisation the text is primarily about (if any).
2. Decide whether the text is RELEVANT or IRRELEVANT for corporate risk & compliance.
3. Write ONE short sentence explaining your decision.

Classification rules:
- **RELEVANT:** The text mainly discusses a specific company AND includes serious negative or risk-related topics such as legal issues, fraud, corruption, regulatory investigations, ESG controversies, safety incidents, data breaches, major product failures, financial misconduct, or significant reputational crises.
- **IRRELEVANT:** The text focuses on marketing, product reviews, advertising, general information, or any content without concrete compliance or risk events.
- If the text describes **resolved or historical compliance cases** framed positively (e.g., lessons learned, reforms, cooperation, ethical improvements), classify it as **Irrelevant**, unless it reports new investigations, penalties, or ongoing legal issues.
- If **the text is very short or lacks meaningful information** (e.g., fewer than two sentences, or mostly headlines/keywords), classify as **Irrelevant**.
- If **no clear company is mentioned**, classify as **Irrelevant**.
- If **a company is mentioned only briefly or as an example**, and is **not the main subject**, classify as **Irrelevant**.

Output format (MUST follow exactly):
Company: <company name or None>
Decision: <Relevant or Irrelevant>
Reason: <one short sentence>

Text:
{text[:2500]}
"""

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=120,
    )

    reply = (completion.choices[0].message.content or "").strip()
    company, decision, reason = "", "Irrelevant", ""

    for line in reply.splitlines():
        lower = line.lower()
        if lower.startswith("company:"):
            company = line.split(":", 1)[1].strip()
        elif lower.startswith("decision:"):
            decision = line.split(":", 1)[1].strip()
        elif lower.startswith("reason:"):
            reason = line.split(":", 1)[1].strip()

    if not company or company.lower() in ("none", "n/a", "no company"):
        company = ""
    decision = "Relevant" if decision.strip().lower().startswith("rel") else "Irrelevant"
    if not reason:
        reason = "Model did not provide a clear reason."

    return company, decision, reason


def load_articles(path: Path) -> list:
    
    # Load articles from a JSON file.

    # Supports two formats:
    #   - A plain list of article dicts or strings
    #   - A dict containing an "articles" list

    # Returns:
    #     List of article items (each as dict or str)
    # Raises:
    #     ValueError if file cannot be parsed or format is invalid
    
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Could not load articles.json: {e}")

    if isinstance(data, dict) and "articles" in data:
        return data["articles"]
    if isinstance(data, list):
        return data
    raise ValueError("articles.json must contain a list or {'articles': [...]}.")


def main():
    
    # Main workflow:
    # - Loads input articles from 'articles.json'
    # - Sends each to analyze_text()
    # - Collects model outputs
    # - Saves all results to 'answers.csv'
    
    
    input_path = Path("articles.json")
    output_path = Path("answers.csv")

    if not input_path.exists():
        print("ERROR: articles.json not found.")
        return

    articles = load_articles(input_path)
    results = []

    for idx, item in enumerate(articles):
        if isinstance(item, str):
            text = item
            article_id = idx
        elif isinstance(item, dict):
            text = item.get("text", "")
            article_id = item.get("id", idx)
        else:
            continue

        if not text.strip():
            continue

        company, decision, reason = analyze_text(text)
        results.append({
            "id": article_id,
            "company": company,
            "decision": decision,
            "reason": reason,
        })

    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "company", "decision", "reason"])
        writer.writeheader()
        writer.writerows(results)

    print(f"Done. Wrote {len(results)} rows to {output_path}")


if __name__ == "__main__":
    main()
