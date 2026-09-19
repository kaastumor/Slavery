# Staging / production deployment boundary

No cloud provider is locked yet. Local Docker Compose is a development environment only.

A future staging/production environment should provide:

- managed or operationally supported PostgreSQL + PostGIS;
- encrypted connections and private database networking;
- separate migration/admin, research-write, and publish-read roles;
- automated backups and point-in-time recovery where available;
- secrets supplied by the deployment platform, never committed `.env` files;
- public services reading only `publish` views/materializations;
- object storage for immutable release artifacts and permitted source assets;
- CI deployment gated by migration, reconciliation, QC and review checks.

Provider-specific infrastructure-as-code should be added only after a hosting provider is selected. Do not make production depend on the local Docker volume.
