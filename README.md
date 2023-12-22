# Electoral Data Analysis Project

## Overview

This repository contains scripts for analyzing electoral data, focusing on Senate elections, processing national budget data, and conducting econometric estimation on Senators and Political Parties. The scripts cover a wide range of tasks, including data loading, processing, graph creation, regression analysis, and exporting results for further exploration or visualization.

## Scripts

### 1. ProcesSenateDataCreateNetworks.py

#### Description

The **ProcesSenateDataCreateNetworks.py** script analyzes electoral data from various sources, including Senate, House, Presidency, Assemblies, Councils, Mayors, and Governorships. The script follows a structured process of data loading, processing, graph creation, graph analysis, and exporting results.

#### Key Steps

1. **Data Loading:**
   - Load electoral data from Senate, House, and other sources.

2. **Data Processing:**
   - Process the loaded data, focusing on relevant columns such as election year, candidate names, party codes, and votes.

3. **Graph Creation:**
   - Utilize the NetworkX library to create individual graphs for each election year, forming relationships between candidates based on shared votes or party affiliations.

4. **Graph Analysis:**
   - Calculate centrality measures for each node (candidate) in the graph, including eigenvector centrality, degree centrality, closeness centrality, and betweenness centrality.

5. **Exporting Results:**
   - Export the generated graphs and associated centrality measures in CSV and Pickle format for further analysis or visualization.

6. **Yearly Results:**
   - Generate CSV files for each election year containing new candidates, party-level results, and a composite graph that includes relationships from all previous years.

### 2. ProcesNationalBudgetData.py

#### Description

The **ProcesNationalBudgetData.py** script processes and analyzes national budget data. It combines information from multiple CSV files to generate a comprehensive dataset. The script calculates proportions, integrates inflation data, and creates visualizations to gain insights into the budget allocation trends over time.

#### Key Steps

1. **Data Loading:**
   - Load national budget data from multiple CSV files.

2. **Data Processing:**
   - Calculate proportions and integrate inflation data.

3. **Exporting Results:**
   - Export the processed data for further analysis.

### 3. EconometricEstimation.do

#### Description

The **EconometricEstimation.do** script conducts econometric estimation on Senators and Political Parties. It includes data loading, variable labeling, regression analysis, descriptive statistics, and exporting results.

#### Key Steps

1. **Data Loading - Senators:**
   - Load electoral data for Senators from a specified CSV file.

2. **Variable Labeling - Senators:**
   - Label relevant variables for clarity in subsequent analyses.

3. **Regression Analysis - Senators:**
   - Conduct regression analyses on various policy sectors for Senators.

4. **Descriptive Statistics - Senators:**
   - Compute descriptive statistics for selected variables.

5. **Data Loading - Political Parties:**
   - Load electoral data for Political Parties from a different CSV file.

6. **Regression Analysis - Political Parties:**
   - Conduct regression analyses at the party level.

7. **Descriptive Statistics - Political Parties:**
   - Compute descriptive statistics for selected variables at the party level.

8. **Data Cleanup:**
   - Drop unnecessary variables to streamline the dataset.

9. **Exporting Results:**
   - Export various results, including regression outputs and descriptive statistics.

10. **Summary Statistics:**
    - Compute additional summary statistics for certain variables.

## Project Notes

- This project represents early exploration into data science and econometric estimation during the 5th semester of university.
- For additional details, refer to the script comments and the context provided for each section.
