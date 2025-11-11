# 🧠 KION Compliance Prefilter (LM Studio + Phi-3 Mini)

This project classifies news articles as **Relevant** or **Irrelevant** for corporate
risk & compliance using a **local language model** hosted in
[LM Studio](https://lmstudio.ai).

The script:
- detects the **main company** mentioned in each article,  
- decides if the text is relevant for risk/compliance,  
- gives a short reason,  
- and saves the results to `answers.csv`.

---

## ⚙️ Requirements

| Component | Version / Note |
|------------|----------------|
| **Python** | 3.12 (3.12.7 recommended) |
| **LM Studio** | local server enabled on `http://127.0.0.1:1234/v1` |
| **Model** | `phi-3-mini-4k-instruct` |
| **Git** | for cloning the repository |

---

## 📦 Setup (Windows & macOS/Linux)

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Stefan-Atanasov/kion-compliance-filter.git
cd kion-compliance-filter
```

### 2️⃣ Create and activate a virtual environment

#### Windows (Git Bash)
```bash
python -m venv .venv
source .venv/Scripts/activate
```

#### Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Start LM Studio local server
1. Open **LM Studio**  
2. Download and load **`phi-3-mini-4k-instruct`**  
3. Start the **local server** (`http://127.0.0.1:1234/v1`)  
4. Keep LM Studio running while you use the script  

---

## 🧩 Running the compliance filter
```bash
python prefilter_lmstudio.py
```

This will:
1. Read article texts from `articles.json`  
2. Send them to your local model  
3. Write structured results into `answers.csv`

Example output:
```
id,company,decision,reason
1,Mercedes-Benz,Irrelevant,Marketing article without compliance issues.
2,ACME Corp.,Relevant,Mentions accounting fraud and regulator investigation.
```

---

## 📰 Example `articles.json`

A simple test file you can use:

```json
[
  {
    "id": 1,
    "text": "Mercedes-Benz introduces a new electric SUV with 700 km range and improved comfort. No legal or compliance matters are discussed."
  },
  {
    "id": 2,
    "text": "ACME Corp's CEO was charged with insider trading, leading to investigations by financial authorities."
  }
]
```

---

## 📁 Project structure
```
kion-compliance-filter/
├─ prefilter_lmstudio.py   # Main script
├─ articles.json           # Input articles
├─ answers.csv             # Output results (generated)
├─ requirements.txt        # Dependencies
├─ .gitignore              # Ignore venv & outputs
└─ README.md               # This file
```

---

## 🧾 `.gitignore`
Make sure your `.gitignore` includes:
```
__pycache__/
*.pyc
.venv/
venv/
answers.csv
.DS_Store
Thumbs.db
```

---

## ✅ Troubleshooting

| Issue | Possible Cause | Fix |
|-------|----------------|-----|
| `Model did not provide a clear reason.` | Model ran out of VRAM / context too long | Shorten text to ~2000 chars |
| `ERROR: articles.json not found.` | Wrong working directory | Run the script from inside the project folder |
| LM Studio not responding | Server not running or wrong URL | Click “Start Server” in LM Studio and check `http://127.0.0.1:1234/v1` |

---

## 🧪 Requirements file
Minimal dependencies (already in `requirements.txt`):

```
openai>=1.40.0
requests>=2.31.0
pandas>=2.2.0
```

---

## 💬 Credits
Developed by **Stefan Atanasov**  
For the **KION Compliance Filter Project** (TU Darmstadt, 2025)
