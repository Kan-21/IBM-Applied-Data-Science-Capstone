# Power BI Analytics Workflow

A reusable checklist based on the SpaceX Falcon 9 historical analytics dashboard.

## 01 | Frame the analytical problem

- Define the audience, business question, decision and scope.
- Identify key metrics, dimensions, grain (one row = what?) and date coverage.
- Write down what the data cannot establish; avoid causal claims from observational patterns.

## 02 | Organise files and provenance

- Create folders for raw/processed data, dashboards, screenshots and documentation.
- Record dataset source URL, download date, coverage, licensing and known limitations.
- Keep source files immutable; work on documented transformed copies.

## 03 | Import and profile data

- Home > Get data: load CSV, Excel, SQL or other supported source.
- Inspect row count, column types, blanks, duplicates, unexpected categories and date parsing.
- Confirm numeric measures have correct units and category labels are consistent.

## 04 | Transform with Power Query

- Home > Transform data: rename fields, set types, handle nulls, standardise text.
- Create reproducible business-rule columns, e.g., LandingClass from landing outcome text.
- Close & Apply; check row counts and inspect transformed columns again.

## 05 | Model and define measures

- Use a clear fact-table grain and relationships if multiple tables are present.
- Prefer measures for dynamic aggregation; calculated columns for row-level categories and sort keys.
- Create DAX measures with DIVIDE for safe rates; COALESCE where missing count should be zero.
- Set percentage, whole number, decimal and mass units deliberately.

## 06 | Validate numbers before visuals

- Reconcile total rows and category counts against source or a separate check.
- Test numerator, denominator, filters, missing values and date range.
- Distinguish a non-successful recorded landing from a failed attempted landing.
- Check zero-success years are displayed as zero, not silently omitted.

## 07 | Design analytical visuals

- Use cards for KPIs, bars for category comparisons, lines for annual trends.
- Use 100% stacked columns for within-category proportions; show raw counts in tooltips.
- Order ordinal bins numerically with a sort column; label units and periods.
- Avoid smoothing discrete annual observations when it obscures exact yearly values.

## 08 | Build interaction and layout

- Add date and launch-site slicers; test cross-filtering and reset behaviour.
- Create a readable header, consistent spacing, aligned visual grid and clear titles.
- Set canvas size intentionally (SpaceX report: 1920 x 1080).
- Check readability at Fit to page and at full size; avoid truncated labels.

## 09 | Perform QA and interpretation

- Check all visuals under full dataset and multiple slicer combinations.
- Verify tooltips, data labels, zero years, sort order and totals.
- Record the key findings and limitations without implying causality.
- Save PBIX and export a full-page PNG or PDF preview.

## 10 | Document and publish

- Keep a Power BI Desktop PBIX file plus an accessible dashboard screenshot.
- Create README with objectives, data source, methods, KPIs, findings, limitations and reproduction instructions.
- Commit a concise Markdown workflow guide to docs/; retain the Word guide for personal study.
- Check sensitive information, credentials, source licensing and GitHub file size before pushing.
- Open the GitHub repository as a visitor and verify all relative links and previews.

## SpaceX project notes

- Historical IBM teaching dataset: 90 records, 2010–2020.
- Recorded successful landings: 60 / 90 (66.7%) with filters cleared.
- `LandingClass = 0` means no recorded successful landing, not necessarily a failed attempted landing.
- Power BI report canvas: 1920 × 1080.
- This is not a live or comprehensive SpaceX operational dataset.

## Publishing checklist

- [ ] Save and reopen the `.pbix` file.
- [ ] Confirm annual 0% values, straight line and annual launch-count tooltip.
- [ ] Test all slicers and clear filters.
- [ ] Export and inspect a full-page screenshot.
- [ ] Document source, findings, limitations and reproduction steps in the main README.
- [ ] Commit PBIX, screenshot and this Markdown guide; check file sizes and licenses.
