"""
AI context for the SII module.
Loaded into the assistant system prompt when this module's tools are active.
"""

CONTEXT = """
## Module Knowledge: SII (Suministro Inmediato de Información)

### Overview
The SII module handles real-time VAT reporting to the Spanish AEAT (Agencia Tributaria)
via the Suministro Inmediato de Información system. Businesses above a threshold must
report invoices and expenses electronically within 4 days of issuance.

### Models

**SIISubmission**
- `reference` (CharField, max 50): unique submission reference
- `submission_type` (CharField, max 30): type of book being submitted:
  - `FacturasEmitidas`: issued invoices (sales)
  - `FacturasRecibidas`: received invoices (purchases/expenses)
  - `BienesInversion`: capital goods
  - `OperacionesIntracomunitarias`: intra-community operations
- `period` (CharField, max 10): reporting period, format `YYYY-MM` e.g. `2026-03`
- `status`: `pending` → `submitted` → `accepted` | `rejected`
- `submitted_at` (DateTimeField, nullable): when batch was sent to AEAT
- `response_code` (CharField, optional): AEAT response code
- `response_message` (TextField, optional): AEAT response details
- `records_count` (PositiveIntegerField, default 0): number of records in this submission

### Key flows

**Submit invoices to SII:**
1. Gather invoices/expenses for the reporting period
2. Create `SIISubmission` with `submission_type`, `period`, `records_count`
3. Generate AEAT-compliant XML and submit to web service
4. On success: set `status='submitted'`, record `submitted_at`
5. Parse AEAT response: set `status='accepted'` or `rejected` with response details

**Check pending submissions:**
- `SIISubmission.objects.filter(status='pending')`
- Submissions must be sent within 4 calendar days of invoice issuance

**Review rejections:**
- Filter `status='rejected'`
- Check `response_code` and `response_message` for error details
- Correct data and resubmit with a new `SIISubmission`

### Relationships
- `SIISubmission` is standalone — no FK to invoicing.Invoice or expenses.Expense
- Cross-referencing with invoices is handled by the submission logic, not enforced at DB level
"""
