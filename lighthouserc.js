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
    upload: {
      target: 'filesystem',
      outputDir: './.lighthouseci',
    },
  },
};
