## Metrics Monitor
An intelligent production incident assistant that combines time-series deep learning (LSTM and GRU) for anomaly forecasting with Retrieval-Augmented Generation (RAG) to map system telemetry directly to actionable recovery runbooks.
This platform continuously evaluates streaming infrastructure metrics, forecasts imminent service degradations, and surfaces the precise remediation procedures engineers need during a high-severity incident.
------------------------------
## Detailed Directory Breakdown

metrics-monitor/
├── chroma_db/                  # Persistent local vector database instances
├── saved_models/               # Serialized deep learning model checkpoints (.pth / .h5)
├── data/
│   ├── raw/                    # Active and historical telemetry streams (metrics.csv)
│   └── runbooks/               # Engineering documentation for standard incident profiles
│       ├── cpu_spike.md        # Triage workflows for compute exhaustion
│       ├── error_rate_surge.md # Remediation paths for HTTP 5xx or RPC error bursts
│       ├── latency_increase.md # Mitigation steps for downstream network/db blockages
│       └── memory_leak.md      # Garbage collection and container restart strategies
├── notebooks/
│   └── exploration.ipynb       # Exploratory Data Analysis (EDA) and signal-to-noise testing
├── src/
│   ├── api/                    # Core FastAPI backend serving layer
│   │   ├── main.py             # Server initialization, middleware, and CORS configuration
│   │   ├── routes_analyze.py   # Statistical trend analysis and threshold validation
│   │   ├── routes_explain.py   # RAG pipeline orchestration mapping telemetry to text
│   │   └── routes_predict.py   # Inference endpoints hosting time-series model evaluations
│   ├── data/                   # Telemetry data pipeline
│   │   ├── encode.py           # Feature scaling, normalization, and sequence formatting
│   │   ├── generate_data.py    # Synthetic telemetry engine injecting system anomalies
│   │   └── preprocess.py       # Missing-value imputation, outlier removal, and alignment
│   ├── evaluation/             # Metrics and performance validation
│   │   ├── metrics.py          # Custom tracking for forecasting loss (MSE, MAE, R-squared)
│   │   └── plots.py            # Automated loss curve generation and prediction charts
│   ├── models/                 # Deep learning model zoo
│   │   ├── baseline.py         # Naive/Moving Average statistical reference benchmarks
│   │   ├── gru_model.py        # Gated Recurrent Unit network architecture definition
│   │   ├── lstm_model.py       # Long Short-Term Memory network architecture definition
│   │   └── train.py            # Optimization loops, validation checks, and serialization
│   └── rag/                    # Knowledge base extraction and embedding systems
│       ├── chunker.py          # Document parsing strategy maximizing contextual bounds
│       ├── embedder.py         # Local text vectorization adapter (e.g., SentenceTransformers)
│       ├── ingest.py           # Multi-threaded file scraper and catalog processing pipeline
│       ├── loader.py           # File system reader parsing raw markdown document trees
│       ├── prompt_maker.py     # Template builder synthesizing alert contexts and runbooks
│       └── vector_store.py     # Client interface abstracting the ChromaDB collection layer
└── static/                     # Single-Page Application (SPA) monitoring UI
    ├── index.html              # Layout skeleton housing charts and query widgets
    ├── script.js               # Reactive DOM manipulator executing asynchronous API polls
    └── style.css               # Material-dark themed visual interface specifications

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


