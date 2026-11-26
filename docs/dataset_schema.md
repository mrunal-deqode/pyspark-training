# Recruitment Analytics – Dataset Schema

## 1. Purpose

This document defines the four synthetic CSV datasets for the independent PySpark training workflow.

The schema is based on the existing Recruitment & Hiring Management project's SQLAlchemy ORM models.

The CSV files will contain synthetic data only. They will not connect to or modify the existing PostgreSQL database during Phase 1.

## 2. Dataset Overview

| CSV File | Source Table | Purpose |
|---|---|---|
| users.csv | users | Candidate and admin account information |
| candidate_profiles.csv | candidate_profiles | Candidate profile and skills information |
| jobs.csv | jobs | Job posting information |
| applications.csv | applications | Candidate applications; primary fact dataset |

## 3. Users Dataset

**File:** `users.csv`

**Primary Key:** `id`

| Column | Data Type | Nullable | Description |
|---|---|---|---|
| id | Integer | No | Unique user identifier |
| role | String | No | User role, such as candidate or admin |
| full_name | String | Yes | Synthetic user's full name |
| is_active | Boolean | No | Whether the account is active |
| created_at | Timestamp | No | Account creation timestamp |

Security note: Password hashes, email addresses and phone numbers are excluded from this analytics dataset.

## 4. Candidate Profiles Dataset

**File:** `candidate_profiles.csv`

**Primary Key:** `id`

**Foreign Key:** `user_id` references `users.id`

| Column | Data Type | Nullable | Description |
|---|---|---|---|
| id | Integer | No | Unique profile identifier |
| user_id | Integer | No | Associated candidate user |
| address | String | Yes | Candidate address |
| education | String | Yes | Candidate education details |
| experience | String | Yes | Candidate experience description |
| skills | String | Yes | Candidate skills information |

The `user_id` column is unique in the source model, so each user can have at most one candidate profile.

The address is not a normalized location field. Any location-based analysis derived from it will require a documented transformation.

Security note: Resume URLs are excluded.

## 5. Jobs Dataset

**File:** `jobs.csv`

**Primary Key:** `id`

**Foreign Key:** `created_by` references `users.id`

| Column | Data Type | Nullable | Description |
|---|---|---|---|
| id | Integer | No | Unique job identifier |
| title | String | No | Job title |
| job_type | String | No | Type of employment |
| location | String | No | Job location |
| min_experience_years | Integer | No | Minimum required experience |
| max_experience_years | Integer | Yes | Maximum required experience |
| salary_min | Integer | Yes | Minimum salary |
| salary_max | Integer | Yes | Maximum salary |
| status | String | No | Current job status |
| is_active | Boolean | No | Whether the job is active |
| created_by | Integer | No | User who created the job |
| created_at | Timestamp | No | Job creation timestamp |
| deadline | Date | No | Application deadline |

The job description is excluded from the initial analytics projection.

## 6. Applications Dataset

**File:** `applications.csv`

**Primary Key:** `id`

**Foreign Keys:**
- `candidate_id` references `users.id`
- `job_id` references `jobs.id`

| Column | Data Type | Nullable | Description |
|---|---|---|---|
| id | Integer | No | Unique application identifier |
| candidate_id | Integer | No | Candidate user identifier |
| job_id | Integer | No | Job identifier |
| years_of_experience | Float | No | Candidate's experience for this application |
| status | String | No | Current application status |
| is_active | Boolean | No | Whether the application is active |
| created_at | Timestamp | No | Application creation timestamp |

The source model has a unique constraint on the combination of `candidate_id` and `job_id`. A candidate cannot apply to the same job more than once.

Only the latest application status is represented. Historical status changes are outside the project scope.

Security note: Cover letters and internal notes are excluded.

## 7. Dataset Relationships

The datasets will be joined using these relationships:

- `users.id` → `candidate_profiles.user_id`
- `users.id` → `applications.candidate_id`
- `jobs.id` → `applications.job_id`
- `users.id` → `jobs.created_by`

A candidate is represented by a user with the candidate role. The application references the candidate's user ID, not the candidate profile ID.

## 8. Initial Dataset Scale

The initial training targets are:

| Dataset | Initial Target |
|---|---:|
| Candidate users | 2,000 |
| Candidate profiles | Up to 2,000 |
| Jobs | 200 |
| Applications | 5,000 |

The users dataset will also contain a small number of admin users to support job ownership relationships.

These are generation targets, not fixed database constraints. The generator must maintain valid foreign-key relationships and unique application pairs.

## 9. Data Generation and Quality

All records will be synthetic and reproducible using a fixed random seed.

The clean base datasets will respect primary keys, foreign keys and uniqueness constraints.

Data-quality problems such as missing values, inconsistent categories and duplicate records may be introduced in separate raw or staging data for PySpark cleaning exercises. They must not silently change the documented source relationships.

## 10. Phase 1 Boundary

- Generate independent synthetic CSV files.
- Read and process them using Apache PySpark.
- Practice joins, filtering, aggregation and data cleaning.
- Do not connect to or modify the existing FastAPI application or PostgreSQL database.

Integration is reserved for Phase 2.
