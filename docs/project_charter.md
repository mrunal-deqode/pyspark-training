# Recruitment Analytics – PySpark Project Charter

## 1. Project Overview

**Domain:** Recruitment & Hiring Management

**Project:** Recruitment Analytics using Apache PySpark

**Primary Dataset:** Applications

**Supporting Datasets:** Users, Candidate Profiles and Jobs

**Technology:** Python, Apache PySpark

This project aims to build an independent data processing and analytics workflow for a Recruitment & Hiring Management System.

The dataset structure is based on the existing project's SQLAlchemy ORM models. All Phase 1 datasets will contain synthetic data.

## 2. Business Questions

The analytics system should answer:

- How many applications are received monthly?
- Which jobs receive the most applications?
- What percentage of applications are shortlisted?
- Which skills are most common among applicants?
- Which locations have the most candidates?
- How are applications distributed across current statuses?
- How does candidate experience vary?

Primary users include recruiters, HR managers and administrators.

Some questions require combining multiple datasets. For example, skills analysis uses candidate profiles, while application trends use application creation timestamps.

## 3. Dataset Design

The project uses four separate CSV datasets based on the existing database tables.

| Dataset | Initial Target | Future Target |
|---|---:|---:|
| Users | 2,000 candidates plus admins | Configurable |
| Candidate Profiles | Up to 2,000 | Configurable |
| Jobs | 200 | 10,000+ |
| Applications | 5,000 | 500,000+ |

Applications will be the primary fact dataset.

### Applications Columns

- id
- candidate_id
- job_id
- years_of_experience
- status
- is_active
- created_at

### Supporting Dataset Relationships

- Candidate profiles connect to users through `candidate_profiles.user_id`.
- Applications connect to candidates through `applications.candidate_id`, which references `users.id`.
- Applications connect to jobs through `applications.job_id`, which references `jobs.id`.
- Jobs connect to their creators through `jobs.created_by`, which references `users.id`.

The complete column definitions and data types are maintained in `docs/dataset_schema.md`.

## 4. Expected Data Quality Problems

The generated datasets will support practical data-quality exercises:

- Missing values
- Duplicate application records
- Inconsistent status capitalization
- Invalid or inconsistent dates
- Missing experience values
- Inconsistent location names
- Unexpected categorical values

The clean base datasets must preserve valid primary keys, foreign keys and unique application pairs. Controlled data-quality issues will be introduced separately for PySpark cleaning exercises.

## 5. Why Applications Is the Primary Dataset

Applications is selected as the main fact dataset because:

- A candidate can apply to multiple jobs.
- A job can receive applications from multiple candidates.
- Application records accumulate continuously.
- It supports application trend analysis.
- It provides opportunities to practice joins, aggregations and large-scale data processing.

The dataset will initially contain a few thousand records and will be scalable through configurable row-count parameters.

## 6. Application Status Tracking Decision

The analytics pipeline will analyze only the latest status of each application.

- Historical application status changes will not be maintained.
- Each application record will contain its current status.
- Analytics will focus on current status distribution and recruitment outcomes.
- Historical status-transition analysis is outside the project scope.

## 7. Data Generation Strategy

Datasets will be generated using Python Faker or Python's random module.

The generation process will:

- Use a fixed random seed for reproducibility.
- Allow configurable row counts.
- Generate realistic recruitment data.
- Maintain valid dataset relationships.
- Introduce controlled data-quality issues separately.
- Support scaling to several hundred thousand application records.

## 8. Initial Architecture

The initial workflow will remain independent of the existing FastAPI application.

Data Generation
       |
       v
Standalone CSV Datasets
       |
       v
Apache Spark
       |
       v
Data Processing and Analytics
       |
       v
Processed Results

Integration with the existing Recruitment & Hiring Management application is reserved for Phase 2.

## 9. Project Scope

### Phase 1 – Independent PySpark Learning

- Follow company PySpark training modules.
- Generate synthetic recruitment datasets.
- Learn PySpark DataFrames and transformations.
- Perform joins, filtering, aggregations and data cleaning.
- Build standalone analytics workflows.
- Keep the existing FastAPI application and PostgreSQL database unchanged.

### Phase 2 – Project Integration

After completing the independent PySpark learning and implementation, integrate the data-processing workflow with the existing Recruitment & Hiring Management application.

Integration details will be planned separately.
