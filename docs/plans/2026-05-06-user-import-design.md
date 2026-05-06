# User Import Design

## Goal

Prepare `MFS COURIERS.json` for import and add a dedicated backend endpoint that loads cleaned courier records into the `User` table.

## Approved Approach

Use a two-step flow:

- clean and deduplicate `MFS COURIERS.json` in the repository first
- add an admin-only import endpoint that accepts a JSON file and imports records through a dedicated import schema

## JSON Preparation Rules

- convert every `phone` value to a string
- remove entire records with invalid `email`
- replace invalid or too-short text values with `"_"` where the field should stay present
- remove duplicate records by `email`, keeping the most complete record
- when two duplicate records are equally complete, keep the one with the later `created_at`

## Completeness Rule

A record is considered more complete when it has more meaningful values across user-facing fields. Values `None`, `""`, and `"_"` do not count as filled. Fields used for scoring should include:

- `name`
- `phone`
- `email`
- `how_found_it`
- `desired_transport`
- `birth_date`
- `telegram`
- `city`
- `address`
- `work_in`
- `citizenship`
- `invoice`
- `status`
- `consent`

## Backend Changes

- add a dedicated import schema that matches the `User` model fields used for creation
- keep this schema intentionally looser than the public `UserCreate` schema so import can accept already-cleaned historical data
- add a service that parses uploaded JSON, validates records against the import schema, skips rows whose `email` already exists in the database, and inserts valid users
- add an admin-only endpoint at `POST /api/v1/users/import`

## Endpoint Behavior

- request body: uploaded JSON file
- auth: admin JWT, same as protected user endpoints
- success response: import report with `received`, `imported`, `skipped`, and per-row error details
- duplicate emails already present in the database should not abort the whole import; they should be reported as skipped

## Validation

- the cleaned `MFS COURIERS.json` should no longer contain invalid emails
- duplicate emails should be removed before import
- the backend endpoint should accept the cleaned file and produce a structured import report
