# AI-Based IDS Diagrams

Below are the Mermaid definitions for the System Architecture, Flowchart, and Block diagrams required for the project documentation. You can render these directly in tools that support Mermaid (like GitHub, Notion, or Mermaid Live Editor).

## 1. System Architecture Diagram

```mermaid
graph TD
    classDef data fill:#f9f,stroke:#333,stroke-width:2px;
    classDef process fill:#bbf,stroke:#333,stroke-width:2px;
    classDef model fill:#fbf,stroke:#333,stroke-width:2px;
    classDef web fill:#bfb,stroke:#333,stroke-width:2px;
    
    A[(NSL-KDD Raw Dataset)]:::data --> B[Data Cleaning & Mapping]:::process
    B --> C[Label Encoding & StandardScaler]:::process
    C --> D{Feature Selection Module}:::process
    D -->|Top 20 Features| E[ML Training Pipeline]:::model
    
    E -.->|Decision Tree| F((Evaluation))
    E -.->|Random Forest| F((Evaluation))
    E -.->|SVM| F((Evaluation))
    E -.->|XGBoost| F((Evaluation))
    
    F -->|Best Model Selection| G[(Saved .pkl Artifacts)]:::data
    
    G --> H[Flask Backend REST API]:::web
    
    H <--> I[Manual Input JSON]:::web
    H <--> J[Batch Upload CSV]:::web
    H <--> K[Live Traffic Stream Sim]:::web
    
    I --> L{Dashboard UI}:::web
    J --> L
    K --> L
```

## 2. Process Flowchart

```mermaid
flowchart TD
    Start([Start System]) --> Load[Load Raw Train/Test Data]
    Load --> Clean[Drop Duplicates / Clean Nulls]
    Clean --> Map[Map 40 Attack Types to 5 Categories]
    Map --> Encode[Encode Categoricals: protocol_type, service, flag]
    Encode --> Scale[Apply StandardScaler to Numeric Features]
    Scale --> RF[Extract Feature Importances via RandomForest]
    RF --> Reduce[Select Top 20 Features]
    
    Reduce --> Train[Train: DT, RF, SVM, XGBoost]
    Train --> Check{Meets Target F1?}
    Check -->|Yes| Save[Save Best Model & Encoders]
    Check -->|No| Tune[GridSearchCV Tuning]
    Tune --> Train

    Save --> Web[Launch Flask App]
    Web --> Route{User Action}
    
    Route -->|Submit Form| Manual[Single Prediction]
    Route -->|Upload File| Batch[Batch Evaluation]
    Route -->|Click Stream| Stream[Ping Live Simulator]
    
    Manual --> View[View Results on Dashboard]
    Batch --> View
    Stream --> View
    View --> End([End])
```

## 3. High-Level Block Diagram

```mermaid
block-beta
    columns 3
    
    DataBlock["DATA LAYER"]
    LogicBlock["DIAGNOSTIC LAYER"]
    PresBlock["PRESENTATION LAYER"]
    
    DB1("Raw NSL-KDD") --> Logic1
    DB2("Processed Data") --> Logic2
    
    space
    
    Logic1("Preprocessing Engine\n(Scalers/Encoders)") --> Logic2("XGBoost Inference Engine\n(Predicts Threat Class)")
    Logic2 --> Pres1
    
    space
    
    Pres1("Flask API Intermediary") --> Pres2("Web Dashboard UI\n(Chart.js, AJAX, CSS)")
    
    style DataBlock fill:#eee,stroke:#333
    style LogicBlock fill:#eee,stroke:#333
    style PresBlock fill:#eee,stroke:#333
```
