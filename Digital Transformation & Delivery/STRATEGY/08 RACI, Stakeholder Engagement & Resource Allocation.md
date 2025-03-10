### 8.1 RACI Matrix

| **Task / Deliverable**            | **Product Manager** | **PDE Modelers** | **HPC Specialists** | **Data Eng** | **DevOps** | **QA** | **SCADA Eng** | **Plant Manager** |
|-----------------------------------|---------------------|------------------|---------------------|-------------|-----------|------|--------------|------------------|
| **1. Data Ingestion & ETL** (UC-01)        | A                   | C                | I                   | R           | C         | I    | I            | I                |
| **2. PDE Model Validation** (UC-02)        | C                   | R                | C                   | I           | I         | I    | I            | I                |
| **3. HPC Setup & Maintenance**             | I                   | C                | R                   | I           | A         | I    | I            | I                |
| **4. PDE Simulation Runs**                 | C                   | R                | C                   | I           | I         | I    | I            | I                |
| **5. Optimization Engine** (UC-03)         | A                   | R                | I                   | I           | C         | I    | I            | I                |
| **6. SCADA Integration** (UC-05)           | C                   | I                | I                   | I           | I         | I    | R            | I                |
| **7. Digital Twin & ML** (UC-06)           | A                   | R                | C                   | I           | I         | I    | I            | I                |
| **8. Dashboards & Reporting** (UC-04)      | C                   | I                | I                   | I           | R         | I    | I            | A                |
| **9. Testing & QA**                        | I                   | I                | I                   | I           | I         | R    | I            | I                |
| **10. Deployment & Maintenance**           | C                   | I                | I                   | I           | R         | I    | I            | I                |

---

### **Notes & Explanations**

1. **Data Ingestion & ETL**  
   - **Data Eng** (R): Implements ETL pipelines.  
   - **Product Manager** (A): Owns final approval of ingestion scope and timelines.  
   - **DevOps** (C): Provides CI/CD or container setups for ingestion services.  

2. **PDE Model Validation**  
   - **PDE Modelers** (R): Perform model calibration and verification.  
   - **HPC Specialists** (C): Offer parallelization guidance or HPC resource allocation.  

3. **HPC Setup & Maintenance**  
   - **HPC Specialists** (R): Configure cluster, manage HPC resources.  
   - **DevOps** (A): Ultimately accountable for infrastructure readiness (containerization, scripts).  

4. **PDE Simulation Runs**  
   - **PDE Modelers** (R): Execute simulation logic.  
   - **HPC Specialists** (C): Provide HPC environment tuning or debugging.  

5. **Optimization Engine**  
   - **Product Manager** (A): Final sign-off on optimization requirements and scope.  
   - **PDE Modelers** (R): Implement solver logic, possibly with domain constraints.  
   - **DevOps** (C): Integrate solver with CI/CD pipeline.  

6. **SCADA Integration**  
   - **SCADA Eng** (R): Responsible for bridging optimized setpoints into SCADA systems.  
   - **Product Manager** (C): Ensures alignment with project goals.  

7. **Digital Twin & ML**  
   - **Product Manager** (A): Approves new ML features or expansions.  
   - **PDE Modelers** (R): Develop or adapt PDE logic for real-time digital twin.  
   - **HPC Specialists** (C): Provide HPC or cloud resources for continuous ML training.  

8. **Dashboards & Reporting**  
   - **DevOps** (R): Builds or configures dashboards (Plotly, Power BI, etc.).  
   - **Plant Manager** (A): Ultimately accountable for usability and adoption on the plant floor.  

9. **Testing & QA**  
   - **QA** (R): Designs and runs test suites (unit, integration, performance).  

10. **Deployment & Maintenance**  
   - **DevOps** (R): Manages container orchestration, release cycles.  
   - **HPC Specialists** (I): Stay informed if HPC resources need updates or expansions.  


### 8.2 Stakeholder Engagement & Resource Allocation

1. **Leadership Alignment**  
   - Bi-monthly executive steering committee meetings to track major KPIs, budget, and roadblocks.  
   - Ongoing sponsor support to ensure resources (budget, staff, hardware) are available as planned.

2. **Resource Planning**  
   - **Data Engineering**: 2–3 dedicated ETL specialists for real-time and batch pipelines.  
   - **Domain (Smelting) Experts**: 1–2 experts ensuring PDE assumptions, constraints align with physical reality.  
   - **Data Science / Optimization**: 2–4 PDE modelers and optimization specialists.  
   - **DevOps**: 1–2 for continuous integration, test automation, environment orchestration in Azure DevOps.  
   - **Product Owners**: 1 main PO (also the Portfolio Manager) plus additional POs for specific sub-use-cases if needed.

3. **Budget Oversight**  
   - Cloud compute (HPC) costs for PDE and optimization runs.  
   - Sensor upgrade or replacement in smelting line if data quality is insufficient.  
   - Training and onboarding costs (external PDE/SAFe workshops, certifications).
