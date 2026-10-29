# Bank-Loan-Default-Analysis

A credit-risk analytics case study on the **`Default_Fin.csv`** dataset (10,000 customer records). The project measures the overall loan-default rate, identifies which customer financial characteristics are associated with default, builds a baseline default-prediction model, and translates the findings into business recommendations — with explicit attention to the dataset's limitations.

> **Important:** All findings are **associations, not causation**, and describe the supplied dataset only — not a bank's live portfolio. The analysis is intended to **support** human-reviewed credit-risk assessment, not to automate loan approvals or rejections.

---

## 📊 Key Findings

| Metric | Value |
|---|---|
| Total customers | 10,000 |
| Defaulters | 333 |
| **Overall default rate** | **3.33%** |
| Employed customers | 70.56% |
| Default rate — unemployed vs employed | 4.31% vs 2.92% |
| Default rate — balance `<5k` → `>20k` | 0% → 40.85% |
| Bank-balance correlation with default | 0.35 (strongest feature) |
| Annual-salary correlation with default | −0.02 (negligible) |
| Baseline model | ROC-AUC 0.948 · recall 0.83 · PR-AUC 0.549 |

**Headline:** Bank balance is the dominant signal for default in this dataset — defaulters hold roughly **2.2×** the average balance of non-defaulters. Employment status is a modest signal; annual salary is essentially not predictive.

---

## 📁 Repository Structure

```
bank-loan-default-analysis/
├── data/
│   └── Default_Fin.csv                          # Source dataset (10,000 records)
├── reports/
│   ├── Bank_Loan_Default_Analysis_Report.pdf    # Full 12-page analysis report
│   └── Bank_Loan_Default_Executive_Summary.pptx # 10-slide executive deck
├── workbook/
│   └── Bank_Loan_Default_Analysis.xlsx          # KPI + segment analysis workbook (with charts)
├── figures/                                     # Exported charts (PNG)
├── src/                                          # Analysis & report-generation scripts
├── README.md
└── .gitignore
```

> Adjust the paths above to match how you organise the files in your local folder before committing.

---

## 🔍 Dataset

`Default_Fin.csv` — 10,000 rows, 5 columns, no missing values, no duplicates.

| Column | Type | Description |
|---|---|---|
| `Index` | Integer | Sequential record identifier |
| `Employed` | Binary | 1 = employed, 0 = unemployed |
| `Bank Balance` | Numeric | Recorded bank balance (currency unspecified) |
| `Annual Salary` | Numeric | Annual salary (currency unspecified) |
| `Defaulted?` | Binary | Target: 1 = default, 0 = no recorded default |

The target is **imbalanced** (3.33% defaulters), so model evaluation uses precision, recall, F1 and PR-AUC rather than accuracy.

---

## 📈 Analysis Deliverables

1. **Data Cleaning & EDA** — type/duplicate/range validation, descriptive statistics, distributions.
2. **Segment Analysis** — default rate by employment, bank-balance band, and salary band.
3. **Business Insights Report** — the full 12-page PDF narrative with charts.
4. **Baseline Default-Prediction Model** — class-weighted logistic regression, evaluated on precision / recall / F1 / PR-AUC.
5. **Executive Summary & Recommendations** — 10-slide deck for a credit-risk audience.

---

## 💡 Recommendations (summary)

- Introduce a **balance-based early-warning flag** (route high-balance accounts to enhanced review).
- Use the model to **rank** applicants for manual review — not to auto-reject.
- **Tune the decision threshold** to business cost once loss/profit figures are known.
- **Investigate** why high balances coincide with default before operationalising it.
- **Monitor for fair-lending risk** before any operational use.

---

## ⚠️ Limitations

The dataset lacks credit scores, loan amounts, repayment history, tenure, and debt-to-income ratios. Without loan amounts or dates, recovery rates, overdue days, and total credit losses cannot be computed. Findings identify associations, not causal relationships.

---

## 🛠️ Tech Stack

Python · pandas · NumPy · Matplotlib · ReportLab (PDF) · python-pptx / pptxgenjs (deck) · xlsxwriter (workbook)

---

## 📄 License

Released under the MIT License — see `LICENSE` (optional; add if you want one).
