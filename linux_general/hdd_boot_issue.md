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
  - /home (ext4)  ← important
- HDD:
  - unused / secondary storage

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
- filesystem corruption
- aging storage

---

## Root Cause (Phase 1)

The system failed to mount /home due to an issue in `/etc/fstab`.

- incorrect or mismatched UUID
- mount failure triggered systemd dependency failure

Result:
- system entered emergency mode during boot

---

## Issue #2 — Root Access / Password Confusion

Initial access to emergency mode was unreliable.

Likely cause:
- keyboard layout mismatch during early boot (US vs non-US layout)

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

## Issue #3 — Filesystem Errors on SSD

After further investigation:

- /home was actually located on /dev/sda (SSD)
- not the HDD as initially assumed

Running:

dmesg | grep -i error

showed read / I/O related errors.

---

## Recovery — Filesystem Repair

Ran filesystem check on SSD partition:

fsck /dev/sdaX

(accepted all fixes)

After reboot:
- system booted successfully
- no emergency mode

---

## Verification

Ran:

lsblk -f  
df -h  

Results:
- partitions mounted correctly
- /home accessible
- no immediate mount failures

---

## Root Cause (Final)

Most likely:

- filesystem corruption on SSD partition containing /home
- possibly triggered by:
  - sudden power issue
  - improper shutdown
  - physical movement (less likely than HDD, but possible)

Important observation:
- system worked normally before
- issue appeared suddenly without config changes

---

## Final Setup

- system stable after fsck repair
- /home functioning normally
- HDD remains secondary / unused

Note:
- long-term SSD health still worth monitoring

---

## Key Takeaways

### 1. /etc/fstab can break boot
- wrong UUID or failed mount = emergency mode
- always validate mounts with:
  mount -a

---

### 2. Emergency mode is often a mount or filesystem issue
Not necessarily a broken OS.

---

### 3. Always verify assumptions about disk layout

Initial assumption:
- /home was on HDD

Actual:
- /home was on SSD

Misreading disk layout can lead to wrong debugging path.

---

### 4. fsck can recover a system quickly

- repaired filesystem corruption
- restored normal boot

However:
- does NOT guarantee long-term disk health

---

### 5. Distinguish between layers of failure

- fstab → configuration
- fsck → filesystem corruption
- I/O errors → potential hardware issue

---

## Commands Used

lsblk -f  
blkid  
journalctl -xb  
dmesg | grep -i error  
mount -a  
fsck /dev/sdaX  

---

## Reflection

This was a hands-on experience debugging:

- Linux boot failures
- fstab configuration issues
- filesystem corruption and repair
- incorrect assumptions about disk layout

Key lesson:

Accurate system understanding (what is mounted where) is critical before attempting fixes. Misidentifying the disk layout can lead to chasing the wrong root cause.