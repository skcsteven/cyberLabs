# Debian Install + Emergency Mode Debugging (Old Laptop Lab)

## Context

Picked up an old ASUS A42J laptop to use as a low-cost Linux lab machine for:

- TryHackMe / CTF practice  
- light virtualization  
- general Linux internals learning  

Specs:
- i5 (1st gen)
- 8GB RAM
- 120GB SSD + 500GB HDD

Goal:
- install Debian
- split storage:
  - SSD → `/`
  - HDD → `/home`

---

## Initial Setup

Installed Debian manually with custom partitioning:

- SSD:
  - `/` (ext4)
  - swap
- HDD:
  - `/home` (ext4)

System initially booted and worked normally.

---

## Issue #1 — Boot Failure (Emergency Mode)

After some normal usage, the system suddenly started booting into:

> “You are in emergency mode…”

Also saw:
- dependency failures for `/home`
- system dropping into maintenance shell

No config changes were made right before this happened.

Possible cause:
- physical movement / drop
- aging HDD hardware failure starting to surface

---

## Root Cause (Phase 1)

The system was failing to mount `/home` due to a bad entry in `/etc/fstab`.

- wrong or invalid UUID
- or disk not being properly detected at boot

This caused:
- mount failure
- systemd dependency failure
- emergency mode boot

---

## Issue #2 — Root Access / Password Confusion

Initially could not reliably access emergency shell.

Likely caused by:
- keyboard layout mismatch during boot (US vs non-US layout)

Solution:
- reset root password via GRUB

---

## Fix — Reset Root Password (GRUB Method)

1. Enter GRUB (`SHIFT` or `ESC`)
2. Select Debian entry → press `e`
3. Add at end of linux line: