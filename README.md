# SII (Spain) Module

Suministro Inmediato de Informacion -- real-time VAT reporting for Spain.

## Features

- Submit VAT records to the Spanish Tax Agency (AEAT) via the SII system
- Track submission status (pending, submitted, accepted, rejected)
- Record submission type, tax period, and number of records per submission
- View AEAT response codes and messages for each submission
- Dashboard with submission overview and compliance metrics

## Installation

This module is installed automatically via the ERPlora Marketplace.

## Configuration

Access settings via: **Menu > SII (Spain) > Settings**

## Usage

Access via: **Menu > SII (Spain)**

### Views

| View | URL | Description |
|------|-----|-------------|
| Dashboard | `/m/sii/dashboard/` | SII compliance overview and metrics |
| Submissions | `/m/sii/submissions/` | List and manage SII submissions to AEAT |
| Settings | `/m/sii/settings/` | Module configuration |

## Models

| Model | Description |
|-------|-------------|
| `SIISubmission` | SII submission record with reference, submission type, period, status, submission timestamp, AEAT response code/message, and records count |

## Permissions

| Permission | Description |
|------------|-------------|
| `sii.view_siisubmission` | View SII submissions |
| `sii.submit_sii` | Submit records to the SII system |
| `sii.manage_settings` | Manage module settings |

## License

MIT

## Author

ERPlora Team - support@erplora.com
