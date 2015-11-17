# Guardian comments scraper

Scrapes comments from guardian articles and outputs them to JSON or CSV formats.

Requires python and `BeautifulSoup` 4.x (`pip install beautifulsoup4`)

## Usage
```
python scrape.py <url>
```

With format specified (defaults to json)
```
python scrape.py <url> -o csv
```

With a list of links (one per line)
```
python scrape.py <file.txt>
```


