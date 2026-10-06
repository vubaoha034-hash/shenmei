# Experimental workflow adapter0.1.1

The original0.1.0 source and evidence remain unchanged. This version fixes the actual409 caused by the new S7_FINAL_REUSE.md native entry and returns the true bound entry path. Native mirror/hash, mainline, authentication, independent-pixel review, and no-promotion gates remain unchanged. Actual reference/artwork extraction and independent review still require separate connected tools.

Root tests use immutable published3e6a5638c2af2bedcfd66d23fabf6aa7d35c957d (S7,350/372) and4d128f7b44dc43163f021b5717f5e003ca70a323 (S4), plus explicitly mutated engineering negative fixtures. Production resolves the live canonical branch. Test authorization is local only and is not hosted identity or a production MCP call.

The copied initialization test initially retained0.1.0 and failed39/40; the version expectation was corrected for this release and actual40/40 passed. No taste criteria or production checks were loosened. Current release, publication, independent source review and connection limitations are recorded in ../CURRENT_RELEASE.json. Runtime/model learning and time savings are not claimed.
