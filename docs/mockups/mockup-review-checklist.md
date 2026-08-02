# Mockup Review Checklist

## Content Accuracy
- [ ] Every KPI shown is supported by the current warehouse snapshot.
- [ ] No unsupported metric appears in labels, tooltips, or captions.
- [ ] Attendance remains blank or null-aware where data is missing.
- [ ] Data-quality messaging matches the current ETL results.

## Layout Quality
- [ ] Executive overview is the clearest page.
- [ ] Filters are consistent across pages.
- [ ] KPI cards have clear labels and readable values.
- [ ] Tables are not overcrowded.

## Navigation
- [ ] The static mockup home page links to every report page.
- [ ] Each page includes a route back to the home page.

## Power BI Readiness
- [ ] Visual-to-data mapping matches the semantic model.
- [ ] The page order matches the expected Power BI build sequence.
- [ ] The mockups can be translated into Power BI visuals without redesigning the KPI structure.

## Repository Hygiene
- [ ] No datasets were added or modified.
- [ ] No `.env` file was created or changed.
- [ ] Only static design and documentation files were added.

## Review Result
- Status: Approved with one minor navigation fix applied.
- Critical issues: none.
- Screenshot status: pending; browser screenshot tooling was not available in this environment.
- Power BI implementation: not started.
