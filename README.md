# windstorminstitute.org

The public website for **The Windstorm Institute** — independent research at the intersection of information theory, molecular biology, and artificial intelligence.

Live site: [windstorminstitute.org](https://windstorminstitute.org)

## Structure

```
index.html              — Homepage: research arc, publications, reading order
articles/               — Long-form article version of each paper
  fons-constraint.html         (Paper 1)
  receiver-limited-floor.html  (Paper 2)
  throughput-basin.html        (Paper 3)
  serial-decoding-basin.html   (Paper 4)
  dissipative-decoder.html     (Paper 5)
  inherited-constraint.html    (Paper 6)
  throughput-basin-origin.html (Paper 7)
  vision-basin.html            (Paper 8)
  hardware-basin.html          (Paper 9)
  speed-limit-of-thought.html  (Series overview)
assets/
  images/               — Publication figures and hero art
  documents/            — Locally-hosted paper PDFs (select papers)
```

## Publishing model

Each scientific paper is published in three surfaces:

1. **Institute repo** — `github.com/Windstorm-Institute/<paper-slug>` — the canonical paper PDF, submission drafts (AAP, arXiv, Entropy, RSIF formats), the article HTML, LICENSE, and the Grand Slam Supplementary Materials where applicable.
2. **Labs repo** — `github.com/Windstorm-Labs/<paper-slug>` — experimental code, data, and plots.
3. **This website** — the long-form article (`articles/<paper-slug>.html`), plus arc-node and pub-card entries on the homepage.

Zenodo archival DOIs are issued for Papers 1–8 (Paper 8 v2.2: [10.5281/zenodo.19672827](https://doi.org/10.5281/zenodo.19672827)). Paper 9 is currently a preprint; DOI pending.

## Related repositories

- [Windstorm-Institute](https://github.com/Windstorm-Institute) — paper publication repos
- [Windstorm-Labs](https://github.com/Windstorm-Labs) — experimental code and data repos

## License

Website content: CC BY 4.0. See individual paper repos for paper and code licenses.
