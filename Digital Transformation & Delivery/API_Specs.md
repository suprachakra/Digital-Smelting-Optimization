# API Specifications for Metalworks Inc. Smelting Project

 [1. Overview](#1-overview)
 
 [2. Data Ingestion & ETL Endpoints (UC-01)](#2-data-ingestion--etl-endpoints-uc-01)
   - [2.1 POST /data-ingestion/streams](#21-post-data-ingestionstreams)
   - [2.2 GET /data-ingestion/streams/{streamId}](#22-get-data-ingestionstreamsstreamid)
   
 [3. PDE Models Service (UC-02)](#3-pde-models-service-uc-02)
   - [3.1 POST /pde-models](#31-post-pde-models)
   - [3.2 GET /pde-models/{modelId}](#32-get-pde-modelsmodelid)
   - [3.3 POST /pde-models/{modelId}/simulate](#33-post-pde-modelsmodelidsimulate)
     
 [4. Optimization Service (UC-03)](#4-optimization-service-uc-03)
   - [4.1 POST /optimizations](#41-post-optimizations)
   - [4.2 GET /optimizations/{optimizationId}](#42-get-optimizationsoptimizationid)
     
 [5. SCADA Integration (UC-05)](#5-scada-integration-uc-05)
 - [5.1 POST /scada/setpoints](#51-post-scadasetpoints)
 - [5.2 GET /scada/status](#52-get-scadastatus)
   
 [6. Digital Twin & ML (UC-06)](#6-digital-twin--ml-uc-06)
 - [6.1 POST /digital-twin/sync](#61-post-digital-twinsync)
 - [6.2 GET /digital-twin/anomalies](#62-get-digital-twinanomalies)
   
 [7. Common Request/Response Headers](#7-common-requestresponse-headers)
  
 [8. Error Codes](#8-error-codes)
 
 [9. Versioning & Backward Compatibility](#9-versioning--backward-compatibility)
 
 [10. Security & Compliance](#10-security--compliance)

```
This document provides detailed references for all RESTful endpoints across the Data Ingestion, PDE Modeling, Optimization, SCADA Integration, and Dashboard services.
```
---

### 1. Overview

We follow RESTful principles with **versioned** endpoints, typically of the form:

```
https://api.metalworks.example.com/industrial-automation/smelting-ops/v1/<service-root>/<resource-id>
```

- **Domain Name**: `metalworks.example.com` (placeholder for actual domain)
- **App Group**: `industrial-automation`
- **Subapp Group**: `smelting-ops`
- **Version**: `v1` (we may introduce `v2`, `v3` in future)
- **Service Root**: `pde-models`, `optimizations`, `dashboards`, `scada`, etc.
- **Resource Id**: Unique identifier (optional) for a PDE model, optimization job, etc.

---

### 2. Data Ingestion & ETL Endpoints (UC-01)

#### 2.1 `POST /data-ingestion/streams`
- **Description**: Registers a new data stream from a smelting line or sensor gateway.
- **Request Body**:
  ```json
  {
    "streamName": "LineA_Sensors",
    "sensorType": "Voltage/Current/Temp",
    "samplingRate": 1,
    "units": "seconds"
  }
  ```
- **Response**:
  ```json
  {
    "streamId": "stream-123",
    "status": "created",
    "links": [
      { "rel": "self", "href": "/data-ingestion/streams/stream-123" }
    ]
  }
  ```
- **Notes**: This endpoint sets up ingestion configurations (Kafka topics, SCADA connectors, etc.).

#### 2.2 `GET /data-ingestion/streams/{streamId}`
- **Description**: Retrieves metadata for a given data stream.
- **Response**:
  ```json
  {
    "streamId": "stream-123",
    "streamName": "LineA_Sensors",
    "sensorType": "Voltage/Current/Temp",
    "status": "active",
    "links": [...]
  }
  ```

---

### 3. PDE Models Service (UC-02)

#### 3.1 `POST /pde-models`
- **Description**: Creates a new PDE model configuration (Fourier, Fick, Butler–Volmer, etc.).
- **Request Body**:
  ```json
  {
    "modelName": "FourierHeatModel",
    "parameters": {
      "thermalConductivity": 200,
      "initialTemperature": 700,
      "boundaryConditions": {
        "topSurface": 750,
        "bottomSurface": 690
      }
    },
    "description": "Model for simulating heat transfer in pot cell."
  }
  ```
- **Response**:
  ```json
  {
    "modelId": "pde-001",
    "modelName": "FourierHeatModel",
    "status": "created",
    "creationTimestamp": "2025-02-01T10:00:00Z",
    "links": [
      {
        "rel": "self",
        "href": "https://api.metalworks.example.com/industrial-automation/smelting-ops/v1/pde-models/pde-001"
      }
    ]
  }
  ```

#### 3.2 `GET /pde-models/{modelId}`
- **Description**: Retrieves details of a specific PDE model configuration.
- **Response**:
  ```json
  {
    "modelId": "pde-001",
    "modelName": "FourierHeatModel",
    "parameters": {
      "thermalConductivity": 200,
      "initialTemperature": 700,
      ...
    },
    "status": "created",
    "creationTimestamp": "2025-02-01T10:00:00Z"
  }
  ```

#### 3.3 `POST /pde-models/{modelId}/simulate`
- **Description**: Triggers a PDE simulation run on HPC or cloud-based cluster.
- **Request Body**:
  ```json
  {
    "meshSize": { "nx": 300, "ny": 300 },
    "timeSteps": 50,
    "dt": 1.0,
    "additionalParams": { "rho": 2700, "cp": 900 }
  }
  ```
- **Response**:
  ```json
  {
    "simulationId": "sim-xyz",
    "modelId": "pde-001",
    "status": "running",
    "links": [
      { "rel": "self", "href": "/pde-models/pde-001/simulate/sim-xyz" }
    ]
  }
  ```

---

### 4. Optimization Service (UC-03)

#### 4.1 `POST /optimizations`
- **Description**: Submits PDE outputs + real-time constraints for energy optimization.
- **Request Body**:
  ```json
  {
    "pdeOutputRef": "sim-xyz",
    "constraints": {
      "temperature": { "min": 779, "max": 782 },
      "throughput": { "target": 120 },
      "voltageBounds": { "min": 4.0, "max": 5.0 }
    }
  }
  ```
- **Response**:
  ```json
  {
    "optimizationId": "opt-abc",
    "status": "in-progress",
    "expectedCompletion": "2025-02-01T11:00:00Z",
    "links": [...]
  }
  ```

#### 4.2 `GET /optimizations/{optimizationId}`
- **Description**: Retrieves the status or results of an optimization run.
- **Response**:
  ```json
  {
    "optimizationId": "opt-abc",
    "status": "completed",
    "results": {
      "recommendedVoltage": [4.2, 4.3, ...],
      "recommendedCurrent": [125, 123, ...],
      "objectiveValue": 25000.0
    }
  }
  ```

---

### 5. SCADA Integration (UC-05)

#### 5.1 `POST /scada/setpoints`
- **Description**: Sends recommended setpoints to SCADA in near real-time.
- **Request Body**:
  ```json
  {
    "lineId": "LineA",
    "voltage": 4.2,
    "current": 120.0,
    "timestamp": "2025-02-01T10:15:00Z"
  }
  ```
- **Response**:
  ```json
  {
    "status": "OK",
    "appliedVoltage": 4.2,
    "appliedCurrent": 120.0,
    "scadaLogId": "scada-123"
  }
  ```

#### 5.2 `GET /scada/status`
- **Description**: Retrieves SCADA system status or override events.
- **Response**:
  ```json
  {
    "lineId": "LineA",
    "status": "running",
    "overrideActive": false,
    "lastOverrideReason": null,
    "timestamp": "2025-02-01T10:20:00Z"
  }
  ```

---

### 6. Digital Twin & ML (UC-06)

#### 6.1 `POST /digital-twin/sync`
- **Description**: Updates the digital twin environment with real-time smelting data.
- **Request Body**:
  ```json
  {
    "lineId": "LineA",
    "temperature": 780.5,
    "current": 122.0,
    "anodePosition": 0.15
  }
  ```
- **Response**:
  ```json
  {
    "twinId": "dt-xyz",
    "status": "updated"
  }
  ```

#### 6.2 `GET /digital-twin/anomalies`
- **Description**: Returns a list of detected anomalies from ML models (LSTM, RNN).
- **Response**:
  ```json
  {
    "anomalies": [
      {
        "timestamp": "2025-02-01T10:25:00Z",
        "metric": "temperature",
        "value": 790,
        "threshold": 785,
        "confidence": 0.85
      }
    ]
  }
  ```

---

### 7. Common Request/Response Headers

| Header Name       | Value Example                                  | Required | Description                          |
|-------------------|-----------------------------------------------|----------|--------------------------------------|
| `Content-Type`    | `application/json`                            | Yes      | Defines request/response format.     |
| `Authorization`   | `Bearer <JWT-Token>`                          | Yes      | For secured endpoints (RBAC).        |
| `x-correlation-id`| `123e4567-e89b-12d3-a456-426655440000`        | No       | For request tracing in logs.         |
| `Cache-Control`   | `no-cache`                                    | No       | Caching directives.                  |

---

### 8. Error Codes

| Error Code | HTTP Status               | Message                                     |
|------------|---------------------------|---------------------------------------------|
| ERR-4001   | 400 Bad Request           | Invalid input or missing required fields    |
| ERR-4011   | 401 Unauthorized          | Missing/Invalid JWT token                   |
| ERR-4033   | 403 Forbidden            | User does not have the required role        |
| ERR-4042   | 404 Not Found            | Resource not found                          |
| ERR-5000   | 500 Internal Server Error | General server-side exception occurred      |

---

### 9. Versioning & Backward Compatibility

- **v1** is our initial release. Future versions (v2, v3) will preserve backward compatibility for a transition period.
- Clients should specify the version in the endpoint path. Failing to do so defaults to `v1`.

---

### 10. Security & Compliance

- **TLS 1.2+** for all in-transit data.
- **RBAC** with roles (Operator, Engineer, Manager).
- **Audit Logs** for SCADA changes (retain for at least 2 years).
- **GDPR/CCPA** compliance for any personal data (if relevant).

---
