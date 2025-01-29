### 3.1 Multi-Physics Modeling

MetalX smelting requires an **integrated** understanding of thermal, mass transfer, and electrochemical phenomena. We employ **Partial Differential Equations (PDEs)** to capture these processes.

---

#### 3.1.1 PDE Model Architecture & Goals

| **Model**           | **Equation**                                                                                                                   | **Physical Significance**                                     | **Implementation Goal**                                                | **Related Use Cases** |
|---------------------|-------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------|-------------------------------------------------------------------------|------------------------|
| **Thermal Model**   | $\rho c_p \frac{\partial T}{\partial t} = \nabla \cdot (k \nabla T) + Q_{\text{electrical}}\$ <br>(Fourier’s Law)               | Tracks **temperature fields** in the molten bath and cell walls. High temperature gradients can lead to excessive heat loss, anode wear. | - Identify hot spots or areas for insulation upgrades <br> - Provide real-time or near-real-time temperature predictions for optimization | UC-02, UC-03           |
| **Mass Transfer**   | $\frac{\partial C_{\text{MetalX}^{n+}}}{\partial t} = \nabla \cdot (D \nabla C_{\text{MetalX}^{n+}}) - R_{\text{electrochemical}}$<br> (Fick’s Law) | Models **ionic concentration** of MetalX in the electrolyte. Distinguishes between well-mixed and diffusion-limited zones.              | - Optimize bath composition <br> - Minimize impurities and maximize yield                                                          | UC-02, UC-06           |
| **Electrochemical** | $\ i = i_0 \Big[\exp\big(\frac{\alpha_a F \eta}{RT}\big) - \exp\big(-\frac{\alpha_c F \eta}{RT}\big)\Big]$ <br> (Butler–Volmer) | Captures **electrode kinetics** and current density vs. overpotential relationships.                | - Predict anode effect frequency <br> - Adjust voltage/current to reduce energy consumption and CO₂ generation                      | UC-02, UC-03, UC-05    |

#### 3.1.2 Boundary Conditions & Domain Considerations

1. **Thermal Boundaries**  
   - **Top Surface**: Typically open to ambient environment or covered by insulating material; modeled with **convective** or **radiative** boundary conditions.  
   - **Side Walls**: Concrete/graphite lining with known **thermal conductivity**; can be partially cooled.  
   - **Bottom**: Insulating layer or water-cooled panels.

2. **Mass Transfer Boundaries**  
   - **Electrode Regions**: Ion flux can be enhanced or diminished by local overpotential.  
   - **Molten Bath Surface**: Possible mass transfer with air or flux additions.  
   - **Inflow/Outflow**: If the smelting line has continuous feed or draw.

3. **Electrochemical Boundaries**  
   - **Anode Boundary**: Overpotential driven by reaction kinetics at the anode.  
   - **Cathode Boundary**: Where metal deposition or side reactions occur.

4. **Domain Geometry**  
   - Often represented in **2D** or **3D** (depending on HPC capacity) with finite element or finite volume discretization.  
   - **Mesh resolution** must be sufficient to capture steep gradients near electrodes.

#### 3.1.3 PDE Solver & Implementation

1. **Frameworks**:  
   - **FEniCS**, **SfePy**, or **OpenFOAM** for PDE discretization and solution.  
   - **Python** integration with **NumPy/SciPy** for data handling and custom routines.

2. **HPC Considerations**:  
   - **Parallelization** using MPI, GPU-accelerated solvers, or cloud-based HPC clusters.  
   - Use case: Real-time or near-real-time PDE solutions may require **coarse-grid** or **reduced-order** models if HPC resources are limited.

3. **Validation & Calibration**:  
   - Compare PDE results with **lab-scale** or **pilot** data.  
   - Conduct **sensitivity analysis** on key parameters (thermal conductivity, diffusion coefficient, reaction rates).

4. **Output Data**:  
   - **Temperature Field**: 2D/3D matrix of T(x,y,z,t).  
   - **Concentration Field**: C(x,y,z,t) for MetalX ions.  
   - **Current Density**: i(x,y,z,t), used for further optimization steps.

---

### 3.2 Optimization Formulation

Building on PDE outputs, we formulate an **optimization problem** to minimize energy consumption while respecting production, quality, and safety constraints.

---

#### 3.2.1 Mathematical Formulation

1. **Objective Function**  
  > $\[
  >   \text{Minimize} \quad \int_0^T (V(t) \cdot I(t))\, dt
  > \]$
  > <br>where \(V(t)\) is the applied voltage, \(I(t)\) is current. Alternatively, a **multi-objective** approach can be used:
><br>
 >  $\[
 >    \min \{ E, GHG, \text{AnodeEffects} \}
 >  \]$
 >  <br>solved via **Pareto front** methods or weighted sums.

2. **Key Constraints**  
   - **Thermal**: $\(T_{\text{min}} \le T(x,y,z,t) \le T_{\text{max}}\)$ to avoid damage to cell lining.  
   - **Production Throughput**: $\(\text{Throughput} \ge \text{TargetRate}\)$.  
   - **Voltage/Current Limits**: $\(V(t) \in [V_{\min}, V_{\max}]\), \(I(t) \in [I_{\min}, I_{\max}]\). $ 
   - **Material Balance**: PDE-based states (concentration, mass flow) must remain feasible.

3. **Variables & Parameters**  
   - **Decision Variables**: Voltage setpoint $\(V\)$, current density \(i\), anode position or insertion timing.  
   - **Parameters**: PDE constants (k, D), cost factors for energy, CO₂ emissions factor, throughput demands.

4. **Solution Methods**  
   - **Nonlinear Programming (NLP)**:  
     - Libraries: **Pyomo**, **CVXPY** with IPOPT, BONMIN, or other solvers.  
     - **Advantages**: Finds local optimum; well-suited if the model is smooth.  
   - **Hybrid Metaheuristics**:  
     - **Genetic Algorithms (GA)**, Particle Swarm Optimization (PSO), etc.  
     - **Advantages**: More robust to non-convex or discontinuous objectives; can handle large solution spaces.  
   - **Reduced-Order Modeling**:  
     - Use simplified PDE or surrogate models (like neural networks) to speed up iterative optimization, especially for near-real-time scenarios.

---

#### 3.2.2 Example Optimization Workflow

Below is a **flow diagram** showcasing how the PDE solutions feed into the optimization routine:

```
  +---------------------------+
  |   PDE Model Simulation    |  (Thermal, Mass Transfer,
  |  (FEniCS / SfePy)         |   Electrochemical)
  +-----------+--------------  -+
              |
              | PDE Outputs (Temp, Conc, Current)
              v
  +---------------------------+        +------------------------------+
  | Data Transformation Layer |  ----> |  Optimization Engine (Pyomo) |
  | (Aggregates PDE results)  |        |  - NLP / GA / Hybrid         |
  +-----------+---------------+        +-------------------+----------+
              |                                            |
              | (Valid constraints, boundary conditions)   |
              v                                            |
  +---------------------------+                            |
  |     Constraints &         |                            |
  |     Business Rules        | <--------------------------+
  +-----------+---------------+
              |
              | (Voltage, Current Range, Production Targets)
              v
  +---------------------------+
  |   Solver Execution &      |
  |   Convergence Check       |
  +-----------+---------------+
              |
              | (Optimal Set Points, e.g., V*, I*, anode schedule)
              v
  +---------------------------+
  |  Results & Integration    |
  |  with SCADA / Dashboards  |
  +---------------------------+
```

1. **PDE Model Simulation**: Takes physical properties, initial/boundary conditions, solves for temperature and concentration fields.  
2. **Data Transformation Layer**: Prepares PDE outputs for the optimizer (e.g., average or boundary values, gradient metrics).  
3. **Constraints & Business Rules**: Throughput, safety, maintenance windows, cost factors.  
4. **Optimization Engine**: Iterates to find feasible setpoints that minimize energy while respecting constraints.  
5. **Results**: Pushed to SCADA or dashboards for real-time operational adjustments.

---
