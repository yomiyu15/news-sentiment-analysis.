# news-sentiment-analysis

Nova Financial Solutions challenge: **Predicting Price Moves with News Sentiment** — EDA, technical indicators, and sentiment–return correlation.

## Repository

- Default branch: `main`
- Task 1 development: branch `task-1`

Remote (replace with your fork if needed):

```text
https://github.com/yomiyu15/news-sentiment-analysis.git
```

> Use a single `.` before `.git` in the URL (not `..git`).

## Setup

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

On macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### FNSPID data

Place the financial news dataset files provided for the challenge under `data/raw/` (for example `fnspid_news.csv`). The EDA notebook picks the first `*.csv` or `*.parquet` in that folder. **Parquet:** install `pyarrow` in the venv if you use `.parquet` files (`pip install pyarrow`).

### Jupyter kernel (optional)

```powershell
.\venv\Scripts\python.exe -m ipykernel install --user --name=news-sentiment --display-name="Python (news-sentiment)"
```

Then choose this kernel when opening `notebooks/01_fnspid_eda.ipynb`.

## Project layout

```text
├── .github/workflows/unittests.yml   # CI: pytest on push/PR
├── data/raw/                         # Local data (gitignored by default)
├── notebooks/                        # Jupyter notebooks
├── src/                              # Shared Python modules
├── tests/                            # Unit tests
└── scripts/                          # Optional CLI scripts
```

## Notebooks

Start with `notebooks/01_fnspid_eda.ipynb` for Task 1 EDA (volume over time, publisher/domain analysis, headline length, CountVectorizer / word patterns). Set **`USE_MOCK = True`** in that notebook to run the full pipeline on synthetic data without placing files in `data/raw/`.

**Task 2:** `notebooks/02_task2_technical_indicators.ipynb` — optional `data/raw/stock_prices.csv`, else **yfinance**; `src/stock_prices.py`; **TA-Lib** SMA/EMA/RSI/MACD; **PyNance** return + vol; five-panel figure (price, RSI, MACD, return, vol).

**TA-Lib:** GitHub Actions installs `libta-lib-dev` on Ubuntu before `pip install`. On Windows, `pip install TA-Lib` needs a compatible wheel for your Python version; if the build fails, use Conda or follow the [ta-lib-python](https://github.com/ta-lib/ta-lib-python) install notes.

## Tests & CI

```powershell
pytest tests/ -v
```

Pushes to `main`, `task-1`, `task-2`, and `task-3` trigger the GitHub Actions workflow.

## Commits

This project follows [Conventional Commits](https://www.conventionalcommits.org/) (e.g. `feat:`, `docs:`, `chore:`, `test:`). Use `analyt:` only if your course explicitly allows that type; otherwise prefer `feat:` or `refactor:` for analysis code.
