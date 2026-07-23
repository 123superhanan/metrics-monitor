## Metrics Monitor
An intelligent production incident assistant that combines time-series deep learning (LSTM and GRU) for anomaly forecasting with Retrieval-Augmented Generation (RAG) to map system telemetry directly to actionable recovery runbooks.
This platform continuously evaluates streaming infrastructure metrics, forecasts imminent service degradations, and surfaces the precise remediation procedures engineers need during a high-severity incident.
------------------------------
## Project Structure

```text
metrics-monitor/
├── data/
│   ├── raw/               # Synthetic and historic metrics (.csv)
│   └── runbooks/          # System recovery documentation (.md)
├── notebooks/             # Exploratory data analysis
├── saved_models/          # Trained LSTM/GRU model artifacts
├── chroma_db/             # Local vector database for runbooks
├── src/
│   ├── api/               # FastAPI endpoints (predict, analyze, explain)
│   ├── data/              # Data generation, preprocessing, and encoding
│   ├── evaluation/        # Validation metrics and charting scripts
│   ├── models/            # Model architectures and training loops
│   └── rag/               # Document ingestion, embedding, and vector storage
└── static/                # Vanilla HTML5/CSS3/JS dashboard frontend
```
------------------------------
## Technical Architecture & Core Pipelines## 1. Predictive Telemetry Pipeline
The telemetry engine extracts patterns from multidimensional tracking streams (CPU utilization, memory usage, request duration, error percentages) to anticipate threshold breaches before they occur.

* Ingestion: Raw telemetry streams pass through preprocess.py to clean anomalies and align time indices.
* Windowing: encode.py slices continuous rows into sliding overlapping temporal blocks (e.g., observing the past 60 minutes to forecast the next 15 minutes).
* Modeling: lstm_model.py or gru_model.py weights historical transitions to compute upcoming system vectors.

## 2. Context-Aware Runbook RAG Pipeline
When an anomaly is predicted or flagged, the platform bridges quantitative alerts with qualitative engineering knowledge fields.

* Vector Ingestion: ingest.py reads Markdown documentation files through loader.py, splits them into logical steps via chunker.py, and indexes them inside chroma_db/.
* Dynamic Search: When the API registers a critical metric shift, vector_store.py runs a semantic similarity match using the anomaly's textual fingerprint.
* Prompt Assembly: prompt_maker.py injects the top-matching operational runs directly into an LLM instruction payload, yielding immediate remediation recipes.

## 3. API & Monitoring UI Layer

* FastAPI Service: Provides non-blocking asynchronous routing via src/api/ to handle overlapping visualization streams and text generation calls simultaneously.
* Dashboard Front-end: A native web console written in raw HTML/JS that polls system changes, streams live predictive plots, and presents interactive AI-generated triage checklists.

------------------------------
## Technical Requirements Specification
The system uses standard open-source libraries for its operational data stacks:

* FastAPI / Uvicorn: High-performance HTTP networking layer.
* PyTorch / TensorFlow: Deep learning engines driving recurrent sequence operations.
* ChromaDB: Native open-source vector substrate optimized for low-latency indexing.
* Pandas / NumPy: In-memory matrix manipulation and analytical compute tooling.

------------------------------


