# Personal Digital Footprint Report

Subject: Subject A (fictional: Krishna Rao)
Date: 2026-11-05
Method: passive OSINT, public sources only, consent confirmed

## Summary
Findings: 6 | Critical: 2 | High: 2 | Medium: 2 | Low: 0
Exposure index: 37/100

## Findings (highest risk first)
1. [Critical 100] Breach: Test email found in a data breach (S4 D5 E5)
   Source: https://breachcheck.example/result | Found: 2026-11-01
   Fix: Change the password everywhere it was used; enable an authenticator app or passkey.
2. [Critical 60] Contact info: Home address on a people-search site (S5 D4 E3)
   Source: https://peoplefind.example/krishna-rao | Found: 2026-11-01
   Fix: Remove or limit public contact details; use an alias email.
3. [High 40] Social: Employer and job title on a professional profile (S2 D5 E4)
   Source: https://linkedin.example/in/krishna-rao | Found: 2026-11-01
   Fix: Tighten privacy settings; remove old posts and location tags.
4. [High 36] Social: Public photo with a location tag (S3 D4 E3)
   Source: https://social.example/krishna/photo1 | Found: 2026-11-01
   Fix: Tighten privacy settings; remove old posts and location tags.
5. [Medium 27] Technical: Old code repo with commit email (S3 D3 E3)
   Source: https://code.example/krishna_sec22/project | Found: 2026-11-01
   Fix: Remove exposed services or secrets; rotate keys.
6. [Medium 16] Accounts: Username visible on a public forum (S2 D4 E2)
   Source: https://forum.example.com/u/krishna_sec22 | Found: 2026-11-01
   Fix: Make the profile private or delete unused accounts.

## 30/60/90 plan
30 days: fix Critical and High items (passwords, 2FA, opt-outs).
60 days: tighten privacy settings and remove old accounts.
90 days: re-scan and compare the exposure index.
