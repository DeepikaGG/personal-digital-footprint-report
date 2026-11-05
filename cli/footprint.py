#!/usr/bin/env python3
"""Personal Digital Footprint Report - command-line tool.

Passive and offline: it never contacts any website. It scores findings you
recorded yourself, redacts sensitive text, builds profile links for manual
review, and compares before/after results.
"""
import argparse
import json
import re
import sys
from datetime import date
from urllib.parse import quote

BANDS = [("Critical", 60), ("High", 30), ("Medium", 12), ("Low", 0)]
MAX_RISK = 125
FIXES = {
    "Breach": "Change the password everywhere it was used; enable an authenticator app or passkey.",
    "Contact info": "Remove or limit public contact details; use an alias email.",
    "Accounts": "Make the profile private or delete unused accounts.",
    "Social": "Tighten privacy settings; remove old posts and location tags.",
    "Physical": "Submit opt-outs; remove geotagged photos.",
    "Identity": "Request removal from people-search sites.",
    "Technical": "Remove exposed services or secrets; rotate keys.",
}
SITES = [
    ("GitHub", "https://github.com/"), ("Reddit", "https://www.reddit.com/user/"),
    ("X", "https://x.com/"), ("Instagram", "https://www.instagram.com/"),
    ("TikTok", "https://www.tiktok.com/@"), ("LinkedIn", "https://www.linkedin.com/in/"),
    ("YouTube", "https://www.youtube.com/@"), ("Medium", "https://medium.com/@"),
    ("Pinterest", "https://www.pinterest.com/"), ("Twitch", "https://www.twitch.tv/"),
    ("Telegram", "https://t.me/"),
]


def risk(f):
    """Risk = Sensitivity x Discoverability x Exploitability (each 1-5)."""
    return f["sensitivity"] * f["discoverability"] * f["exploitability"]


def rating(score):
    for name, minimum in BANDS:
        if score >= minimum:
            return name


def load(path):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if not data.get("consent"):
        sys.exit("Error: set \"consent\": true in the data file (own data or written consent only).")
    for i, f in enumerate(data.get("findings", []), 1):
        for key in ("sensitivity", "discoverability", "exploitability"):
            if not isinstance(f.get(key), int) or not 1 <= f[key] <= 5:
                sys.exit(f"Error: finding {i}: '{key}' must be a whole number from 1 to 5.")
    return data


def summarise(findings):
    counts = {name: 0 for name, _ in BANDS}
    total = 0
    for f in findings:
        s = risk(f)
        counts[rating(s)] += 1
        total += s
    n = len(findings)
    index = round(total / (n * MAX_RISK) * 100) if n else 0
    return {"count": n, "exposure": index, "by_rating": counts}


def build_report(data):
    fs = sorted(data["findings"], key=risk, reverse=True)
    s = summarise(fs)
    c = s["by_rating"]
    lines = [
        "# Personal Digital Footprint Report", "",
        f"Subject: {data.get('subject', 'Subject A')}",
        f"Date: {date.today().isoformat()}",
        "Method: passive OSINT, public sources only, consent confirmed", "",
        "## Summary",
        f"Findings: {s['count']} | Critical: {c['Critical']} | High: {c['High']} | "
        f"Medium: {c['Medium']} | Low: {c['Low']}",
        f"Exposure index: {s['exposure']}/100", "",
        "## Findings (highest risk first)",
    ]
    for i, f in enumerate(fs, 1):
        r = risk(f)
        lines += [
            f"{i}. [{rating(r)} {r}] {f['category']}: {f['description']} "
            f"(S{f['sensitivity']} D{f['discoverability']} E{f['exploitability']})",
            f"   Source: {f.get('source_url', 'n/a')} | Found: {f.get('date', 'n/a')}",
            f"   Fix: {FIXES.get(f['category'], 'Reduce public visibility.')}",
        ]
    lines += ["", "## 30/60/90 plan",
              "30 days: fix Critical and High items (passwords, 2FA, opt-outs).",
              "60 days: tighten privacy settings and remove old accounts.",
              "90 days: re-scan and compare the exposure index."]
    return "\n".join(lines) + "\n"


def redact(text, extra=()):
    text = re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", "[EMAIL]", text)
    text = re.sub(r"\b(?:\d[ -]?){13,16}\b", "[CARD]", text)
    text = re.sub(r"\b\d{1,3}(?:\.\d{1,3}){3}\b", "[IP]", text)
    text = re.sub(r"(\+?\d[\d\s().-]{7,}\d)", "[PHONE]", text)
    text = re.sub(r"\b\d{1,5}\s+[A-Za-z]+(?:\s[A-Za-z]+)*\s(?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Drive|Dr|Boulevard|Blvd)\b",
                  "[ADDRESS]", text, flags=re.I)
    for word in extra:
        if word.strip():
            text = re.sub(re.escape(word.strip()), "[HIDDEN]", text, flags=re.I)
    return text


def cmd_score(a):
    data = load(a.file)
    for f in sorted(data["findings"], key=risk, reverse=True):
        r = risk(f)
        print(f"{r:>4}  {rating(r):<8} {f['category']:<13} {f['description']}")
    s = summarise(data["findings"])
    print(f"\nFindings: {s['count']}  Exposure: {s['exposure']}/100  {s['by_rating']}")


def cmd_report(a):
    out = build_report(load(a.file))
    if a.output:
        with open(a.output, "w", encoding="utf-8") as fh:
            fh.write(out)
        print(f"Report written to {a.output}")
    else:
        print(out)


def cmd_redact(a):
    text = open(a.file, encoding="utf-8").read() if a.file else sys.stdin.read()
    print(redact(text, a.hide.split(",") if a.hide else ()))


def cmd_usernames(a):
    for name, base in SITES:
        print(f"{name:<10} {base}{quote(a.username)}")
    print("\nOpen each link yourself and note what is publicly visible. Nothing is fetched.")


def cmd_compare(a):
    b, af = summarise(load(a.before)["findings"]), summarise(load(a.after)["findings"])
    print(f"{'Measure':<10} {'Before':>8} {'After':>8}")
    print(f"{'Exposure':<10} {b['exposure']:>8} {af['exposure']:>8}")
    for name, _ in BANDS:
        print(f"{name:<10} {b['by_rating'][name]:>8} {af['by_rating'][name]:>8}")
    print(f"\nExposure change: {b['exposure'] - af['exposure']} points lower")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("score", help="score findings from a JSON file"); s.add_argument("file"); s.set_defaults(fn=cmd_score)
    s = sub.add_parser("report", help="write a Markdown report"); s.add_argument("file"); s.add_argument("-o", "--output"); s.set_defaults(fn=cmd_report)
    s = sub.add_parser("redact", help="mask sensitive text"); s.add_argument("file", nargs="?"); s.add_argument("--hide", help="comma-separated extra words"); s.set_defaults(fn=cmd_redact)
    s = sub.add_parser("usernames", help="profile links to review manually"); s.add_argument("username"); s.set_defaults(fn=cmd_usernames)
    s = sub.add_parser("compare", help="before/after comparison"); s.add_argument("before"); s.add_argument("after"); s.set_defaults(fn=cmd_compare)
    a = p.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
