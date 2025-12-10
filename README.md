#  Project Architecture Overview

The architecture maintains a strict **separation of concerns**, with shared models and utilities centralized in the **common** module.

---

## Core Modules & Services

### **1. api_service**

**Role:** API Layer built with **FastAPI**.

**Purpose:**

* Handles all incoming HTTP requests.
* Exposes interactive OpenAPI documentation.
* Manages communication between the client and the database.

**Key Functionality:**

* Provides **CRUD** endpoints for raw clinical trial data.
* Provides **READ** endpoints for computed analysis results.

**Examples:**

* `GET /trials/`
* `GET /analysis/results/`
* `GET /analysis/results/?result_type=GLOBAL_CONDITION_COUNT`

---

### **2. analysis_service**

**Role:** Business Logic & Data Processing Layer.

**Purpose:**

* Performs complex analysis tasks.
* Computes statistical metrics and frequent keyword/condition counts.

**Key Functionality:**

* Executes global analysis pipelines.
* Saves results to the `AnalysisResult` table.

---

### **3. scraper_service** *(Planned)*

**Role:** External Data Ingestion Layer.

**Purpose:**

* Fetches raw clinical trial data from external sources.
* Parses and persists the data into the `RawClinicalTrial` table.

**Key Functionality:**

* Connects to external APIs.
* Extracts, normalizes, and stores raw data.

---

### **4. common**

**Role:** Shared Utilities & Models Module.

**Purpose:**

* Acts as the backbone of the entire project.
* Provides unified data models, database schemas, and shared utilities.

**Key Functionality:**

* Shared Pydantic models
* SQLAlchemy schemas
* Utility functions and constants

---
