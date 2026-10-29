import json, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm as CM
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image, Table,
    TableStyle, PageBreak, HRFlowable, CondPageBreak)

R=json.load(open(f"{WORKSPACE_DIR}/results.json"))
F=f"{WORKSPACE_DIR}/artifacts/figs"
OUT=f"{WORKSPACE_DIR}/artifacts/Bank_Loan_Default_Analysis_Report.pdf"

NAVY=colors.HexColor("#1f3a5f"); TEAL=colors.HexColor("#2a9d8f"); RED=colors.HexColor("#c1121f")
GREY=colors.HexColor("#6c757d"); LIGHT=colors.HexColor("#eef2f6"); GOLD=colors.HexColor("#e9a000")
GRID=colors.HexColor("#c9d3dd")

ss=getSampleStyleSheet()
def St(name,**kw):
    base=kw.pop('parent',ss['Normal']); return ParagraphStyle(name,parent=base,**kw)
body=St('body',fontSize=10.2,leading=14.5,alignment=TA_JUSTIFY,spaceAfter=6)
h1=St('h1',fontSize=16,leading=20,textColor=NAVY,spaceBefore=4,spaceAfter=8,fontName='Helvetica-Bold')
h2=St('h2',fontSize=12,leading=15,textColor=NAVY,spaceBefore=10,spaceAfter=5,fontName='Helvetica-Bold')
h3=St('h3',fontSize=10.8,leading=13,textColor=TEAL,spaceBefore=7,spaceAfter=3,fontName='Helvetica-Bold')
bullet=St('bullet',parent=body,leftIndent=13,spaceAfter=3)
cap=St('cap',fontSize=8.5,textColor=GREY,alignment=TA_CENTER,spaceAfter=9,spaceBefore=2)
note=St('note',fontSize=9,leading=12.5,textColor=GREY,alignment=TA_JUSTIFY,spaceAfter=6)
story=[]
def para(t,st=body): story.append(Paragraph(t,st))
def bl(items,st=bullet):
    for it in items: story.append(Paragraph(f"\u2022&nbsp;&nbsp;{it}",st))
def img(fn,w=14.5*CM,caption=None):
    story.append(Image(f"{F}/{fn}",width=w,height=w*0.52))
    if caption: story.append(Paragraph(caption,cap))
def tbl(rows,widths,header_bg=NAVY,total_row=False,align_num=True):
    t=Table(rows,colWidths=widths)
    sty=[('BACKGROUND',(0,0),(-1,0),header_bg),('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),9),
        ('GRID',(0,0),(-1,-1),0.4,GRID),('VALIGN',(0,0),(-1,-1),'TOP'),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,LIGHT]),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),('LEFTPADDING',(0,0),(-1,-1),6)]
    if align_num and len(rows[0])>2: sty.append(('ALIGN',(1,0),(-1,-1),'CENTER'))
    if total_row:
        sty+=[('BACKGROUND',(0,-1),(-1,-1),colors.HexColor("#dce6ef")),('FONTNAME',(0,-1),(-1,-1),'Helvetica-Bold')]
    t.setStyle(TableStyle(sty)); story.append(t)
def rule(): story.append(HRFlowable(width="100%",thickness=0.8,color=GOLD)); story.append(Spacer(1,6))

# COVER
story.append(Spacer(1,3.0*CM))
story.append(Paragraph("Bank Loan Default Analysis",St('cv',fontSize=28,leading=34,textColor=NAVY,alignment=TA_CENTER,fontName='Helvetica-Bold')))
story.append(Spacer(1,6))
story.append(Paragraph("Default Prediction &amp; Credit-Risk Insights",St('sb',fontSize=14,textColor=TEAL,alignment=TA_CENTER)))
story.append(Spacer(1,12))
story.append(HRFlowable(width="55%",thickness=1.2,color=GOLD,hAlign='CENTER'))
story.append(Spacer(1,20))
story.append(Paragraph("Business Case Study &nbsp;\u2022&nbsp; Dataset: <b>Default_Fin.csv</b> (10,000 records)",St('m',fontSize=11,alignment=TA_CENTER,textColor=GREY)))
story.append(Spacer(1,4))
story.append(Paragraph("Prepared for: Credit Risk &amp; Lending Decisions",St('m2',fontSize=10.5,alignment=TA_CENTER,textColor=GREY)))
story.append(Spacer(1,1.5*CM))
kb=Table([[f"{R['total_customers']:,}", f"{R['default_rate']}%", f"{R['total_defaulters']}", f"{R['employment_rate']}%"],
          ["Total customers","Default rate","Defaulters","Employed"]],colWidths=[4.0*CM]*4)
kb.setStyle(TableStyle([('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,0),19),
    ('FONTSIZE',(0,1),(-1,1),9),('TEXTCOLOR',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,1),(-1,1),GREY),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,0),10),('BOTTOMPADDING',(0,1),(-1,1),12),
    ('BACKGROUND',(0,0),(-1,-1),LIGHT),('LINEABOVE',(0,0),(-1,0),2,TEAL)]))
story.append(kb)
story.append(Spacer(1,1.2*CM))
story.append(Paragraph("<i>Figures describe the supplied dataset and are associations, not causal relationships or statements about the bank's live portfolio.</i>",note))
story.append(PageBreak())

# 1 EXEC SUMMARY
story.append(Paragraph("1.&nbsp; Executive Summary",h1)); rule()
para(f"This report analyses <b>{R['total_customers']:,} customer records</b> from <b>Default_Fin.csv</b> to understand which financial "
     f"characteristics are associated with loan default. The observed default rate is <b>{R['default_rate']}%</b> ({R['total_defaulters']} "
     "defaulters) \u2014 a highly imbalanced target, roughly 1 defaulter for every 29 non-defaulters.")
para("The single most important finding is that <b>bank balance is the dominant signal for default in this dataset</b>. Default risk is "
     f"near-zero below 5,000 but rises to <b>{R['bal_bands']['20k+']['rate']}%</b> above 20,000. Counter-intuitively, defaulters hold about "
     f"<b>2.2\u00d7 the average balance</b> of non-defaulters ({R['def_profile']['default']['bal_mean']:,.0f} vs "
     f"{R['def_profile']['nondefault']['bal_mean']:,.0f}). Employment matters far less, and salary shows almost no monotonic relationship.")
story.append(Paragraph("Key takeaways",h3))
bl([
 f"<b>Overall default rate {R['default_rate']}%</b> \u2014 {R['total_defaulters']} of {R['total_customers']:,} customers.",
 f"<b>Unemployed default more</b>: {R['emp']['0']['rate']}% vs {R['emp']['1']['rate']}% employed \u2014 real but modest.",
 f"<b>Bank balance is decisive</b>: 0% (&lt;5k) \u2192 {R['bal_bands']['20k+']['rate']}% (&gt;20k); correlation {R['corr']['Bank Balance']}.",
 f"<b>Salary is weak</b>: near the {R['default_rate']}% baseline across all bands (correlation {R['corr']['Annual Salary']}).",
 f"A baseline model reaches <b>ROC-AUC {R['model']['roc_auc']}</b>, recall {R['model']['recall']} \u2014 features rank risk well, chiefly via balance.",
])
story.append(Paragraph("Bottom line",h3))
para("Bank balance alone separates most future defaulters, so it should anchor any early-warning rule. But the dataset lacks credit "
     "scores, loan amounts and repayment history, so these findings should <b>inform</b> \u2014 not automate \u2014 lending decisions, and "
     "must be checked for fair-lending compliance before operational use.")

# 2 BACKGROUND (same page flow)
story.append(Paragraph("2.&nbsp; Business Background &amp; Objectives",h1)); rule()
para("A bank lends to customers with varying employment statuses, bank balances and annual salaries. Some borrowers fail to repay, "
     "causing losses. The bank wants to analyse historical data to understand factors associated with default, identify high-risk "
     "customers, and make more informed lending decisions.")
story.append(Paragraph("Specific objectives",h3))
bl(["Measure the overall loan default rate.","Compare default rates between employed and unemployed customers.",
    "Investigate how bank balance and annual salary relate to default risk.","Identify segments needing extra credit-risk assessment.",
    "Develop a data-driven approach to support loan-approval decisions.","Lay a foundation for a future probability-of-default model."])
story.append(Paragraph("Business questions addressed",h3))
tbl([["#","Business question","Where answered"],
 ["Q1","What is the overall default rate?","\u00a73, \u00a74"],
 ["Q2","Does employment status relate to default risk?","\u00a75"],
 ["Q3","How does bank balance relate to default?","\u00a76"],
 ["Q4","Does annual salary relate to default risk?","\u00a77"],
 ["Q5","Which characteristics distinguish defaulters?","\u00a76\u2013\u00a78"],
 ["Q6","Can the bank identify high-risk customers?","\u00a79 (model)"]],
 [1.1*CM,10.3*CM,4.0*CM])
story.append(PageBreak())

# 3 DATASET
story.append(Paragraph("3.&nbsp; Dataset Overview &amp; Data Cleaning",h1))
story.append(Paragraph("Deliverable 1 \u2014 Data Cleaning &amp; Exploratory Data Analysis",h3)); rule()
para("The dataset contains 10,000 records and 5 columns with no missing values. Each row is one customer.")
tbl([["Column","Type","Description"],
 ["Index","Integer","Sequential record identifier"],
 ["Employed","Binary","1 = employed, 0 = unemployed"],
 ["Bank Balance","Numeric","Recorded bank balance (currency unspecified)"],
 ["Annual Salary","Numeric","Annual salary (currency unspecified)"],
 ["Defaulted?","Binary","Target: 1 = default, 0 = no recorded default"]],
 [3.3*CM,2.6*CM,9.5*CM],align_num=False)
story.append(Spacer(1,8))
story.append(Paragraph("Data-quality validation",h3))
tbl([["Check","Result"],["Total records","10,000"],["Total columns","5"],["Missing values","0 (all columns)"],
 ["Duplicate rows (full / excl. Index)","0 / 0"],["Recorded defaulters","333"],["Non-defaulters","9,667"],
 ["Binary fields valid (0/1 only)","Employed \u2713, Defaulted? \u2713"],["Negative values","None"],
 ["Target","Defaulted? (imbalanced, 3.33%)"]],[8.0*CM,7.4*CM],header_bg=TEAL,align_num=False)
story.append(Spacer(1,8))
story.append(Paragraph("Descriptive statistics",h3))
tbl([["Metric","Bank Balance","Annual Salary"],
 ["Mean",f"{R['avg_balance']:,.0f}",f"{R['avg_salary']:,.0f}"],
 ["Median",f"{R['median_balance']:,.0f}",f"{R['median_salary']:,.0f}"],
 ["Minimum","0","9,264"],["Maximum","31,852","882,651"]],[5.1*CM,5.2*CM,5.1*CM])
story.append(Paragraph("<i>A number of customers record a bank balance of exactly 0, treated as valid; salary has a floor near 9,264.</i>",note))
story.append(PageBreak())

# 4 OVERALL
story.append(Paragraph("4.&nbsp; Overall Default Rate (Q1)",h1)); rule()
para(f"Of {R['total_customers']:,} customers, <b>{R['total_defaulters']} defaulted</b> ({R['default_rate']}%) and "
     f"<b>{R['total_nondefaulters']:,} did not</b> ({R['nondefault_rate']}%). This heavy imbalance is the central challenge: a model "
     "predicting 'no default' for everyone would be 96.67% accurate yet useless \u2014 so accuracy must be replaced by precision, "
     "recall, F1 and PR-AUC when evaluating any model.")
img("fig1_dist.png",w=13*CM,caption="Figure 1 \u2014 Default vs non-default distribution across the 10,000 customers.")
story.append(Spacer(1,4))
# 5 EMPLOYMENT (flows under 4)
story.append(Paragraph("5.&nbsp; Default Rate by Employment Status (Q2)",h1)); rule()
para(f"Unemployed customers default at <b>{R['emp']['0']['rate']}%</b> versus <b>{R['emp']['1']['rate']}%</b> for employed \u2014 "
     "roughly 1.5\u00d7 more likely. A genuine but modest difference; employment alone is a weak classifier because both rates are low.")
tbl([["Employment","Customers","Defaulters","Default rate"],
 ["Unemployed (0)",f"{R['emp']['0']['count']:,}",f"{R['emp']['0']['def']}",f"{R['emp']['0']['rate']}%"],
 ["Employed (1)",f"{R['emp']['1']['count']:,}",f"{R['emp']['1']['def']}",f"{R['emp']['1']['rate']}%"],
 ["All",f"{R['total_customers']:,}",f"{R['total_defaulters']}",f"{R['default_rate']}%"]],
 [4.6*CM,3.6*CM,3.6*CM,3.6*CM],total_row=True)
story.append(Spacer(1,6))
img("fig2_emp.png",w=12.5*CM,caption="Figure 2 \u2014 Default rate by employment status vs the 3.33% baseline.")
story.append(PageBreak())

# 6 BALANCE
story.append(Paragraph("6.&nbsp; Bank Balance &amp; Default Risk (Q3, Q5)",h1)); rule()
para("Bank balance is the strongest signal in the dataset. Default rate escalates steeply and monotonically with balance \u2014 from "
     f"<b>0% below 5,000</b> to <b>{R['bal_bands']['20k+']['rate']}% above 20,000</b>. Correlation with default is "
     f"<b>{R['corr']['Bank Balance']}</b>, by far the largest of any feature.")
tbl([["Balance band","Customers","Defaulters","Default rate"]]+
 [[k,f"{R['bal_bands'][k]['count']:,}",f"{R['bal_bands'][k]['def']}",f"{R['bal_bands'][k]['rate']}%"]
  for k in ['0\u20135k','5k\u201310k','10k\u201315k','15k\u201320k','20k+']],
 [4.0*CM,3.8*CM,3.8*CM,3.8*CM])
story.append(Spacer(1,6))
img("fig3_bal.png",caption="Figure 3 \u2014 Default rate rises sharply with bank balance; the 20k+ band concentrates most defaults.")
para(f"Defaulters hold a far higher average balance ({R['def_profile']['default']['bal_mean']:,.0f}) than non-defaulters "
     f"({R['def_profile']['nondefault']['bal_mean']:,.0f}); the distributions below show defaulters shifted strongly to the right.")
img("fig6_baldist.png",caption="Figure 4 \u2014 Bank balance distribution: defaulters (red) cluster at much higher balances.")
story.append(Paragraph("Interpretation &amp; caution",h3))
para("This striking association must be read carefully. A high recorded balance coinciding with default may reflect how this dataset "
     "was constructed, or an unobserved factor. It does <b>not</b> prove that holding more money causes default \u2014 but it does make "
     "balance an effective <i>ranking</i> variable for flagging accounts for review.")
story.append(PageBreak())

# 7 SALARY + 8 PROFILE
story.append(Paragraph("7.&nbsp; Annual Salary &amp; Default Risk (Q4)",h1)); rule()
para(f"Annual salary shows almost no relationship with default. Across all bands the rate stays near the {R['default_rate']}% baseline, "
     f"and correlation with default is only <b>{R['corr']['Annual Salary']}</b> (effectively zero). Salary is not a useful standalone predictor.")
tbl([["Salary band","Customers","Defaulters","Default rate"]]+
 [[k,f"{R['sal_bands'][k]['count']:,}",f"{R['sal_bands'][k]['def']}",f"{R['sal_bands'][k]['rate']}%"]
  for k in ['<150k','150k\u2013300k','300k\u2013450k','450k\u2013600k','600k+']],
 [4.0*CM,3.8*CM,3.8*CM,3.8*CM])
story.append(Spacer(1,6))
img("fig4_sal.png",caption="Figure 5 \u2014 Default rate is essentially flat across salary bands.")
story.append(Paragraph("8.&nbsp; What Distinguishes Defaulters (Q5)",h1)); rule()
dp=R['def_profile']
tbl([["Metric","Non-defaulters","Defaulters"],
 ["Avg bank balance",f"{dp['nondefault']['bal_mean']:,.0f}",f"{dp['default']['bal_mean']:,.0f}"],
 ["Median bank balance",f"{dp['nondefault']['bal_med']:,.0f}",f"{dp['default']['bal_med']:,.0f}"],
 ["Avg annual salary",f"{dp['nondefault']['sal_mean']:,.0f}",f"{dp['default']['sal_mean']:,.0f}"],
 ["Median annual salary",f"{dp['nondefault']['sal_med']:,.0f}",f"{dp['default']['sal_med']:,.0f}"]],
 [5.3*CM,5.1*CM,5.0*CM])
story.append(Spacer(1,6))
img("fig5_profile.png",caption="Figure 6 \u2014 Defaulters hold ~2.2\u00d7 the average balance but similar salary.")
para("The defining difference is <b>bank balance</b>, not salary. A simple at-risk profile is <b>high bank balance, unemployed or "
     "lower-salaried</b> \u2014 with balance doing most of the discriminating work.")
story.append(PageBreak())

# 9 MODEL
story.append(Paragraph("9.&nbsp; Baseline Default-Prediction Model (Q6)",h1))
story.append(Paragraph("Deliverable 4 \u2014 Optional Default Prediction Model",h3)); rule()
para("A baseline <b>logistic regression</b> was trained on a 70/30 stratified split with <b>class weighting</b> to correct the 3.33% "
     "imbalance and standardised features. Given the imbalance, it is judged on precision, recall, F1 and PR-AUC rather than accuracy.")
tbl([["Metric","Value","Reading"],
 ["ROC-AUC",f"{R['model']['roc_auc']}","Excellent ranking of risk"],
 ["PR-AUC",f"{R['model']['pr_auc']}","Strong vs 0.033 baseline"],
 ["Recall (defaulters caught)",f"{R['model']['recall']}","Catches most true defaulters"],
 ["Precision",f"{R['model']['precision']}","Many false alarms at 0.5 cutoff"],
 ["F1-score",f"{R['model']['f1']}","Precision/recall trade-off"]],
 [5.6*CM,2.8*CM,7.0*CM],header_bg=TEAL,align_num=False)
story.append(Spacer(1,6))
CMX=R['model']['cm']
para(f"On the held-out test set the model correctly flagged <b>{CMX[1][1]} of {CMX[1][0]+CMX[1][1]}</b> actual defaulters "
     f"(recall {R['model']['recall']}), at the cost of {CMX[0][1]} false alarms. The high ROC-AUC ({R['model']['roc_auc']}) confirms the "
     "features \u2014 led overwhelmingly by bank balance \u2014 rank customers by risk very effectively. Low precision at the 0.5 "
     "threshold is expected under imbalance and is a <b>threshold-tuning</b> decision, not a model failure.")
img("fig7_cm.png",w=9*CM,caption="Figure 7 \u2014 Confusion matrix on the test set (threshold 0.5).")
mc=R['model_coef']
para(f"<b>Feature contribution</b> (standardised coefficients): <b>Bank Balance {mc['Bank Balance']}</b> (dominant), "
     f"Employed {mc['Employed']}, Annual Salary {mc['Annual Salary']} (negligible). The bank can identify high-risk customers from "
     "these features, but the predictive power is almost entirely a balance effect \u2014 this validates signal, it is not a production credit model.")
story.append(PageBreak())

# 10 DASHBOARD
story.append(Paragraph("10.&nbsp; Interactive Business Dashboard",h1))
story.append(Paragraph("Deliverable 2 \u2014 Dashboard specification",h3)); rule()
para("The following can be built directly in Power BI or Tableau from Default_Fin.csv, presenting the KPIs and segment comparisons as an interactive view.")
story.append(Paragraph("KPI cards",h3))
bl([f"Total Customers \u2014 {R['total_customers']:,}", f"Total Defaulters \u2014 {R['total_defaulters']}",
    f"Default Rate \u2014 {R['default_rate']}%", f"Employment Rate \u2014 {R['employment_rate']}%",
    f"Avg Bank Balance \u2014 {R['avg_balance']:,.0f}", f"Avg Annual Salary \u2014 {R['avg_salary']:,.0f}"])
story.append(Paragraph("Visuals",h3))
bl(["Bar \u2014 default rate by employment status.","Column \u2014 default rate by bank-balance band.",
    "Column \u2014 default rate by salary band.","Histogram \u2014 balance distribution split by default status.",
    "Donut \u2014 defaulters vs non-defaulters share.","Table \u2014 segment drill-down (employment \u00d7 balance band)."])
story.append(Paragraph("Slicers / filters",h3))
bl(["Employment status","Bank-balance band","Salary band","Default flag"])
story.append(Paragraph("KPI definitions (data model)",h3))
tbl([["KPI","Definition"],
 ["Default Rate (%)","Defaulters \u00f7 Total Customers \u00d7 100"],
 ["Non-Default Rate (%)","Non-defaulters \u00f7 Total Customers \u00d7 100"],
 ["Employment Rate (%)","Employed \u00f7 Total Customers \u00d7 100"],
 ["Default Rate by Employment","Default rate within each employment group"],
 ["Default Rate by Balance Band","Default rate within each balance band"],
 ["Default Rate by Salary Band","Default rate within each salary band"]],[6.2*CM,9.2*CM],align_num=False)
story.append(PageBreak())

# 11 CONSTRAINTS
story.append(Paragraph("11.&nbsp; Constraints, Assumptions &amp; Limitations",h1)); rule()
tbl([["Area","Constraint / assumption"],
 ["Dataset scope","Limited to the 10,000 supplied records."],
 ["Target variable","Defaulted?=1 is a recorded default; exact definition not provided."],
 ["Employment","Employed=1 means employed; 0 means unemployed."],
 ["Missing data","No missing values found."],
 ["Data quality","No duplicates or negative values; balances of 0 treated as valid."],
 ["Currency","Currency of salary and balance is unspecified."],
 ["Causation","Findings are associations, not causal relationships."],
 ["Predictive modelling","Any model needs validation, imbalance handling and proper metrics."],
 ["Business costs","Cost of approving a defaulter vs rejecting a good customer is unknown."],
 ["Fair lending","Features must be checked for fairness and regulatory compliance before use."]],
 [4.3*CM,11.1*CM],align_num=False)
story.append(Spacer(1,8))
story.append(Paragraph("Key analytical challenges",h3))
bl([
 "<b>Class imbalance</b> \u2014 only 3.33% defaulters, so accuracy is misleading; use recall / PR-AUC.",
 "<b>Limited features</b> \u2014 no credit score, loan amount, repayment history, tenure or debt-to-income ratio.",
 "<b>Correlation \u2260 causation</b> \u2014 especially the counter-intuitive balance effect.",
 "<b>Threshold choice</b> \u2014 weigh missed defaults against false alarms on good customers.",
 "<b>No loss quantification</b> \u2014 without loan amounts or dates, recovery rates, overdue days and total losses cannot be computed.",
])
story.append(PageBreak())

# 12 RECOMMENDATIONS
story.append(Paragraph("12.&nbsp; Recommendations &amp; Next Steps",h1))
story.append(Paragraph("Deliverable 5 \u2014 Executive summary &amp; recommendations",h3)); rule()
story.append(Paragraph("Most important findings",h3))
bl([
 f"Portfolio default rate is <b>{R['default_rate']}%</b>; defaults are concentrated, not spread evenly.",
 f"<b>Bank balance is the dominant risk marker</b> \u2014 the 20k+ band has a {R['bal_bands']['20k+']['rate']}% default rate and holds most defaulters.",
 f"<b>Unemployment adds moderate risk</b> ({R['emp']['0']['rate']}% vs {R['emp']['1']['rate']}%).",
 "<b>Salary is not predictive</b> on its own.",
])
story.append(Paragraph("Recommended actions",h3))
bl([
 "<b>Introduce a balance-based early-warning flag.</b> Route high-balance accounts (e.g. 15k+) to enhanced review rather than auto-decisioning.",
 "<b>Use the model for ranking, not rejection.</b> Score and rank applicants by default probability to prioritise manual review.",
 "<b>Tune the decision threshold to business cost.</b> Set the cutoff to minimise expected cost once loss/profit figures are known, not 0.5.",
 "<b>Investigate the balance\u2013default relationship</b> before operationalising it.",
 "<b>Monitor for fair-lending risk</b> \u2014 validate the features create no prohibited disparate impact.",
])
story.append(Paragraph("Additional data needed before lending decisions",h3))
bl(["Credit score / bureau history","Loan amount, tenure and product type","Repayment history and days-past-due",
 "Debt-to-income ratio and existing obligations","Dates (origination, default) for recovery and loss",
 "Cost parameters (loss given default, profit on a good loan)"])
story.append(Paragraph("Final outcome",h2))
para("The bank now has a clear, quantified picture of the observed default rate, the strong role of bank balance, the modest role of "
     "employment and the weak role of salary \u2014 with an explicit statement of the dataset's limits. These findings should <b>support "
     "better-informed, human-reviewed risk assessment</b> and provide a validated foundation for a future, richer predictive model once "
     "additional credit data is available \u2014 not, on their own, automate loan approvals or rejections.")

doc=SimpleDocTemplate(OUT,pagesize=A4,topMargin=1.7*CM,bottomMargin=1.7*CM,leftMargin=2.0*CM,rightMargin=2.0*CM,
    title="Bank Loan Default Analysis",author="Amazon Quick")
def footer(c,d):
    c.saveState(); c.setFont('Helvetica',8); c.setFillColor(GREY)
    c.drawString(2.0*CM,1.1*CM,"Bank Loan Default Analysis \u2014 Default_Fin.csv")
    c.drawRightString(A4[0]-2.0*CM,1.1*CM,f"Page {d.page}")
    c.setStrokeColor(colors.HexColor("#d4dbe2")); c.line(2.0*CM,1.35*CM,A4[0]-2.0*CM,1.35*CM)
    c.restoreState()
doc.build(story,onFirstPage=lambda c,d:None,onLaterPages=footer)
print("BUILT",OUT,round(os.path.getsize(OUT)/1024,1),"KB")
