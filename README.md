# Corpus of traditional tunes in ABC format

This corpus, collected in April 2017, contains all of the notated tunes in the
[Traditional Tune Archive](http://tunearch.org/) that have a [theme code
index](http://tunearch.org/wiki/Theme_Code_Index).

## Caveats

Be warned that this list contains a non-trivial number of duplicates due to the
scraping algorithm, which performs a breadth-first traversal of all tunes by
theme code prefix. For example, a tune with the theme code prefix `115L` could be
scraped twice: once for `115` and again for `115L`. A tune with the theme code
prefix `1117bL` could be scraped three times, for each of: `1117`, `1117b`,
and `1117bL`.

## Running the scraper

```bash
cd tunearch-corpus
pip install -r requirements.txt
mkdir tune-files
python scrape.py
```

The scraper's speed is limited by the requests it makes against the Tune
Archive's API. The scraper takes approximately 12 hours to run, but it saves
progress to disk frequently, and can be killed and restarted without losing
progress.
