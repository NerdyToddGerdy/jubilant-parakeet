# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] – 2025-07-18
### Added
- CHANGELOG.md
- Logged encounters to EncounterHistory table (Step 3)
- Integrated monster storage from Open5e if not cached
- Tagged monster source as "open5e"

### Fixed
- Replaced `float` with `Decimal` for DynamoDB compatibility

## [0.1.0] – 2025-07-17
### Added
- Initial Lambda that pulls monster from Open5e by CR
- Inserts monsters into `Monsters` table if missing
- Setup Pulumi, Poetry, DynamoDB tables, and IAM roles
