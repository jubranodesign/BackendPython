#  Project Architecture Overview

This project is structured using a clear modular architecture that separates responsibilities across multiple service layers. Each service focuses on a dedicated aspect of the system, API handling, data processing, ingestion, and shared utilities.
allowing the application to remain scalable, maintainable, and easy to extend.

**At its core, the architecture ensures:**

1. Loose coupling between services

2. Clear separation of concerns

3. Shared, consistent data models across all components

4. Independent development and scaling of each service layer
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
