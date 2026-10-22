# RabTech Academy — Task 2: Reproducible Research Preregistration

## Research topic
Study time and final mathematics grades in the UCI Student Performance dataset.

## Research question
In the mathematics-course dataset, do students reporting higher study time (categories 3–4) have a higher average final grade (`G3`) than students reporting lower study time (categories 1–2)?

## Important
This is an observational analysis. It can show an association, not prove that study time causes higher grades.

## Dataset
Use the official UCI Machine Learning Repository page:
https://archive.ics.uci.edu/dataset/320/student+performance

Download `student-mat.csv` and place it at:
`data/raw/student-mat.csv`

Do not edit the raw file. Keep the original file unchanged.

## Project structure
- `preregistration.md` — research question and analysis plan written before analysis
- `requirements.txt` — package versions for the environment
- `src/analyze.py` — reproducible analysis pipeline
- `tests/test_pipeline.py` — synthetic, data-blind pipeline test
- `notebooks/analysis.ipynb` — notebook outline for documenting analysis
- `data/raw/` — original dataset
- `data/interim/` — intermediate data
- `data/processed/` — cleaned analysis dataset
- `reports/` — results and figures

## Run it
Create a virtual environment, install dependencies, then run:

```bash
python -m pip install -r requirements.txt
python src/analyze.py
python -m unittest discover -s tests -v
```

The analysis script will stop with a clear message if the raw CSV is missing.

## Reproducibility notes
- The hypothesis and analysis choices are written in `preregistration.md`.
- The raw dataset should not be overwritten.
- The script saves the cleaned data and a text report.
- The test uses synthetic data only and does not inspect the real dataset.
- After installing packages successfully, create a full environment lockfile using:
  `python -m pip freeze > requirements-lock.txt`
  Commit that file only after you have run the project in your own environment.

## Before submission
1. Download the official dataset and put it in `data/raw/`.
2. Run the analysis and the test successfully.
3. Check the report and notebook; do not claim results until you have run them.
4. Commit the project to a public GitHub repository only if you are comfortable making it public.
5. Submit the public repository URL in the internship portal.
