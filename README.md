# SII (Spain)

## Overview

| Property | Value |
|----------|-------|
| **Module ID** | `sii` |
| **Version** | `1.0.0` |
| **Icon** | `shield-outline` |
| **Dependencies** | None |

## Models

### `SIISubmission`

SIISubmission(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, reference, submission_type, period, status, submitted_at, response_code, response_message, records_count)

| Field | Type | Details |
|-------|------|---------|
| `reference` | CharField | max_length=50 |
| `submission_type` | CharField | max_length=30 |
| `period` | CharField | max_length=10 |
| `status` | CharField | max_length=20, choices: pending, submitted, accepted, rejected |
| `submitted_at` | DateTimeField | optional |
| `response_code` | CharField | max_length=50, optional |
| `response_message` | TextField | optional |
| `records_count` | PositiveIntegerField |  |

## URL Endpoints

Base path: `/m/sii/`

| Path | Name | Method |
|------|------|--------|
| `(root)` | `dashboard` | GET |
| `submissions/` | `submissions` | GET |
| `sii_submissions/` | `sii_submissions_list` | GET |
| `sii_submissions/add/` | `sii_submission_add` | GET/POST |
| `sii_submissions/<uuid:pk>/edit/` | `sii_submission_edit` | GET |
| `sii_submissions/<uuid:pk>/delete/` | `sii_submission_delete` | GET/POST |
| `sii_submissions/bulk/` | `sii_submissions_bulk_action` | GET/POST |
| `settings/` | `settings` | GET |

## Permissions

| Permission | Description |
|------------|-------------|
| `sii.view_siisubmission` | View Siisubmission |
| `sii.submit_sii` | Submit Sii |
| `sii.manage_settings` | Manage Settings |

**Role assignments:**

- **admin**: All permissions
- **manager**: `submit_sii`, `view_siisubmission`
- **employee**: `view_siisubmission`

## Navigation

| View | Icon | ID | Fullpage |
|------|------|----|----------|
| Dashboard | `speedometer-outline` | `dashboard` | No |
| Submissions | `shield-outline` | `submissions` | No |
| Settings | `settings-outline` | `settings` | No |

## AI Tools

Tools available for the AI assistant:

### `list_sii_submissions`

List SII (Suministro Inmediato de Información) submissions.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status` | string | No | pending, submitted, accepted, rejected |
| `period` | string | No |  |

### `get_sii_submission`

Get detailed SII submission info including response code and message.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `submission_id` | string | Yes | Submission ID |

### `create_sii_submission`

Create a new SII submission for a tax period.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `submission_type` | string | Yes | Type: issued_invoices, received_invoices |
| `period` | string | Yes | Tax period (e.g. 2026-01, 2026-Q1) |
| `reference` | string | No | Submission reference |

### `get_sii_summary`

Get SII submission summary: counts by status for a period.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `period` | string | No | Tax period to summarize |

## File Structure

```
README.md
__init__.py
admin.py
ai_tools.py
apps.py
forms.py
locale/
  en/
    LC_MESSAGES/
      django.po
  es/
    LC_MESSAGES/
      django.po
migrations/
  0001_initial.py
  __init__.py
models.py
module.py
static/
  icons/
    icon.svg
  sii/
    css/
    js/
templates/
  sii/
    pages/
      dashboard.html
      index.html
      settings.html
      sii_submission_add.html
      sii_submission_edit.html
      sii_submissions.html
      submissions.html
    partials/
      dashboard_content.html
      panel_sii_submission_add.html
      panel_sii_submission_edit.html
      settings_content.html
      sii_submission_add_content.html
      sii_submission_edit_content.html
      sii_submissions_content.html
      sii_submissions_list.html
      submissions_content.html
tests/
  __init__.py
  conftest.py
  test_models.py
  test_views.py
urls.py
views.py
```
