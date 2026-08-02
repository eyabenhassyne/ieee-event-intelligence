# Dashboard Design System

## Purpose
- Provide a consistent visual language for Power BI dashboard mockups.
- Keep the design aligned with the supported warehouse metrics and the current KPI layer.
- Avoid implying unsupported metrics such as registration conversion, no-show rate, feedback, or satisfaction.

## Visual Direction
- Tone: executive, calm, analytical, and modern.
- Layout: card-led dashboard with clear section hierarchy.
- Density: medium, with enough whitespace for quick scanning.
- Emphasis: portfolio totals first, then trends, then ranked breakdowns, then data-quality context.

## Color Palette
- `Navy`: `#102A43` for primary headings and navigation.
- `Blue`: `#1D4ED8` for primary KPI accents.
- `Teal`: `#0F766E` for attendance and positive-supporting trends.
- `Gold`: `#D97706` for caution and mixed-status reporting.
- `Red`: `#B91C1C` for errors and rejected rows.
- `Slate`: `#475569` for body text.
- `Mist`: `#F8FAFC` for page background.
- `Border`: `#D9E2EC` for card borders and table dividers.

## Typography
- Headings: `Segoe UI Semibold` or Power BI default sans-serif equivalent.
- Body: `Segoe UI` or the closest available system sans-serif.
- Numbers: bold, large, and tightly spaced in KPI cards.
- Table labels: regular weight with small caps only where needed for labels.

## Components
- KPI card
  - Use for totals, rates, and data-quality counts.
  - Include label, main value, and one short context line.
- Trend chart
  - Use for monthly event trend, attendance trend, and load trend.
- Ranked bar chart
  - Use for categories, organizing units, countries, and data-quality rules.
- Table
  - Use for event inventory, monthly export, and issue detail.
- Filter rail
  - Use a compact left rail for year, month, category, country, host type, and status filters.

## Layout Rules
- Every page starts with four to six KPI cards.
- Every page includes one primary trend or ranked chart.
- Every page ends with either a supporting table or a data-quality block.
- Avoid overcrowding the executive overview with every available metric.

## Accessibility Rules
- Keep strong contrast between text and background.
- Use labels, not color alone, to communicate severity.
- Avoid tiny text in tables.
- Keep alternative text available for every visual in the final Power BI build.

## Supported Metric Boundaries
- Supported: event count, publishing status, cancellation status, virtual status, attendance totals, attendance reporting rate, category, subcategory, country, state, organizing unit, physical-location coverage, ETL run status, and data-quality issues.
- Unsupported / deferred: registration conversion, no-show rate, feedback, satisfaction, promotion effectiveness, reporting compliance, and cost-per-attendee analysis.

## Mockup Goals
- Make the next build step straightforward for Power BI.
- Show where each report page belongs in the semantic model.
- Highlight data gaps without overpromising precision that the warehouse does not support.
