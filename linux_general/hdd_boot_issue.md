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
  - SSD → /
  - HDD → /home

---

## Initial Setup

Installed Debian manually with custom partitioning:

- SSD:
  - / (ext4)
  - swap
- HDD:
  - /home (ext4)

System initially booted and worked normally.

---

## Issue #1 — Boot Failure (Emergency Mode)

After normal usage, the system suddenly started booting into:

“Emergency mode”

Also observed:
- dependency failures for /home
- system dropping into maintenance shell

No config changes were made right before this happened.

Possible causes:
- physical movement or drop
- aging HDD starting to fail

---

## Root Cause (Phase 1)

The system was failing to mount /home due to a bad entry in /etc/fstab.

- incorrect or invalid UUID
- or disk not properly detected at boot

This caused:
- mount failure
- systemd dependency failure
- emergency mode boot

---

## Issue #2 — Root Access / Password Confusion

Initial access to emergency mode was unreliable.

Likely cause:
- keyboard layout mismatch during boot (US vs non-US layout)

Solution:
- reset root password via GRUB

---

## Fix — Reset Root Password (GRUB Method)

1. Enter GRUB (SHIFT or ESC)
2. Select Debian entry → press e
3. Find linux line and append:
   init=/bin/bash
4. Boot with Ctrl + X
5. Remount filesystem:
   mount -o remount,rw /
6. Reset password:
   passwd

---

## Fix — Temporary Boot Recovery

Edit /etc/fstab:

nano /etc/fstab

Comment out /home line:

#UUID=xxxx /home ext4 defaults 0 2

Reboot system.

Result:
- system boots normally again

---

## Issue #3 — HDD Failure

After attempting to restore /home:

- reformatted /dev/sdb1
- ran mount -a

Errors appeared:
- read block errors
- I/O errors in logs

Confirmed with:

dmesg | grep -i error

---

## Root Cause (Final)

The HDD is physically failing:

- bad sectors
- read errors under load
- unstable disk behavior

Important observation:
- system worked normally before
- issue appeared suddenly
- likely triggered by physical movement or existing wear

---

## Final Setup

- HDD removed from boot usage
- system running entirely on SSD:
  - /
  - /home

System now stable and boots normally.

---

## Key Takeaways

### 1. /etc/fstab can break boot
- wrong UUID = emergency mode
- always validate mounts

### 2. Emergency mode is usually a mount issue
Not necessarily a broken OS.

### 3. Config vs hardware matters

- fstab issue → configuration problem
- I/O errors → hardware failure

### 4. Old hardware fails unpredictably
- works fine initially
- then fails suddenly due to degradation or physical shock

### 5. Keep early Linux setups simple
- SSD-only setups are more stable
- fewer moving parts = fewer failures

---

## Commands Used

lsblk -f
blkid
journalctl -xb
dmesg -i error
mount -a

---

## Reflection

This was one of the first hands-on experiences debugging:

- Linux boot failures
- filesystem mounting issues
- separation of software vs hardware faults

Key lesson:

Not all Linux issues are configuration problems — sometimes the hardware is the root cause.