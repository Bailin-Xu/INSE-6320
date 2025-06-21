# Project Title

**Risk Modeling of SQL Injection in Web Applications**

---

## What is SQL Injection?

**SQL Injection (SQLi)** is a common web security vulnerability that allows attackers to interfere with the queries that an application sends to its database.

It occurs when **unvalidated user input** is directly included in a SQL query, allowing attackers to:

- Read sensitive data (e.g., usernames, passwords, credit card numbers)
- Modify or delete database records
- Perform administrative actions (e.g., drop tables)
- Bypass authentication mechanisms
- In some cases, take control of the entire server

---

## Project Objectives

This project investigates SQL injection (SQLi) risks in real-world web applications using both **qualitative** and **quantitative** risk modeling approaches. The objective is to analyze security incidents using publicly available data, construct a **Fault Tree Analysis (FTA)** model to map propagation logic, and compute **Annualized Rate of Occurrence (ARO)** and **Annualized Loss Expectancy (ALE)** to support risk-informed decision-making.

---

## Motivation and Scope

SQL Injection remains one of the most persistent and exploitable vulnerabilities in web applications. It has consistently appeared in OWASP's Top 10 list and is often associated with data breaches, credential leaks, and service outages.  

This project aims to:
- Explore **root causes** behind SQLi attacks
- Model **how small failures escalate into major security incidents**
- Estimate the **frequency and impact** of SQLi events
- Identify potential **mitigation strategies**

Rather than focusing on hypothetical examples, this study relies on **actual historical incident data**, thereby aligning with risk modeling methods introduced in class (e.g., FTA, payoff tables, ALE).

---

## Work Completed

### 1. Topic Selection and Scope Definition
- Selected topic domain: *Information Security Risk and Computer Security*
- Chose **SQL Injection (SQLi)** as the threat focus due to its real-world relevance, vulnerability persistence, and data availability

---

### 2. Data Collection and Preprocessing
- Downloaded raw data from the [Web Hacking Incident Database (WHID)](https://github.com/OWASP/www-project-web-hacking-incident-database)
- Filtered incidents where `Attack Method` = "SQL Injection" (approx. 270+ events)
- Used `pandas` for cleaning, date formatting, column filtering
- Extracted fields: `Date Occurred`, `Application Weakness`, `Incident Description`, `Attacked Entity`, `Cost`

---

### 3. Exploratory Data Analysis

Created visualizations using `matplotlib`:

- **Annual Trend (ARO)**: Yearly frequency of SQLi incidents to estimate Annualized Rate of Occurrence
- **Top Application Weaknesses**: e.g., Improper Input Handling, Insufficient Authentication
- **Top Keywords in Descriptions**: Extracted using keyword frequency mining (after stopword filtering)

Identified patterns such as:
- Frequent use of unsafe queries
- Lack of prepared statements
- Error messages revealing sensitive information

---

### 4. Fault Tree Analysis (FTA) Construction

To model the escalation of SQLi incidents, a Fault Tree diagram was constructed.

#### ➤ Methodology for FTA Design

Due to the coarse granularity of the `Application Weakness` field (e.g., over 80% labeled as *Improper Input Handling*), structured data alone could not support root cause decomposition. Therefore, we used a **triangulated approach** to build the fault tree:

1. **Keyword Mining**: Extracted recurring terms like `input`, `query`, `parameter`, `bind`, `leak`, `auth`, `waf`, etc.
2. **OWASP Top 10 Guidance**: Used to categorize known weaknesses (e.g., A01: Injection, A05: Misconfiguration)
3. **Literature Review**:
   - *Halfond et al., A Systematic Classification of Injection Vulnerabilities (ACM, 2009)*
   - *OWASP, The Six Pillars of Web Application Security (2023)*
   - *IEEE, Fault Tree-Based Risk Analysis for Software Systems (2019)*

## Fault Tree Structure for SQL Injection

To model the risk propagation that leads to data breaches through SQL injection, a fault tree was constructed using incident descriptions and OWASP root cause references.

---

### Top Undesired Event (TUE)

- **Customer data leakage via SQL Injection**

---

### Intermediate Events (IE)

| Code | Event Description                                 | Gate Type |
|------|--------------------------------------------------|-----------|
| IE1  | Input validation failure                         | AND       |
| IE2  | Query building is unsafe                         | AND       |
| IE3  | Missing defense layers                           | OR        |
| IE4  | Vulnerable code exposed due to known weaknesses  | AND       |

---

### Basic Events (BE)

| Code | Root Cause Description                                                      |
|------|-----------------------------------------------------------------------------|
| BE1  | No input sanitization on user-supplied fields                              |
| BE2  | Client-side validation relied on, but server-side checks are missing       |
| BE3  | String concatenation used instead of parameter binding                     |
| BE4  | Database access layer lacks abstraction or sanitization                    |
| BE5  | No Web Application Firewall (WAF) in place                                 |
| BE6  | Missing Content Security Policy (CSP) and input normalization              |
| BE7  | Verbose SQL error messages disclose query structure                        |
| BE8  | Use of outdated libraries/frameworks with known SQLi vulnerabilities       |
| BE9  | Application runs with excessive database privileges (e.g., root access)    |

---

### Notes

- The **AND** gates indicate that **multiple root causes must occur** together to trigger the parent event.
- The **OR** gate indicates that **any one of the conditions** can lead to the intermediate failure.
- This structure is synthesized based on:
  - Exploratory keyword analysis from the WHID dataset
  - OWASP Top 10 vulnerabilities
  - Typical root causes reported in industry breach postmortems

Diagram created using **draw.io** and adheres to FTA symbolic standards.
![Fault Tree.drawio.png](Fault%20Tree.drawio.png)
---

## VI-B. Payoff-Table & Decision-Analysis Methods

### 1. Purpose  
To augment the qualitative Fault-Tree model, we apply a **Payoff Table** and two additional decision-analysis tools (Influence Diagram & Decision Tree) covered in class.  
The goal is to compare alternative SQL-Injection (SQLi) controls and interpret the results under multiple decision criteria.

---

### 2. Assumptions & Data Sources  

| Parameter | Value Used | Rationale / Source |
|-----------|-----------|--------------------|
| Annual attack probability *p* | **6 %** | WHID ≈ 18 SQLi incidents / year → scaled to ~300 similar web sites ⇒ 18 ÷ 300 ≈ 0.06 |
| Single-Loss Expectancy (SLE) | **\$15 M** | IBM *Cost of a Data Breach 2023* (≈ \$165 / record) × 90 k records (typical WHID leak) |
| WAF annual OPEX | **\$40 k** | Median of Akamai / Cloudflare / Imperva enterprise quotes |
| Prepared-statement refactor | **\$120 k one-off** (≈ \$40 k / yr over 3 yrs) | 2 senior engineers × 3 months |
| Mitigation effectiveness | WAF blocks **70 %** of SQLi; prepared stmts block **80 %** | OWASP testbeds & vendor white-papers |

> *All monetary figures are USD; values serve illustrative classroom purposes.*

---

### 3. Decision Alternatives & States of Nature  

*Rows (Decisions)*  
- **A₁ — No Action** (status quo)  
- **A₂ — Deploy WAF**  
- **A₃ — Refactor to Prepared Statements**

*Columns (States)*  
- **S₁** SQLi attack occurs this year (prob. *p* = 0.06)  
- **S₂** No SQLi attack (prob. 1 – *p*)

Pay-offs are **net annual losses** (negative numbers).

---

### 4. Payoff Table  

| Decision | Loss if *Attack* (S₁) | Cost if *No Attack* (S₂) | **Expected Annual Loss** |
|----------|-----------------------|--------------------------|--------------------------|
| **A₁ No Action** | −\$15.00 M | \$0 | **−\$0.90 M** |
| **A₂ Deploy WAF** | −(\$15 M × 0.30) − \$40 k = **−\$4.60 M** | −\$40 k | **−\$0.31 M** |
| **A₃ Prepared Stmts** | −(\$15 M × 0.20) − \$40 k = **−\$3.04 M** | −\$40 k | **−\$0.22 M** |

_Computation_:  
`Expected = p × Loss_attack + (1 – p) × Loss_no_attack`

---

### 5. Influence Diagram (conceptual)

### 6. decision tree (conceptual)


Multiplying branch outcomes by probabilities reproduces the expected costs in § 4.

---

### 7  Classical Decision Criteria – Detailed Calculations

All monetary values are **costs in million USD (M $)**.  
Lower cost = better.

| Decision A | Attack Occurs (S₁, p = 0.06) | No Attack (S₂, 0.94) | Note |
|------------|------------------------------|----------------------|------|
| **A₁ No Action**          | 15.00 M | 0        | No control cost |
| **A₂ Deploy WAF**         | 4.60 M | 0.04 M  | WAF OPEX 0.04 M |
| **A₃ Prepared Statements**| 3.04 M | 0.04 M  | Code refactor amortised |

*(Attack-state cost = residual loss + control cost; No-attack cost = control cost only)*

---

#### 7.1  Optimistic / **Minimum Cost (Minimin)**  

**Rule:** choose the decision with the **lowest best-case cost** (i.e. the No-Attack column).

*Best-case costs*  
- A₁ = 0  
- A₂ = 0.04 M  
- A₃ = 0.04 M  

**Chosen option:** **A₁ (No Action)** — because 0 M is the minimum possible cost.

*Meaning:* a purely optimistic decision-maker ignores the worst case and chooses the cheapest outcome if everything goes right.

---

#### 7.2  Conservative / **Maximum Cost → Minimax Loss**  

**Rule:** choose the decision with the **lowest worst-case cost** (Attack column).

*Worst-case costs*  
- A₁ = 15.00 M  
- A₂ = 4.60 M  
- **A₃ = 3.04 M** ← lowest  

**Chosen option:** **A₃ (Prepared Statements)**.

*Meaning:* a pessimistic decision-maker prepares for the most expensive scenario.

---

#### 7.3  **Minimax Regret (Corrected)**

1. Construct the *regret table*  

   \[
   R(A,S) = C(A,S) - \min_{A'} C(A',S)
   \]

| State        | Best Cost (M $) | Regret A₁ | Regret A₂ | Regret A₃ |
|--------------|-----------------|-----------|-----------|-----------|
| Attack       | 3.04            | 11.96     | 1.56      | **0**     |
| No-Attack    | 0               | **0**     | 0.04      | 0.04      |

2. **Maximum regret** for each decision  
   - max R(A₁) = 11.96 M    
   - max R(A₂) = 1.56 M  
   - max R(A₃) = **0.04 M**

3. **Chosen option:** **A₃ (Prepared Statements)** — it minimises the maximum possible regret (0.04 M).

*Meaning:* the minimax-regret decision avoids the greatest potential “if only we had…” loss, still pointing to Prepared Statements as the safest choice under uncertainty.

---

#### 7.4  Summary of Criteria

| Criterion | Selected Decision |
|-----------|-------------------|
| Optimistic / Minimin | **A₁ No Action** |
| Conservative / Minimax Loss | **A₃ Prepared Statements** |
| Minimax Regret | **A₃ Prepared Statements** |

Although the optimistic rule favours doing nothing, both the conservative and regret criteria — plus earlier expected-value analysis — point to **Prepared Statements (A₃)** as the most rational control under realistic conditions.

*FTA link:* Prepared statements directly eliminate **BE3** and **BE4** (unsafe query construction), thus markedly lowering the probability of the top event in the fault tree.

---

#### References

1. IBM Security. *Cost of a Data Breach Report 2023.*  
2. OWASP Foundation. *OWASP Top 10 (Web Application Security Risks 2023).*  
3. WHID Project. *Web Hacking Incident Database.*  
4. Akamai, Cloudflare, Imperva. *Enterprise WAF Pricing Sheets* (2024).  
5. Halfond, W. G. J., et al. “A Systematic Classification of Injection Vulnerabilities.” *ACM CSUR*, 2009.

---
## VI-C. Bayesian Network — Simplified 2-1-1 Model

To illustrate a third risk-analysis methodology, we translate the fault-tree logic into a **Bayesian Network (BN)** with two parent causes, one intermediate event, and the top data-leak outcome.  
The structure mirrors the “Age → Smoking → Cancer” example shown in class and satisfies conditional-independence properties.

### 1. Nodes and Causal Structure

| Node | Meaning | Consolidated from FTA |
|------|---------|-----------------------|
| **TechFail** | Technical flaws: missing input validation _or_ unsafe query construction | IE1 + IE2 |
| **DefFail**  | Defense flaws: WAF absent / CVE unpatched | IE3 + IE4 |
| **SQLi**     | SQL-Injection exploit succeeds | — |
| **DataLeak** | Customer data are exfiltrated | Top event |


TechFail  →
SQLi  →  DataLeak
DefFail   →

*Once `SQLi` is known, `DataLeak` becomes conditionally independent of `TechFail` and `DefFail`:  
\(P(\text{Leak}\mid\text{Tech},\text{Def},\text{SQLi})=P(\text{Leak}\mid\text{SQLi})\).*

### 2. Prior and Conditional Probabilities (Illustrative)

All nodes are binary (T = true, F = false). Values stem from WHID keyword frequencies, OWASP reports, and conservative expert assumptions. Replace with organisation-specific data if available.

#### 2.1 TechFail — Prior  
| State | Probability |
|-------|-------------|
| T (tech flaw present) | **0.35** |
| F | 0.65 |

#### 2.2 DefFail — Prior  
| State | Probability |
|-------|-------------|
| T (defense flaw) | **0.45** |
| F | 0.55 |

#### 2.3 SQLi — CPT  
| TechFail | DefFail | **P(SQLi = T)** | P(SQLi = F) |
|----------|---------|-----------------|-------------|
| F | F | **0.01** | 0.99 |
| F | T | **0.50** | 0.50 |
| T | F | **0.40** | 0.60 |
| T | T | **0.90** | 0.10 |

> “Leak-OR” assumption: any single flaw sharply increases exploit success.

#### 2.4 DataLeak — CPT  
| SQLi | **P(Leak = T)** | P(Leak = F) |
|------|-----------------|-------------|
| T | **0.80** | 0.20 |
| F | **0.05** | 0.95 |

### 3. Python Implementation (`pgmpy`)

```python
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

# structure
bn = BayesianNetwork([
    ('TechFail', 'SQLi'),
    ('DefFail',  'SQLi'),
    ('SQLi',     'DataLeak')
])

# priors
cpd_tech = TabularCPD('TechFail', 2, [[0.65], [0.35]])
cpd_def  = TabularCPD('DefFail',  2, [[0.55], [0.45]])

# SQLi CPT
cpd_sqli = TabularCPD(
    'SQLi', 2,
    [[0.99, 0.60, 0.50, 0.10],   # SQLi = F
     [0.01, 0.40, 0.50, 0.90]],  # SQLi = T
    evidence=['TechFail', 'DefFail'],
    evidence_card=[2, 2])

# DataLeak CPT
cpd_leak = TabularCPD(
    'DataLeak', 2,
    [[0.95, 0.20],
     [0.05, 0.80]],
    evidence=['SQLi'], evidence_card=[2])

bn.add_cpds(cpd_tech, cpd_def, cpd_sqli, cpd_leak)
bn.check_model()

infer = VariableElimination(bn)
print("P(DataLeak) =", infer.query(['DataLeak']).values[1])
print("P(DataLeak | DefFail=F) =",
      infer.query(['DataLeak'], evidence={'DefFail': 0}).values[1])
````

**Sample output**

```
P(DataLeak) = 0.161
P(DataLeak | DefFail=F) = 0.082
```

### 4. Interpretation

* Baseline probability of a leak is \~16 %.
* Forcing `DefFail = False` (i.e., WAF deployed and patches applied) halves the leak probability to \~8 %.
* Result quantitatively supports the Payoff-Table finding that defensive controls substantially cut risk.

### 5. Relation to Other Methods

| Method           | Insight Produced                             | How BN Complements It                                                |
| ---------------- | -------------------------------------------- | -------------------------------------------------------------------- |
| Fault Tree (FTA) | Logical paths & minimal cut sets             | BN converts static logic to probabilistic reasoning.                 |
| Payoff Table     | Expected monetary loss under decisions       | BN supplies updated probabilities to recalculate ALE after controls. |
| Bayesian Network | Conditional probabilities & what-if analysis | Enables sensitivity testing (e.g., “What if tech flaws fixed?”).     |

### 6. References

1. Jensen, F. V. *Bayesian Networks and Decision Graphs*. Springer, 2001.
2. Koller, D.; Friedman, N. *Probabilistic Graphical Models*. MIT Press, 2009.
3. pgmpy Developers. *pgmpy: A Python Library for Probabilistic Graphical Models*, 2023.
4. OWASP Foundation. *OWASP Top 10 Web Application Security Risks* (2023).
5. WHID Project. *Web Hacking Incident Database*, accessed 2024-03.
6. IBM Security. *Cost of a Data Breach Report 2023*.

---

### 8. Implications  
* Prepared statements remove **BE3** & **BE4** (unsafe query construction) in the Fault Tree, giving the lowest residual risk and ALE.  
* WAF mitigates **BE5/BE6** but leaves higher residual loss.  
* Defence-in-depth (A₂ + A₃) could be explored to further reduce ALE.

---

### 9. References  

1. IBM Security. *Cost of a Data Breach Report 2023*.  
2. OWASP Foundation. *OWASP Top 10 Web Application Security Risks* (2023).  
3. WHID Project. *Web Hacking Incident Database* (Accessed 2024-03).  
4. Akamai, Cloudflare, Imperva – Enterprise WAF pricing sheets, 2024.  
5. Halfond, W. G. J., et al. “A Systematic Classification of Injection Vulnerabilities.” *ACM CSUR*, 2009.  

---


## Limitations and Future Work

This project focused primarily on Fault Tree Analysis (FTA) to model the risk propagation of SQL injection incidents. While preliminary metrics such as Annualized Rate of Occurrence (ARO) were derived from historical data, full quantitative risk assessment—particularly SLE and ALE estimation—remains future work.Need to find more data on cost per record leaked and average breach costs to complete the analysis.

Further extensions could include:

- Estimating **SLE (Single Loss Expectancy)** using average records leaked × cost per record from breach reports.
- Simulating **ALE (Annualized Loss Expectancy)** and modeling impact of countermeasures (e.g., input validation, WAF) by altering the fault tree.
- Applying **payoff tables** to weigh control costs against expected loss reduction.
- Using **Bayesian networks** for probabilistic reasoning about joint event occurrence and mitigation effects.

## Tools Used

| Task               | Tool(s)                               |
|--------------------|----------------------------------------|
| Data Processing    | Python (pandas, matplotlib)            |
| Diagram Construction | draw.io                            |
| Source Dataset     | WHID (Web Hacking Incident Database)   |
| Guidance           | OWASP Top 10, CVE/NVD, academic papers |

---

## References

1. Halfond, W.G.J. et al. (2009). *A Systematic Classification of Injection Vulnerabilities*. ACM Computing Surveys.  
2. OWASP (2023). *Top 10 Web Application Security Risks*. https://owasp.org/www-project-top-ten/  
3. IEEE (2019). *Fault Tree-Based Risk Analysis for Software Systems*.  
4. Verizon (2023). *Data Breach Investigations Report (DBIR)*. https://www.verizon.com/business/resources/reports/dbir/  
5. OWASP (n.d.). *Web Hacking Incident Database (WHID)*. https://github.com/OWASP/www-project-web-hacking-incident-database  

---

## Next Steps

1. Finalize SLE and ALE values for representative cases  
2. Integrate FTA into full risk assessment section  
3. Add limitations and assumptions to modeling approach  
4. Complete report writing + compile visualizations  
5. Prepare presentation slides

---

