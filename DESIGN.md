# Phoebe · a little light, a little code

This profile follows the section order of [snooze26h/snooze26h](https://github.com/snooze26h/snooze26h): hero, short about, statistics and streak cards, contribution snake, footer. The implementation and artwork are newly authored.

The visual reference is [Theater-ahyeon/phoebe-atelier](https://github.com/Theater-ahyeon/phoebe-atelier): moon ivory `#F7F5EE`, champagne gold `#D9C089`, luminous blue `#A9C6E8`, midnight blue `#101A3A`.

## Artwork

The illustrations in `assets/art` were generated with the built-in image tool using the owner's Phoebe skin images as references. They are unofficial fan art, not official promotional artwork. Phoebe and Wuthering Waves belong to KURO GAMES. Reference skin: CC BY-NC-SA 4.0; derived fan-art assets are shared under the same terms, subject to underlying character rights. See [the reference notice](https://github.com/Theater-ahyeon/phoebe-atelier/blob/main/phoebe-atelier/NOTICE).

The SVGs embed the JPEG art so GitHub's image renderer does not need to fetch external nested resources. Exact text is authored in SVG, not baked into generated art. Run `python scripts/build_art.py` after replacing the art.

## Live data

`Refresh Phoebe profile` runs daily at 01:23 UTC and can be dispatched manually. It writes only the generated `output` branch. README images reference this branch; no third-party live stats endpoint is needed.

- Repository count and stars: public, owned, non-fork repositories.
- Contributions: GitHub's past-year contribution calendar as visible to the workflow token.
- Current and longest streak: consecutive active UTC calendar dates in that same window; an unfinished inactive current day does not break yesterday's streak. Longest is not an all-time metric.
- Contribution snake: [Platane/snk](https://github.com/Platane/snk), with matching theme colors.
- `output/data.json` contains the snapshot and refresh timestamp.

No personal access token is required. If fetching data, rendering or validation fails, the workflow fails before publication, leaving the previous output intact.

Local maintenance: authenticate `gh`, run `python scripts/build_cards.py`. GitHub Actions generates both snake files and runs `python scripts/check_assets.py` before publishing.
