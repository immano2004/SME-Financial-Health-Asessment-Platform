# 🏗️ System Architecture & Technical Documentation

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                       PRESENTATION LAYER                         │
│                    (Streamlit Frontend)                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐ │
│  │ Dashboard  │  │  Analytics │  │  Reports   │  │ Admin      │ │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                    BUSINESS LOGIC LAYER                          │
│                 (Utility Modules - Python)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ Metrics      │  │ Scoring      │  │ AI Advisor   │           │
│  │ Calculation  │  │ Engine       │  │ LLM-powered  │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ Tax          │  │ Working      │  │ Cost         │           │
│  │ Compliance   │  │ Capital      │  │ Optimization │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ Credit Risk  │  │ Forecasting  │  │ Products     │           │
│  │ Analysis     │  │ Engine       │  │ Recommender  │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│  ┌──────────────┐  ┌──────────────┐                             │
│  │ Data         │  │ Security &   │                             │
│  │ Validation   │  │ Compliance   │                             │
│  └──────────────┘  └──────────────┘                             │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                       DATA LAYER                                 │
│     ┌──────────────┐              ┌──────────────┐             │
│     │ Local Files  │              │ PostgreSQL   │             │
│     │ CSV/XLSX     │              │ (Production) │             │
│     └──────────────┘              └──────────────┘             │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                    INTEGRATION LAYER                             │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐    │
│  │ Banking APIs   │  │ GST APIs       │  │ Payment APIs   │    │
│  └────────────────┘  └────────────────┘  └────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## Module Architecture

### 1. Core Metrics Module (`metrics.py`)
**Purpose**: Calculate fundamental financial metrics

**Functions**:
- `calculate_metrics(df)`: Computes revenue, expenses, profit margin, expense ratio
- Returns: Dictionary with all financial KPIs

**Dependencies**: pandas, numpy

**Data Flow**:
```
Input DataFrame → Data Cleaning → Metric Calculation → Output Dictionary
```

### 2. Scoring Engine (`scoring.py`)
**Purpose**: Generate health score (0-100)

**Algorithm**:
```
Health Score = (Profit Margin × 20) + (Liquidity × 30) + (Growth × 25) + (Efficiency × 25)
```

**Output**: 0-100 scale health score

### 3. Tax Compliance Module (`tax_compliance.py`)
**Purpose**: Tax regulation compliance checking

**Key Functions**:
- `check_tax_compliance()`: GST eligibility, income tax slab, compliance issues
- `get_tax_deductions()`: Industry-specific deduction recommendations
- `compliance_recommendations_by_language()`: Multilingual compliance guide

**Compliance Checks**:
- GST threshold: ₹40L (services), ₹20L (others)
- Income tax slabs (India)
- Audit requirements
- MSME benefits

### 4. Working Capital Module (`working_capital.py`)
**Purpose**: Cash flow and liquidity optimization

**Key Metrics**:
- Receivables Days = (Avg Receivables / Daily Revenue)
- Inventory Days = (Avg Inventory / Daily COGS)
- Payables Days = (Avg Payables / Daily Expenses)
- Cash Conversion Cycle = Receivables + Inventory - Payables

**Products Recommended**:
- Invoice Discounting (if receivables > 45 days)
- Inventory Finance (if inventory > 60 days)
- Working Capital Loan (if CCC > 60 days)

### 5. Cost Optimization Module (`cost_optimization.py`)
**Purpose**: Cost structure analysis and reduction strategies

**Expense Categories**:
1. Personnel & Salaries (30%)
2. Raw Materials/Inventory (25%)
3. Rent & Utilities (10%)
4. Logistics & Transportation (10%)
5. Marketing & Advertising (8%)
6. Maintenance & Repairs (7%)
7. Miscellaneous (10%)

**Industry Benchmarks**:
- Retail: 70% expense ratio
- Manufacturing: 75%
- Services: 65%
- E-commerce: 80%
- Agriculture: 60%

### 6. Creditworthiness Module (`creditworthiness.py`)
**Purpose**: Detailed credit risk assessment

**Credit Ratings**:
- **AAA** (Score 85+): Minimal risk, best rates
- **AA** (Score 75-84): Low risk, favorable rates
- **A** (Score 65-74): Moderate risk, standard rates
- **BBB** (Score 50-64): Higher risk, premium rates
- **B** (Score <50): High risk, limited options

**Default Risk Calculation**:
```
Default Probability = (100 - Score × 1.2) %
```

**Loan Eligibility Matrix**:
- Working Capital Loan (eligible if score > 40)
- Term Loan (eligible if score > 50)
- Overdraft (eligible if score > 50)
- Equipment Finance (eligible if score > 45)
- Invoice Discounting (eligible if score > 30)

### 7. Forecasting Module (`forecasting.py`)
**Purpose**: Financial projections and trend analysis

**Forecasting Methods**:
1. **Linear**: Least squares polynomial fit
2. **Exponential**: Compound growth rate
3. **Moving Average**: Historical average trend

**Scenarios**:
- Base Case: Expected growth rate
- Optimistic: 1.5× growth, 10% better efficiency
- Pessimistic: 0.5× growth, 10% worse efficiency

**Trend Analysis**:
- Growth Rate Calculation
- Momentum Assessment
- Breakeven Point

### 8. Products Recommender (`products_recommender.py`)
**Purpose**: Personalized financial product recommendations

**Product Categories**:

**Immediate Financing**:
- Working Capital Loans
- Business Overdrafts
- Invoice Discounting

**Growth Products**:
- Asset Financing
- Venture Debt
- Term Loans

**Insurance Products**:
- Business Interruption Insurance
- Key Person Insurance
- Cyber Insurance

**Affordability Calculation**:
```
Monthly EMI = P × [r(1+r)^n] / [(1+r)^n - 1]
where:
  P = Principal Loan Amount
  r = Monthly Interest Rate
  n = Tenure in Months
```

### 9. Data Validation Module (`data_validation.py`)
**Purpose**: Input data quality assurance

**Validation Rules**:
1. Required columns: Date, Revenue, Expense
2. Data types: Numeric for financial fields
3. Range checks: No negative revenues
4. Completeness: Minimum 3 months data
5. Outlier detection: IQR method

**Quality Scoring**:
- Base Score: 100
- Deduction for missing values: -5 per field
- Deduction for duplicates: -2 per duplicate
- Deduction for outliers: -1 per outlier

### 10. Security & Compliance Module (`security_compliance.py`)
**Purpose**: Data protection and regulatory compliance

**Encryption Standards**:
- Sensitive Data: SHA-256 hashing
- PII: AES-256 encryption
- Audit Logs: Complete activity tracking

**Compliance Checking**:
- RBI Guidelines
- GST Requirements
- Income Tax Act
- Data Protection Laws

**Audit Trail**:
```
{
  "timestamp": "2024-01-30T10:30:00Z",
  "action": "data_analysis",
  "user_id": "user_hash",
  "data_accessed": ["revenue", "expenses"],
  "status": "success"
}
```

## Data Flow Architecture

### Input Processing Pipeline
```
┌─────────────┐
│ Upload File │ (CSV/XLSX)
└──────┬──────┘
       ↓
┌─────────────────────┐
│ Data Validation     │ - Check format
└──────┬──────────────┘ - Verify columns
       │              - Detect issues
       ↓
┌─────────────────────┐
│ Data Sanitization   │ - Remove duplicates
└──────┬──────────────┘ - Handle missing
       │              - Normalize values
       ↓
┌─────────────────────┐
│ Quality Scoring     │ - Assess data completeness
└──────┬──────────────┘ - Identify risks
       │              - Flag issues
       ↓
┌─────────────────────┐
│ Passed to Analysis  │ - Metrics calculation
└─────────────────────┘ - Score generation
                        - Recommendations
```

### Analysis Pipeline
```
┌─────────────────────────────┐
│ Financial Metrics           │
│ Calculation                 │
└──────────┬──────────────────┘
           ↓
      ┌────┴────┬──────────────┬──────────────┬─────────────┬─────────────┬─────────────┐
      ↓         ↓              ↓              ↓              ↓             ↓
   Score    Tax          Working        Cost           Credit        Forecasting
   Engine   Compliance   Capital        Optimization   Analysis      & Trends
      │         │          │              │              │             │
      └────┬────┴──────────┴──────────────┴──────────────┴─────────────┘
           ↓
      ┌──────────────────────┐
      │ Product              │
      │ Recommendations      │
      │ (Loans/Insurance)    │
      └──────────┬───────────┘
                 ↓
            ┌─────────────┐
            │ Report      │
            │ Generation  │
            └─────────────┘
```

## Database Schema (Production - PostgreSQL)

```sql
-- Users Table
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR UNIQUE NOT NULL,
  business_name VARCHAR NOT NULL,
  industry VARCHAR NOT NULL,
  pan_hash VARCHAR,
  gst_hash VARCHAR,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Financial Data
CREATE TABLE financial_records (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  analysis_date DATE,
  revenue DECIMAL(15,2),
  expense DECIMAL(15,2),
  profit DECIMAL(15,2),
  health_score INT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Audit Logs
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  action VARCHAR,
  data_accessed TEXT,
  timestamp TIMESTAMP DEFAULT NOW()
);

-- Recommendations
CREATE TABLE recommendations (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  product_type VARCHAR,
  product_name VARCHAR,
  amount DECIMAL(15,2),
  created_at TIMESTAMP DEFAULT NOW()
);
```

## Security Architecture

### Data Protection Layers
```
┌─────────────────────────────────────────┐
│ Layer 1: Input Validation               │
│ - Sanitize all user inputs              │
│ - Validate file formats                 │
└──────────────────┬──────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│ Layer 2: Encryption at Rest             │
│ - AES-256 for sensitive data            │
│ - SHA-256 for hashing                   │
└──────────────────┬──────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│ Layer 3: Encryption in Transit          │
│ - HTTPS/TLS for all communications      │
│ - API token authentication              │
└──────────────────┬──────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│ Layer 4: Access Control                 │
│ - Role-based access control (RBAC)      │
│ - Session management                    │
└──────────────────┬──────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│ Layer 5: Audit & Monitoring             │
│ - Complete activity logging             │
│ - Security event alerting               │
└─────────────────────────────────────────┘
```

## Performance Architecture

### Optimization Strategies
1. **Data Caching**
   - Cache industry benchmarks
   - Cache tax rules
   - Cache product database

2. **Query Optimization**
   - Index financial tables
   - Use connection pooling
   - Implement query caching

3. **Async Processing**
   - Background report generation
   - Asynchronous API calls
   - Batch processing for large datasets

4. **Load Balancing**
   - Horizontal scaling with multiple instances
   - Session affinity
   - Health check monitoring

## Scalability Architecture

### Horizontal Scaling
```
┌─────────────────────────────────────┐
│         Load Balancer               │
│         (nginx/haproxy)             │
└────────────┬────────────────────────┘
      ┌──────┴──────┬──────────┐
      ↓             ↓          ↓
  ┌────────┐  ┌────────┐  ┌────────┐
  │Instance│  │Instance│  │Instance│
  │  1     │  │  2     │  │  3     │
  └────┬───┘  └────┬───┘  └────┬───┘
       └───────────┼───────────┘
                   ↓
            ┌─────────────┐
            │ PostgreSQL  │
            │ with        │
            │ Read Replica│
            └─────────────┘
```

### Vertical Scaling
```
Increase per instance:
- CPU cores: 2 → 4 → 8 → 16
- RAM: 4GB → 8GB → 16GB → 32GB
- Storage: 50GB → 100GB → 500GB → 1TB
```

## Integration Architecture

### Banking API Integration
```
┌──────────────────────────────┐
│ Platform Application         │
└──────────────┬───────────────┘
               ↓
        ┌──────────────┐
        │ API Gateway  │
        └──────┬───────┘
               ↓
        ┌──────────────────────┐
        │ Bank 1 API           │
        │ (Transactions)       │
        └──────────────────────┘
               ↓
        ┌──────────────────────┐
        │ Bank 2 API           │
        │ (Loan Products)      │
        └──────────────────────┘
```

### GST Integration
```
┌──────────────────────────────┐
│ Platform Application         │
└──────────────┬───────────────┘
               ↓
        ┌──────────────────────┐
        │ GST Filing Portal API│
        │ (GSTR Returns)       │
        └──────────────────────┘
```

## Deployment Architecture

### Development Environment
```
Developer's Machine
├── Local Streamlit App
├── Sample Data (CSV)
└── Local Logs
```

### Staging Environment
```
Cloud Server (AWS/GCP)
├── Staging Streamlit App
├── Test Database (PostgreSQL)
├── Test Data
└── Staging Logs
```

### Production Environment
```
Production Cluster (Kubernetes)
├── Multiple App Instances
├── PostgreSQL Primary + Replicas
├── Redis Cache Layer
├── Monitoring & Logging Stack
├── Backup & Recovery System
└── Security & Compliance Layer
```

## Technology Stack Justification

| Component | Choice | Reason |
|-----------|--------|--------|
| **Frontend** | Streamlit | Rapid development, interactive, built-in charts |
| **Backend** | Python | Data science libraries, rapid prototyping |
| **Database** | PostgreSQL | Reliability, ACID compliance, scalability |
| **Analytics** | Pandas/NumPy | Powerful data manipulation, industry standard |
| **Visualization** | Plotly | Interactive, professional charts |
| **Encryption** | AES-256 | Industry standard, secure |
| **Deployment** | Docker/K8s | Containerization, orchestration, scalability |
| **LLM** | Claude/GPT-4 | Advanced reasoning, multilingual support |

---

**Architecture Version**: 1.0  
**Last Updated**: January 2026  
**Maintainer**: Technical Architecture Team
