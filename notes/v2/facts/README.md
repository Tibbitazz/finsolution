# Facts registries

**Document status:** ACCEPTED as registry v1 (G3, 2026-10-01); physical format provisional (S6b/S8) · Policy: [03_FACTS_REGISTRY_POLICY.md](../03_FACTS_REGISTRY_POLICY.md) · Contract: [S3_REGISTRY_ARCHITECTURE.md §1](../research/S3_REGISTRY_ARCHITECTURE.md) · Evidence: [S3_FINDINGS.md](../research/S3_FINDINGS.md)

These are provisional registry records verified on 2026-10-01. They are
public, independently verifiable facts (class B). No personal data belongs
here. Pension saving (ADR-0020) and wealth tax (ADR-0021) are out of scope
and must not be added. 82 records.

| File | Domain | Content |
|---|---|---|
| [no_tax.yaml](no_tax.yaml) | tax | Norwegian individual income taxation 2026 (income, share income, shielding, funds, credit, exit tax); 2027 parameters and the 2026 shielding rate recorded as `unavailable`. Wealth tax out of scope (ADR-0021) |
| [no_wrappers.yaml](no_wrappers.yaml) | wrapper | ASK (incl. the seven-part foreign-withholding credit decomposition and FX rule) and the ordinary taxable account (no pension wrappers, ADR-0020) |
| [withholding_us_no.yaml](withholding_us_no.yaml) | withholding | US → NO dividend withholding layers W1–W9 |
| [regulation_eea_no.yaml](regulation_eea_no.yaml) | regulation | PRIIPs, MiFID II / vphl definitions, CFD measures, ESMA advice briefing |
| [broker_nordnet.yaml](broker_nordnet.yaml) | broker | Nordnet Bank NUF |
| [broker_etoro.yaml](broker_etoro.yaml) | broker | eToro (Europe) Ltd |

**Format notes:**
- Each logical record is `file_defaults` merged with the record; the record's own fields win.
- `value: null` with `verification_status: unavailable` means **unknown**. It never means false or zero.
- The file layout is provisional. Physical storage is decided at S6b/S8.

**Meaning of acceptance at G3:** each fact is accepted into registry v1 at
its stated source, scope, verification level, valid-time coordinates, and
knowledge-time coordinates, based on the evidence available on its
verification date. Acceptance does not certify a fact forever and does not
turn it into a preference or decision. Later authoritative changes create
new effective-dated facts; historical facts are never rewritten.

`value: null` + `unavailable` = **unknown**. A capability is *not offered*
only where a source says so.
