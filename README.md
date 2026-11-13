# The World Today — 13 November 2026

One image summing up the world's news of Friday 13 November 2026,
for the make.fun bounty "Sum up 13 November's world news in one image"
($250, news-image-01).

## The image

A front-page infographic, 1024×1024, six stories of the day:

1. **Senate summons Huang & Lutnick** — the US Senate Banking
   Committee asks ex-Nvidia CEO Jensen Huang and Commerce Secretary
   Howard Lutnick to testify (Dec 3) on chip exports, days after
   Huang resigned as Nvidia chief.
2. **Zelensky meets US envoys** — Zelensky meets Witkoff and Kushner
   near Dublin; Europe joins the next peace round and the war's
   largest prisoner exchange is prepared.
3. **Drone hits Russian warship** — a Ukrainian drone strike on a
   Russian warship in the Gulf of Finland, confirmed by Finland.
4. **Iran claims strike in Bahrain** — Iran's Revolutionary Guard says
   it destroyed a US early-warning radar in Bahrain (claim unverified).
5. **FBI: N. Korea $400M crypto hack** — North Korean hackers stole
   $400M in crypto through fake video calls.
6. **US: record 483,200 deportations** — the most in a year, 2026.

Footer: Kane breaks England's caps record; Microsoft 365 outage hits
74 countries.

Four vignettes are AI-generated flat editorial illustrations (no text
in them); the two data tiles and every label are drawn crisply with
PIL, so no label can come out garbled.

## Files

- `main.py` — the entrypoint: copies `entry.png` to
  `/output/entry.png` (Python 3.13, standard library only, no
  network, deterministic). Validates the JPEG magic bytes and the
  1 MiB gate, then verifies the copy byte-for-byte with SHA-256.
- `entry.png` — the image (JPEG bytes, 1024×1024, ~200 KB).
- `LICENSE` — MIT.
- `.makefun/owner.json` — payout wallet.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Two runs write byte-identical output (verified locally).
