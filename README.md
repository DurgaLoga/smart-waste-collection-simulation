# ♻️ Smart Waste Collection — Monte Carlo Simulation & Policy Optimization

### Using Data Analytics and Simulation to Support Smarter Urban Waste Management

**Python | Monte Carlo Simulation | Probability Modeling | Scenario Analysis | Smart Cities | Operations Analytics**

An end-to-end academic analytics project investigating how historical smart-bin sensor data and probabilistic simulation can support better waste collection decisions.

The project explores a practical operational question:

> **How frequently should smart waste bins be collected to balance collection efficiency with the risk of excessive bin fullness?**

**Domain:** Smart Cities | Waste Management | Operations Analytics  
**Status:** Completed Academic Project | Simulation-Based Decision Support

---

## 1. Business Problem

Traditional waste collection often follows fixed schedules, regardless of how quickly individual bins fill.

This can create two operational challenges:

- **Unnecessary collections:** Bins may be emptied before collection is required.
- **Delayed collections:** Bins may become excessively full before the next scheduled collection.

Smart-bin sensors provide historical information that can help organizations understand waste accumulation behavior.

However, waste accumulation is uncertain. Different bins can fill at different rates, and the same bin may behave differently over time.

### Project Objective

Develop a simulation-based analytical framework to evaluate alternative waste collection policies.

The goal is to understand the trade-off between:

**Collection frequency ↔ Risk of excessive bin fullness**

The project evaluates these trade-offs through probability modeling, Monte Carlo simulation, and scenario analysis.

---

## 2. Dataset Overview

The project uses historical smart-bin sensor observations from Wyndham, Australia.

| Attribute | Value |
|---|---:|
| Original Observations | 31,427 |
| Unique Smart Bins | 33 |
| Duplicate Records Removed | 766 |
| Bins Used for Behavioral Modeling | 32 |
| Daily Transitions Analyzed | 29,999 |

The dataset provides historical observations of smart-bin fullness.

These observations are used to estimate how bin fullness changes over time.

### Data Preparation

The analytical workflow included:

- Examining sensor records and dataset structure.
- Checking missing values and duplicates.
- Identifying inconsistencies in recorded observations.
- Organizing observations by bin and time.
- Preparing daily fullness transitions.
- Deriving empirical probability distributions for simulation.

The resulting data supported the development of a stochastic waste accumulation model.

---

## 3. Analytical Workflow

The project followed six major stages:

**Data Understanding → Data Auditing → Data Preparation → Probability Modeling → Monte Carlo Simulation → Scenario & Sensitivity Analysis**

Each stage is documented through Python scripts and Jupyter notebooks.

| Stage | Implementation |
|---|---|
| Data Auditing | [data_audit.py](code/data_audit.py) |
| Data Understanding | [01_data_understanding.ipynb](code/01_data_understanding.ipynb) |
| Data Preparation | [02_data_preparation.ipynb](code/02_data_preparation.ipynb) |
| Probability Modeling | [03_random_variable_preparation.ipynb](code/03_random_variable_preparation.ipynb) |
| Monte Carlo Simulation | [04_simulation_model.ipynb](code/04_simulation_model.ipynb) |
| Scenario & Sensitivity Analysis | [05_scenario_sensitivity_analysis.ipynb](code/05_scenario_sensitivity_analysis.ipynb) |

---

## 4. Probability Modeling

Rather than assuming that waste accumulates at a fixed rate, the project models waste accumulation as a random process.

Two empirical random variables were developed.

### Random Variable 1: Accumulation Occurrence

Represents whether waste accumulation occurs during a simulated time interval.

This captures uncertainty in the occurrence of waste accumulation.

**[View RV1 Probability Distribution](results/simulation_RV1_accumulation_occurrence.csv)**

### Random Variable 2: Increase Magnitude

Represents the magnitude of a fullness increase when accumulation occurs.

This captures variation in how much waste is added.

**[View RV2 Probability Distribution](results/simulation_RV2_increase_magnitude.csv)**

Together, these distributions provide the probabilistic inputs for the simulation.

---

## 5. Monte Carlo Simulation

The simulation generates possible waste accumulation trajectories using the estimated probability distributions.

### Baseline Simulation Configuration

| Parameter | Value |
|---|---:|
| Simulation Horizon | 365 Days |
| Monte Carlo Replications | 1,000 |
| Baseline Collection Threshold | 8 |
| Collection Policy | Threshold-Based |

The simulation evaluates how often collections would be required under the specified policy.

### Baseline Results

| Metric | Result |
|---|---:|
| Average Annual Collections | 62.836 |
| Median Annual Collections | 63 |
| Minimum Annual Collections | 48 |
| Maximum Annual Collections | 78 |

The results illustrate how uncertain waste accumulation can affect annual collection requirements.

**[View Baseline Simulation Summary](results/simulation_base_summary.csv)**

**[View Individual Simulation Run Summaries](results/simulation_base_run_summary.csv)**

The detailed daily simulation output is not included in the repository because of its size.

---

## 6. Collection Policy Scenario Analysis

The project evaluates alternative collection thresholds to understand their operational implications.

### Scenario Comparison

| Collection Threshold | Average Annual Collections | High-Fullness Days |
|---|---:|---:|
| 6 | 75.30 | 9.18% |
| 8 | 62.84 | 17.22% |
| 10 | 24.93 | 66.42% |

*Source: Project scenario analysis. These are simulated results rather than observed operational outcomes.*

### Interpretation

**Threshold 6 — More Frequent Collection**

- Higher collection frequency.
- Lower exposure to highly full bins.
- Potentially greater collection workload.

**Threshold 8 — Intermediate Policy**

- Moderate collection frequency.
- Moderate exposure to high fullness.
- Provides a comparison point between the alternatives.

**Threshold 10 — Less Frequent Collection**

- Substantially fewer collections.
- Much higher exposure to excessive fullness.
- Greater potential service-quality concerns.

### Key Finding

A lower collection threshold reduces high-fullness exposure but requires more frequent collections.

A higher threshold reduces collection frequency but increases the risk of bins remaining highly full.

The appropriate threshold depends on operational priorities, service requirements, and collection costs.

---

## 7. Sensitivity Analysis

Sensitivity analysis examines how simulation outcomes respond to changes in model assumptions and input parameters.

This helps assess whether conclusions remain stable under different conditions.

The project uses sensitivity analysis to explore the robustness of collection policy decisions.

This is particularly important because historical waste accumulation patterns may not remain constant.

**[View Scenario and Sensitivity Analysis Notebook](code/05_scenario_sensitivity_analysis.ipynb)**

---

## 8. Business and Operational Value

The project demonstrates how simulation can support operational planning when future demand is uncertain.

### Potential Applications

**Collection Policy Evaluation**

Compare alternative collection thresholds before introducing operational changes.

**Resource Planning**

Estimate how different policies could affect collection workload.

**Service Quality Management**

Understand the trade-off between collection frequency and excessive bin fullness.

**Scenario-Based Decision Support**

Evaluate policies under different assumptions without disrupting real-world operations.

**Smart-City Analytics**

Demonstrate how sensor observations can be transformed into decision-support models.

The project does not establish verified cost savings or real-world collection improvements.

Such benefits would require additional operational data and field validation.

---

## 9. Technologies and Methods

| Category | Technologies / Methods |
|---|---|
| Programming | Python |
| Data Processing | pandas, NumPy |
| Development Environment | Jupyter Notebook |
| Statistical Modeling | Empirical Probability Distributions |
| Simulation | Monte Carlo Simulation |
| Analytical Techniques | Scenario Analysis, Sensitivity Analysis |
| Business Domain | Smart Cities, Operations Analytics, Waste Management |

---

## 10. Repository Structure

```text
smart-waste-collection-simulation/
│
├── code/
│   ├── README.md
│   ├── data_audit.py
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_preparation.ipynb
│   ├── 03_random_variable_preparation.ipynb
│   ├── 04_simulation_model.ipynb
│   └── 05_scenario_sensitivity_analysis.ipynb
│
├── documentation/
│   ├── README.md
│   ├── SmartWasteCollection_Presentation.pdf
│   └── Smart_Waste_Collection_Doc.pdf
│
├── results/
│   ├── README.md
│   ├── simulation_base_summary.csv
│   ├── simulation_base_run_summary.csv
│   ├── simulation_RV1_accumulation_occurrence.csv
│   └── simulation_RV2_increase_magnitude.csv
│
├── .gitignore
└── README.md
```

---

## 11. Project Documentation

**[View Project Presentation](documentation/SmartWasteCollection_Presentation.pdf)**

**[View Detailed Project Report](documentation/Smart_Waste_Collection_Doc.pdf)**

The documentation provides additional context about the methodology, assumptions, and findings.

---

## 12. Limitations and Future Improvements

This project is an academic simulation rather than a production waste collection system.

### Current Limitations

- Historical sensor behavior may not fully represent future conditions.
- Simulation results depend on estimated probability distributions.
- Collection costs and vehicle-routing constraints are not directly optimized.
- Operational improvements have not been validated through field deployment.

### Potential Future Enhancements

- Incorporate weather and seasonal effects.
- Model individual bin behavior more explicitly.
- Integrate collection vehicle capacity and routing constraints.
- Introduce cost-based optimization.
- Evaluate predictive waste accumulation models.
- Develop an interactive simulation dashboard.

---

## 13. Key Takeaways

This project demonstrates how probabilistic simulation can support operational decisions when future conditions are uncertain.

**Key lessons:**

1. Historical sensor data can be transformed into probability-based simulation inputs.
2. Monte Carlo simulation helps quantify variation in operational outcomes.
3. Collection policies involve trade-offs between resource utilization and service quality.
4. Scenario analysis provides a structured way to compare alternative decisions.
5. Simulation results require operational validation before real-world implementation.

### Final Perspective

**Smart waste collection is not simply about collecting less frequently. It is about selecting policies that balance operational efficiency, uncertainty, and service quality.**
