# Facts registries

**Document status:** PROVISIONAL (S3, for G3) · Policy: [03_FACTS_REGISTRY_POLICY.md](../03_FACTS_REGISTRY_POLICY.md) · Contract: [S3_REGISTRY_ARCHITECTURE.md §1](../research/S3_REGISTRY_ARCHITECTURE.md) · Evidence: [S3_FINDINGS.md](../research/S3_FINDINGS.md)

These are provisional registry records verified on 2026-10-01. They are
public, independently verifiable facts (class B). No personal data belongs
here.

| File | Domain | Content |
|---|---|---|
| [no_tax.yaml](no_tax.yaml) | tax | Norwegian individual taxation 2026 (income, share income, shielding, funds, wealth tax, credit, exit tax); 2027 and the 2026 shielding rate recorded as `unavailable`; NOU 2026:9 as `proposed` |
| [no_wrappers.yaml](no_wrappers.yaml) | wrapper | ASK and the ordinary taxable account (no pension wrappers, ADR-0020) |
| [withholding_us_no.yaml](withholding_us_no.yaml) | withholding | US → NO dividend withholding layers W1–W9 |
| [regulation_eea_no.yaml](regulation_eea_no.yaml) | regulation | PRIIPs, MiFID II / vphl definitions, CFD measures, ESMA advice briefing |
| [broker_nordnet.yaml](broker_nordnet.yaml) | broker | Nordnet Bank NUF |
| [broker_etoro.yaml](broker_etoro.yaml) | broker | eToro (Europe) Ltd |

**Format notes:**
- Each logical record is `file_defaults` merged with the record; the record's own fields win.
- `value: null` with `verification_status: unavailable` means **unknown**. It never means false or zero.
- The file layout is provisional. Physical storage is decided at S6b/S8.

Accepting these records at G3 accepts them **as evidence-backed facts as of
their verification date**. It does not accept them as preferences or
decisions. Later changes in the world create new effective-dated versions.
