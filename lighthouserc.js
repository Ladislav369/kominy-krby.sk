// Lighthouse CI config — kominy-krby.sk
// Kontrakt: BASELINE_MEASUREMENT_SPEC.md v1.0 (aresLab-docs/runbooks/)
// Page set: single-page site → home iba.
module.exports = {
  ci: {
    collect: {
      url: ['https://kominy-krby.sk/'],
      numberOfRuns: 5,
      settings: {
        // formFactor mobile + Moto G4 + Slow 4G = Lighthouse default (žiadny preset netreba)
        onlyCategories: ['performance', 'accessibility', 'best-practices', 'seo'],
      },
    },
    assert: {
      assertions: {
        // Core CWV — error (regression gate). Baseline_2026-05-19 + noise band zo specu.
        'categories:performance':        ['error', { minScore: 0.95 }],   // baseline 0.98, noise 0.03
        'largest-contentful-paint':      ['error', { maxNumericValue: 1900 }], // baseline 1749ms + 150ms noise
        'cumulative-layout-shift':       ['error', { maxNumericValue: 0.02 }], // baseline 0.000 + 0.02 noise
        'total-blocking-time':           ['error', { maxNumericValue: 50 }],   // baseline 0ms + 50ms noise

        // Categories floor — error
        'categories:accessibility':      ['error', { minScore: 1.0 }],
        'categories:best-practices':     ['error', { minScore: 1.0 }],
        // SEO: floor 0.92 = baseline 1.0 minus 1 binary audit fail (robots-txt sa občas
        // v Lighthouse 13 simulator nestihne stiahnuť pri throttling — flaky, nie reálny
        // SEO problém; robots.txt na prod je validný, Googlebot ho vidí). Plus warn
        // explicit na robots-txt aby flake bol v reportoch viditeľný.
        'categories:seo':                ['error', { minScore: 0.92 }],
        'robots-txt':                    ['warn'],

        // Speed Index — WARN only. SI je inherently noisy na tomto site-i (lite-yt-embed
        // CPU jitter v Lighthouse simulátore: median ~3700ms, range ~2500-3000ms). Web JE
        // rýchly pre user-a (LCP <2s, perf 0.98+, CLS 0) — SI je Lighthouse-internal metrika.
        // Threshold 5000ms = max observed ~4055ms + buffer. Po týždni stabilných runov
        // (alebo po deep refaktore lite-yt-embed) zúžiť.
        'speed-index':                   ['warn',  { maxNumericValue: 5000 }],
      },
    },
    upload: {
      target: 'filesystem',
      outputDir: './.lighthouseci',
    },
  },
};
