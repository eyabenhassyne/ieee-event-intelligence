# Pull Request

## Title

Add dashboard mockups for IEEE event intelligence

## Summary

- Added a dashboard design system note for the supported Power BI reporting pages.
- Added low-fidelity wireframes for the executive, inventory, attendance, organizational-unit, category, geography, data-quality, and monthly export pages.
- Added a static HTML mockup set under `mockups/`.
- Added a visual-to-data mapping document that ties each mockup to the warehouse and analytics views.
- Added a mockup review checklist.
- Added a verification script for the mockup package.
- Added a dashboard mockup summary report.
- Updated the repository README with dashboard mockup status.

## Validation

- Mockup verification: PASS
- Repository tests: 9 passed
- Manual review: APPROVED with a Home-navigation fix applied
- Screenshot status: pending, because browser screenshot tooling was not available

## Scope Guardrails

- No Power BI file was created.
- No unsupported metrics were introduced.
- No datasets or `.env` files were modified.
- No external API calls were added to the mockup pages.

## Review Checklist

- Confirm the static pages match the current KPI layer.
- Confirm the supported metric boundaries are preserved.
- Confirm no data files were added.
- Confirm the mockups are suitable as Power BI build references.

## Final Review Notes

- Every report page now includes a route back to the home page.
- Attendance language now uses "not reported" where attendance is missing.
- Power BI implementation remains not started.
