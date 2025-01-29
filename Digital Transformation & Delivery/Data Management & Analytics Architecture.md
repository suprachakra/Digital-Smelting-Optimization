
## 4. Data Management & Analytics Architecture

### 4.1 Big Data Pipeline

MetalX smelting generates **massive volumes** of real-time sensor data (voltages, currents, temperatures, chemical analyses) and also requires historical data for **PDE modeling**, **optimization**, and **dashboards**. The **Big Data Pipeline** is central to ensuring accurate, timely, and secure data flow for all use cases.

---

#### 4.1.1 Pipeline Overview & Alignment with Use Cases

| **Pipeline Stage**         | **Description**                                                                                                  | **Primary Use Cases**                                                 | **Value Proposition**                                                                                              |
|----------------------------|------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| **Data Ingestion**         | Collect raw sensor data from smelting lines (voltage, current, temperature, chemical composition).               | - UC-01 (Data Ingestion & ETL)<br>- UC-03 (Optimization)              | Single source of truth for PDE models and optimization.                                                             |
| **Landing / Staging**      | Store **raw** data in the Data Lake (Bronze layer) with minimal transformations.                                | - UC-01 (Data Ingestion & ETL)                                        | Ensures raw data integrity for reprocessing or re-analysis.                                                         |
| **ETL / Data Transformation** | Clean, validate, and transform data to curated layers (Silver, Gold), handle outliers, missing values, calibration data. | - UC-02 (PDE Model Validation)<br>- UC-06 (Digital Twin & ML)         | Improves data quality for PDE simulations, ML anomaly detection, and reporting.                                     |
| **Analytics & Modeling**   | Feed the **PDE models**, **optimization engine**, and **dashboards**; provide real-time or batch data for HPC cluster. | - UC-02 (PDE Modeling)<br>- UC-03 (Optimization Engine)<br>- UC-04 (Dashboards)<br>- UC-06 (Digital Twin & ML) | Delivers actionable insights (optimal setpoints, anomaly alerts) to reduce energy consumption and enhance throughput. |
| **Real-Time Stream (Future)** | Integrate **real-time streaming** (e.g., via Kafka or Azure Event Hub) for near real-time PDE adjustments and SCADA updates. | - UC-05 (SCADA Integration)<br>- UC-06 (Digital Twin & ML)            | Enables immediate operational changes, further minimizing energy usage and downtime.                               |

**Key Goals**:
1. **Reliability**: High uptime for mission-critical smelting data.  
2. **Scalability**: Ability to handle thousands of data points per second per smelting line.  
3. **Security**: Encryption at rest and in transit, with strict role-based access.  
4. **Performance**: Low-latency ingestion and transformation to support near real-time optimization.

---

#### 4.1.2 Detailed Pipeline Steps

1. **Sensor Data Capture**:  
   - Field devices (voltage/current meters, temperature probes, chemical analyzers) stream data via SCADA or IoT gateways.  
   - Typically timestamped at high frequency (1–5s intervals or faster).

2. **Data Ingestion Service**:  
   - Responsible for pulling data from SCADA/IoT gateways into the data platform.  
   - May use queue or streaming solutions (Kafka, Azure Event Hubs, RabbitMQ) depending on volume and latency needs.

3. **Landing Zone (Bronze Layer)**:  
   - Stores raw data in the Data Lake with minimal transformations.  
   - Includes a data schema registry to handle changes in sensor formats.

4. **Data Transformation (ETL/ELT)**:  
   - **Cleaning**: Removes duplicates, corrects format, flags outliers.  
   - **Validation**: Compares sensor readings against known operating ranges; suspicious data might be quarantined.  
   - **Aggregation**: Some metrics might be aggregated or re-sampled for PDE or optimization tasks (e.g., 1-min averages).

5. **Curated Zones (Silver, Gold)**:  
   - **Silver**: Partially processed data, structured or semi-structured.  
   - **Gold**: Fully processed data sets optimized for PDE inputs, dashboards, or ML features.

6. **Analytics & Modeling**:  
   - PDE models or optimization routines can pull “Gold” data for batch runs or real-time data (if streaming is enabled).  
   - Results (e.g., temperature fields, recommended setpoints) can be written back to the data lake for archiving or to ephemeral storage for real-time dashboards.

7. **Real-Time Stream (Future)**:  
   - Extends the pipeline to push partial PDE solutions or anomaly alerts directly to an operational environment.  
   - Helps quicken the feedback loop with SCADA (UC-05) or digital twins (UC-06).

---

### 4.2 Infrastructure & Tools

1. **Python Ecosystem**:  
   - **SciPy, NumPy, Pandas** for data manipulation, cleaning, quick analytics.  
   - Integration with **FEniCS / SfePy** (PDE modeling) and **Pyomo / CVXPY** (optimization).

2. **Data Storage**:  
   - **Data Lake**: Hadoop-based or cloud object storage (e.g., Azure Data Lake, AWS S3) to store raw (Bronze) and curated (Silver/Gold) data sets.  
   - **Relational / SQL DB**: Potentially for metadata, sensor inventory, or aggregated metrics.

3. **Orchestration & Scheduling**:  
   - Tools like **Airflow**, **Azure Data Factory**, or **Databricks** for pipeline scheduling, monitoring, and lineage tracking.

4. **Visualization Tools**:  
   - **Plotly / Dash**: Interactive dashboards for operational monitoring.  
   - Could be integrated with **Power BI** or **Tableau** if enterprise standards require.

5. **Real-Time Processing** (Planned):  
   - Solutions like **Apache Kafka** Streams, **Spark Streaming**, or **Flink** for real-time ingestion and transformation.

---

### 4.3 Detailed Requirements

Like in previous sections, we present **Functional Requirements (FR)** and **Non-Functional Requirements (NFR)** aligned with **SAFe** epics and relevant use cases.

#### 4.3.1 Functional Requirements

| **Feature**              | **User Story**                                                                                                                     | **Acceptance Criteria**                                                                                                                                       | **Associated Epic / UC**              | **Priority** |
|--------------------------|------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------|-------------|
| **Data Ingestion**       | “As a **Data Engineer**, <br>I need to collect real-time sensor data (50,000 points/min) into a Data Lake, <br>so that PDE/optimization teams have a single source of truth.”         | - Successful ingestion within < 5s latency for 95% of data <br> - 99% system uptime for ingestion <br> - Data schema registry handles sensor format changes                                         | EPIC-1 (UC-01)                        | High        |
| **ETL Cleaning**         | “As a **Data Scientist**,<br> I want to detect and handle outliers, missing data, and invalid sensor readings,<br>so that PDE models receive high-quality data.”                   | - Automated pipeline flags or quarantines suspicious data <br> - Documented transformations in metadata store <br> - At least 95% data quality in curated layer                                   | EPIC-1 (UC-01), EPIC-2 (UC-02)         | High        |
| **Data Validation & Curation** | “As a **Smelting Engineer**,<br> I want curated data sets (temperature, voltage, composition) in the Gold layer,<br> so that I can calibrate PDE and run mass-balance checks.” | - Curation jobs run every hour <br> - Data sets are aggregated and easily accessible by PDE scripts <br> - Minimal manual intervention needed                                                       | EPIC-2 (UC-02), EPIC-6 (UC-06)         | High        |
| **Batch & Real-Time Feeds**  | “As a **Process Engineer**,<br> I need both batch historical data and near real-time data for optimization routines.”                                                  | - Batch pipelines (hourly/daily) maintain historical data <br> - Real-time feed (sub-5s latency) for critical parameters <br> - Integration tested with optimization engine                         | EPIC-3 (UC-03), EPIC-5 (UC-05)         | Medium      |
| **Metadata & Lineage**   | “As an **Audit/Compliance Officer**,<br> I need a complete lineage of transformations,<br> so that we can trace data usage for safety or regulatory checks.”                        | - End-to-end traceability: sensor → raw → curated <br> - Automatic logs of each transformation <br> - Retention of logs for 2+ years                                                             | EPIC-4 (Dashboards), UC-04, UC-05      | Medium      |
| **Data Access & Security**   | “As a **Production Manager**,<br> I want role-based access to data for Operators, Engineers, and Management,<br> so that each sees only the relevant data.”                     | - RBAC policies configured in data lake <br> - Access logs for read/write operations <br> - Security audits pass with no critical findings                                                        | EPIC-1–EPIC-6 (all UC)                 | Critical    |

#### 4.3.2 Non-Functional Requirements

| **NFR Category**  | **Requirement**                                                                                                                                       | **Acceptance Criteria**                                                                              | **Priority** |
|-------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------|-------------|
| **Performance**   | “**Ingestion** must sustain up to 50,000 data points/min with <5s latency. **ETL** transformations must complete within 15 minutes for hourly batches.” | - Tested with load simulation <br> - 95th percentile ingestion <5s <br> - ETL job completes in <15 min for average dataset size          | High        |
| **Scalability**   | “System must handle **3X growth** in sensor data (expansion to additional smelting lines) without major redesign.”                                                                          | - Horizontal scaling of ingestion service <br> - Data lake storage autoscaling <br> - Performance tested at 3X data load               | High        |
| **Reliability**   | “Achieve **99.9%** pipeline availability for data ingestion and transformation.”                                                                                                             | - Monitoring & alerting with SLA <br> - Failover strategies documented <br> - Minimal downtime for patching/upgrades                   | Critical    |
| **Security**      | “Data at rest must be encrypted (AES-256), data in transit via TLS 1.2+; strict RBAC for PDE, optimization, dashboard layers.”                                                               | - Encryption validated <br> - RBAC tested with multiple user roles <br> - Regular security audits pass                                 | Critical    |
| **Maintainability** | “All pipeline code (scripts, orchestrations) must be version-controlled, with automated testing and CI/CD integration.”                                                                  | - 80%+ code coverage in pipeline scripts <br> - Automated build & deployment with each commit <br> - Clear rollback procedures        | High        |
| **Audit & Compliance** | “Complete data lineage and transformation logs must be stored for **2+ years**, fulfilling operational/regulatory needs.”                                                              | - Data lineage documented for each job <br> - Automated retention policies in data lake <br> - Audit logs accessible to compliance team | High        |
| **Usability**     | “Engineers and data scientists should easily locate curated data sets for PDE modeling and ML in a standardized folder structure or table.”                                                   | - Documented data schemas <br> - Self-service data discovery (e.g., data catalog)                                                      | Medium      |

---

### 4.4 Architecture & Data Flow Diagrams

#### 4.4.1 High-Level Data Architecture Diagram

Below is an **expanded** architecture showing **batch** and **real-time** data flows, including where PDE modeling, optimization, and dashboards interact.

```
                      +-----------------------------+
                      |        SCADA/IoT Gateways  |
                      | (Sensors: Voltage, Current,|
                      |  Temp, Chemical Analysis)   |
                      +-----------+-----------------+
                                  | (Raw Data Stream)
                                  v
   +---------------------------------------------------+   +---------------------------+
   |               Data Ingestion Service              |-->|  Real-Time Processing     |
   | (Streaming ingestion with Kafka/other connectors) |   | (Future: Kafka Streams,   |
   +------------------+--------------------------------+   |  Spark, Flink, etc.)      |
                      |                                    +----------+----------------+
                      |                                               |
(Landing in Bronze)   |                                               v
                      v                       +---------------------------------------+
+-------------------------------+             | PDE/Optimization Cluster (Batch/Real) |
|  Data Lake (Bronze, Silver,   |-------------|(Pull curated data for PDE & Opt runs) |
|  Gold zones: Raw & Processed) |             |(Write results back to curated/Gold)   |
+-------------------------------+             +---------------------------------------+
        | (ETL/ELT jobs)         \
        |                         \
        v                          \
+------------------------+          \
| Orchestration &        |           \
|  Scheduling (Airflow,  |------------>  +-----------------------------+
|  Azure Data Factory)   |               |  Operational Dashboards     |
+------------+-----------+               | (Plotly/Dash)               |
             |                           +--------------+--------------+
             |                                           |
             | (Scheduling pipeline runs, dependencies)  |
             v                                           v
  +------------------------+              +-----------------------------------+
  | Digital Twin & ML      |<-------------| HPC or Cloud ML Environment       |
  | (UC-06: Anomaly Detect)|              | (Batch or streaming ML pipelines) |
  +------------------------+              +-----------------------------------+
```

1. **SCADA/IoT Gateways** push sensor data to the **Data Ingestion Service**.  
2. **Ingestion** writes raw data to **Bronze** layer in the **Data Lake**.  
3. **Orchestration** triggers **ETL/ELT** to create cleaned, enriched data in **Silver** and **Gold** layers.  
4. **PDE/Optimization** services consume curated data for batch or near real-time runs.  
5. **Results** (e.g., recommended setpoints, PDE fields) are written back to the lake or served to dashboards.  
6. Future **Real-Time Processing** (e.g., Kafka Streams) can feed immediate updates to dashboards or SCADA.

---

#### 4.4.2 Data Flow for PDE & Optimization

This **detailed** data flow shows how PDE modeling (UC-02) and the Optimization Engine (UC-03) retrieve data and publish results.

```
[Data Lake (Gold Layer)] ---> [Batch read by PDE Solver] ---> PDE Outputs -> [Optimization Engine]
            |                           ^                                                   |
            |                           | (Stores logs & intermediate data)                 |
            v                           |                                                   v
[ETL/ELT] <--- [Data Lake (Silver)] <---+                                              [Recommended Setpoints]
                                               \                                         /  
                                                \---------------------------------------/
                                                  (Written back to Data Lake or to SCADA)
```

1. Curated data in **Gold** is fetched by the PDE solver for each run.  
2. PDE solver writes intermediate results (e.g., temperature fields, concentration arrays) back to a designated location in the lake.  
3. **Optimization Engine** reads PDE results, runs optimization, and outputs recommended setpoints.  
4. Final setpoints can be published to **SCADA** (for real-time adjustments) or stored for offline analysis.

---

### 4.5 Summary & Next Steps

- The **Big Data Pipeline** underpins **all** use cases by providing **reliable**, **clean**, and **timely** data.  
- By adhering to **functional** (ETL processes, curated layers) and **non-functional** (performance, security, scalability) requirements, Metalworks Inc. ensures high data quality for **PDE modeling** (UC-02), **optimization** (UC-03), **dashboards** (UC-04), **SCADA integration** (UC-05), and **digital twin/ML** (UC-06).  
- **Future Real-Time** capabilities will further optimize the feedback loop, reducing energy costs and GHG emissions in near real-time.

**Next Steps**:  
1. **Finalize Data Ingestion & ETL framework** for pilot lines (UC-01).  
2. **Build and test PDE/optimization ingestion** from curated data (UC-02, UC-03).  
3. **Expand real-time streaming** for SCADA (UC-05) and anomaly detection (UC-06).  
4. **Integrate CI/CD** to automate pipeline deployment and testing, ensuring maintainability and rapid iteration.

With this we can scale its **Industry 4.0** transformation, leveraging high-quality data for advanced analytics, PDE modeling, and real-time optimization.
