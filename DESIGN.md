# Phoebe sticker notebook

A fresh visual theme based on the chibi Phoebe front/side/back references supplied by the owner. The new waving-at-a-laptop sticker was generated with the built-in image tool. It is fan art, not official artwork. Phoebe / Wuthering Waves belong to KURO GAMES. The supplied reference images retain their original authorship; they are not redistributed here or claimed as our work.

Cream graph paper, periwinkle notes, lavender accents, rounded typography and washi tape replace the previous cathedral theme. Light and dark variants share the same layout. Text, decorations, dividers and statistic cards are authored in SVG; the generated sticker is embedded with transparency.

The source section sequence still follows snooze26h/snooze26h: hero, short about, stats and streak cards, contribution snake, footer. Historical cathedral artwork remains in Git history and the unused art files; it is not displayed.

## Maintenance

- Run `python scripts/build_art.py` to rebuild static SVGs.
- Run `python scripts/build_cards.py` with authenticated gh for public metrics.
- GitHub Actions runs daily at 01:23 UTC and publishes stats and Platane/snk contribution snakes atomically to the output branch.
- Public original repos and stars exclude forks and private repos. Streaks use the past-year GitHub calendar, UTC; an unfinished inactive current day does not break yesterday's streak.
- A failed refresh leaves the previous published assets intact. No personal access token is required.
