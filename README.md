# The Wallet Vote: Economics & Presidential Approval

A research-oriented data science project investigating the causal relationship between economic indicators and US Presidential approval ratings.

## Research Question
> "Do changes in core economic indicators (Inflation, Unemployment, Gas Prices) serve as leading indicators for Presidential approval ratings?"

## Methodology
This project employs rigorous time-series analysis:
1.  **Data Ingestion:** Automated fetching of FRED economic data and Gallup/FiveThirtyEight approval data.
2.  **Stationarity Testing:** Augmented Dickey-Fuller (ADF) tests to determine the integration order of the series.
3.  **Granger Causality:** Testing if past values of economic metrics provide statistically significant predictive power for approval ratings.
4.  **Interactive Visualization:** Utilizing **Altair** for multi-layered time-series exploration and cross-correlation heatmaps.

## Reproducibility (Docker)
This project is fully containerized. To run the analysis environment:

1.  **Build the image:**
    ```bash
    docker build -t wallet-vote-research .
    ```

2.  **Run the container:**
    ```bash
    docker run -p 8888:8888 -v $(pwd):/app wallet-vote-research
    ```

3.  **Access:** Open the link provided in the terminal (usually `http://localhost:8888`) to access JupyterLab.

## Project Structure
- `data/`: Processed datasets (ignored by git if using large files).
- `notebooks/`: Literate programming analysis notebooks.
- `src/`: Modular Python scripts for data fetching and processing.
- `Dockerfile`: Environment definition.
- `requirements.txt`: Python dependencies.
