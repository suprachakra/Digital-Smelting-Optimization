### 4.1 Component Diagram (High-Level)

Below is a high-level **Component Diagram** illustrating how different systems integrate:

```mermaid
---
config:
  layout: dagre
---
flowchart TD
 subgraph Azure_Cloud["🌐 AZURE CLOUD"]
        A["📥 Data Ingestion Service<br>(UC-01)<br>• Sensor / SCADA Connectors<br>• Cleansing / Validation"]
        B["🧮 PDE Modeling Service<br>(UC-02)<br>• Fourier, Fick, Butler-Volmer<br>• HPC/Grid Compute<br>• FEniCS/SfePy"]
        C["🗄️ Data Lake / Lakehouse<br>• Bronze, Silver, Gold Zones<br>• Historical &amp; Real-Time Storage"]
        D["🧠 Optimization Engine<br>(UC-03)<br>• Pyomo, CVXPY, GA/NLP<br>• RESTful API"]
        E["🔗 SCADA Integration<br>(UC-05)<br>• Real-Time Commands<br>• Safety Overrides"]
        F["🖥️ Digital Twin &amp; ML<br>(UC-06)<br>• Anomaly Detection (LSTM/RNN)<br>• Virtual Environment"]
        G["📡 Real-Time Events<br>(Streaming)"]
        H["📊 Operational Dashboards<br>(UC-04)<br>• Visual Analytics, KPIs, Alerts"]
        I["⚙ CI/CD &amp; Containerization<br>• Docker/Kubernetes<br>• HPC Config (YAML)<br>• Automated Testing"]
  end
    A -- ETL --> B
    A -- Transformed Data --> C
    B -- Model Outputs & Results --> D
    C <--> D
    D -- Optimized Setpoints --> E
    E -- Data Backflow --> F
    F <--> G
    G -- Alerts --> H
    H -- Feedback Loop --> G
    B -- Parallel PDE Solves --> I
    D -- Deploy/Update Optimization --> I
     A:::data_ingestion
     A:::VanGoghYellow
     B:::pde_modeling
     B:::MonetBlue
     C:::data_storage
     C:::RenoirPink
     D:::optimization_engine
     D:::TurnerMist
     E:::scada
     E:::CezannePeach
     F:::digital_twin
     F:::TurnerMist
     F:::MatisseLavender
     G:::real_time_events
     G:::TurnerMist
     H:::dashboard
     H:::Pine
     I:::ci_cd
     I:::DegasGreen
    classDef PicassoBlue stroke-width:1px, stroke-dasharray:none, stroke:#5A84A2, fill:#CDE0F2, color:#2D4661  
    classDef KlimtGold stroke-width:1px, stroke-dasharray:none, stroke:#D4A017, fill:#FBF2C1, color:#705A16
    classDef Rose stroke-width:1px, stroke-dasharray:none, stroke:#FF5978, fill:#FFDFE5, color:#8E2236
    classDef Aqua stroke-width:1px, stroke-dasharray:none, stroke:#46EDC8, fill:#DEFFF8, color:#378E7A
    classDef Ash stroke-width:1px, stroke-dasharray:none, stroke:#999999, fill:#EEEEEE, color:#000000
    classDef HokusaiWave stroke-width:1px, stroke-dasharray:none, stroke:#6188A9, fill:#D4E8F2, color:#2A425D
    classDef Sky stroke-width:1px, stroke-dasharray:none, stroke:#374D7C, fill:#E2EBFF, color:#374D7C
    classDef Peach stroke-width:1px, stroke-dasharray:none, stroke:#FBB35A, fill:#FFEFDB, color:#8F632D
    classDef VanGoghYellow stroke-width:1px, stroke-dasharray:none, stroke:#E3B448, fill:#FDF6C9, color:#7D5A17
    classDef RenoirPink stroke-width:1px, stroke-dasharray:none, stroke:#E4A0A0, fill:#FBE5E5, color:#7D3E3E
    classDef MonetBlue stroke-width:1px, stroke-dasharray:none, stroke:#87AFC7, fill:#D4EAF7, color:#30577B
    classDef DegasGreen stroke-width:1px, stroke-dasharray:none, stroke:#A7C796, fill:#E6F4E2, color:#3E6A42
    classDef CezannePeach stroke-width:1px, stroke-dasharray:none, stroke:#E2A07D, fill:#FBE7DA, color:#6D4532
    classDef TurnerMist stroke-width:1px, stroke-dasharray:none, stroke:#B8C4D1, fill:#EAF2F8, color:#4A5B6F
    classDef MatisseLavender stroke-width:1px, stroke-dasharray:none, stroke:#B39DBC, fill:#ECE3F5, color:#4E3A5E
    classDef Pine stroke-width:1px, stroke-dasharray:none, stroke:#254336, fill:#27654A, color:#FFFFFF
    style Azure_Cloud fill:transparent
```

#### Component Responsibilities
1. **Data Ingestion Service** (UC-01): Responsible for collecting raw data from sensors/SCADA and pushing cleaned data into the **Data Lake**.  
2. **Data Lake/Lakehouse**: Central repository for storing historical, current, and curated data sets.  
3. **PDE Modeling Service** (UC-02): Houses the physics-based modeling logic, typically running on HPC resources (on-prem or cloud).  
4. **Optimization Engine** (UC-03): Runs nonlinear programming or metaheuristics to find optimal smelting parameters, pulling PDE outputs and constraints from the lake.  
5. **SCADA Integration** (UC-05): Communicates setpoints in near real-time to the actual production environment; includes override and safety logic.  
6. **Digital Twin & ML** (UC-06): Mirrors real-world processes for advanced analysis and anomaly detection.  
7. **Operational Dashboards** (UC-04): Visualizes all relevant KPIs, real-time metrics, alerts, and historical trends for operational decisions.

---
### **4.2 Engineering & Architecture Perspective**

#### High-Level Architecture
1. **Data Ingestion & ETL**: Real-time pipeline capturing ~50k sensor points/min, stored in a tiered Data Lake (Bronze → Silver → Gold).  
2. **HPC & PDE Modeling**: Multi-physics PDE modules (Fourier, Fick, Butler–Volmer) run on HPC clusters for rapid iteration.  
3. **Optimization Engine**: Pyomo/CVXPY or metaheuristics (GA) for single/multi-objective constraints, ensuring stable setpoints.  
4. **SCADA & Dashboards**: Low-latency communication for real-time control, combined with user-friendly visualization.

#### Tech Stack 
- **Python Ecosystem**: FEniCS/SfePy for PDE, Pyomo for optimization, Pandas for data transformations.  
- **Containerization & CI/CD**: Docker images for consistent HPC runs; GitHub Actions or Jenkins for automated testing and deployment.  
- **Scalability & Reliability**: Horizontal scale in HPC for PDE solves; robust scheduling with Airflow or Azure Data Factory.  
- **Security & Compliance**: TLS 1.2+ for data in transit, AES-256 for data at rest, thorough audit logs for SCADA changes.

#### Extensibility & Maintenance
- **Modular PDE**: Each physics module (thermal, mass transfer, electrochem) can evolve independently.  
- **Config-Driven**: HPC mesh sizes, solver parameters, and PDE constraints stored in YAML for easy updates.  
- **Testing Framework**: Automated coverage across PDE solves, optimization routines, SCADA endpoints, ensuring robust code quality.
