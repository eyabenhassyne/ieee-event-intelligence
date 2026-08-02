# IEEE Event Intelligence Platform

## Overview

The IEEE Event Intelligence Platform is a Business Intelligence and
decision-support prototype for monitoring IEEE events.

The platform consolidates authorized event data, processes it through an ETL
workflow, stores cleaned data in an analytics database, and presents KPIs
through Power BI dashboards and management reports.

## Main Objectives

- Map available IEEE event data sources
- Build a repeatable ETL workflow
- Detect and report data-quality issues
- Design a PostgreSQL dimensional model
- Define event-monitoring KPIs
- Build Power BI dashboards
- Produce technical and user documentation

## Scope

The project includes:

- CSV and Excel data imports
- Data validation and normalization
- PostgreSQL analytics database
- Fact and dimension tables
- KPI definitions
- Power BI dashboards
- Data-quality monitoring
- Reporting and documentation

## Out of Scope

The project does not include:

- Event registration
- Payment processing
- Authentication or user accounts
- Mobile application development
- Full event-management functionality
- Conference paper-management workflows

## Proposed Architecture

1. IEEE and local data sources
2. Raw and staging layers
3. ETL and data-quality processing
4. PostgreSQL analytics database
5. Power BI semantic model
6. Dashboards and decision-support reports

## Technology Stack

- Python
- pandas
- PostgreSQL
- SQL
- Power BI
- Git
- Markdown

## Project Status

Current phase: Project initialization and requirements analysis.

## Data Warehouse Design

The project uses a PostgreSQL star schema centered on one `FactEvents` row per IEEE event.

Implemented dimensions include:
- `DimDate`
- `DimCategory`
- `DimSubcategory`
- `DimCountry`
- `DimState`
- `DimLocation`
- `DimOrganizingUnit`

Audit support is modeled through:
- `audit.etl_run`
- `audit.source_file`
- `audit.data_quality_issue`

Missing attendance remains `NULL` and must not be coerced to zero. Registration, feedback, promotion, and reporting-compliance analytics are deferred unless new source data becomes available.

## Current Status

- Database schema design: implemented in SQL scripts
- Database deployment: pending manual PostgreSQL password update in `.env` and schema application
