# TShark Challenge I: Teamwork — Lessons Learned

**Platform:** TryHackMe | **Category:** Network Forensics / PCAP Analysis

---

## Overview
Analyzed `teamwork.pcap` using TShark to extract credentials and artifacts from captured HTTP traffic. The challenge focused on identifying POST request data and understanding URL-encoded payloads.

---

## Key Commands Used

```bash
# Basic pcap read
tshark -r exercise-files/teamwork.pcap

# Export full output with hex/ASCII data to JSON
tshark -r teamwork.pcap -T json -x > output.json

# Extract HTTP file data from a specific frame
tshark -r teamwork.pcap -Y "frame.number == 202" -T fields -e http.file_data
```

## Findings

**Frame 202** contained a `POST /inc/login.php` request from `192.168.1.100 → 184.154.127.226`.

Extracted URL-encoded payload revealed credentials and a browser fingerprint:
- **Email:** `johnny5alive@gmail.com`
- **Password:** `johnny5alive`
- **Browser:** Mozilla Firefox v43 on Linux Desktop
- **Timezone:** Mon Apr 17 2017 22:00:35 GMT-0400 (EDT)
- **Resolution:** 1920x1080

---

## Lessons Learned

- **`-T fields -e http.file_data`** is the clean way to extract POST body content without the noise of `-V` verbose output.
- **URL decoding matters** — `%40` = `@`, `%3A` = `:`, `+` = space. Always decode before analyzing credentials or timestamps.
- **VirusTotal** can be used to look up suspicious IPs/domains found in traffic to check reputation and historical context.
- **Defanged notation** (`hxxp://`, `192[.]168[.]1[.]1`) is the standard safe way to share URLs and IPs in writeups to prevent accidental clicks or auto-linking.
- Filtering by `frame.number` is useful for drilling into a specific packet once identified from an initial broad sweep.
- Exporting to JSON (`-T json -x`) is helpful for programmatic analysis or reviewing hex dumps outside the terminal.

---

## Tools Used
- `tshark` — CLI packet analyzer
- VirusTotal — IP/URL reputation lookup
