# Security

## Source acquisition

- Accept only HTTP(S) source contracts from Engine 1.
- Never fetch arbitrary URLs supplied by generated content.
- Future network adapters must validate DNS resolution and block loopback, link-local, private, multicast and reserved destinations.
- Revalidate redirect destinations.

## Files

- Treat every source file as untrusted.
- Validate declared and detected MIME/signature.
- Enforce size and decompression limits.
- Reject archive path traversal and unsafe symlinks.
- Never execute extracted content.

## Content and prompt safety

Source documents can contain prompt-injection text. Extracted source text is data, not instructions. AI prompts must clearly separate system/developer instructions from source evidence.

The model must return structured data validated against application schemas. No LLM output may be interpreted as SQL, shell commands, filesystem paths or executable code without an explicit safe adapter.

## PYQ exclusion

PYQ and PYQ-compilation detection is a hard policy boundary. Detection should happen before generation and before publication. A low-confidence classification must quarantine/review rather than silently publish.

## AI controls

AI cannot:
- publish content
- delete source evidence
- overwrite approved versions
- modify curriculum definitions
- change learner marks/mastery
- bypass review gates
- execute arbitrary tools

Every AI run should eventually record model/version, prompt version, pipeline version, input hashes and output hash.

## Privacy and credentials

Secrets, browser cookies, access tokens and personal credentials must never be stored in source documents, logs or generated content. Use environment/secret storage and redact sensitive values from observability output.

## Auditability

Content changes, review actions, publication events, conflict resolutions and security decisions must be attributable to an actor and timestamped.
