import random
from datetime import datetime, timedelta, timezone

from faker import Faker

import csv

from src.data_generation.config import (
    NUM_CANDIDATES,
    NUM_ADMINS,
    NUM_JOBS,
    NUM_APPLICATIONS,
    RANDOM_SEED,
    RAW_DATA_DIR,
)

fake = Faker()
Faker.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)


def generate_users():
    """Generate synthetic candidate and admin users."""

    users = []

    start_date = datetime(2023, 1, 1, tzinfo=timezone.utc)

    # Generate candidate users
    for user_id in range(1, NUM_CANDIDATES + 1):
        created_at = start_date + timedelta(
            days=random.randint(0, 1000)
        )

        users.append({
            "id": user_id,
            "role": "candidate",
            "full_name": fake.name(),
            "is_active": random.choice([True, True, True, False]),
            "created_at": created_at.isoformat(),
        })

    # Generate admin users
    admin_start_id = NUM_CANDIDATES + 1

    for user_id in range(
        admin_start_id,
        admin_start_id + NUM_ADMINS
    ):
        created_at = start_date + timedelta(
            days=random.randint(0, 1000)
        )

        users.append({
            "id": user_id,
            "role": "admin",
            "full_name": fake.name(),
            "is_active": True,
            "created_at": created_at.isoformat(),
        })

    return users


def generate_candidate_profiles(users):
    """Generate one synthetic profile for each candidate user."""

    profiles = []

    candidate_users = [
        user for user in users
        if user["role"] == "candidate"
    ]

    education_options = [
        "B.Tech in Computer Science",
        "BCA",
        "MCA",
        "MBA",
        "B.Sc in Information Technology",
        "M.Tech in Computer Science",
    ]

    skill_options = [
        "Python", "Java", "SQL", "PySpark",
        "React", "FastAPI", "AWS", "Docker",
        "Machine Learning", "Data Analysis",
        "Spring Boot", "PostgreSQL",
    ]

    for profile_id, user in enumerate(candidate_users, start=1):
        selected_skills = random.sample(
            skill_options,
            k=random.randint(3, 6)
        )

        profiles.append({
            "id": profile_id,
            "user_id": user["id"],
            "address": fake.city(),
            "education": random.choice(education_options),
            "experience": (
                f"{random.randint(0, 8)} years of professional experience"
            ),
            "skills": ", ".join(selected_skills),
        })

    return profiles


def generate_jobs(users):
    """Generate synthetic job postings."""

    jobs = []

    admin_users = [
        user for user in users
        if user["role"] == "admin"
    ]

    job_titles = [
        "Python Developer",
        "Java Developer",
        "Data Engineer",
        "Data Analyst",
        "PySpark Developer",
        "Backend Developer",
        "Frontend Developer",
        "Full Stack Developer",
        "Machine Learning Engineer",
        "DevOps Engineer",
    ]

    job_types = ["Full-time", "Contract", "Internship"]

    locations = [
        "Indore", "Pune", "Mumbai", "Bangalore",
        "Hyderabad", "Delhi", "Chennai",
    ]

    job_statuses = ["open", "closed", "on_hold"]

    start_date = datetime(2024, 1, 1, tzinfo=timezone.utc)

    for job_id in range(1, NUM_JOBS + 1):
        created_at = start_date + timedelta(
            days=random.randint(0, 700)
        )

        min_experience = random.randint(0, 5)
        max_experience = min_experience + random.randint(1, 5)

        salary_min = random.randint(300000, 1200000)
        salary_max = salary_min + random.randint(100000, 800000)

        deadline = created_at.date() + timedelta(
            days=random.randint(15, 90)
        )

        creator = random.choice(admin_users)

        jobs.append({
            "id": job_id,
            "title": random.choice(job_titles),
            "job_type": random.choice(job_types),
            "location": random.choice(locations),
            "min_experience_years": min_experience,
            "max_experience_years": max_experience,
            "salary_min": salary_min,
            "salary_max": salary_max,
            "status": random.choice(job_statuses),
            "is_active": random.choice([True, True, True, False]),
            "created_by": creator["id"],
            "created_at": created_at.isoformat(),
            "deadline": deadline.isoformat(),
        })

    return jobs


def generate_applications(users, jobs):
    """Generate applications with valid and unique candidate-job pairs."""

    applications = []

    candidate_ids = [
        user["id"] for user in users
        if user["role"] == "candidate"
    ]

    job_ids = [job["id"] for job in jobs]
    job_by_id = {job["id"]: job for job in jobs}

    available_pairs = [
        (candidate_id, job_id)
        for candidate_id in candidate_ids
        for job_id in job_ids
    ]

    selected_pairs = random.sample(
        available_pairs,
        k=NUM_APPLICATIONS
    )

    statuses = [
        "Applied",
        "Under Review",
        "Shortlisted",
        "Interview Scheduled",
        "Rejected",
        "Selected",
    ]

    start_date = datetime(2024, 1, 1, tzinfo=timezone.utc)

    for application_id, (candidate_id, job_id) in enumerate(
        selected_pairs,
        start=1
    ):
        job = job_by_id[job_id]

        job_created_at = datetime.fromisoformat(job["created_at"])
        job_deadline = datetime.fromisoformat(job["deadline"]).date()

        application_day_offset = random.randint(
            0,
            (job_deadline - job_created_at.date()).days
        )

        created_at = job_created_at + timedelta(
            days=application_day_offset
        )

        applications.append({
            "id": application_id,
            "candidate_id": candidate_id,
            "job_id": job_id,
            "years_of_experience": round(
                random.uniform(0, 12), 1
            ),
            "status": random.choice(statuses),
            "is_active": random.choice([True, True, True, False]),
            "created_at": created_at.isoformat(),
        })

    return applications


def validate_datasets(users, profiles, jobs, applications):
    """Validate generated datasets and their relationships."""

    user_ids = {user["id"] for user in users}
    candidate_ids = {
        user["id"] for user in users
        if user["role"] == "candidate"
    }
    admin_ids = {
        user["id"] for user in users
        if user["role"] == "admin"
    }
    job_ids = {job["id"] for job in jobs}

    # Primary key validation
    assert len(user_ids) == len(users), "Duplicate user IDs"
    assert len({p["id"] for p in profiles}) == len(
        profiles), "Duplicate profile IDs"
    assert len(job_ids) == len(jobs), "Duplicate job IDs"
    assert len({a["id"] for a in applications}) == len(
        applications), "Duplicate application IDs"

    # Candidate profile relationship validation
    profile_user_ids = [p["user_id"] for p in profiles]

    assert len(profile_user_ids) == len(set(profile_user_ids)), (
        "Duplicate candidate profile user references"
    )
    assert all(user_id in candidate_ids for user_id in profile_user_ids), (
        "Invalid candidate profile user reference"
    )

    # Job creator validation
    assert all(job["created_by"] in admin_ids for job in jobs), (
        "Invalid job creator reference"
    )

    # Application relationship validation
    application_pairs = [
        (a["candidate_id"], a["job_id"])
        for a in applications
    ]

    assert len(application_pairs) == len(set(application_pairs)), (
        "Duplicate candidate-job application pairs"
    )

    assert all(a["candidate_id"] in candidate_ids for a in applications), (
        "Invalid application candidate reference"
    )

    assert all(a["job_id"] in job_ids for a in applications), (
        "Invalid application job reference"
    )

    print("All dataset validation checks passed.")


def save_datasets(users, profiles, jobs, applications):
    """Save all generated datasets as CSV files."""

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    datasets = {
        "users.csv": users,
        "candidate_profiles.csv": profiles,
        "jobs.csv": jobs,
        "applications.csv": applications,
    }

    for filename, records in datasets.items():
        file_path = RAW_DATA_DIR / filename

        with file_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=records[0].keys(),
                lineterminator="\n"
            )

            writer.writeheader()
            writer.writerows(records)

        print(f"Generated {filename}: {len(records)} records")


def generate_all_datasets():
    """Generate, validate, and save all recruitment datasets."""

    # Reset seeds to ensure reproducible output on every run
    random.seed(RANDOM_SEED)
    fake.seed_instance(RANDOM_SEED)

    print("Starting recruitment dataset generation...")

    users = generate_users()
    profiles = generate_candidate_profiles(users)
    jobs = generate_jobs(users)
    applications = generate_applications(users, jobs)

    validate_datasets(users, profiles, jobs, applications)

    save_datasets(users, profiles, jobs, applications)

    print("\nDataset generation completed successfully.")


if __name__ == "__main__":
    generate_all_datasets()
