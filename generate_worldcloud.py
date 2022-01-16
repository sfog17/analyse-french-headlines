import csv
import re
from collections import Counter
from pathlib import Path
from typing import List, Literal, Optional, get_args
import nltk
from wordcloud import WordCloud

nltk.download("stopwords")

Website = Literal[
    "lemonde",
    "lefigaro",
    "francetvinfo",
    "vingtminutes",
    "leparisien",
    "ouestfrance",
    "bfmtv",
    "mediapart",
    "cnews",
]
WEBSITES = get_args(Website)


def filter_articles(
    regex_pattern: Optional[re.Pattern] = None, website: Optional[Website] = None
) -> List[str]:
    articles = set()
    data_dir = (
        Path(__file__)
        .parent.parent.joinpath("scraper-french-headlines")
        .joinpath("data")
    )
    file_pattern = f"*{website}.csv" if website else "*.csv"
    for file in data_dir.glob(file_pattern):
        with open(file, encoding="utf-8") as f_in:
            csv_reader = csv.DictReader(f_in)
            for line in csv_reader:
                if regex_pattern:
                    if regex_pattern.search(line["title"]):
                        articles.add(line["title"])
                else:
                    articles.add(line["title"])
    return articles


def generate_frequencies(articles: List[str]) -> Counter:
    text = " ".join(articles)
    punctuation = (":", ",", ".", "«", "»")
    for p in punctuation:
        text = text.replace(p, " ")
    counter = Counter(text.strip().lower().split())
    stopwords = nltk.corpus.stopwords.words("french")
    for word in stopwords:
        counter.pop(word, None)
    return counter


def plot_wordcloud(word: Optional[str] = None, website: Optional[Website] = None):
    if word:
        print(f"Generating word cloud for candidatee {word}")
        regex_pattern = re.compile(word, re.IGNORECASE)
    else:
        regex_pattern = None
    freq = generate_frequencies(filter_articles(regex_pattern, website))
    wordcloud = WordCloud().generate_from_frequencies(freq)
    imagefile = wordcloud.to_image()
    with imagefile:
        # Name file
        outfile = "wordcloud"
        if website:
            outfile += f"_{website}"
        else:
            outfile += f"_all"
        if word:
            outfile += f"_{word.replace(' ', '-')}"
        outfile += ".png"
        imagefile.save(Path(outfile), format="png", optimize=True)
