# Business Requirements Document

## 1. Project Title

IEEE Event Intelligence Platform

## 2. Project Overview

The IEEE Event Intelligence Platform is a Business Intelligence and
decision-support prototype for monitoring IEEE events.

The platform will consolidate authorized data from IEEE and local sources,
process it through an ETL workflow, store cleaned data in an analytics
database, and present KPIs through Power BI dashboards and management reports.

## 3. Problem Statement

IEEE event information may be distributed across several files, reports,
surveys, and organizational units.

This creates several problems:

- Event data is not centralized.
- File formats and field names may differ.
- Reports may be missing or incomplete.
- Attendance and registration values may be inconsistent.
- Duplicate event records may exist.
- Monthly reporting may require manual work.
- Data-quality problems may reduce confidence in the results.

The project aims to create a controlled analytics workflow that transforms
available event data into reliable decision-support information.

## 4. Project Objectives

- Identify and document available event data sources.
- Define stakeholder questions and reporting needs.
- Build a repeatable ETL workflow.
- Validate, clean, normalize, and consolidate event data.
- Store analytics-ready data in PostgreSQL.
- Design a dimensional data model.
- Define and document KPIs.
- Build Power BI dashboards.
- Display data-quality issues clearly.
- Produce technical and user documentation.

## 5. Main Stakeholders

- IEEE Tunisia Section coordinators
- Chapter officers
- Affinity Group leaders
- Student Branch leaders
- Region-level reviewers
- Internship supervisor

## 6. Main Business Questions

1. How many events were planned, published, completed, or reported?
2. Which completed events are still missing reports?
3. Which events have missing attendance information?
4. Which organizational units are the most active?
5. Which organizational units have no recent activity?
6. How does event activity change by month?
7. How does attendance change by category and modality?
8. What percentage of registered participants attended?
9. What is the no-show rate?
10. Which events are missing feedback?
11. What is the average satisfaction score?
12. Which sources contain the most data-quality problems?
13. Which records may be duplicates?
14. Which units have the highest reporting compliance?
15. Which event categories are underrepresented?

## 7. Project Scope

The project includes:

- Requirements analysis
- Data-source mapping
- Data profiling
- CSV and Excel imports
- ETL development
- Data validation and normalization
- Duplicate detection
- Data-quality monitoring
- PostgreSQL analytics database
- Dimensional modeling
- KPI dictionary
- Power BI dashboards
- Testing
- User guide
- Technical documentation
- Deployment recommendations
- Final report and presentation

## 8. Out of Scope

The project does not include:

- Event registration
- Payment processing
- Authentication or user accounts
- Mobile application development
- Full event-management software
- Conference paper submission or peer review
- Real-time synchronization
- Production-grade enterprise deployment

## 9. Assumptions

- Authorized sample event data will be provided.
- Data may arrive in different formats.
- Some fields may be incomplete or inconsistent.
- The first version will use manual data refresh.
- PostgreSQL and Power BI Desktop will be available.
- Stakeholders will validate the most important KPIs.
- Personal data will be minimized or anonymized.

## 10. Constraints

- The internship lasts eight weeks.
- One intern is handling requirements, ETL, database, Power BI, testing, and documentation.
- IEEE API access may not be available.
- Historical data may be incomplete.
- Some KPIs may not be possible if required fields are missing.
- The work must remain a BI prototype.

## 11. Open Questions

1. Which exact data sources will be available?
2. Which years should be included?
3. Which event statuses are officially used?
4. What defines a completed event?
5. What is the deadline for submitting an event report?
6. When is a report considered late?
7. Is feedback required for every event?
8. How is attendance confirmed?
9. Are members and guests stored separately?
10. Which organizational units should be compared?
11. Which event categories should be used?
12. What satisfaction scale is used?
13. Which fields contain personal information?
14. Which KPIs are mandatory?
15. How often should the data be refreshed?