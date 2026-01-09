# Lane profiles (policy, not implementation)

We use **one envelope schema** (`meta + payload`) but different lanes require different **minimum meta** fields.

## Compact profile (Spinal high-rate)
Applies to:
- `/sc/aff/event/...`
- `/sc/media/event/...`

Minimum required meta (in addition to schema requirements):
- `message_id`
- `schema_version` (v1)
- `contract` and `message_type` (must match)
- `origin_plane`
- `source` (and optional `device` object)
- `scope_level`, `scope`
- `produced_at` (ISO UTC)
- `content_type`, `content_encoding`
Recommended:
- `ttl_ms` (short)
Optional:
- tracing fields (`trace_id`, `span_id`, `parent_span_id`)
- `priority`, `qos_hint`
- `hlc` (useful for ordering/replay)

## Full profile (Control/Reliable/Reflect)
Applies to:
- `/bs/relay/event/...`
- `/C/cmd/event/...`
- `/E/outcome/event/...`
- `/X/reflect/event/...`

Additional minimum expectations:
- `ttl_ms` or `expires_at` for events; `deadline_ms` for commands
- `priority` for commands
- tracing fields recommended for observability

## Drift rule
For all lanes in v1:
- `meta.contract` MUST equal `meta.message_type`
- mismatch → reject + `RejectEvent`
