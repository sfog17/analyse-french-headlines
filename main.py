from generate_worldcloud import plot_wordcloud, WEBSITES

CANDIDATES = [
    "mélenchon",
    "taubira",
    "hidalgo",
    "jadot",
    "macron",
    "pécresse",
    "le pen",
    "zemmour",
]

for site in WEBSITES:
    plot_wordcloud(website=site)
for candidate in CANDIDATES:
    plot_wordcloud(word=candidate)
