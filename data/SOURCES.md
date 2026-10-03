# Source manifest

## WHO World Health Statistics 2024

- PDF: `raw/who_2024/world_health_statistics_2024.pdf`
- Original report: https://www.who.int/southeastasia/publications/i/item/9789240094703
- Downloaded from the UN Digital Library's copy of the WHO publication: https://digitallibrary.un.org/record/4050651
- Local PDF SHA-256: `f7b08734131ff6b3e07a508f2efc12a94c85ce19eaee2a98f0bbc57fad3c3555`
- 96 PDF pages, including covers and front matter; WHO lists 86 numbered report pages. The report contains selectable text, captions, charts and tables. Example: PDF page 16 has Figure 1.3, life expectancy and healthy life expectancy by income group.
- PDF license: CC BY-NC-SA 3.0 IGO, according to the report's copyright page. Cite WHO and check license requirements before redistribution or commercial use.

- Excel annex: `raw/who_2024/world_health_statistics_2024_annex.xlsx`
- Original download: https://cdn.who.int/media/docs/default-source/gho-documents/world-health-statistic-reports/2024/web_download.xlsx?sfvrsn=4e7bbebd_1
- Listing page: https://www.who.int/data/gho/publications/world-health-statistics
- Local XLSX SHA-256: `d94750a54aa8ecd89b3e8ec2556e98cc94daf3e154f6d7bd5c7c8cf7d5ca1067`
- Workbook sheets: `readme` and `data`. `data` has 10,503 records, 60 distinct indicator names and 206 geography names. Columns: `IND_NAME`, `DIM_GEO_NAME`, `IND_CODE`, `DIM_GEO_CODE`, `DIM_TIME_YEAR`, `DIM_1_CODE`, `VALUE_NUMERIC`, `VALUE_STRING`, `VALUE_COMMENTS`.
- The `readme` sheet says figures are the latest available as of May 2024. An indicator's data year can differ from 2024. `DIM_1_CODE` carries dimensions such as sex or age group; include it in lookup keys to avoid false matches.

These files are related because WHO lists the spreadsheet as the statistical tables accompanying the 2024 report. Charts in the report are not guaranteed to be reconstructible from this annex alone; some use time series or measures not included in the snapshot.
