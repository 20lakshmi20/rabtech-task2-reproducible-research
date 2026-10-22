# Preregistration: Study Time and Final Mathematics Grade

**Status:** Planned analysis — complete this document before examining analysis results.  
**Project:** RabTech Academy Data Science with Python & R internship, Task 2.  
**Dataset:** UCI Student Performance, mathematics course (`student-mat.csv`).

## 1. Research question
Among students in the mathematics-course dataset, is reporting higher study time associated with a higher final mathematics grade?

## 2. Population and sample
- **Target population:** Students similar to those represented by the UCI Student Performance mathematics-course dataset.
- **Study sample:** All rows in `student-mat.csv` that have valid values for `studytime` and `G3`.
- **Unit of observation:** One student record.
- **Scope limitation:** The dataset is not guaranteed to represent all students or schools. Findings will be described as applying to this dataset, not all students.

## 3. Exposure and comparator
- **Exposure:** Higher reported study time, defined before analysis as `studytime` categories 3 or 4.
- **Comparator:** Lower reported study time, defined before analysis as `studytime` categories 1 or 2.
- These are categories in the dataset, not measured hours per week.

## 4. Outcome and observation window
- **Primary outcome:** Final mathematics grade, `G3`, on the dataset's 0–20 scale.
- **Observation window:** The records and final-grade measure supplied in the downloaded UCI mathematics-course dataset. The dataset does not provide a common calendar observation window for this analysis.

## 5. Hypotheses
- **Null hypothesis (H0):** The mean `G3` grade is the same in the higher- and lower-study-time groups.
- **Alternative hypothesis (H1):** The mean `G3` grade differs between the groups.
- A two-sided test will be used. The expected direction is higher grades in the higher-study-time group, but the test will not be changed after seeing results.

## 6. Inclusion and exclusion rules
- Include all student rows in the mathematics dataset.
- Exclude rows only if `studytime` or `G3` is missing or cannot be converted to numeric.
- Exclude records with `studytime` values outside categories 1–4 from the primary comparison and report how many were excluded.
- Do not remove observations based on grade values or whether they support the hypothesis.
- Report the sample size in each group.

## 7. Data transformations
1. Keep the downloaded source CSV unchanged in `data/raw/`.
2. Load the CSV using the correct semicolon delimiter.
3. Convert `studytime` and `G3` to numeric values.
4. Create `study_group`: `higher` for `studytime` 3–4 and `lower` for 1–2.
5. Save the analysis-ready columns to `data/processed/analysis_data.csv`.

## 8. Primary statistical analysis
- Calculate the number of students, mean `G3`, and standard deviation of `G3` in each group.
- Calculate the mean difference: higher-study-time group minus lower-study-time group.
- Use a two-sided Welch independent-samples t-test (does not assume equal group variances).
- Report the p-value and Cohen's d as an effect-size estimate.
- Use a significance level of 0.05. Report the effect size and group summaries regardless of statistical significance.
- Do not interpret a p-value as the probability that the hypothesis is true.

## 9. Robustness checks
- Repeat the group comparison using the median and interquartile range as descriptive summaries.
- Repeat the comparison after excluding students whose final grade `G3` is zero; clearly label this as a sensitivity analysis, not the primary analysis.
- Report if a group is too small for a meaningful comparison.
- Do not silently change the primary definitions or tests after viewing results.

## 10. Missing data
Report the number of rows excluded because `studytime` or `G3` is missing/invalid. No imputation is planned for the primary analysis.

## 11. Reproducible environment and files
- Python and package versions will be recorded in `requirements-lock.txt` after a successful local run.
- The raw file will be retained unchanged.
- Processed data, analysis code, notebook, and report will be saved in their designated folders.
- A synthetic-data test will check pipeline behaviour without using the real dataset.

## 12. Limitations
- This is observational data, so the result cannot establish causation.
- Study time is represented by categories rather than exact measured hours.
- Other factors (for example, prior grades, attendance, family circumstances, and school context) may relate to both study time and grades.
- Results may not generalize beyond the dataset.

## 13. Amendments
If the plan must change, record the date, reason, and exact change below before reporting the updated analysis.

| Date | Change | Reason |
|---|---|---|
| Not applicable yet | No amendments planned | Analysis has not been run |
