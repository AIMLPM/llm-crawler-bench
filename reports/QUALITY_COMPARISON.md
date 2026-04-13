# Extraction Quality Comparison
<!-- style: v2, 2026-04-12 -->

markcrawl produces the cleanest output for RAG: 100% content signal with only
12 words of preamble per page, compared to 224-348 for other tools. Its recall
is lower (87% vs 97%) because it strips nav/footer content — a trade-off that
favors RAG where fewer junk tokens per chunk means better retrieval precision.

**Run:** `run_20260412_195003` | **Sites:** 4 | **Tools:** 7

## Methodology

Four automated quality metrics — no LLM or human review needed:

1. **Junk phrases** — known boilerplate strings (nav, footer, breadcrumbs) found in output
2. **Preamble [1]** — average words per page appearing *before* the first heading.
   Nav chrome (version selectors, language pickers, prev/next links) lives here.
   A tool with a high preamble count is injecting site chrome into every chunk.
3. **Cross-page repeat rate** — fraction of sentences that appear on >50% of pages.
   Real content appears on at most a few pages; nav text repeats everywhere.
   High repeat rate = nav boilerplate polluting every chunk in the RAG index.
4. **Cross-tool consensus** — precision (how much output is agreed real content?)
   and recall (how much agreed content did this tool capture?).

> **Why preamble + repeat rate matter for RAG:** A tool that embeds 200 words of
> nav chrome before each article degrades retrieval in two ways: (1) chunks contain
> irrelevant tokens that dilute semantic similarity, and (2) the same nav sentences
> match queries on every page, flooding results with false positives.

## Summary: RAG readiness at a glance

For RAG pipelines, **clean output matters more than comprehensive output.**
A tool that includes 1,000 words of nav chrome per page pollutes every
chunk in the vector index, degrading retrieval for every query.

| Tool | Content signal | Preamble [1] | Repeat rate | Junk/page | Precision | Recall |
|---|---|---|---|---|---|---|
| **markcrawl** | **100%** | **12** | **0%** | **0.8** | **98%** | **87%** |
| crawl4ai | 90% | 348 [!] | 1% | 4.5 | 100% | 90% |
| crawl4ai-raw | 90% | 348 [!] | 1% | 4.5 | 100% | 90% |
| scrapy+md | 94% | 224 [!] | 1% | 4.3 | 100% | 92% |
| crawlee | 93% | 252 [!] | 1% | 5.1 | 100% | 97% |
| colly+md | 93% | 234 [!] | 1% | 5.1 | 100% | 97% |
| playwright | 93% | 251 [!] | 1% | 5.1 | 100% | 97% |
| firecrawl | — | — | — | — | — | — |

**[1]** Avg words per page before the first heading (nav chrome).


**Key takeaway:** markcrawl achieves 100% content signal with only 12 words of preamble per page — compared to 348 for crawl4ai-raw. Its recall is lower (87% vs 97%) because it strips nav, footer, and sponsor content that other tools include. For RAG use cases, this trade-off typically favors cleaner output: fewer junk tokens per chunk means better embedding quality and retrieval precision.

> **Content signal** = percentage of output that is content (not preamble nav chrome).
> Higher is better. A tool with 100% content signal has zero nav/header pollution.
> **Repeat rate** = fraction of phrases appearing on >50% of pages (boilerplate).
> **Junk/page** = known boilerplate phrases detected per page.

## quotes-toscrape

| Tool | Avg words | Preamble [1] | Repeat rate | Junk found | Headings | Code blocks | Precision | Recall |
|---|---|---|---|---|---|---|---|---|
| **markcrawl** | **214** | **15** | **0%** | **0** | **0.9** | **0.0** | **100%** | **100%** |
| crawl4ai | 242 | 0 | 2% | 1 | 2.7 | 0.0 | 100% | 100% |
| crawl4ai-raw | 242 | 0 | 2% | 1 | 2.7 | 0.0 | 100% | 100% |
| scrapy+md | 242 | 0 | 2% | 1 | 2.7 | 0.0 | 100% | 100% |
| crawlee | 245 | 3 | 2% | 1 | 2.7 | 0.0 | 100% | 100% |
| colly+md | 245 | 3 | 2% | 1 | 2.7 | 0.0 | 100% | 100% |
| playwright | 245 | 3 | 2% | 1 | 2.7 | 0.0 | 100% | 100% |
| firecrawl | — | — | — | — | — | — | — | — |

**[1]** Avg words per page before the first heading (nav chrome). **[!]** = likely nav/boilerplate problem (preamble >50 or repeat rate >20%).

<details>
<summary>Sample output — first 40 lines of <code>quotes.toscrape.com/tag/friendship</code></summary>

This shows what each tool outputs at the *top* of the same page.
Nav boilerplate appears here before the real content starts.

**markcrawl**
```
### Viewing tag: [friendship](/tag/friendship/page/1/)

“It is not a lack of love, but a lack of friendship that makes unhappy marriages.”
by Friedrich Nietzsche
[(about)](/author/Friedrich-Nietzsche)

“Good friends, good books, and a sleepy conscience: this is the ideal life.”
by Mark Twain
[(about)](/author/Mark-Twain)

“The truth is, everyone is going to hurt you. You just got to find the ones worth suffering for.”
by Bob Marley
[(about)](/author/Bob-Marley)

“There is nothing I would not do for those who are really my friends. I have no notion of loving people by halves, it is not my nature.”
by Jane Austen
[(about)](/author/Jane-Austen)

“If I had a flower for every time I thought of you...I could walk through my garden forever.”
by Alfred Tennyson
[(about)](/author/Alfred-Tennyson)
```

**crawl4ai**
```
#  [Quotes to Scrape](https://quotes.toscrape.com/)
[Login](https://quotes.toscrape.com/login)
### Viewing tag: [friendship](https://quotes.toscrape.com/tag/friendship/page/1/)
“It is not a lack of love, but a lack of friendship that makes unhappy marriages.” by Friedrich Nietzsche [(about)](https://quotes.toscrape.com/author/Friedrich-Nietzsche)
Tags: [friendship](https://quotes.toscrape.com/tag/friendship/page/1/) [lack-of-friendship](https://quotes.toscrape.com/tag/lack-of-friendship/page/1/) [lack-of-love](https://quotes.toscrape.com/tag/lack-of-love/page/1/) [love](https://quotes.toscrape.com/tag/love/page/1/) [marriage](https://quotes.toscrape.com/tag/marriage/page/1/) [unhappy-marriage](https://quotes.toscrape.com/tag/unhappy-marriage/page/1/)
“Good friends, good books, and a sleepy conscience: this is the ideal life.” by Mark Twain [(about)](https://quotes.toscrape.com/author/Mark-Twain)
Tags: [books](https://quotes.toscrape.com/tag/books/page/1/) [contentment](https://quotes.toscrape.com/tag/contentment/page/1/) [friends](https://quotes.toscrape.com/tag/friends/page/1/) [friendship](https://quotes.toscrape.com/tag/friendship/page/1/) [life](https://quotes.toscrape.com/tag/life/page/1/)
“The truth is, everyone is going to hurt you. You just got to find the ones worth suffering for.” by Bob Marley [(about)](https://quotes.toscrape.com/author/Bob-Marley)
Tags: [friendship](https://quotes.toscrape.com/tag/friendship/page/1/)
“There is nothing I would not do for those who are really my friends. I have no notion of loving people by halves, it is not my nature.” by Jane Austen [(about)](https://quotes.toscrape.com/author/Jane-Austen)
Tags: [friendship](https://quotes.toscrape.com/tag/friendship/page/1/) [love](https://quotes.toscrape.com/tag/love/page/1/)
“If I had a flower for every time I thought of you...I could walk through my garden forever.” by Alfred Tennyson [(about)](https://quotes.toscrape.com/author/Alfred-Tennyson)
Tags: [friendship](https://quotes.toscrape.com/tag/friendship/page/1/) [love](https://quotes.toscrape.com/tag/love/page/1/)
## Top Ten tags
[love](https://quotes.toscrape.com/tag/love/) [inspirational](https://quotes.toscrape.com/tag/inspirational/) [life](https://quotes.toscrape.com/tag/life/) [humor](https://quotes.toscrape.com/tag/humor/) [books](https://quotes.toscrape.com/tag/books/) [reading](https://quotes.toscrape.com/tag/reading/) [friendship](https://quotes.toscrape.com/tag/friendship/) [friends](https://quotes.toscrape.com/tag/friends/) [truth](https://quotes.toscrape.com/tag/truth/) [simile](https://quotes.toscrape.com/tag/simile/)
Quotes by: [GoodReads.com](https://www.goodreads.com/quotes)
Made with ❤ by [Zyte](https://www.zyte.com)
```

**crawl4ai-raw**
```
#  [Quotes to Scrape](https://quotes.toscrape.com/)
[Login](https://quotes.toscrape.com/login)
### Viewing tag: [friendship](https://quotes.toscrape.com/tag/friendship/page/1/)
“It is not a lack of love, but a lack of friendship that makes unhappy marriages.” by Friedrich Nietzsche [(about)](https://quotes.toscrape.com/author/Friedrich-Nietzsche)
Tags: [friendship](https://quotes.toscrape.com/tag/friendship/page/1/) [lack-of-friendship](https://quotes.toscrape.com/tag/lack-of-friendship/page/1/) [lack-of-love](https://quotes.toscrape.com/tag/lack-of-love/page/1/) [love](https://quotes.toscrape.com/tag/love/page/1/) [marriage](https://quotes.toscrape.com/tag/marriage/page/1/) [unhappy-marriage](https://quotes.toscrape.com/tag/unhappy-marriage/page/1/)
“Good friends, good books, and a sleepy conscience: this is the ideal life.” by Mark Twain [(about)](https://quotes.toscrape.com/author/Mark-Twain)
Tags: [books](https://quotes.toscrape.com/tag/books/page/1/) [contentment](https://quotes.toscrape.com/tag/contentment/page/1/) [friends](https://quotes.toscrape.com/tag/friends/page/1/) [friendship](https://quotes.toscrape.com/tag/friendship/page/1/) [life](https://quotes.toscrape.com/tag/life/page/1/)
“The truth is, everyone is going to hurt you. You just got to find the ones worth suffering for.” by Bob Marley [(about)](https://quotes.toscrape.com/author/Bob-Marley)
Tags: [friendship](https://quotes.toscrape.com/tag/friendship/page/1/)
“There is nothing I would not do for those who are really my friends. I have no notion of loving people by halves, it is not my nature.” by Jane Austen [(about)](https://quotes.toscrape.com/author/Jane-Austen)
Tags: [friendship](https://quotes.toscrape.com/tag/friendship/page/1/) [love](https://quotes.toscrape.com/tag/love/page/1/)
“If I had a flower for every time I thought of you...I could walk through my garden forever.” by Alfred Tennyson [(about)](https://quotes.toscrape.com/author/Alfred-Tennyson)
Tags: [friendship](https://quotes.toscrape.com/tag/friendship/page/1/) [love](https://quotes.toscrape.com/tag/love/page/1/)
## Top Ten tags
[love](https://quotes.toscrape.com/tag/love/) [inspirational](https://quotes.toscrape.com/tag/inspirational/) [life](https://quotes.toscrape.com/tag/life/) [humor](https://quotes.toscrape.com/tag/humor/) [books](https://quotes.toscrape.com/tag/books/) [reading](https://quotes.toscrape.com/tag/reading/) [friendship](https://quotes.toscrape.com/tag/friendship/) [friends](https://quotes.toscrape.com/tag/friends/) [truth](https://quotes.toscrape.com/tag/truth/) [simile](https://quotes.toscrape.com/tag/simile/)
Quotes by: [GoodReads.com](https://www.goodreads.com/quotes)
Made with ❤ by [Zyte](https://www.zyte.com)
```

**scrapy+md**
```
# [Quotes to Scrape](/)

[Login](/login)

### Viewing tag: [friendship](/tag/friendship/page/1/)

“It is not a lack of love, but a lack of friendship that makes unhappy marriages.”
by Friedrich Nietzsche
[(about)](/author/Friedrich-Nietzsche)

Tags:
[friendship](/tag/friendship/page/1/)
[lack-of-friendship](/tag/lack-of-friendship/page/1/)
[lack-of-love](/tag/lack-of-love/page/1/)
[love](/tag/love/page/1/)
[marriage](/tag/marriage/page/1/)
[unhappy-marriage](/tag/unhappy-marriage/page/1/)

“Good friends, good books, and a sleepy conscience: this is the ideal life.”
by Mark Twain
[(about)](/author/Mark-Twain)

Tags:
[books](/tag/books/page/1/)
[contentment](/tag/contentment/page/1/)
[friends](/tag/friends/page/1/)
[friendship](/tag/friendship/page/1/)
[life](/tag/life/page/1/)

“The truth is, everyone is going to hurt you. You just got to find the ones worth suffering for.”
by Bob Marley
[(about)](/author/Bob-Marley)

Tags:
[friendship](/tag/friendship/page/1/)

“There is nothing I would not do for those who are really my friends. I have no notion of loving people by halves, it is not my nature.”
by Jane Austen
[(about)](/author/Jane-Austen)
```

**crawlee**
```
Quotes to Scrape



# [Quotes to Scrape](/)

[Login](/login)

### Viewing tag: [friendship](/tag/friendship/page/1/)

“It is not a lack of love, but a lack of friendship that makes unhappy marriages.”
by Friedrich Nietzsche
[(about)](/author/Friedrich-Nietzsche)

Tags:
[friendship](/tag/friendship/page/1/)
[lack-of-friendship](/tag/lack-of-friendship/page/1/)
[lack-of-love](/tag/lack-of-love/page/1/)
[love](/tag/love/page/1/)
[marriage](/tag/marriage/page/1/)
[unhappy-marriage](/tag/unhappy-marriage/page/1/)

“Good friends, good books, and a sleepy conscience: this is the ideal life.”
by Mark Twain
[(about)](/author/Mark-Twain)

Tags:
[books](/tag/books/page/1/)
[contentment](/tag/contentment/page/1/)
[friends](/tag/friends/page/1/)
[friendship](/tag/friendship/page/1/)
[life](/tag/life/page/1/)

“The truth is, everyone is going to hurt you. You just got to find the ones worth suffering for.”
by Bob Marley
[(about)](/author/Bob-Marley)

Tags:
[friendship](/tag/friendship/page/1/)
```

**colly+md**
```
Quotes to Scrape



# [Quotes to Scrape](/)

[Login](/login)

### Viewing tag: [friendship](/tag/friendship/page/1/)

“It is not a lack of love, but a lack of friendship that makes unhappy marriages.”
by Friedrich Nietzsche
[(about)](/author/Friedrich-Nietzsche)

Tags:
[friendship](/tag/friendship/page/1/)
[lack-of-friendship](/tag/lack-of-friendship/page/1/)
[lack-of-love](/tag/lack-of-love/page/1/)
[love](/tag/love/page/1/)
[marriage](/tag/marriage/page/1/)
[unhappy-marriage](/tag/unhappy-marriage/page/1/)

“Good friends, good books, and a sleepy conscience: this is the ideal life.”
by Mark Twain
[(about)](/author/Mark-Twain)

Tags:
[books](/tag/books/page/1/)
[contentment](/tag/contentment/page/1/)
[friends](/tag/friends/page/1/)
[friendship](/tag/friendship/page/1/)
[life](/tag/life/page/1/)

“The truth is, everyone is going to hurt you. You just got to find the ones worth suffering for.”
by Bob Marley
[(about)](/author/Bob-Marley)

Tags:
[friendship](/tag/friendship/page/1/)
```

**playwright**
```
Quotes to Scrape



# [Quotes to Scrape](/)

[Login](/login)

### Viewing tag: [friendship](/tag/friendship/page/1/)

“It is not a lack of love, but a lack of friendship that makes unhappy marriages.”
by Friedrich Nietzsche
[(about)](/author/Friedrich-Nietzsche)

Tags:
[friendship](/tag/friendship/page/1/)
[lack-of-friendship](/tag/lack-of-friendship/page/1/)
[lack-of-love](/tag/lack-of-love/page/1/)
[love](/tag/love/page/1/)
[marriage](/tag/marriage/page/1/)
[unhappy-marriage](/tag/unhappy-marriage/page/1/)

“Good friends, good books, and a sleepy conscience: this is the ideal life.”
by Mark Twain
[(about)](/author/Mark-Twain)

Tags:
[books](/tag/books/page/1/)
[contentment](/tag/contentment/page/1/)
[friends](/tag/friends/page/1/)
[friendship](/tag/friendship/page/1/)
[life](/tag/life/page/1/)

“The truth is, everyone is going to hurt you. You just got to find the ones worth suffering for.”
by Bob Marley
[(about)](/author/Bob-Marley)

Tags:
[friendship](/tag/friendship/page/1/)
```

**firecrawl** — no output for this URL

</details>

<details>
<summary>Per-page word counts and preamble [1]</summary>

| URL | markcrawl words / preamble [1] | crawl4ai words / preamble [1] | crawl4ai-raw words / preamble [1] | scrapy+md words / preamble [1] | crawlee words / preamble [1] | colly+md words / preamble [1] | playwright words / preamble [1] | firecrawl words / preamble [1] |
|---|---|---|---|---|---|---|---|---|
| quotes.toscrape.com | 212 / 212 | 282 / 0 | 282 / 0 | 282 / 0 | 285 / 3 | 285 / 3 | 285 / 3 | — |
| quotes.toscrape.com/author/Albert-Einstein | 616 / 0 | 629 / 0 | 629 / 0 | 629 / 0 | 632 / 3 | 632 / 3 | 632 / 3 | — |
| quotes.toscrape.com/author/Eleanor-Roosevelt | 237 / 0 | 250 / 0 | 250 / 0 | 250 / 0 | 253 / 3 | 253 / 3 | 253 / 3 | — |
| quotes.toscrape.com/author/Steve-Martin | 134 / 0 | 147 / 0 | 147 / 0 | 147 / 0 | 150 / 3 | 150 / 3 | 150 / 3 | — |
| quotes.toscrape.com/tag/abilities/page/1 | 24 / 0 | 54 / 0 | 54 / 0 | 54 / 0 | 57 / 3 | 57 / 3 | 57 / 3 | — |
| quotes.toscrape.com/tag/aliteracy/page/1 | 27 / 0 | 59 / 0 | 59 / 0 | 59 / 0 | 62 / 3 | 62 / 3 | 62 / 3 | — |
| quotes.toscrape.com/tag/books/page/1 | 262 / 0 | 340 / 0 | 340 / 0 | 340 / 0 | 343 / 3 | 343 / 3 | 343 / 3 | — |
| quotes.toscrape.com/tag/change/page/1 | 29 / 0 | 61 / 0 | 61 / 0 | 61 / 0 | 64 / 3 | 64 / 3 | 64 / 3 | — |
| quotes.toscrape.com/tag/choices/page/1 | 24 / 0 | 54 / 0 | 54 / 0 | 54 / 0 | 57 / 3 | 57 / 3 | 57 / 3 | — |
| quotes.toscrape.com/tag/edison/page/1 | — | 53 / 0 | 53 / 0 | 53 / 0 | 56 / 3 | 56 / 3 | 56 / 3 | — |
| quotes.toscrape.com/tag/friendship | 118 / 0 | 166 / 0 | 166 / 0 | 166 / 0 | 169 / 3 | 169 / 3 | 169 / 3 | — |
| quotes.toscrape.com/tag/life | 434 / 0 | 509 / 0 | 509 / 0 | 509 / 0 | 512 / 3 | 512 / 3 | 512 / 3 | — |
| quotes.toscrape.com/tag/love/page/1 | 619 / 0 | 684 / 0 | 684 / 0 | 684 / 0 | 687 / 3 | 687 / 3 | 687 / 3 | — |
| quotes.toscrape.com/tag/reading | 197 / 0 | 255 / 0 | 255 / 0 | 255 / 0 | 258 / 3 | 258 / 3 | 258 / 3 | — |
| quotes.toscrape.com/tag/thinking/page/1 | 57 / 0 | 93 / 0 | 93 / 0 | 93 / 0 | 96 / 3 | 96 / 3 | 96 / 3 | — |

</details>

## books-toscrape

| Tool | Avg words | Preamble [1] | Repeat rate | Junk found | Headings | Code blocks | Precision | Recall |
|---|---|---|---|---|---|---|---|---|
| **markcrawl** | **339** | **66** | **0%** | **0** | **1.8** | **0.0** | **100%** | **99%** |
| crawl4ai | 493 | 178 [!] | 2% | 0 | 10.7 | 0.0 | 100% | 99% |
| crawl4ai-raw | 493 | 178 [!] | 2% | 0 | 10.7 | 0.0 | 100% | 99% |
| scrapy+md | 387 | 101 [!] | 1% | 0 | 1.8 | 0.0 | 100% | 99% |
| crawlee | 395 | 110 [!] | 1% | 0 | 1.8 | 0.0 | 100% | 100% |
| colly+md | 395 | 110 [!] | 1% | 0 | 1.8 | 0.0 | 100% | 100% |
| playwright | 395 | 110 [!] | 1% | 0 | 1.8 | 0.0 | 100% | 100% |
| firecrawl | — | — | — | — | — | — | — | — |

**[1]** Avg words per page before the first heading (nav chrome). **[!]** = likely nav/boilerplate problem (preamble >50 or repeat rate >20%).

**Reading the numbers:**
The word count gap (339 vs 493 avg words) is largely explained by preamble: 178 words of nav chrome account for ~36% of crawl4ai's output on this site.

<details>
<summary>Sample output — first 40 lines of <code>books.toscrape.com/catalogue/category/books/christian-fiction_34/index.html</code></summary>

This shows what each tool outputs at the *top* of the same page.
Nav boilerplate appears here before the real content starts.

**markcrawl**
```
* [Home](../../../../index.html)
* [Books](../../books_1/index.html)
* Christian Fiction

# Christian Fiction


**6** results.

**Warning!** This is a demo website for web scraping purposes. Prices and ratings here were randomly assigned and have no real meaning.

1. ### [Redeeming Love](../../../redeeming-love_826/index.html "Redeeming Love")

   £20.47

   In stock

   Add to basket
2. ### [Close to You](../../../close-to-you_798/index.html "Close to You")

   £49.46

   In stock

   Add to basket
3. ### [Shadows of the Past ...](../../../shadows-of-the-past-logan-point-1_541/index.html "Shadows of the Past (Logan Point #1)")

   £39.67

   In stock

   Add to basket
4. ### [Like Never Before (Walker ...](../../../like-never-before-walker-family-2_476/index.html "Like Never Before (Walker Family #2)")

   £28.77

   In stock

   Add to basket
5. ### [Counted With the Stars ...](../../../counted-with-the-stars-out-from-egypt-1_463/index.html "Counted With the Stars (Out from Egypt #1)")
```

**crawl4ai**
```
[Books to Scrape](https://books.toscrape.com/index.html) We love being scraped!
  * [Home](https://books.toscrape.com/index.html)
  * [Books](https://books.toscrape.com/catalogue/category/books_1/index.html)
  * Christian Fiction


  * [ Books ](https://books.toscrape.com/catalogue/category/books_1/index.html)
    * [ Travel ](https://books.toscrape.com/catalogue/category/books/travel_2/index.html)
    * [ Mystery ](https://books.toscrape.com/catalogue/category/books/mystery_3/index.html)
    * [ Historical Fiction ](https://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html)
    * [ Sequential Art ](https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html)
    * [ Classics ](https://books.toscrape.com/catalogue/category/books/classics_6/index.html)
    * [ Philosophy ](https://books.toscrape.com/catalogue/category/books/philosophy_7/index.html)
    * [ Romance ](https://books.toscrape.com/catalogue/category/books/romance_8/index.html)
    * [ Womens Fiction ](https://books.toscrape.com/catalogue/category/books/womens-fiction_9/index.html)
    * [ Fiction ](https://books.toscrape.com/catalogue/category/books/fiction_10/index.html)
    * [ Childrens ](https://books.toscrape.com/catalogue/category/books/childrens_11/index.html)
    * [ Religion ](https://books.toscrape.com/catalogue/category/books/religion_12/index.html)
    * [ Nonfiction ](https://books.toscrape.com/catalogue/category/books/nonfiction_13/index.html)
    * [ Music ](https://books.toscrape.com/catalogue/category/books/music_14/index.html)
    * [ Default ](https://books.toscrape.com/catalogue/category/books/default_15/index.html)
    * [ Science Fiction ](https://books.toscrape.com/catalogue/category/books/science-fiction_16/index.html)
    * [ Sports and Games ](https://books.toscrape.com/catalogue/category/books/sports-and-games_17/index.html)
    * [ Add a comment ](https://books.toscrape.com/catalogue/category/books/add-a-comment_18/index.html)
    * [ Fantasy ](https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html)
    * [ New Adult ](https://books.toscrape.com/catalogue/category/books/new-adult_20/index.html)
    * [ Young Adult ](https://books.toscrape.com/catalogue/category/books/young-adult_21/index.html)
    * [ Science ](https://books.toscrape.com/catalogue/category/books/science_22/index.html)
    * [ Poetry ](https://books.toscrape.com/catalogue/category/books/poetry_23/index.html)
    * [ Paranormal ](https://books.toscrape.com/catalogue/category/books/paranormal_24/index.html)
    * [ Art ](https://books.toscrape.com/catalogue/category/books/art_25/index.html)
    * [ Psychology ](https://books.toscrape.com/catalogue/category/books/psychology_26/index.html)
    * [ Autobiography ](https://books.toscrape.com/catalogue/category/books/autobiography_27/index.html)
    * [ Parenting ](https://books.toscrape.com/catalogue/category/books/parenting_28/index.html)
    * [ Adult Fiction ](https://books.toscrape.com/catalogue/category/books/adult-fiction_29/index.html)
    * [ Humor ](https://books.toscrape.com/catalogue/category/books/humor_30/index.html)
    * [ Horror ](https://books.toscrape.com/catalogue/category/books/horror_31/index.html)
    * [ History ](https://books.toscrape.com/catalogue/category/books/history_32/index.html)
    * [ Food and Drink ](https://books.toscrape.com/catalogue/category/books/food-and-drink_33/index.html)
    * [ **Christian Fiction** ](https://books.toscrape.com/catalogue/category/books/christian-fiction_34/index.html)
```

**crawl4ai-raw**
```
[Books to Scrape](https://books.toscrape.com/index.html) We love being scraped!
  * [Home](https://books.toscrape.com/index.html)
  * [Books](https://books.toscrape.com/catalogue/category/books_1/index.html)
  * Christian Fiction


  * [ Books ](https://books.toscrape.com/catalogue/category/books_1/index.html)
    * [ Travel ](https://books.toscrape.com/catalogue/category/books/travel_2/index.html)
    * [ Mystery ](https://books.toscrape.com/catalogue/category/books/mystery_3/index.html)
    * [ Historical Fiction ](https://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html)
    * [ Sequential Art ](https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html)
    * [ Classics ](https://books.toscrape.com/catalogue/category/books/classics_6/index.html)
    * [ Philosophy ](https://books.toscrape.com/catalogue/category/books/philosophy_7/index.html)
    * [ Romance ](https://books.toscrape.com/catalogue/category/books/romance_8/index.html)
    * [ Womens Fiction ](https://books.toscrape.com/catalogue/category/books/womens-fiction_9/index.html)
    * [ Fiction ](https://books.toscrape.com/catalogue/category/books/fiction_10/index.html)
    * [ Childrens ](https://books.toscrape.com/catalogue/category/books/childrens_11/index.html)
    * [ Religion ](https://books.toscrape.com/catalogue/category/books/religion_12/index.html)
    * [ Nonfiction ](https://books.toscrape.com/catalogue/category/books/nonfiction_13/index.html)
    * [ Music ](https://books.toscrape.com/catalogue/category/books/music_14/index.html)
    * [ Default ](https://books.toscrape.com/catalogue/category/books/default_15/index.html)
    * [ Science Fiction ](https://books.toscrape.com/catalogue/category/books/science-fiction_16/index.html)
    * [ Sports and Games ](https://books.toscrape.com/catalogue/category/books/sports-and-games_17/index.html)
    * [ Add a comment ](https://books.toscrape.com/catalogue/category/books/add-a-comment_18/index.html)
    * [ Fantasy ](https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html)
    * [ New Adult ](https://books.toscrape.com/catalogue/category/books/new-adult_20/index.html)
    * [ Young Adult ](https://books.toscrape.com/catalogue/category/books/young-adult_21/index.html)
    * [ Science ](https://books.toscrape.com/catalogue/category/books/science_22/index.html)
    * [ Poetry ](https://books.toscrape.com/catalogue/category/books/poetry_23/index.html)
    * [ Paranormal ](https://books.toscrape.com/catalogue/category/books/paranormal_24/index.html)
    * [ Art ](https://books.toscrape.com/catalogue/category/books/art_25/index.html)
    * [ Psychology ](https://books.toscrape.com/catalogue/category/books/psychology_26/index.html)
    * [ Autobiography ](https://books.toscrape.com/catalogue/category/books/autobiography_27/index.html)
    * [ Parenting ](https://books.toscrape.com/catalogue/category/books/parenting_28/index.html)
    * [ Adult Fiction ](https://books.toscrape.com/catalogue/category/books/adult-fiction_29/index.html)
    * [ Humor ](https://books.toscrape.com/catalogue/category/books/humor_30/index.html)
    * [ Horror ](https://books.toscrape.com/catalogue/category/books/horror_31/index.html)
    * [ History ](https://books.toscrape.com/catalogue/category/books/history_32/index.html)
    * [ Food and Drink ](https://books.toscrape.com/catalogue/category/books/food-and-drink_33/index.html)
    * [ **Christian Fiction** ](https://books.toscrape.com/catalogue/category/books/christian-fiction_34/index.html)
```

**scrapy+md**
```
[Books to Scrape](../../../../index.html) We love being scraped!

* [Home](../../../../index.html)
* [Books](../../books_1/index.html)
* Christian Fiction

* [Books](../../books_1/index.html)
  + [Travel](../travel_2/index.html)
  + [Mystery](../mystery_3/index.html)
  + [Historical Fiction](../historical-fiction_4/index.html)
  + [Sequential Art](../sequential-art_5/index.html)
  + [Classics](../classics_6/index.html)
  + [Philosophy](../philosophy_7/index.html)
  + [Romance](../romance_8/index.html)
  + [Womens Fiction](../womens-fiction_9/index.html)
  + [Fiction](../fiction_10/index.html)
  + [Childrens](../childrens_11/index.html)
  + [Religion](../religion_12/index.html)
  + [Nonfiction](../nonfiction_13/index.html)
  + [Music](../music_14/index.html)
  + [Default](../default_15/index.html)
  + [Science Fiction](../science-fiction_16/index.html)
  + [Sports and Games](../sports-and-games_17/index.html)
  + [Add a comment](../add-a-comment_18/index.html)
  + [Fantasy](../fantasy_19/index.html)
  + [New Adult](../new-adult_20/index.html)
  + [Young Adult](../young-adult_21/index.html)
  + [Science](../science_22/index.html)
  + [Poetry](../poetry_23/index.html)
  + [Paranormal](../paranormal_24/index.html)
  + [Art](../art_25/index.html)
  + [Psychology](../psychology_26/index.html)
  + [Autobiography](../autobiography_27/index.html)
  + [Parenting](../parenting_28/index.html)
  + [Adult Fiction](../adult-fiction_29/index.html)
  + [Humor](../humor_30/index.html)
  + [Horror](../horror_31/index.html)
  + [History](../history_32/index.html)
  + [Food and Drink](../food-and-drink_33/index.html)
  + [**Christian Fiction**](index.html)
```

**crawlee**
```
Christian Fiction |
Books to Scrape - Sandbox




[Books to Scrape](../../../../index.html) We love being scraped!

* [Home](../../../../index.html)
* [Books](../../books_1/index.html)
* Christian Fiction

* [Books](../../books_1/index.html)
  + [Travel](../travel_2/index.html)
  + [Mystery](../mystery_3/index.html)
  + [Historical Fiction](../historical-fiction_4/index.html)
  + [Sequential Art](../sequential-art_5/index.html)
  + [Classics](../classics_6/index.html)
  + [Philosophy](../philosophy_7/index.html)
  + [Romance](../romance_8/index.html)
  + [Womens Fiction](../womens-fiction_9/index.html)
  + [Fiction](../fiction_10/index.html)
  + [Childrens](../childrens_11/index.html)
  + [Religion](../religion_12/index.html)
  + [Nonfiction](../nonfiction_13/index.html)
  + [Music](../music_14/index.html)
  + [Default](../default_15/index.html)
  + [Science Fiction](../science-fiction_16/index.html)
  + [Sports and Games](../sports-and-games_17/index.html)
  + [Add a comment](../add-a-comment_18/index.html)
  + [Fantasy](../fantasy_19/index.html)
  + [New Adult](../new-adult_20/index.html)
  + [Young Adult](../young-adult_21/index.html)
  + [Science](../science_22/index.html)
  + [Poetry](../poetry_23/index.html)
  + [Paranormal](../paranormal_24/index.html)
  + [Art](../art_25/index.html)
  + [Psychology](../psychology_26/index.html)
  + [Autobiography](../autobiography_27/index.html)
  + [Parenting](../parenting_28/index.html)
```

**colly+md**
```
  


Christian Fiction |
Books to Scrape - Sandbox




[Books to Scrape](../../../../index.html) We love being scraped!

* [Home](../../../../index.html)
* [Books](../../books_1/index.html)
* Christian Fiction

* [Books](../../books_1/index.html)
  + [Travel](../travel_2/index.html)
  + [Mystery](../mystery_3/index.html)
  + [Historical Fiction](../historical-fiction_4/index.html)
  + [Sequential Art](../sequential-art_5/index.html)
  + [Classics](../classics_6/index.html)
  + [Philosophy](../philosophy_7/index.html)
  + [Romance](../romance_8/index.html)
  + [Womens Fiction](../womens-fiction_9/index.html)
  + [Fiction](../fiction_10/index.html)
  + [Childrens](../childrens_11/index.html)
  + [Religion](../religion_12/index.html)
  + [Nonfiction](../nonfiction_13/index.html)
  + [Music](../music_14/index.html)
  + [Default](../default_15/index.html)
  + [Science Fiction](../science-fiction_16/index.html)
  + [Sports and Games](../sports-and-games_17/index.html)
  + [Add a comment](../add-a-comment_18/index.html)
  + [Fantasy](../fantasy_19/index.html)
  + [New Adult](../new-adult_20/index.html)
  + [Young Adult](../young-adult_21/index.html)
  + [Science](../science_22/index.html)
  + [Poetry](../poetry_23/index.html)
  + [Paranormal](../paranormal_24/index.html)
  + [Art](../art_25/index.html)
```

**playwright**
```
Christian Fiction |
Books to Scrape - Sandbox




[Books to Scrape](../../../../index.html) We love being scraped!

* [Home](../../../../index.html)
* [Books](../../books_1/index.html)
* Christian Fiction

* [Books](../../books_1/index.html)
  + [Travel](../travel_2/index.html)
  + [Mystery](../mystery_3/index.html)
  + [Historical Fiction](../historical-fiction_4/index.html)
  + [Sequential Art](../sequential-art_5/index.html)
  + [Classics](../classics_6/index.html)
  + [Philosophy](../philosophy_7/index.html)
  + [Romance](../romance_8/index.html)
  + [Womens Fiction](../womens-fiction_9/index.html)
  + [Fiction](../fiction_10/index.html)
  + [Childrens](../childrens_11/index.html)
  + [Religion](../religion_12/index.html)
  + [Nonfiction](../nonfiction_13/index.html)
  + [Music](../music_14/index.html)
  + [Default](../default_15/index.html)
  + [Science Fiction](../science-fiction_16/index.html)
  + [Sports and Games](../sports-and-games_17/index.html)
  + [Add a comment](../add-a-comment_18/index.html)
  + [Fantasy](../fantasy_19/index.html)
  + [New Adult](../new-adult_20/index.html)
  + [Young Adult](../young-adult_21/index.html)
  + [Science](../science_22/index.html)
  + [Poetry](../poetry_23/index.html)
  + [Paranormal](../paranormal_24/index.html)
  + [Art](../art_25/index.html)
  + [Psychology](../psychology_26/index.html)
  + [Autobiography](../autobiography_27/index.html)
  + [Parenting](../parenting_28/index.html)
```

**firecrawl** — no output for this URL

</details>

<details>
<summary>Per-page word counts and preamble [1]</summary>

| URL | markcrawl words / preamble [1] | crawl4ai words / preamble [1] | crawl4ai-raw words / preamble [1] | scrapy+md words / preamble [1] | crawlee words / preamble [1] | colly+md words / preamble [1] | playwright words / preamble [1] | firecrawl words / preamble [1] |
|---|---|---|---|---|---|---|---|---|
| books.toscrape.com | 397 / 5 | 702 / 232 | 702 / 232 | 531 / 130 | 539 / 138 | 539 / 138 | 539 / 138 | — |
| books.toscrape.com/catalogue/category/books/academic_40 | 32 / 6 | 282 / 233 | 282 / 233 | 185 / 131 | 192 / 138 | 192 / 138 | 192 / 138 | — |
| books.toscrape.com/catalogue/category/books/add-a-comme | 424 / 8 | 745 / 235 | 745 / 235 | 558 / 133 | 567 / 142 | 567 / 142 | 567 / 142 | — |
| books.toscrape.com/catalogue/category/books/adult-ficti | 34 / 7 | 284 / 234 | 284 / 234 | 187 / 132 | 195 / 140 | 195 / 140 | 195 / 140 | — |
| books.toscrape.com/catalogue/category/books/art_25/inde | 163 / 0 | 422 / 233 | 422 / 233 | 303 / 131 | 310 / 138 | 310 / 138 | 310 / 138 | — |
| books.toscrape.com/catalogue/category/books/autobiograp | 163 / 0 | 412 / 233 | 412 / 233 | 303 / 131 | 310 / 138 | 310 / 138 | 310 / 138 | — |
| books.toscrape.com/catalogue/category/books/biography_3 | 32 / 6 | 410 / 233 | 410 / 233 | 279 / 131 | 286 / 138 | 286 / 138 | 286 / 138 | — |
| books.toscrape.com/catalogue/category/books/business_35 | 290 / 0 | 612 / 233 | 612 / 233 | 430 / 131 | 437 / 138 | 437 / 138 | 437 / 138 | — |
| books.toscrape.com/catalogue/category/books/childrens_1 | 360 / 0 | 642 / 233 | 642 / 233 | 500 / 131 | 507 / 138 | 507 / 138 | 507 / 138 | — |
| books.toscrape.com/catalogue/category/books/christian-f | 140 / 7 | 388 / 234 | 388 / 234 | 274 / 132 | 282 / 140 | 282 / 140 | 282 / 140 | — |
| books.toscrape.com/catalogue/category/books/christian_4 | 32 / 6 | 342 / 233 | 342 / 233 | 230 / 131 | 237 / 138 | 237 / 138 | 237 / 138 | — |
| books.toscrape.com/catalogue/category/books/classics_6/ | 320 / 0 | 593 / 233 | 593 / 233 | 460 / 131 | 467 / 138 | 467 / 138 | 467 / 138 | — |
| books.toscrape.com/catalogue/category/books/contemporar | 78 / 0 | 320 / 233 | 320 / 233 | 218 / 131 | 225 / 138 | 225 / 138 | 225 / 138 | — |
| books.toscrape.com/catalogue/category/books/crime_51/in | 52 / 0 | 296 / 233 | 296 / 233 | 192 / 131 | 199 / 138 | 199 / 138 | 199 / 138 | — |
| books.toscrape.com/catalogue/category/books/cultural_49 | 40 / 0 | 274 / 233 | 274 / 233 | 180 / 131 | 187 / 138 | 187 / 138 | 187 / 138 | — |
| books.toscrape.com/catalogue/category/books/default_15/ | 433 / 0 | 777 / 233 | 777 / 233 | 573 / 131 | 580 / 138 | 580 / 138 | 580 / 138 | — |
| books.toscrape.com/catalogue/category/books/erotica_50/ | 38 / 0 | 271 / 233 | 271 / 233 | 178 / 131 | 185 / 138 | 185 / 138 | 185 / 138 | — |
| books.toscrape.com/catalogue/category/books/fantasy_19/ | 430 / 0 | 764 / 233 | 764 / 233 | 570 / 131 | 577 / 138 | 577 / 138 | 577 / 138 | — |
| books.toscrape.com/catalogue/category/books/fiction_10/ | 359 / 0 | 636 / 233 | 636 / 233 | 499 / 131 | 506 / 138 | 506 / 138 | 506 / 138 | — |
| books.toscrape.com/catalogue/category/books/food-and-dr | 548 / 8 | 978 / 235 | 978 / 235 | 682 / 133 | 691 / 142 | 691 / 142 | 691 / 142 | — |
| books.toscrape.com/catalogue/category/books/health_47/i | 118 / 0 | 384 / 233 | 384 / 233 | 258 / 131 | 265 / 138 | 265 / 138 | 265 / 138 | — |
| books.toscrape.com/catalogue/category/books/historical_ | 69 / 0 | 315 / 233 | 315 / 233 | 209 / 131 | 216 / 138 | 216 / 138 | 216 / 138 | — |
| books.toscrape.com/catalogue/category/books/horror_31/i | 269 / 0 | 524 / 233 | 524 / 233 | 409 / 131 | 416 / 138 | 416 / 138 | 416 / 138 | — |
| books.toscrape.com/catalogue/category/books/humor_30/in | 233 / 0 | 529 / 233 | 529 / 233 | 373 / 131 | 380 / 138 | 380 / 138 | 380 / 138 | — |
| books.toscrape.com/catalogue/category/books/music_14/in | 298 / 0 | 616 / 233 | 616 / 233 | 438 / 131 | 445 / 138 | 445 / 138 | 445 / 138 | — |
| books.toscrape.com/catalogue/category/books/mystery_3/i | 401 / 0 | 710 / 233 | 710 / 233 | 541 / 131 | 548 / 138 | 548 / 138 | 548 / 138 | — |
| books.toscrape.com/catalogue/category/books/new-adult_2 | 130 / 7 | 370 / 234 | 370 / 234 | 264 / 132 | 272 / 140 | 272 / 140 | 272 / 140 | — |
| books.toscrape.com/catalogue/category/books/novels_46/i | 32 / 6 | 286 / 233 | 286 / 233 | 187 / 131 | 194 / 138 | 194 / 138 | 194 / 138 | — |
| books.toscrape.com/catalogue/category/books/parenting_2 | 32 / 6 | 286 / 233 | 286 / 233 | 187 / 131 | 194 / 138 | 194 / 138 | 194 / 138 | — |
| books.toscrape.com/catalogue/category/books/poetry_23/i | 349 / 0 | 642 / 233 | 642 / 233 | 489 / 131 | 496 / 138 | 496 / 138 | 496 / 138 | — |
| books.toscrape.com/catalogue/category/books/politics_48 | 88 / 0 | 340 / 233 | 340 / 233 | 228 / 131 | 235 / 138 | 235 / 138 | 235 / 138 | — |
| books.toscrape.com/catalogue/category/books/psychology_ | 178 / 0 | 460 / 233 | 460 / 233 | 318 / 131 | 325 / 138 | 325 / 138 | 325 / 138 | — |
| books.toscrape.com/catalogue/category/books/science-fic | 322 / 7 | 615 / 234 | 615 / 234 | 456 / 132 | 464 / 140 | 464 / 140 | 464 / 140 | — |
| books.toscrape.com/catalogue/category/books/science_22/ | 344 / 0 | 690 / 233 | 690 / 233 | 484 / 131 | 491 / 138 | 491 / 138 | 491 / 138 | — |
| books.toscrape.com/catalogue/category/books/short-stori | 39 / 0 | 273 / 234 | 273 / 234 | 180 / 132 | 188 / 140 | 188 / 140 | 188 / 140 | — |
| books.toscrape.com/catalogue/category/books/spiritualit | 165 / 0 | 447 / 233 | 447 / 233 | 305 / 131 | 312 / 138 | 312 / 138 | 312 / 138 | — |
| books.toscrape.com/catalogue/category/books/sports-and- | 137 / 8 | 391 / 235 | 391 / 235 | 271 / 133 | 280 / 142 | 280 / 142 | 280 / 142 | — |
| books.toscrape.com/catalogue/category/books/suspense_44 | 46 / 0 | 284 / 233 | 284 / 233 | 186 / 131 | 193 / 138 | 193 / 138 | 193 / 138 | — |
| books.toscrape.com/catalogue/category/books/thriller_37 | 205 / 0 | 465 / 233 | 465 / 233 | 345 / 131 | 352 / 138 | 352 / 138 | 352 / 138 | — |
| books.toscrape.com/catalogue/category/books/travel_2/in | 252 / 0 | 550 / 233 | 550 / 233 | 392 / 131 | 399 / 138 | 399 / 138 | 399 / 138 | — |
| books.toscrape.com/catalogue/category/books/womens-fict | 330 / 7 | 614 / 234 | 614 / 234 | 464 / 132 | 472 / 140 | 472 / 140 | 472 / 140 | — |
| books.toscrape.com/catalogue/category/books/young-adult | 386 / 7 | 676 / 234 | 676 / 234 | 520 / 132 | 528 / 140 | 528 / 140 | 528 / 140 | — |
| books.toscrape.com/catalogue/category/books_1/index.htm | 391 / 0 | 700 / 231 | 700 / 231 | 529 / 129 | 536 / 136 | 536 / 136 | 536 / 136 | — |
| books.toscrape.com/catalogue/its-only-the-himalayas_981 | 667 / 230 | 480 / 22 | 480 / 22 | 463 / 18 | 473 / 28 | 473 / 28 | 473 / 28 | — |
| books.toscrape.com/catalogue/libertarianism-for-beginne | 596 / 195 | 442 / 20 | 442 / 20 | 426 / 17 | 435 / 26 | 435 / 26 | 435 / 26 | — |
| books.toscrape.com/catalogue/olio_984/index.html | 703 / 249 | 491 / 16 | 491 / 16 | 477 / 15 | 484 / 22 | 484 / 22 | 484 / 22 | — |
| books.toscrape.com/catalogue/our-band-could-be-your-lif | 531 / 163 | 419 / 40 | 419 / 40 | 403 / 27 | 422 / 46 | 422 / 46 | 422 / 46 | — |
| books.toscrape.com/catalogue/page-2.html | 413 / 5 | 726 / 232 | 726 / 232 | 547 / 130 | 555 / 138 | 555 / 138 | 555 / 138 | — |
| books.toscrape.com/catalogue/sapiens-a-brief-history-of | 761 / 304 | 481 / 26 | 481 / 26 | 485 / 20 | 497 / 32 | 497 / 32 | 497 / 32 | — |
| books.toscrape.com/catalogue/scott-pilgrims-precious-li | 515 / 148 | 428 / 31 | 428 / 31 | 398 / 23 | 412 / 37 | 412 / 37 | 412 / 37 | — |
| books.toscrape.com/catalogue/set-me-free_988/index.html | 486 / 132 | 411 / 21 | 411 / 21 | 380 / 18 | 389 / 27 | 389 / 27 | 389 / 27 | — |
| books.toscrape.com/catalogue/shakespeares-sonnets_989/i | 509 / 143 | 421 / 18 | 421 / 18 | 390 / 16 | 398 / 24 | 398 / 24 | 398 / 24 | — |
| books.toscrape.com/catalogue/sharp-objects_997/index.ht | 685 / 274 | 427 / 18 | 427 / 18 | 435 / 16 | 443 / 24 | 443 / 24 | 443 / 24 | — |
| books.toscrape.com/catalogue/soumission_998/index.html | 452 / 163 | 304 / 16 | 304 / 16 | 312 / 15 | 319 / 22 | 319 / 22 | 319 / 22 | — |
| books.toscrape.com/catalogue/starving-hearts-triangular | 619 / 196 | 486 / 26 | 486 / 26 | 451 / 20 | 463 / 32 | 463 / 32 | 463 / 32 | — |
| books.toscrape.com/catalogue/the-black-maria_991/index. | 1150 / 464 | 742 / 20 | 742 / 20 | 711 / 17 | 720 / 26 | 720 / 26 | 720 / 26 | — |
| books.toscrape.com/catalogue/the-coming-woman-a-novel-b | 1335 / 568 | 818 / 44 | 818 / 44 | 804 / 29 | 825 / 50 | 825 / 50 | 825 / 50 | — |
| books.toscrape.com/catalogue/the-dirty-little-secrets-o | 757 / 284 | 508 / 32 | 508 / 32 | 504 / 23 | 519 / 38 | 519 / 38 | 519 / 38 | — |
| books.toscrape.com/catalogue/the-requiem-red_995/index. | 509 / 170 | 362 / 21 | 362 / 21 | 365 / 18 | 374 / 27 | 374 / 27 | 374 / 27 | — |
| books.toscrape.com/catalogue/tipping-the-velvet_999/ind | 444 / 165 | 298 / 21 | 298 / 21 | 305 / 18 | 314 / 27 | 314 / 27 | 314 / 27 | — |

</details>

## fastapi-docs

| Tool | Avg words | Preamble [1] | Repeat rate | Junk found | Headings | Code blocks | Precision | Recall |
|---|---|---|---|---|---|---|---|---|
| **markcrawl** | **2084** | **13** | **0%** | **186** | **20.2** | **14.3** | **93%** | **68%** |
| crawl4ai | 3519 | 1420 [!] | 1% | 183 | 20.1 | 14.2 | 100% | 92% |
| crawl4ai-raw | 3521 | 1420 [!] | 1% | 183 | 20.1 | 14.2 | 100% | 92% |
| scrapy+md | 2851 | 765 [!] | 0% | 328 | 20.2 | 14.3 | 100% | 69% |
| crawlee | 3154 | 1004 [!] | 1% | 628 | 20.1 | 14.2 | 100% | 96% |
| colly+md | 3175 | 986 [!] | 1% | 632 | 20.2 | 14.3 | 100% | 97% |
| playwright | 3160 | 999 [!] | 1% | 632 | 20.1 | 14.3 | 100% | 97% |
| firecrawl | — | — | — | — | — | — | — | — |

**[1]** Avg words per page before the first heading (nav chrome). **[!]** = likely nav/boilerplate problem (preamble >50 or repeat rate >20%).

**Reading the numbers:**
**markcrawl** produces the cleanest output with 13 words of preamble per page, while **crawl4ai-raw** injects 1420 words of nav chrome before content begins. The word count gap (2084 vs 3521 avg words) is largely explained by preamble: 1420 words of nav chrome account for ~40% of crawl4ai-raw's output on this site. markcrawl's lower recall (68% vs 97%) reflects stricter content filtering — the "missed" sentences are predominantly navigation, sponsor links, and footer text that other tools include as content. For RAG, this is typically a net positive: fewer junk tokens per chunk tends to improve embedding quality and retrieval precision.

<details>
<summary>Sample output — first 40 lines of <code>fastapi.tiangolo.com/tutorial/body-fields</code></summary>

This shows what each tool outputs at the *top* of the same page.
Nav boilerplate appears here before the real content starts.

**markcrawl**
```
*FastAPI framework, high performance, easy to learn, fast to code, ready for production*


# Body - Fields[¶](#body-fields "Permanent link")

The same way you can declare additional validation and metadata in *path operation function* parameters with `Query`, `Path` and `Body`, you can declare validation and metadata inside of Pydantic models using Pydantic's `Field`.

## Import `Field`[¶](#import-field "Permanent link")

First, you have to import it:

Python 3.10+

```
from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results
```

🤓 Other versions and variants

Python 3.10+ - non-Annotated
```

**crawl4ai**
```
[ Skip to content ](https://fastapi.tiangolo.com/tutorial/body-fields/#body-fields)
[ **FastAPI Cloud** waiting list 🚀 ](https://fastapicloud.com)
[ Follow **@fastapi** on **X (Twitter)** to stay updated ](https://x.com/fastapi)
[ Follow **FastAPI** on **LinkedIn** to stay updated ](https://www.linkedin.com/company/fastapi)
[ **FastAPI and friends** newsletter 🎉 ](https://fastapi.tiangolo.com/newsletter/)
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/blockbee-banner.png) ](https://blockbee.io?ref=fastapi "BlockBee Cryptocurrency Payment Gateway")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/scalar-banner.svg) ](https://github.com/scalar/scalar/?utm_source=fastapi&utm_medium=website&utm_campaign=top-banner "Scalar: Beautiful Open-Source API References from Swagger/OpenAPI files")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/propelauth-banner.png) ](https://www.propelauth.com/?utm_source=fastapi&utm_campaign=1223&utm_medium=topbanner "Auth, user management and more for your B2B product")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/zuplo-banner.png) ](https://zuplo.link/fastapi-web "Zuplo: Scale, Protect, Document, and Monetize your FastAPI")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/liblab-banner.png) ](https://liblab.com?utm_source=fastapi "liblab - Generate SDKs from FastAPI")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/render-banner.svg) ](https://docs.render.com/deploy-fastapi?utm_source=deploydoc&utm_medium=referral&utm_campaign=fastapi "Deploy & scale any full-stack web app on Render. Focus on building apps, not infra.")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/coderabbit-banner.png) ](https://www.coderabbit.ai/?utm_source=fastapi&utm_medium=banner&utm_campaign=fastapi "Cut Code Review Time & Bugs in Half with CodeRabbit")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/subtotal-banner.svg) ](https://subtotal.com/?utm_source=fastapi&utm_medium=sponsorship&utm_campaign=open-source "Making Retail Purchases Actionable for Brands and Developers")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/railway-banner.png) ](https://docs.railway.com/guides/fastapi?utm_medium=integration&utm_source=docs&utm_campaign=fastapi "Deploy enterprise applications at startup speed")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/serpapi-banner.png) ](https://serpapi.com/?utm_source=fastapi_website "SerpApi: Web Search API")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/greptile-banner.png) ](https://www.greptile.com/?utm_source=fastapi&utm_medium=sponsorship&utm_campaign=fastapi_sponsor_page "Greptile: The AI Code Reviewer")
[ ![logo](https://fastapi.tiangolo.com/img/icon-white.svg) ](https://fastapi.tiangolo.com/ "FastAPI")
FastAPI 
Body - Fields 
  * [ en - English ](https://fastapi.tiangolo.com/)
  * [ de - Deutsch ](https://fastapi.tiangolo.com/de/)
  * [ es - español ](https://fastapi.tiangolo.com/es/)
  * [ fr - français ](https://fastapi.tiangolo.com/fr/)
  * [ ja - 日本語 ](https://fastapi.tiangolo.com/ja/)
  * [ ko - 한국어 ](https://fastapi.tiangolo.com/ko/)
  * [ pt - português ](https://fastapi.tiangolo.com/pt/)
  * [ ru - русский язык ](https://fastapi.tiangolo.com/ru/)
  * [ tr - Türkçe ](https://fastapi.tiangolo.com/tr/)
  * [ uk - українська мова ](https://fastapi.tiangolo.com/uk/)
  * [ zh - 简体中文 ](https://fastapi.tiangolo.com/zh/)
  * [ zh-hant - 繁體中文 ](https://fastapi.tiangolo.com/zh-hant/)


[ ](https://fastapi.tiangolo.com/tutorial/body-fields/?q= "Share")
Type to start searching
[ fastapi/fastapi 
  * 0.135.3
  * 97.1k
  * 9.1k
```

**crawl4ai-raw**
```
[ Skip to content ](https://fastapi.tiangolo.com/tutorial/body-fields/#body-fields)
[ **FastAPI Cloud** waiting list 🚀 ](https://fastapicloud.com)
[ Follow **@fastapi** on **X (Twitter)** to stay updated ](https://x.com/fastapi)
[ Follow **FastAPI** on **LinkedIn** to stay updated ](https://www.linkedin.com/company/fastapi)
[ **FastAPI and friends** newsletter 🎉 ](https://fastapi.tiangolo.com/newsletter/)
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/blockbee-banner.png) ](https://blockbee.io?ref=fastapi "BlockBee Cryptocurrency Payment Gateway")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/scalar-banner.svg) ](https://github.com/scalar/scalar/?utm_source=fastapi&utm_medium=website&utm_campaign=top-banner "Scalar: Beautiful Open-Source API References from Swagger/OpenAPI files")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/propelauth-banner.png) ](https://www.propelauth.com/?utm_source=fastapi&utm_campaign=1223&utm_medium=topbanner "Auth, user management and more for your B2B product")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/zuplo-banner.png) ](https://zuplo.link/fastapi-web "Zuplo: Scale, Protect, Document, and Monetize your FastAPI")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/liblab-banner.png) ](https://liblab.com?utm_source=fastapi "liblab - Generate SDKs from FastAPI")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/render-banner.svg) ](https://docs.render.com/deploy-fastapi?utm_source=deploydoc&utm_medium=referral&utm_campaign=fastapi "Deploy & scale any full-stack web app on Render. Focus on building apps, not infra.")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/coderabbit-banner.png) ](https://www.coderabbit.ai/?utm_source=fastapi&utm_medium=banner&utm_campaign=fastapi "Cut Code Review Time & Bugs in Half with CodeRabbit")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/subtotal-banner.svg) ](https://subtotal.com/?utm_source=fastapi&utm_medium=sponsorship&utm_campaign=open-source "Making Retail Purchases Actionable for Brands and Developers")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/railway-banner.png) ](https://docs.railway.com/guides/fastapi?utm_medium=integration&utm_source=docs&utm_campaign=fastapi "Deploy enterprise applications at startup speed")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/serpapi-banner.png) ](https://serpapi.com/?utm_source=fastapi_website "SerpApi: Web Search API")
[ sponsor ![](https://fastapi.tiangolo.com/img/sponsors/greptile-banner.png) ](https://www.greptile.com/?utm_source=fastapi&utm_medium=sponsorship&utm_campaign=fastapi_sponsor_page "Greptile: The AI Code Reviewer")
[ ![logo](https://fastapi.tiangolo.com/img/icon-white.svg) ](https://fastapi.tiangolo.com/ "FastAPI")
FastAPI 
Body - Fields 
  * [ en - English ](https://fastapi.tiangolo.com/)
  * [ de - Deutsch ](https://fastapi.tiangolo.com/de/)
  * [ es - español ](https://fastapi.tiangolo.com/es/)
  * [ fr - français ](https://fastapi.tiangolo.com/fr/)
  * [ ja - 日本語 ](https://fastapi.tiangolo.com/ja/)
  * [ ko - 한국어 ](https://fastapi.tiangolo.com/ko/)
  * [ pt - português ](https://fastapi.tiangolo.com/pt/)
  * [ ru - русский язык ](https://fastapi.tiangolo.com/ru/)
  * [ tr - Türkçe ](https://fastapi.tiangolo.com/tr/)
  * [ uk - українська мова ](https://fastapi.tiangolo.com/uk/)
  * [ zh - 简体中文 ](https://fastapi.tiangolo.com/zh/)
  * [ zh-hant - 繁體中文 ](https://fastapi.tiangolo.com/zh-hant/)


[ ](https://fastapi.tiangolo.com/tutorial/body-fields/?q= "Share")
Type to start searching
[ fastapi/fastapi 
  * 0.135.3
  * 97.1k
  * 9.1k
```

**scrapy+md**
```
FastAPI

[fastapi/fastapi](https://github.com/fastapi/fastapi "Go to repository")

* [FastAPI](../..)
* [Features](../../features/)
* [Learn](../../learn/)

  Learn
  + [Python Types Intro](../../python-types/)
  + [Concurrency and async / await](../../async/)
  + [Environment Variables](../../environment-variables/)
  + [Virtual Environments](../../virtual-environments/)
  + [Tutorial - User Guide](../)

    Tutorial - User Guide
    - [First Steps](../first-steps/)
    - [Path Parameters](../path-params/)
    - [Query Parameters](../query-params/)
    - [Request Body](../body/)
    - [Query Parameters and String Validations](../query-params-str-validations/)
    - [Path Parameters and Numeric Validations](../path-params-numeric-validations/)
    - [Query Parameter Models](../query-param-models/)
    - [Body - Multiple Parameters](../body-multiple-params/)
    - Body - Fields

      [Body - Fields](./)



      Table of contents
      * [Import `Field`](#import-field)
      * [Declare model attributes](#declare-model-attributes)
      * [Add extra information](#add-extra-information)
      * [Recap](#recap)
    - [Body - Nested Models](../body-nested-models/)
    - [Declare Request Example Data](../schema-extra-example/)
    - [Extra Data Types](../extra-data-types/)
    - [Cookie Parameters](../cookie-params/)
    - [Header Parameters](../header-params/)
```

**crawlee**
```
Body - Fields - FastAPI




:root{--md-text-font:"Roboto";--md-code-font:"Roboto Mono"}



\_\_md\_scope=new URL("../..",location),\_\_md\_hash=e=>[...e].reduce(((e,\_)=>(e<<5)-e+\_.charCodeAt(0)),0),\_\_md\_get=(e,\_=localStorage,t=\_\_md\_scope)=>JSON.parse(\_.getItem(t.pathname+"."+e)),\_\_md\_set=(e,\_,t=localStorage,a=\_\_md\_scope)=>{try{t.setItem(a.pathname+"."+e,JSON.stringify(\_))}catch(e){}}













.grecaptcha-badge {
visibility: hidden;
}





[Skip to content](https://fastapi.tiangolo.com/tutorial/body-fields/#body-fields)

[Join the **FastAPI Cloud** waiting list 🚀](https://fastapicloud.com)

[Follow **@fastapi** on **X (Twitter)** to stay updated](https://x.com/fastapi)

[Follow **FastAPI** on **LinkedIn** to stay updated](https://www.linkedin.com/company/fastapi)

[Subscribe to the **FastAPI and friends** newsletter 🎉](https://fastapi.tiangolo.com/newsletter/)
```

**colly+md**
```
Body - Fields - FastAPI




:root{--md-text-font:"Roboto";--md-code-font:"Roboto Mono"}



\_\_md\_scope=new URL("../..",location),\_\_md\_hash=e=>[...e].reduce(((e,\_)=>(e<<5)-e+\_.charCodeAt(0)),0),\_\_md\_get=(e,\_=localStorage,t=\_\_md\_scope)=>JSON.parse(\_.getItem(t.pathname+"."+e)),\_\_md\_set=(e,\_,t=localStorage,a=\_\_md\_scope)=>{try{t.setItem(a.pathname+"."+e,JSON.stringify(\_))}catch(e){}}






[Skip to content](#body-fields)

[Join the **FastAPI Cloud** waiting list 🚀](https://fastapicloud.com)

[Follow **@fastapi** on **X (Twitter)** to stay updated](https://x.com/fastapi)

[Follow **FastAPI** on **LinkedIn** to stay updated](https://www.linkedin.com/company/fastapi)

[Subscribe to the **FastAPI and friends** newsletter 🎉](https://fastapi.tiangolo.com/newsletter/)

[sponsor](https://blockbee.io?ref=fastapi "BlockBee Cryptocurrency Payment Gateway")

[sponsor](https://github.com/scalar/scalar/?utm_source=fastapi&utm_medium=website&utm_campaign=top-banner "Scalar: Beautiful Open-Source API References from Swagger/OpenAPI files")

[sponsor](https://www.propelauth.com/?utm_source=fastapi&utm_campaign=1223&utm_medium=topbanner "Auth, user management and more for your B2B product")

[sponsor](https://zuplo.link/fastapi-web "Zuplo: Scale, Protect, Document, and Monetize your FastAPI")

[sponsor](https://liblab.com?utm_source=fastapi "liblab - Generate SDKs from FastAPI")

[sponsor](https://docs.render.com/deploy-fastapi?utm_source=deploydoc&utm_medium=referral&utm_campaign=fastapi "Deploy & scale any full-stack web app on Render. Focus on building apps, not infra.")

[sponsor](https://www.coderabbit.ai/?utm_source=fastapi&utm_medium=banner&utm_campaign=fastapi "Cut Code Review Time & Bugs in Half with CodeRabbit")
```

**playwright**
```
Body - Fields - FastAPI




:root{--md-text-font:"Roboto";--md-code-font:"Roboto Mono"}



\_\_md\_scope=new URL("../..",location),\_\_md\_hash=e=>[...e].reduce(((e,\_)=>(e<<5)-e+\_.charCodeAt(0)),0),\_\_md\_get=(e,\_=localStorage,t=\_\_md\_scope)=>JSON.parse(\_.getItem(t.pathname+"."+e)),\_\_md\_set=(e,\_,t=localStorage,a=\_\_md\_scope)=>{try{t.setItem(a.pathname+"."+e,JSON.stringify(\_))}catch(e){}}






[Skip to content](https://fastapi.tiangolo.com/tutorial/body-fields/#body-fields)

[Join the **FastAPI Cloud** waiting list 🚀](https://fastapicloud.com)

[Follow **@fastapi** on **X (Twitter)** to stay updated](https://x.com/fastapi)

[Follow **FastAPI** on **LinkedIn** to stay updated](https://www.linkedin.com/company/fastapi)

[Subscribe to the **FastAPI and friends** newsletter 🎉](https://fastapi.tiangolo.com/newsletter/)

[sponsor](https://blockbee.io?ref=fastapi "BlockBee Cryptocurrency Payment Gateway")

[sponsor](https://github.com/scalar/scalar/?utm_source=fastapi&utm_medium=website&utm_campaign=top-banner "Scalar: Beautiful Open-Source API References from Swagger/OpenAPI files")

[sponsor](https://www.propelauth.com/?utm_source=fastapi&utm_campaign=1223&utm_medium=topbanner "Auth, user management and more for your B2B product")

[sponsor](https://zuplo.link/fastapi-web "Zuplo: Scale, Protect, Document, and Monetize your FastAPI")

[sponsor](https://liblab.com?utm_source=fastapi "liblab - Generate SDKs from FastAPI")

[sponsor](https://docs.render.com/deploy-fastapi?utm_source=deploydoc&utm_medium=referral&utm_campaign=fastapi "Deploy & scale any full-stack web app on Render. Focus on building apps, not infra.")

[sponsor](https://www.coderabbit.ai/?utm_source=fastapi&utm_medium=banner&utm_campaign=fastapi "Cut Code Review Time & Bugs in Half with CodeRabbit")
```

**firecrawl** — no output for this URL

</details>

<details>
<summary>Per-page word counts and preamble [1]</summary>

| URL | markcrawl words / preamble [1] | crawl4ai words / preamble [1] | crawl4ai-raw words / preamble [1] | scrapy+md words / preamble [1] | crawlee words / preamble [1] | colly+md words / preamble [1] | playwright words / preamble [1] | firecrawl words / preamble [1] |
|---|---|---|---|---|---|---|---|---|
| fastapi.tiangolo.com | 2243 / 13 | 3991 / 1538 | 3979 / 1526 | 3092 / 839 | 3374 / 1071 | 3404 / 1054 | 3362 / 1059 | — |
| fastapi.tiangolo.com/about | 28 / 13 | 1303 / 1241 | 1303 / 1241 | 677 / 646 | 1015 / 882 | 998 / 863 | 1008 / 875 | — |
| fastapi.tiangolo.com/advanced | 128 / 13 | 1415 / 1261 | 1415 / 1261 | 792 / 661 | 1126 / 901 | 1113 / 882 | 1124 / 899 | — |
| fastapi.tiangolo.com/advanced/additional-responses | 1287 / 13 | 2648 / 1332 | 2650 / 1334 | 2008 / 718 | 2344 / 960 | 2337 / 941 | 2342 / 958 | — |
| fastapi.tiangolo.com/advanced/additional-status-codes | 485 / 13 | 1796 / 1280 | 1794 / 1278 | 1165 / 677 | 1504 / 917 | 1491 / 898 | 1497 / 910 | — |
| fastapi.tiangolo.com/advanced/advanced-dependencies | 2213 / 13 | 3660 / 1434 | 3658 / 1432 | 3012 / 796 | 3328 / 1032 | 3335 / 1015 | 3323 / 1027 | — |
| fastapi.tiangolo.com/advanced/advanced-python-types | 343 / 13 | 1642 / 1266 | 1644 / 1268 | 1015 / 669 | 1355 / 909 | 1340 / 890 | 1348 / 902 | — |
| fastapi.tiangolo.com/advanced/async-tests | 659 / 13 | 1991 / 1308 | 1991 / 1308 | 1354 / 692 | 1684 / 930 | 1678 / 911 | 1682 / 928 | — |
| fastapi.tiangolo.com/advanced/behind-a-proxy | 2231 / 13 | 3672 / 1478 | 3674 / 1480 | 3055 / 821 | 3318 / 1061 | 3378 / 1042 | 3381 / 1054 | — |
| fastapi.tiangolo.com/advanced/custom-response | 2000 / 13 | 3459 / 1450 | 3457 / 1448 | 2782 / 779 | 3097 / 1027 | 3116 / 1008 | 3090 / 1020 | — |
| fastapi.tiangolo.com/advanced/dataclasses | 791 / 13 | 2115 / 1296 | 2117 / 1298 | 1482 / 688 | 1813 / 926 | 1804 / 907 | 1811 / 924 | — |
| fastapi.tiangolo.com/advanced/events | 1513 / 13 | 2886 / 1356 | 2886 / 1356 | 2240 / 724 | 2556 / 962 | 2559 / 943 | 2549 / 955 | — |
| fastapi.tiangolo.com/advanced/generate-clients | 1665 / 13 | 3177 / 1480 | 3177 / 1480 | 2498 / 828 | 2810 / 1066 | 2823 / 1047 | 2803 / 1059 | — |
| fastapi.tiangolo.com/advanced/json-base64-bytes | 756 / 13 | 2096 / 1314 | 2096 / 1314 | 1462 / 703 | 1799 / 947 | 1790 / 928 | 1792 / 940 | — |
| fastapi.tiangolo.com/advanced/middleware | 610 / 13 | 1944 / 1308 | 1942 / 1306 | 1303 / 690 | 1630 / 928 | 1625 / 909 | 1623 / 921 | — |
| fastapi.tiangolo.com/advanced/openapi-callbacks | 1759 / 13 | 3155 / 1376 | 3157 / 1378 | 2510 / 748 | 2831 / 986 | 2832 / 967 | 2829 / 984 | — |
| fastapi.tiangolo.com/advanced/openapi-webhooks | 532 / 13 | 1868 / 1304 | 1870 / 1306 | 1231 / 696 | 1564 / 934 | 1555 / 915 | 1557 / 927 | — |
| fastapi.tiangolo.com/advanced/path-operation-advanced-c | 1336 / 13 | 2727 / 1374 | 2727 / 1374 | 2083 / 744 | 2405 / 984 | 2408 / 967 | 2400 / 979 | — |
| fastapi.tiangolo.com/advanced/response-change-status-co | 305 / 13 | 1612 / 1280 | 1612 / 1280 | 985 / 677 | 1324 / 921 | 1311 / 902 | 1322 / 919 | — |
| fastapi.tiangolo.com/advanced/response-cookies | 389 / 13 | 1706 / 1290 | 1706 / 1290 | 1076 / 684 | 1409 / 922 | 1398 / 903 | 1402 / 915 | — |
| fastapi.tiangolo.com/advanced/response-directly | 750 / 13 | 2099 / 1322 | 2101 / 1324 | 1461 / 708 | 1798 / 950 | 1791 / 931 | 1791 / 943 | — |
| fastapi.tiangolo.com/advanced/response-headers | 364 / 13 | 1680 / 1288 | 1682 / 1290 | 1051 / 684 | 1385 / 922 | 1374 / 903 | 1378 / 915 | — |
| fastapi.tiangolo.com/advanced/security | 103 / 13 | 1395 / 1265 | 1397 / 1267 | 770 / 664 | 1101 / 900 | 1090 / 883 | 1096 / 895 | — |
| fastapi.tiangolo.com/advanced/security/http-basic-auth | 1182 / 13 | 2553 / 1351 | 2553 / 1351 | 1913 / 728 | 2240 / 968 | 2237 / 949 | 2238 / 966 | — |
| fastapi.tiangolo.com/advanced/security/oauth2-scopes | 9002 / 13 | 10454 / 1445 | 10452 / 1443 | 9798 / 793 | 10106 / 1029 | 10119 / 1012 | 10101 / 1024 | — |
| fastapi.tiangolo.com/advanced/settings | 2195 / 13 | 3544 / 1472 | 3544 / 1472 | 3006 / 808 | 3191 / 1048 | 3330 / 1031 | 3317 / 1043 | — |
| fastapi.tiangolo.com/advanced/stream-data | 2736 / 13 | 4109 / 1354 | 4111 / 1356 | 3465 / 726 | 3787 / 964 | 3788 / 945 | 3780 / 957 | — |
| fastapi.tiangolo.com/advanced/strict-content-type | 535 / 13 | 1858 / 1296 | 1860 / 1298 | 1225 / 687 | 1559 / 927 | 1550 / 908 | 1552 / 920 | — |
| fastapi.tiangolo.com/advanced/sub-applications | 476 / 13 | 1829 / 1326 | 1829 / 1326 | 1187 / 708 | 1519 / 950 | 1512 / 931 | 1517 / 948 | — |
| fastapi.tiangolo.com/advanced/templates | 571 / 13 | 1917 / 1328 | 1913 / 1326 | 1281 / 707 | 1601 / 943 | 1599 / 924 | 1598 / 936 | — |
| fastapi.tiangolo.com/advanced/testing-dependencies | 707 / 13 | 2034 / 1296 | 2036 / 1298 | 1400 / 690 | 1740 / 932 | 1729 / 913 | 1733 / 925 | — |
| fastapi.tiangolo.com/advanced/testing-events | 276 / 13 | 1562 / 1253 | 1562 / 1253 | 929 / 650 | 1278 / 898 | 1261 / 879 | 1271 / 891 | — |
| fastapi.tiangolo.com/advanced/testing-websockets | 130 / 13 | 1414 / 1248 | 1414 / 1248 | 783 / 650 | 1125 / 888 | 1108 / 869 | 1118 / 881 | — |
| fastapi.tiangolo.com/advanced/using-request-directly | 370 / 13 | 1692 / 1296 | 1692 / 1296 | 1063 / 690 | 1399 / 932 | 1388 / 913 | 1397 / 930 | — |
| fastapi.tiangolo.com/advanced/vibe | 402 / 13 | 1717 / 1280 | 1719 / 1282 | 1081 / 676 | 1413 / 914 | 1402 / 895 | 1411 / 912 | — |
| fastapi.tiangolo.com/advanced/websockets | 1651 / 13 | 3048 / 1374 | 3046 / 1374 | 2397 / 743 | 2714 / 979 | 2714 / 960 | 2711 / 972 | — |
| fastapi.tiangolo.com/advanced/wsgi | 260 / 13 | 1565 / 1278 | 1565 / 1278 | 937 / 674 | 1276 / 918 | 1265 / 901 | 1276 / 918 | — |
| fastapi.tiangolo.com/alternatives | 3306 / 13 | 4757 / 1458 | 4759 / 1460 | 4087 / 778 | 4383 / 1020 | 4412 / 1001 | 4376 / 1013 | — |
| fastapi.tiangolo.com/async | 3664 / 13 | 5198 / 1484 | 5198 / 1484 | 4478 / 811 | 4782 / 1055 | 4805 / 1036 | 4775 / 1048 | — |
| fastapi.tiangolo.com/benchmarks | 538 / 13 | 1831 / 1256 | 1829 / 1254 | 1202 / 661 | 1537 / 897 | 1522 / 878 | 1530 / 890 | — |
| fastapi.tiangolo.com/contributing | 1612 / 13 | 3118 / 1494 | 3116 / 1494 | 2438 / 823 | 2755 / 1063 | 2765 / 1044 | 2753 / 1056 | — |
| fastapi.tiangolo.com/deployment | 253 / 13 | 1540 / 1257 | 1542 / 1259 | 915 / 659 | 1247 / 895 | 1234 / 876 | 1240 / 888 | — |
| fastapi.tiangolo.com/deployment/cloud | 155 / 13 | 1466 / 1278 | 1466 / 1278 | 833 / 675 | 1176 / 919 | 1163 / 900 | 1169 / 912 | — |
| fastapi.tiangolo.com/deployment/concepts | 3079 / 13 | 4699 / 1606 | 4701 / 1608 | 3988 / 906 | 4276 / 1144 | 4313 / 1125 | 4269 / 1137 | — |
| fastapi.tiangolo.com/deployment/docker | 4170 / 13 | 5537 / 1722 | 5539 / 1724 | 5156 / 983 | 5068 / 1225 | 5488 / 1208 | 5417 / 1220 | — |
| fastapi.tiangolo.com/deployment/fastapicloud | 308 / 13 | 1638 / 1306 | 1637 / 1306 | 1005 / 694 | 1328 / 930 | 1326 / 913 | 1334 / 925 | — |
| fastapi.tiangolo.com/deployment/https | 2106 / 13 | 3541 / 1396 | 3543 / 1398 | 2857 / 748 | 3168 / 986 | 3179 / 967 | 3161 / 979 | — |
| fastapi.tiangolo.com/deployment/manually | 811 / 13 | 2054 / 1332 | 2054 / 1334 | 1528 / 714 | 1736 / 956 | 1852 / 937 | 1814 / 954 | — |
| fastapi.tiangolo.com/deployment/server-workers | 877 / 13 | 2027 / 1296 | 2026 / 1296 | 1564 / 684 | 1725 / 928 | 1898 / 911 | 1798 / 923 | — |
| fastapi.tiangolo.com/deployment/versions | 550 / 13 | 1886 / 1318 | 1886 / 1318 | 1254 / 701 | 1580 / 941 | 1575 / 922 | 1573 / 934 | — |
| fastapi.tiangolo.com/editor-support | 323 / 13 | 1621 / 1274 | 1623 / 1276 | 998 / 672 | 1328 / 910 | 1317 / 891 | 1321 / 903 | — |
| fastapi.tiangolo.com/environment-variables | 1147 / 13 | 2462 / 1326 | 2449 / 1326 | 1862 / 712 | 2150 / 948 | 2185 / 931 | 2222 / 948 | — |
| fastapi.tiangolo.com/external-links | 712 / 13 | 1999 / 1254 | 1999 / 1254 | 1375 / 660 | 1714 / 898 | 1699 / 879 | 1707 / 891 | — |
| fastapi.tiangolo.com/fastapi-cli | 671 / 13 | 1825 / 1296 | 1827 / 1298 | 1364 / 690 | 1523 / 928 | 1684 / 909 | 1621 / 921 | — |
| fastapi.tiangolo.com/fastapi-people | 1447 / 13 | 3349 / 1432 | 3347 / 1430 | 2230 / 780 | 2536 / 1018 | 2551 / 999 | 2529 / 1011 | — |
| fastapi.tiangolo.com/features | 1167 / 13 | 2569 / 1366 | 2571 / 1368 | 1899 / 729 | 2206 / 965 | 2215 / 946 | 2204 / 963 | — |
| fastapi.tiangolo.com/help-fastapi | 1968 / 13 | 3519 / 1564 | 3519 / 1564 | 2842 / 875 | 3141 / 1119 | 3172 / 1100 | 3134 / 1112 | — |
| fastapi.tiangolo.com/history-design-future | 632 / 13 | 1946 / 1296 | 1948 / 1298 | 1315 / 680 | 1645 / 922 | 1640 / 903 | 1638 / 915 | — |
| fastapi.tiangolo.com/how-to | 110 / 13 | 1400 / 1251 | 1400 / 1251 | 764 / 651 | 1112 / 893 | 1095 / 874 | 1105 / 886 | — |
| fastapi.tiangolo.com/how-to/authentication-error-status | 207 / 13 | 1492 / 1254 | 1492 / 1254 | 861 / 651 | 1208 / 899 | 1191 / 880 | 1201 / 892 | — |
| fastapi.tiangolo.com/how-to/conditional-openapi | 393 / 13 | 1713 / 1287 | 1715 / 1289 | 1083 / 687 | 1422 / 925 | 1406 / 906 | 1415 / 918 | — |
| fastapi.tiangolo.com/how-to/configure-swagger-ui | 1577 / 13 | 2923 / 1317 | 2923 / 1317 | 2284 / 704 | 2618 / 944 | 2611 / 925 | 2611 / 937 | — |
| fastapi.tiangolo.com/how-to/custom-docs-ui-assets | 1545 / 13 | 3044 / 1481 | 3044 / 1481 | 2377 / 829 | 2702 / 1075 | 2713 / 1056 | 2700 / 1073 | — |
| fastapi.tiangolo.com/how-to/custom-request-and-route | 1523 / 13 | 2896 / 1355 | 2896 / 1355 | 2262 / 736 | 2592 / 980 | 2587 / 961 | 2585 / 973 | — |
| fastapi.tiangolo.com/how-to/extending-openapi | 772 / 13 | 2145 / 1349 | 2147 / 1351 | 1500 / 725 | 1828 / 963 | 1827 / 944 | 1826 / 961 | — |
| fastapi.tiangolo.com/how-to/general | 366 / 13 | 1806 / 1419 | 1806 / 1419 | 1152 / 783 | 1484 / 1029 | 1487 / 1010 | 1477 / 1022 | — |
| fastapi.tiangolo.com/how-to/graphql | 377 / 13 | 1705 / 1295 | 1707 / 1297 | 1068 / 688 | 1403 / 924 | 1394 / 905 | 1396 / 917 | — |
| fastapi.tiangolo.com/how-to/migrate-from-pydantic-v1-to | 957 / 13 | 2267 / 1369 | 2267 / 1369 | 1698 / 738 | 1955 / 986 | 2031 / 967 | 2025 / 979 | — |
| fastapi.tiangolo.com/how-to/separate-openapi-schemas | 900 / 13 | 2345 / 1411 | 2345 / 1411 | 1679 / 776 | 2014 / 1026 | 2017 / 1009 | 2009 / 1021 | — |
| fastapi.tiangolo.com/how-to/testing-database | 55 / 13 | 1344 / 1252 | 1344 / 1252 | 709 / 651 | 1052 / 889 | 1037 / 872 | 1047 / 884 | — |
| fastapi.tiangolo.com/learn | 48 / 13 | 1322 / 1241 | 1324 / 1243 | 697 / 646 | 1032 / 882 | 1015 / 863 | 1025 / 875 | — |
| fastapi.tiangolo.com/management | 228 / 13 | 1535 / 1280 | 1537 / 1282 | 905 / 674 | 1233 / 912 | 1224 / 893 | 1226 / 905 | — |
| fastapi.tiangolo.com/management-tasks | 1811 / 13 | 3193 / 1370 | 3195 / 1372 | 2553 / 739 | 2871 / 977 | 2876 / 960 | 2871 / 977 | — |
| fastapi.tiangolo.com/newsletter | 23 / 13 | 1299 / 1244 | 1301 / 1246 | 672 / 646 | 1014 / 888 | 997 / 869 | 1012 / 886 | — |
| fastapi.tiangolo.com/project-generation | 266 / 13 | 1568 / 1272 | 1570 / 1274 | 945 / 676 | 1285 / 918 | 1270 / 899 | 1278 / 911 | — |
| fastapi.tiangolo.com/python-types | 1905 / 13 | 3337 / 1422 | 3339 / 1424 | 2671 / 763 | 2978 / 1003 | 2995 / 984 | 2976 / 1001 | — |
| fastapi.tiangolo.com/reference | 57 / 13 | 1334 / 1241 | 1336 / 1243 | 706 / 646 | 1044 / 880 | 1029 / 863 | 1044 / 880 | — |
| fastapi.tiangolo.com/reference/apirouter | 24902 / 13 | 26603 / 1404 | 26605 / 1406 | 25651 / 746 | 25971 / 984 | 25976 / 965 | 25964 / 977 | — |
| fastapi.tiangolo.com/reference/background | 388 / 13 | 1715 / 1298 | 1715 / 1298 | 1079 / 688 | 1418 / 930 | 1403 / 911 | 1416 / 928 | — |
| fastapi.tiangolo.com/reference/dependencies | 1530 / 13 | 2839 / 1280 | 2839 / 1280 | 2206 / 673 | 2548 / 917 | 2535 / 898 | 2541 / 910 | — |
| fastapi.tiangolo.com/reference/encoders | 1130 / 13 | 2415 / 1252 | 2417 / 1254 | 1792 / 659 | 2131 / 897 | 2116 / 880 | 2131 / 897 | — |
| fastapi.tiangolo.com/reference/exceptions | 759 / 13 | 2099 / 1310 | 2097 / 1308 | 1455 / 693 | 1795 / 935 | 1784 / 918 | 1790 / 930 | — |
| fastapi.tiangolo.com/reference/fastapi | 29540 / 13 | 31322 / 1454 | 31322 / 1454 | 30321 / 778 | 30633 / 1016 | 30640 / 997 | 30626 / 1009 | — |
| fastapi.tiangolo.com/reference/httpconnection | 305 / 13 | 1669 / 1334 | 1669 / 1334 | 1022 / 714 | 1358 / 952 | 1341 / 933 | 1351 / 945 | — |
| fastapi.tiangolo.com/reference/middleware | 1043 / 13 | 2490 / 1410 | 2490 / 1410 | 1811 / 765 | 2152 / 1001 | 2135 / 982 | 2145 / 994 | — |
| fastapi.tiangolo.com/reference/openapi | 45 / 13 | 1320 / 1245 | 1322 / 1247 | 696 / 648 | 1028 / 882 | 1013 / 865 | 1023 / 877 | — |
| fastapi.tiangolo.com/reference/openapi/docs | 1770 / 13 | 3076 / 1276 | 3076 / 1276 | 2445 / 672 | 2783 / 912 | 2764 / 891 | 2774 / 903 | — |
| fastapi.tiangolo.com/reference/openapi/models | 3721 / 13 | 7396 / 3188 | 7394 / 3186 | 5672 / 1948 | 6009 / 2186 | 5992 / 2167 | 6007 / 2184 | — |
| fastapi.tiangolo.com/reference/parameters | 12469 / 13 | 13849 / 1286 | 13851 / 1288 | 13154 / 682 | 13489 / 918 | 13474 / 901 | 13484 / 913 | — |
| fastapi.tiangolo.com/reference/request | 693 / 13 | 2122 / 1388 | 2122 / 1388 | 1446 / 750 | 1784 / 988 | 1767 / 969 | 1777 / 981 | — |
| fastapi.tiangolo.com/reference/response | 664 / 13 | 2012 / 1310 | 2012 / 1310 | 1365 / 698 | 1709 / 936 | 1692 / 917 | 1702 / 929 | — |
| fastapi.tiangolo.com/reference/responses | 5521 / 13 | 7509 / 1886 | 7509 / 1886 | 6601 / 1077 | 6947 / 1329 | 6934 / 1310 | 6940 / 1322 | — |
| fastapi.tiangolo.com/reference/security | 8822 / 13 | 10907 / 1922 | 10905 / 1920 | 9911 / 1086 | 10207 / 1324 | 10232 / 1305 | 10200 / 1317 | — |
| fastapi.tiangolo.com/reference/staticfiles | 1000 / 13 | 2365 / 1332 | 2367 / 1334 | 1715 / 712 | 2058 / 954 | 2041 / 935 | 2056 / 952 | — |
| fastapi.tiangolo.com/reference/status | 1009 / 13 | 2768 / 1730 | 2770 / 1732 | 1986 / 974 | 2327 / 1218 | 2306 / 1193 | 2319 / 1210 | — |
| fastapi.tiangolo.com/reference/templating | 636 / 13 | 1974 / 1276 | 1976 / 1278 | 1314 / 675 | 1655 / 913 | 1640 / 896 | 1650 / 908 | — |
| fastapi.tiangolo.com/reference/testclient | 2181 / 13 | 3662 / 1448 | 3662 / 1448 | 2972 / 788 | 3312 / 1028 | 3297 / 1011 | 3312 / 1028 | — |
| fastapi.tiangolo.com/reference/uploadfile | 726 / 13 | 2072 / 1314 | 2070 / 1312 | 1427 / 698 | 1765 / 936 | 1750 / 917 | 1763 / 934 | — |
| fastapi.tiangolo.com/reference/websockets | 1280 / 13 | 2826 / 1466 | 2826 / 1466 | 2086 / 803 | 2419 / 1039 | 2404 / 1020 | 2412 / 1032 | — |
| fastapi.tiangolo.com/release-notes | 52954 / 13 | 59610 / 8426 | 59795 / 8426 | 57519 / 4562 | 56030 / 4800 | 57836 / 4781 | 56208 / 4793 | — |
| fastapi.tiangolo.com/resources | 27 / 13 | 1302 / 1241 | 1302 / 1241 | 676 / 646 | 1014 / 882 | 997 / 863 | 1007 / 875 | — |
| fastapi.tiangolo.com/tutorial | 587 / 13 | 1719 / 1270 | 1717 / 1268 | 1255 / 665 | 1423 / 907 | 1579 / 888 | 1526 / 905 | — |
| fastapi.tiangolo.com/tutorial/background-tasks | 987 / 13 | 2334 / 1325 | 2336 / 1327 | 1695 / 705 | 2021 / 943 | 2018 / 924 | 2014 / 936 | — |
| fastapi.tiangolo.com/tutorial/bigger-applications | 3340 / 13 | 4914 / 1567 | 4912 / 1565 | 4229 / 886 | 4534 / 1130 | 4557 / 1111 | 4532 / 1128 | — |
| fastapi.tiangolo.com/tutorial/body | 1244 / 13 | 2652 / 1381 | 2652 / 1381 | 1994 / 747 | 2314 / 985 | 2317 / 966 | 2307 / 978 | — |
| fastapi.tiangolo.com/tutorial/body-fields | 665 / 13 | 1989 / 1297 | 1989 / 1297 | 1354 / 686 | 1689 / 926 | 1680 / 907 | 1682 / 919 | — |
| fastapi.tiangolo.com/tutorial/body-multiple-params | 1418 / 13 | 2781 / 1341 | 2781 / 1341 | 2142 / 721 | 2473 / 963 | 2468 / 944 | 2466 / 956 | — |
| fastapi.tiangolo.com/tutorial/body-nested-models | 1476 / 13 | 2929 / 1443 | 2927 / 1441 | 2270 / 791 | 2584 / 1031 | 2597 / 1014 | 2579 / 1026 | — |
| fastapi.tiangolo.com/tutorial/body-updates | 1024 / 13 | 2377 / 1333 | 2377 / 1333 | 1743 / 716 | 2068 / 954 | 2065 / 937 | 2063 / 949 | — |
| fastapi.tiangolo.com/tutorial/cookie-param-models | 601 / 13 | 1932 / 1303 | 1932 / 1303 | 1296 / 692 | 1628 / 932 | 1619 / 913 | 1621 / 925 | — |
| fastapi.tiangolo.com/tutorial/cookie-params | 378 / 13 | 1686 / 1281 | 1688 / 1283 | 1058 / 677 | 1388 / 913 | 1379 / 896 | 1383 / 908 | — |
| fastapi.tiangolo.com/tutorial/cors | 765 / 13 | 2109 / 1323 | 2109 / 1323 | 1467 / 699 | 1794 / 941 | 1791 / 922 | 1792 / 939 | — |
| fastapi.tiangolo.com/tutorial/debugging | 393 / 13 | 1735 / 1303 | 1733 / 1301 | 1090 / 694 | 1425 / 930 | 1408 / 911 | 1418 / 923 | — |
| fastapi.tiangolo.com/tutorial/dependencies | 1806 / 13 | 3109 / 1334 | 3111 / 1336 | 2521 / 712 | 2786 / 948 | 2841 / 929 | 2784 / 946 | — |
| fastapi.tiangolo.com/tutorial/dependencies/classes-as-d | 1956 / 13 | 3312 / 1333 | 3312 / 1333 | 2673 / 714 | 2998 / 954 | 2993 / 935 | 2991 / 947 | — |
| fastapi.tiangolo.com/tutorial/dependencies/dependencies | 913 / 13 | 2286 / 1357 | 2286 / 1357 | 1648 / 732 | 1976 / 976 | 1973 / 957 | 1974 / 974 | — |
| fastapi.tiangolo.com/tutorial/dependencies/dependencies | 2593 / 13 | 3819 / 1467 | 3819 / 1467 | 3414 / 818 | 3479 / 1058 | 3735 / 1039 | 3719 / 1051 | — |
| fastapi.tiangolo.com/tutorial/dependencies/global-depen | 295 / 13 | 1603 / 1275 | 1603 / 1275 | 973 / 675 | 1312 / 913 | 1297 / 894 | 1305 / 906 | — |
| fastapi.tiangolo.com/tutorial/dependencies/sub-dependen | 877 / 13 | 2211 / 1319 | 2213 / 1321 | 1586 / 706 | 1903 / 942 | 1908 / 923 | 1913 / 940 | — |
| fastapi.tiangolo.com/tutorial/encoder | 294 / 13 | 1590 / 1265 | 1592 / 1267 | 965 / 668 | 1304 / 908 | 1289 / 889 | 1302 / 906 | — |
| fastapi.tiangolo.com/tutorial/extra-data-types | 726 / 13 | 2028 / 1273 | 2028 / 1273 | 1401 / 672 | 1738 / 912 | 1725 / 893 | 1731 / 905 | — |
| fastapi.tiangolo.com/tutorial/extra-models | 1232 / 13 | 2649 / 1405 | 2649 / 1405 | 1998 / 763 | 2313 / 999 | 2322 / 982 | 2308 / 994 | — |
| fastapi.tiangolo.com/tutorial/first-steps | 1797 / 13 | 3327 / 1589 | 3329 / 1591 | 2693 / 893 | 2816 / 1129 | 3015 / 1112 | 2916 / 1124 | — |
| fastapi.tiangolo.com/tutorial/handling-errors | 1723 / 13 | 3161 / 1421 | 3161 / 1421 | 2503 / 777 | 2819 / 1015 | 2826 / 996 | 2812 / 1008 | — |
| fastapi.tiangolo.com/tutorial/header-param-models | 715 / 13 | 2059 / 1315 | 2059 / 1315 | 1420 / 702 | 1751 / 940 | 1746 / 923 | 1751 / 940 | — |
| fastapi.tiangolo.com/tutorial/header-params | 710 / 13 | 2033 / 1301 | 2033 / 1301 | 1402 / 689 | 1730 / 927 | 1723 / 908 | 1723 / 920 | — |
| fastapi.tiangolo.com/tutorial/metadata | 1185 / 13 | 2563 / 1361 | 2561 / 1359 | 1917 / 729 | 2240 / 971 | 2241 / 952 | 2233 / 964 | — |
| fastapi.tiangolo.com/tutorial/middleware | 611 / 13 | 1951 / 1301 | 1951 / 1301 | 1308 / 694 | 1644 / 930 | 1635 / 911 | 1637 / 923 | — |
| fastapi.tiangolo.com/tutorial/path-operation-configurat | 913 / 13 | 2278 / 1341 | 2278 / 1341 | 1632 / 716 | 1956 / 956 | 1955 / 937 | 1949 / 949 | — |
| fastapi.tiangolo.com/tutorial/path-params | 1556 / 13 | 3029 / 1469 | 3029 / 1469 | 2360 / 801 | 2659 / 1039 | 2680 / 1020 | 2652 / 1032 | — |
| fastapi.tiangolo.com/tutorial/path-params-numeric-valid | 1747 / 13 | 3179 / 1399 | 3179 / 1399 | 2518 / 768 | 2847 / 1012 | 2848 / 993 | 2840 / 1005 | — |
| fastapi.tiangolo.com/tutorial/query-param-models | 551 / 13 | 1887 / 1305 | 1887 / 1305 | 1250 / 696 | 1586 / 936 | 1577 / 917 | 1579 / 929 | — |
| fastapi.tiangolo.com/tutorial/query-params | 876 / 13 | 2208 / 1311 | 2210 / 1313 | 1578 / 699 | 1905 / 937 | 1898 / 918 | 1898 / 930 | — |
| fastapi.tiangolo.com/tutorial/query-params-str-validati | 4084 / 13 | 5684 / 1593 | 5684 / 1593 | 4987 / 900 | 5283 / 1142 | 5316 / 1125 | 5278 / 1137 | — |
| fastapi.tiangolo.com/tutorial/request-files | 1804 / 13 | 3199 / 1373 | 3201 / 1375 | 2548 / 741 | 2867 / 979 | 2870 / 960 | 2865 / 977 | — |
| fastapi.tiangolo.com/tutorial/request-form-models | 458 / 13 | 1782 / 1299 | 1782 / 1299 | 1152 / 691 | 1481 / 929 | 1472 / 910 | 1474 / 922 | — |
| fastapi.tiangolo.com/tutorial/request-forms | 501 / 13 | 1824 / 1293 | 1826 / 1295 | 1189 / 685 | 1519 / 923 | 1510 / 904 | 1512 / 916 | — |
| fastapi.tiangolo.com/tutorial/request-forms-and-files | 401 / 13 | 1723 / 1295 | 1721 / 1293 | 1091 / 687 | 1424 / 927 | 1415 / 910 | 1419 / 922 | — |
| fastapi.tiangolo.com/tutorial/response-model | 3163 / 13 | 4718 / 1555 | 4716 / 1553 | 4040 / 874 | 4346 / 1122 | 4367 / 1099 | 4335 / 1111 | — |
| fastapi.tiangolo.com/tutorial/response-status-code | 639 / 13 | 1964 / 1295 | 1964 / 1295 | 1332 / 690 | 1665 / 930 | 1654 / 911 | 1658 / 923 | — |
| fastapi.tiangolo.com/tutorial/schema-extra-example | 2019 / 13 | 3481 / 1451 | 3483 / 1453 | 2823 / 801 | 3139 / 1043 | 3150 / 1024 | 3132 / 1036 | — |
| fastapi.tiangolo.com/tutorial/security | 700 / 13 | 2010 / 1288 | 2012 / 1290 | 1381 / 678 | 1705 / 914 | 1702 / 895 | 1698 / 907 | — |
| fastapi.tiangolo.com/tutorial/security/first-steps | 1539 / 13 | 2915 / 1355 | 2915 / 1355 | 2263 / 721 | 2588 / 963 | 2587 / 944 | 2581 / 956 | — |
| fastapi.tiangolo.com/tutorial/security/get-current-user | 1550 / 13 | 2913 / 1339 | 2915 / 1341 | 2269 / 716 | 2600 / 956 | 2597 / 937 | 2598 / 954 | — |
| fastapi.tiangolo.com/tutorial/security/oauth2-jwt | 4431 / 13 | 5893 / 1431 | 5893 / 1431 | 5212 / 778 | 5552 / 1030 | 5549 / 1011 | 5550 / 1028 | — |
| fastapi.tiangolo.com/tutorial/security/simple-oauth2 | 3609 / 13 | 5078 / 1455 | 5080 / 1457 | 4405 / 793 | 4726 / 1039 | 4741 / 1020 | 4719 / 1032 | — |
| fastapi.tiangolo.com/tutorial/server-sent-events | 1462 / 13 | 2837 / 1359 | 2837 / 1359 | 2195 / 730 | 2515 / 968 | 2518 / 951 | 2510 / 963 | — |
| fastapi.tiangolo.com/tutorial/sql-databases | 10604 / 13 | 12264 / 1637 | 12262 / 1635 | 11545 / 938 | 11842 / 1176 | 11872 / 1159 | 11837 / 1171 | — |
| fastapi.tiangolo.com/tutorial/static-files | 258 / 13 | 1575 / 1293 | 1575 / 1293 | 944 / 683 | 1274 / 921 | 1265 / 902 | 1267 / 914 | — |
| fastapi.tiangolo.com/tutorial/stream-json-lines | 1227 / 13 | 2544 / 1343 | 2544 / 1343 | 1950 / 720 | 2224 / 958 | 2276 / 941 | 2272 / 953 | — |
| fastapi.tiangolo.com/tutorial/testing | 1498 / 13 | 2853 / 1341 | 2851 / 1339 | 2217 / 716 | 2533 / 952 | 2534 / 933 | 2526 / 945 | — |
| fastapi.tiangolo.com/virtual-environments | 3022 / 13 | 4539 / 1524 | 4528 / 1524 | 3869 / 844 | 4153 / 1082 | 4191 / 1063 | 4264 / 1075 | — |
| fastapi.tiangolo.com/zh-hant | 1139 / 13 | 2714 / 1341 | 2714 / 1341 | 1786 / 637 | 2068 / 869 | 2098 / 852 | 2051 / 852 | — |

</details>

## python-docs

| Tool | Avg words | Preamble [1] | Repeat rate | Junk found | Headings | Code blocks | Precision | Recall |
|---|---|---|---|---|---|---|---|---|
| **markcrawl** | **3766** | **5** | **0%** | **378** | **11.9** | **7.3** | **98%** | **82%** |
| crawl4ai | 4180 | 50 [!] | 0% | 3111 | 19.4 | 7.4 | 100% | 70% |
| crawl4ai-raw | 4180 | 50 [!] | 0% | 3111 | 19.4 | 7.4 | 100% | 70% |
| scrapy+md | 4796 | 4 | 0% | 2086 | 22.7 | 9.5 | 100% | 99% |
| crawlee | 4140 | 47 | 0% | 3111 | 19.1 | 7.3 | 100% | 92% |
| colly+md | 4070 | 26 | 0% | 3111 | 19.1 | 7.3 | 100% | 92% |
| playwright | 4140 | 47 | 0% | 3111 | 19.1 | 7.3 | 100% | 92% |
| firecrawl | — | — | — | — | — | — | — | — |

**[1]** Avg words per page before the first heading (nav chrome). **[!]** = likely nav/boilerplate problem (preamble >50 or repeat rate >20%).

**Reading the numbers:**
**scrapy+md** produces the cleanest output with 4 words of preamble per page, while **crawl4ai** injects 50 words of nav chrome before content begins.

<details>
<summary>Sample output — first 40 lines of <code>docs.python.org/3.10/whatsnew/2.2.html</code></summary>

This shows what each tool outputs at the *top* of the same page.
Nav boilerplate appears here before the real content starts.

**markcrawl**
```
# What’s New in Python 2.2[¶](#what-s-new-in-python-2-2 "Permalink to this headline")

Author
:   A.M. Kuchling

## Introduction[¶](#introduction "Permalink to this headline")

This article explains the new features in Python 2.2.2, released on October 14,
2002. Python 2.2.2 is a bugfix release of Python 2.2, originally released on
December 21, 2001.

Python 2.2 can be thought of as the “cleanup release”. There are some features
such as generators and iterators that are completely new, but most of the
changes, significant and far-reaching though they may be, are aimed at cleaning
up irregularities and dark corners of the language design.

This article doesn’t attempt to provide a complete specification of the new
features, but instead provides a convenient overview. For full details, you
should refer to the documentation for Python 2.2, such as the [Python Library
Reference](https://docs.python.org/2.2/lib/lib.html) and the [Python
Reference Manual](https://docs.python.org/2.2/ref/ref.html). If you want to
understand the complete implementation and design rationale for a change, refer
to the PEP for a particular new feature.

## PEPs 252 and 253: Type and Class Changes[¶](#peps-252-and-253-type-and-class-changes "Permalink to this headline")

The largest and most far-reaching changes in Python 2.2 are to Python’s model of
objects and classes. The changes should be backward compatible, so it’s likely
that your code will continue to run unchanged, but the changes provide some
amazing new capabilities. Before beginning this, the longest and most
complicated section of this article, I’ll provide an overview of the changes and
offer some comments.

A long time ago I wrote a web page listing flaws in Python’s design. One of the
most significant flaws was that it’s impossible to subclass Python types
implemented in C. In particular, it’s not possible to subclass built-in types,
so you can’t just subclass, say, lists in order to add a single useful method to
them. The `UserList` module provides a class that supports all of the
methods of lists and that can be subclassed further, but there’s lots of C code
that expects a regular Python list and won’t accept a `UserList`
```

**crawl4ai**
```
[ ![Python logo](https://docs.python.org/3.10/_static/py.svg) ](https://www.python.org/) dev (3.15) 3.14 3.13 3.12 3.11 3.10.20 3.9 3.8 3.7 3.6 3.5 3.4 3.3 3.2 3.1 3.0 2.7 2.6
Greek | Ελληνικά English Spanish | español French | français Italian | italiano Japanese | 日本語 Korean | 한국어 Polish | polski Brazilian Portuguese | Português brasileiro Romanian | Românește Turkish | Türkçe Simplified Chinese | 简体中文 Traditional Chinese | 繁體中文
Theme  Auto Light Dark
### [Table of Contents](https://docs.python.org/3.10/contents.html)
  * [What’s New in Python 2.2](https://docs.python.org/3.10/whatsnew/2.2.html#)
    * [Introduction](https://docs.python.org/3.10/whatsnew/2.2.html#introduction)
    * [PEPs 252 and 253: Type and Class Changes](https://docs.python.org/3.10/whatsnew/2.2.html#peps-252-and-253-type-and-class-changes)
      * [Old and New Classes](https://docs.python.org/3.10/whatsnew/2.2.html#old-and-new-classes)
      * [Descriptors](https://docs.python.org/3.10/whatsnew/2.2.html#descriptors)
      * [Multiple Inheritance: The Diamond Rule](https://docs.python.org/3.10/whatsnew/2.2.html#multiple-inheritance-the-diamond-rule)
      * [Attribute Access](https://docs.python.org/3.10/whatsnew/2.2.html#attribute-access)
      * [Related Links](https://docs.python.org/3.10/whatsnew/2.2.html#related-links)
    * [PEP 234: Iterators](https://docs.python.org/3.10/whatsnew/2.2.html#pep-234-iterators)
    * [PEP 255: Simple Generators](https://docs.python.org/3.10/whatsnew/2.2.html#pep-255-simple-generators)
    * [PEP 237: Unifying Long Integers and Integers](https://docs.python.org/3.10/whatsnew/2.2.html#pep-237-unifying-long-integers-and-integers)
    * [PEP 238: Changing the Division Operator](https://docs.python.org/3.10/whatsnew/2.2.html#pep-238-changing-the-division-operator)
    * [Unicode Changes](https://docs.python.org/3.10/whatsnew/2.2.html#unicode-changes)
    * [PEP 227: Nested Scopes](https://docs.python.org/3.10/whatsnew/2.2.html#pep-227-nested-scopes)
    * [New and Improved Modules](https://docs.python.org/3.10/whatsnew/2.2.html#new-and-improved-modules)
    * [Interpreter Changes and Fixes](https://docs.python.org/3.10/whatsnew/2.2.html#interpreter-changes-and-fixes)
    * [Other Changes and Fixes](https://docs.python.org/3.10/whatsnew/2.2.html#other-changes-and-fixes)
    * [Acknowledgements](https://docs.python.org/3.10/whatsnew/2.2.html#acknowledgements)


#### Previous topic
[What’s New in Python 2.3](https://docs.python.org/3.10/whatsnew/2.3.html "previous chapter")
#### Next topic
[What’s New in Python 2.1](https://docs.python.org/3.10/whatsnew/2.1.html "next chapter")
### This Page
  * [Report a Bug](https://docs.python.org/3.10/bugs.html)
  * [Show Source ](https://github.com/python/cpython/blob/3.10/Doc/whatsnew/2.2.rst)


### Navigation
  * [index](https://docs.python.org/3.10/genindex.html "General Index")
  * [modules](https://docs.python.org/3.10/py-modindex.html "Python Module Index") |
  * [next](https://docs.python.org/3.10/whatsnew/2.1.html "What’s New in Python 2.1") |
  * [previous](https://docs.python.org/3.10/whatsnew/2.3.html "What’s New in Python 2.3") |
  * ![Python logo](https://docs.python.org/3.10/_static/py.svg)
  * [Python](https://www.python.org/) »
```

**crawl4ai-raw**
```
[ ![Python logo](https://docs.python.org/3.10/_static/py.svg) ](https://www.python.org/) dev (3.15) 3.14 3.13 3.12 3.11 3.10.20 3.9 3.8 3.7 3.6 3.5 3.4 3.3 3.2 3.1 3.0 2.7 2.6
Greek | Ελληνικά English Spanish | español French | français Italian | italiano Japanese | 日本語 Korean | 한국어 Polish | polski Brazilian Portuguese | Português brasileiro Romanian | Românește Turkish | Türkçe Simplified Chinese | 简体中文 Traditional Chinese | 繁體中文
Theme  Auto Light Dark
### [Table of Contents](https://docs.python.org/3.10/contents.html)
  * [What’s New in Python 2.2](https://docs.python.org/3.10/whatsnew/2.2.html#)
    * [Introduction](https://docs.python.org/3.10/whatsnew/2.2.html#introduction)
    * [PEPs 252 and 253: Type and Class Changes](https://docs.python.org/3.10/whatsnew/2.2.html#peps-252-and-253-type-and-class-changes)
      * [Old and New Classes](https://docs.python.org/3.10/whatsnew/2.2.html#old-and-new-classes)
      * [Descriptors](https://docs.python.org/3.10/whatsnew/2.2.html#descriptors)
      * [Multiple Inheritance: The Diamond Rule](https://docs.python.org/3.10/whatsnew/2.2.html#multiple-inheritance-the-diamond-rule)
      * [Attribute Access](https://docs.python.org/3.10/whatsnew/2.2.html#attribute-access)
      * [Related Links](https://docs.python.org/3.10/whatsnew/2.2.html#related-links)
    * [PEP 234: Iterators](https://docs.python.org/3.10/whatsnew/2.2.html#pep-234-iterators)
    * [PEP 255: Simple Generators](https://docs.python.org/3.10/whatsnew/2.2.html#pep-255-simple-generators)
    * [PEP 237: Unifying Long Integers and Integers](https://docs.python.org/3.10/whatsnew/2.2.html#pep-237-unifying-long-integers-and-integers)
    * [PEP 238: Changing the Division Operator](https://docs.python.org/3.10/whatsnew/2.2.html#pep-238-changing-the-division-operator)
    * [Unicode Changes](https://docs.python.org/3.10/whatsnew/2.2.html#unicode-changes)
    * [PEP 227: Nested Scopes](https://docs.python.org/3.10/whatsnew/2.2.html#pep-227-nested-scopes)
    * [New and Improved Modules](https://docs.python.org/3.10/whatsnew/2.2.html#new-and-improved-modules)
    * [Interpreter Changes and Fixes](https://docs.python.org/3.10/whatsnew/2.2.html#interpreter-changes-and-fixes)
    * [Other Changes and Fixes](https://docs.python.org/3.10/whatsnew/2.2.html#other-changes-and-fixes)
    * [Acknowledgements](https://docs.python.org/3.10/whatsnew/2.2.html#acknowledgements)


#### Previous topic
[What’s New in Python 2.3](https://docs.python.org/3.10/whatsnew/2.3.html "previous chapter")
#### Next topic
[What’s New in Python 2.1](https://docs.python.org/3.10/whatsnew/2.1.html "next chapter")
### This Page
  * [Report a Bug](https://docs.python.org/3.10/bugs.html)
  * [Show Source ](https://github.com/python/cpython/blob/3.10/Doc/whatsnew/2.2.rst)


### Navigation
  * [index](https://docs.python.org/3.10/genindex.html "General Index")
  * [modules](https://docs.python.org/3.10/py-modindex.html "Python Module Index") |
  * [next](https://docs.python.org/3.10/whatsnew/2.1.html "What’s New in Python 2.1") |
  * [previous](https://docs.python.org/3.10/whatsnew/2.3.html "What’s New in Python 2.3") |
  * ![Python logo](https://docs.python.org/3.10/_static/py.svg)
  * [Python](https://www.python.org/) »
```

**scrapy+md**
```
Theme
Auto
Light
Dark

### [Table of Contents](../contents.html)

* [What’s New in Python 2.2](#)
  + [Introduction](#introduction)
  + [PEPs 252 and 253: Type and Class Changes](#peps-252-and-253-type-and-class-changes)
    - [Old and New Classes](#old-and-new-classes)
    - [Descriptors](#descriptors)
    - [Multiple Inheritance: The Diamond Rule](#multiple-inheritance-the-diamond-rule)
    - [Attribute Access](#attribute-access)
    - [Related Links](#related-links)
  + [PEP 234: Iterators](#pep-234-iterators)
  + [PEP 255: Simple Generators](#pep-255-simple-generators)
  + [PEP 237: Unifying Long Integers and Integers](#pep-237-unifying-long-integers-and-integers)
  + [PEP 238: Changing the Division Operator](#pep-238-changing-the-division-operator)
  + [Unicode Changes](#unicode-changes)
  + [PEP 227: Nested Scopes](#pep-227-nested-scopes)
  + [New and Improved Modules](#new-and-improved-modules)
  + [Interpreter Changes and Fixes](#interpreter-changes-and-fixes)
  + [Other Changes and Fixes](#other-changes-and-fixes)
  + [Acknowledgements](#acknowledgements)

#### Previous topic

[What’s New in Python 2.3](2.3.html "previous chapter")

#### Next topic

[What’s New in Python 2.1](2.1.html "next chapter")

### This Page

* [Report a Bug](../bugs.html)
* [Show Source](https://github.com/python/cpython/blob/3.10/Doc/whatsnew/2.2.rst)

### Navigation
```

**crawlee**
```
What’s New in Python 2.2 — Python 3.10.20 documentation

















@media only screen {
table.full-width-table {
width: 100%;
}
}



dev (3.15)3.143.133.123.113.10.203.93.83.73.63.53.43.33.23.13.02.72.6

Greek | ΕλληνικάEnglishSpanish | españolFrench | françaisItalian | italianoJapanese | 日本語Korean | 한국어Polish | polskiBrazilian Portuguese | Português brasileiroRomanian | RomâneșteTurkish | TürkçeSimplified Chinese | 简体中文Traditional Chinese | 繁體中文

Theme
Auto
Light
Dark

### [Table of Contents](../contents.html)

* [What’s New in Python 2.2](#)
  + [Introduction](#introduction)
  + [PEPs 252 and 253: Type and Class Changes](#peps-252-and-253-type-and-class-changes)
```

**colly+md**
```
What’s New in Python 2.2 — Python 3.10.20 documentation

















@media only screen {
table.full-width-table {
width: 100%;
}
}



Theme
Auto
Light
Dark

### [Table of Contents](../contents.html)

* [What’s New in Python 2.2](#)
  + [Introduction](#introduction)
  + [PEPs 252 and 253: Type and Class Changes](#peps-252-and-253-type-and-class-changes)
    - [Old and New Classes](#old-and-new-classes)
    - [Descriptors](#descriptors)
    - [Multiple Inheritance: The Diamond Rule](#multiple-inheritance-the-diamond-rule)
    - [Attribute Access](#attribute-access)
```

**playwright**
```
What’s New in Python 2.2 — Python 3.10.20 documentation

















@media only screen {
table.full-width-table {
width: 100%;
}
}



dev (3.15)3.143.133.123.113.10.203.93.83.73.63.53.43.33.23.13.02.72.6

Greek | ΕλληνικάEnglishSpanish | españolFrench | françaisItalian | italianoJapanese | 日本語Korean | 한국어Polish | polskiBrazilian Portuguese | Português brasileiroRomanian | RomâneșteTurkish | TürkçeSimplified Chinese | 简体中文Traditional Chinese | 繁體中文

Theme
Auto
Light
Dark

### [Table of Contents](../contents.html)

* [What’s New in Python 2.2](#)
  + [Introduction](#introduction)
  + [PEPs 252 and 253: Type and Class Changes](#peps-252-and-253-type-and-class-changes)
```

**firecrawl** — no output for this URL

</details>

<details>
<summary>Per-page word counts and preamble [1]</summary>

| URL | markcrawl words / preamble [1] | crawl4ai words / preamble [1] | crawl4ai-raw words / preamble [1] | scrapy+md words / preamble [1] | crawlee words / preamble [1] | colly+md words / preamble [1] | playwright words / preamble [1] | firecrawl words / preamble [1] |
|---|---|---|---|---|---|---|---|---|
| docs.python.org/2.6 | 189 / 0 | 323 / 0 | 323 / 0 | — | 349 / 20 | 349 / 20 | 349 / 20 | — |
| docs.python.org/2.7 | 186 / 0 | 320 / 28 | 320 / 28 | — | 315 / 30 | 309 / 30 | 315 / 30 | — |
| docs.python.org/2.7/about.html | 179 / 0 | 352 / 28 | 352 / 28 | — | 343 / 34 | 337 / 34 | 343 / 34 | — |
| docs.python.org/2.7/bugs.html | 604 / 0 | 787 / 28 | 787 / 28 | — | 779 / 33 | 773 / 33 | 779 / 33 | — |
| docs.python.org/2.7/c-api/index.html | 276 / 0 | 447 / 28 | 447 / 28 | — | 439 / 35 | 433 / 35 | 439 / 35 | — |
| docs.python.org/2.7/contents.html | 12899 / 0 | 13051 / 28 | 13051 / 28 | — | 13041 / 34 | 13035 / 34 | 13041 / 34 | — |
| docs.python.org/2.7/download.html | 246 / 0 | 384 / 28 | 384 / 28 | — | 357 / 32 | 351 / 32 | 357 / 32 | — |
| docs.python.org/2.7/extending/index.html | 394 / 0 | 574 / 28 | 574 / 28 | — | 568 / 37 | 562 / 37 | 568 / 37 | — |
| docs.python.org/2.7/glossary.html | 5184 / 0 | 5287 / 28 | 5287 / 28 | — | 5356 / 32 | 5350 / 32 | 5356 / 32 | — |
| docs.python.org/2.7/howto/index.html | 52 / 0 | 304 / 28 | 304 / 28 | — | 294 / 33 | 288 / 33 | 294 / 33 | — |
| docs.python.org/2.7/installing/index.html | 1143 / 0 | 1421 / 28 | 1421 / 28 | — | 1413 / 34 | 1407 / 34 | 1413 / 34 | — |
| docs.python.org/2.7/library/index.html | 2969 / 0 | 3138 / 28 | 3138 / 28 | — | 3129 / 35 | 3123 / 35 | 3129 / 35 | — |
| docs.python.org/2.7/license.html | 6376 / 0 | 6656 / 28 | 6656 / 28 | — | 6647 / 34 | 6641 / 34 | 6647 / 34 | — |
| docs.python.org/2.7/py-modindex.html | 5398 / 0 | 5580 / 28 | 5580 / 28 | — | 5565 / 37 | 5559 / 37 | 5565 / 37 | — |
| docs.python.org/2.7/reference/index.html | 380 / 0 | 554 / 28 | 554 / 28 | — | 546 / 35 | 540 / 35 | 546 / 35 | — |
| docs.python.org/2.7/tutorial/index.html | 928 / 0 | 1105 / 28 | 1105 / 28 | — | 1096 / 34 | 1090 / 34 | 1096 / 34 | — |
| docs.python.org/2.7/using/index.html | 248 / 0 | 419 / 28 | 419 / 28 | — | 411 / 35 | 405 / 35 | 411 / 35 | — |
| docs.python.org/2.7/whatsnew/2.7.html | 16861 / 0 | 17267 / 28 | 17267 / 28 | — | 17275 / 36 | 17269 / 36 | 17275 / 36 | — |
| docs.python.org/2.7/whatsnew/index.html | 823 / 0 | 997 / 28 | 997 / 28 | — | 989 / 35 | 983 / 35 | 989 / 35 | — |
| docs.python.org/3.0 | 183 / 0 | 281 / 0 | 281 / 0 | — | 307 / 20 | 307 / 20 | 307 / 20 | — |
| docs.python.org/3.0/about.html | 878 / 0 | 1003 / 0 | 1003 / 0 | — | 1021 / 22 | 1021 / 22 | 1021 / 22 | — |
| docs.python.org/3.0/bugs.html | 459 / 0 | 531 / 0 | 531 / 0 | — | 553 / 23 | 553 / 23 | 553 / 23 | — |
| docs.python.org/3.0/c-api/index.html | 288 / 0 | 363 / 0 | 363 / 0 | — | 386 / 23 | 386 / 23 | 386 / 23 | — |
| docs.python.org/3.0/contents.html | 8408 / 0 | 8477 / 0 | 8477 / 0 | — | 8495 / 22 | 8495 / 22 | 8495 / 22 | — |
| docs.python.org/3.0/copyright.html | 94 / 0 | 176 / 0 | 176 / 0 | — | 191 / 20 | 191 / 20 | 191 / 20 | — |
| docs.python.org/3.0/distutils/index.html | 632 / 0 | 711 / 0 | 711 / 0 | — | 733 / 22 | 733 / 22 | 733 / 22 | — |
| docs.python.org/3.0/documenting/index.html | 240 / 0 | 314 / 0 | 314 / 0 | — | 332 / 21 | 332 / 21 | 332 / 21 | — |
| docs.python.org/3.0/download.html | 243 / 0 | 297 / 0 | 297 / 0 | — | 314 / 20 | 314 / 20 | 314 / 20 | — |
| docs.python.org/3.0/extending/index.html | 375 / 0 | 454 / 0 | 454 / 0 | — | 479 / 25 | 479 / 25 | 479 / 25 | — |
| docs.python.org/3.0/genindex.html | 91 / 0 | 198 / 0 | 198 / 0 | — | 211 / 20 | 211 / 20 | 211 / 20 | — |
| docs.python.org/3.0/glossary.html | 3770 / 0 | 3791 / 0 | 3791 / 0 | — | 3871 / 20 | 3871 / 20 | 3871 / 20 | — |
| docs.python.org/3.0/howto/index.html | 141 / 0 | 223 / 0 | 223 / 0 | — | 241 / 21 | 241 / 21 | 241 / 21 | — |
| docs.python.org/3.0/install/index.html | 6166 / 0 | 6261 / 0 | 6261 / 0 | — | 6259 / 22 | 6259 / 22 | 6259 / 22 | — |
| docs.python.org/3.0/library/index.html | 2022 / 0 | 2093 / 0 | 2093 / 0 | — | 2116 / 23 | 2116 / 23 | 2116 / 23 | — |
| docs.python.org/3.0/license.html | 4649 / 0 | 4803 / 0 | 4803 / 0 | — | 4822 / 22 | 4822 / 22 | 4822 / 22 | — |
| docs.python.org/3.0/modindex.html | 3599 / 0 | 3667 / 0 | 3667 / 0 | — | 3669 / 25 | 3669 / 25 | 3669 / 25 | — |
| docs.python.org/3.0/reference/index.html | 357 / 0 | 432 / 0 | 432 / 0 | — | 455 / 23 | 455 / 23 | 455 / 23 | — |
| docs.python.org/3.0/search.html | 51 / 0 | 105 / 0 | 105 / 0 | — | 122 / 20 | 122 / 20 | 122 / 20 | — |
| docs.python.org/3.0/tutorial/index.html | 840 / 0 | 919 / 0 | 919 / 0 | — | 941 / 22 | 941 / 22 | 941 / 22 | — |
| docs.python.org/3.0/using/index.html | 240 / 0 | 326 / 0 | 326 / 0 | — | 344 / 21 | 344 / 21 | 344 / 21 | — |
| docs.python.org/3.0/whatsnew/3.0.html | 5433 / 0 | 5676 / 0 | 5676 / 0 | — | 5689 / 24 | 5689 / 24 | 5689 / 24 | — |
| docs.python.org/3.0/whatsnew/index.html | 836 / 0 | 919 / 0 | 919 / 0 | — | 938 / 23 | 938 / 23 | 938 / 23 | — |
| docs.python.org/3.1 | 191 / 0 | 315 / 0 | 315 / 0 | — | 341 / 20 | 341 / 20 | 341 / 20 | — |
| docs.python.org/3.1/about.html | 881 / 0 | 1016 / 0 | 1016 / 0 | — | 1035 / 22 | 1035 / 22 | 1035 / 22 | — |
| docs.python.org/3.1/bugs.html | 538 / 0 | 676 / 0 | 676 / 0 | — | 696 / 21 | 696 / 21 | 696 / 21 | — |
| docs.python.org/3.1/c-api/index.html | 328 / 0 | 418 / 0 | 418 / 0 | — | 441 / 23 | 441 / 23 | 441 / 23 | — |
| docs.python.org/3.1/contents.html | 11438 / 0 | 11520 / 0 | 11520 / 0 | — | 11538 / 22 | 11538 / 22 | 11538 / 22 | — |
| docs.python.org/3.1/copyright.html | 96 / 0 | 187 / 0 | 187 / 0 | — | 202 / 20 | 202 / 20 | 202 / 20 | — |
| docs.python.org/3.1/distutils/index.html | 736 / 0 | 830 / 0 | 830 / 0 | — | 852 / 22 | 852 / 22 | 852 / 22 | — |
| docs.python.org/3.1/documenting/index.html | 188 / 0 | 277 / 0 | 277 / 0 | — | 295 / 21 | 295 / 21 | 295 / 21 | — |
| docs.python.org/3.1/download.html | 243 / 0 | 310 / 0 | 310 / 0 | — | 327 / 20 | 327 / 20 | 327 / 20 | — |
| docs.python.org/3.1/extending/index.html | 410 / 0 | 506 / 0 | 506 / 0 | — | 531 / 25 | 531 / 25 | 531 / 25 | — |
| docs.python.org/3.1/faq/index.html | 29 / 29 | 204 / 0 | 204 / 0 | — | 227 / 23 | 227 / 23 | 227 / 23 | — |
| docs.python.org/3.1/genindex.html | 104 / 0 | 211 / 0 | 211 / 0 | — | 228 / 20 | 228 / 20 | 228 / 20 | — |
| docs.python.org/3.1/glossary.html | 4196 / 0 | 4228 / 0 | 4228 / 0 | — | 4314 / 20 | 4314 / 20 | 4314 / 20 | — |
| docs.python.org/3.1/howto/index.html | 152 / 0 | 245 / 0 | 245 / 0 | — | 263 / 21 | 263 / 21 | 263 / 21 | — |
| docs.python.org/3.1/install/index.html | 6226 / 0 | 6339 / 0 | 6339 / 0 | — | 6334 / 22 | 6334 / 22 | 6334 / 22 | — |
| docs.python.org/3.1/library/index.html | 2300 / 0 | 2388 / 0 | 2388 / 0 | — | 2411 / 23 | 2411 / 23 | 2411 / 23 | — |
| docs.python.org/3.1/license.html | 6281 / 0 | 6464 / 0 | 6464 / 0 | — | 6481 / 22 | 6481 / 22 | 6481 / 22 | — |
| docs.python.org/3.1/modindex.html | 3649 / 0 | 3731 / 0 | 3731 / 0 | — | 3738 / 25 | 3738 / 25 | 3738 / 25 | — |
| docs.python.org/3.1/reference/index.html | 429 / 0 | 521 / 0 | 521 / 0 | — | 544 / 23 | 544 / 23 | 544 / 23 | — |
| docs.python.org/3.1/search.html | 51 / 0 | 118 / 0 | 118 / 0 | — | 135 / 20 | 135 / 20 | 135 / 20 | — |
| docs.python.org/3.1/tutorial/index.html | 968 / 0 | 1062 / 0 | 1062 / 0 | — | 1084 / 22 | 1084 / 22 | 1084 / 22 | — |
| docs.python.org/3.1/using/index.html | 250 / 0 | 398 / 0 | 398 / 0 | — | 418 / 23 | 418 / 23 | 418 / 23 | — |
| docs.python.org/3.1/whatsnew/3.1.html | 2974 / 0 | 3167 / 0 | 3167 / 0 | — | 3194 / 24 | 3194 / 24 | 3194 / 24 | — |
| docs.python.org/3.1/whatsnew/index.html | 858 / 0 | 954 / 0 | 954 / 0 | — | 973 / 23 | 973 / 23 | 973 / 23 | — |
| docs.python.org/3.10 | 190 / 0 | 711 / 68 | 711 / 68 | 521 / 4 | 629 / 47 | 533 / 16 | 629 / 47 | — |
| docs.python.org/3.10/about.html | 180 / 0 | 604 / 68 | 604 / 68 | 407 / 4 | 520 / 52 | 424 / 21 | 520 / 52 | — |
| docs.python.org/3.10/bugs.html | 666 / 0 | 1104 / 68 | 1104 / 68 | 913 / 4 | 1026 / 52 | 930 / 21 | 1026 / 52 | — |
| docs.python.org/3.10/c-api/apiabiversion.html | 240 / 0 | 656 / 68 | 656 / 68 | 465 / 4 | 579 / 53 | 483 / 22 | 579 / 53 | — |
| docs.python.org/3.10/c-api/arg.html | 4786 / 0 | 5210 / 68 | 5210 / 68 | 5075 / 4 | 5190 / 54 | 5094 / 23 | 5190 / 54 | — |
| docs.python.org/3.10/c-api/bytes.html | 1173 / 0 | 1584 / 68 | 1584 / 68 | 1400 / 4 | 1512 / 51 | 1416 / 20 | 1512 / 51 | — |
| docs.python.org/3.10/c-api/call.html | 2257 / 0 | 2751 / 68 | 2751 / 68 | 2536 / 4 | 2648 / 51 | 2552 / 20 | 2648 / 51 | — |
| docs.python.org/3.10/c-api/cell.html | 341 / 0 | 755 / 68 | 755 / 68 | 564 / 4 | 676 / 51 | 580 / 20 | 676 / 51 | — |
| docs.python.org/3.10/c-api/code.html | 399 / 0 | 838 / 68 | 838 / 68 | 618 / 4 | 730 / 51 | 634 / 20 | 730 / 51 | — |
| docs.python.org/3.10/c-api/codec.html | 899 / 0 | 1338 / 68 | 1338 / 68 | 1164 / 4 | 1279 / 54 | 1183 / 23 | 1279 / 54 | — |
| docs.python.org/3.10/c-api/datetime.html | 1262 / 0 | 1676 / 68 | 1676 / 68 | 1493 / 4 | 1605 / 51 | 1509 / 20 | 1605 / 51 | — |
| docs.python.org/3.10/c-api/dict.html | 1461 / 0 | 1865 / 68 | 1865 / 68 | 1680 / 4 | 1792 / 51 | 1696 / 20 | 1792 / 51 | — |
| docs.python.org/3.10/c-api/exceptions.html | 6000 / 0 | 6509 / 68 | 6509 / 68 | 6295 / 4 | 6407 / 51 | 6311 / 20 | 6407 / 51 | — |
| docs.python.org/3.10/c-api/gcsupport.html | 1284 / 0 | 1728 / 68 | 1728 / 68 | 1545 / 4 | 1659 / 53 | 1563 / 22 | 1659 / 53 | — |
| docs.python.org/3.10/c-api/import.html | 2010 / 0 | 2412 / 68 | 2412 / 68 | 2233 / 4 | 2345 / 51 | 2249 / 20 | 2345 / 51 | — |
| docs.python.org/3.10/c-api/index.html | 427 / 0 | 837 / 68 | 837 / 68 | 640 / 4 | 754 / 53 | 658 / 22 | 754 / 53 | — |
| docs.python.org/3.10/c-api/init.html | 9920 / 0 | 10601 / 68 | 10601 / 68 | 10501 / 4 | 10615 / 53 | 10519 / 22 | 10615 / 53 | — |
| docs.python.org/3.10/c-api/init_config.html | 5810 / 0 | 6237 / 68 | 6237 / 68 | 6123 / 4 | 6236 / 52 | 6140 / 21 | 6236 / 52 | — |
| docs.python.org/3.10/c-api/intro.html | 4747 / 0 | 5225 / 68 | 5225 / 68 | 5042 / 4 | 5153 / 50 | 5057 / 19 | 5153 / 50 | — |
| docs.python.org/3.10/c-api/iter.html | 331 / 0 | 742 / 68 | 742 / 68 | 550 / 4 | 662 / 51 | 566 / 20 | 662 / 51 | — |
| docs.python.org/3.10/c-api/list.html | 809 / 0 | 1219 / 68 | 1219 / 68 | 1028 / 4 | 1140 / 51 | 1044 / 20 | 1140 / 51 | — |
| docs.python.org/3.10/c-api/long.html | 1626 / 0 | 2018 / 68 | 2018 / 68 | 1849 / 4 | 1961 / 51 | 1865 / 20 | 1961 / 51 | — |
| docs.python.org/3.10/c-api/module.html | 3388 / 0 | 3833 / 68 | 3833 / 68 | 3663 / 4 | 3775 / 51 | 3679 / 20 | 3775 / 51 | — |
| docs.python.org/3.10/c-api/number.html | 2106 / 0 | 2495 / 68 | 2495 / 68 | 2325 / 4 | 2437 / 51 | 2341 / 20 | 2437 / 51 | — |
| docs.python.org/3.10/c-api/refcounting.html | 719 / 0 | 1130 / 68 | 1130 / 68 | 940 / 4 | 1052 / 51 | 956 / 20 | 1052 / 51 | — |
| docs.python.org/3.10/c-api/reflection.html | 357 / 0 | 775 / 68 | 775 / 68 | 590 / 4 | 701 / 50 | 605 / 19 | 701 / 50 | — |
| docs.python.org/3.10/c-api/set.html | 1013 / 0 | 1411 / 68 | 1411 / 68 | 1232 / 4 | 1344 / 51 | 1248 / 20 | 1344 / 51 | — |
| docs.python.org/3.10/c-api/stable.html | 980 / 0 | 3894 / 68 | 3894 / 68 | 3695 / 4 | 3808 / 52 | 3712 / 21 | 3808 / 52 | — |
| docs.python.org/3.10/c-api/structures.html | 2619 / 0 | 3074 / 68 | 3074 / 68 | 2902 / 4 | 3015 / 52 | 2919 / 21 | 3015 / 52 | — |
| docs.python.org/3.10/c-api/tuple.html | 1271 / 0 | 1708 / 68 | 1708 / 68 | 1520 / 4 | 1632 / 51 | 1536 / 20 | 1632 / 51 | — |
| docs.python.org/3.10/c-api/type.html | 1541 / 0 | 1945 / 68 | 1945 / 68 | 1790 / 4 | 1902 / 51 | 1806 / 20 | 1902 / 51 | — |
| docs.python.org/3.10/c-api/typeobj.html | 12666 / 0 | 14124 / 68 | 14124 / 68 | 13963 / 4 | 14075 / 51 | 13979 / 20 | 14075 / 51 | — |
| docs.python.org/3.10/c-api/unicode.html | 10151 / 0 | 10726 / 68 | 10726 / 68 | 10552 / 4 | 10666 / 53 | 10570 / 22 | 10666 / 53 | — |
| docs.python.org/3.10/c-api/veryhigh.html | 2443 / 0 | 2891 / 68 | 2891 / 68 | 2662 / 4 | 2777 / 54 | 2681 / 23 | 2777 / 54 | — |
| docs.python.org/3.10/contents.html | 19401 / 0 | 19782 / 68 | 19782 / 68 | 19584 / 4 | 19697 / 52 | 19601 / 21 | 19697 / 52 | — |
| docs.python.org/3.10/copyright.html | 58 / 0 | 460 / 68 | 460 / 68 | 261 / 4 | 372 / 50 | 276 / 19 | 372 / 50 | — |
| docs.python.org/3.10/distributing/index.html | 976 / 0 | 1481 / 68 | 1481 / 68 | 1285 / 4 | 1402 / 52 | 1306 / 21 | 1402 / 52 | — |
| docs.python.org/3.10/download.html | 277 / 0 | 599 / 68 | 599 / 68 | 404 / 4 | 515 / 50 | 419 / 19 | 515 / 50 | — |
| docs.python.org/3.10/extending/index.html | 578 / 0 | 1108 / 68 | 1108 / 68 | 912 / 4 | 1028 / 55 | 932 / 24 | 1028 / 55 | — |
| docs.python.org/3.10/faq/index.html | 65 / 65 | 454 / 68 | 454 / 68 | 257 / 4 | 371 / 53 | 275 / 22 | 371 / 53 | — |
| docs.python.org/3.10/genindex.html | 65 / 65 | 391 / 68 | 391 / 68 | 196 / 4 | 307 / 50 | 211 / 19 | 307 / 50 | — |
| docs.python.org/3.10/glossary.html | 7963 / 0 | 8264 / 68 | 8264 / 68 | 8186 / 4 | 8302 / 50 | 8201 / 19 | 8302 / 50 | — |
| docs.python.org/3.10/howto/annotations.html | 1520 / 0 | 1908 / 68 | 1908 / 68 | 1853 / 4 | 1966 / 52 | 1870 / 21 | 1966 / 52 | — |
| docs.python.org/3.10/howto/index.html | 52 / 0 | 553 / 68 | 553 / 68 | 356 / 4 | 468 / 51 | 372 / 20 | 468 / 51 | — |
| docs.python.org/3.10/installing/index.html | 1207 / 0 | 1808 / 68 | 1808 / 68 | 1612 / 4 | 1725 / 52 | 1629 / 21 | 1725 / 52 | — |
| docs.python.org/3.10/library/__main__.html | 1810 / 0 | 2311 / 68 | 2311 / 68 | 2127 / 4 | 2247 / 54 | 2146 / 23 | 2247 / 54 | — |
| docs.python.org/3.10/library/_thread.html | 1141 / 0 | 1569 / 68 | 1569 / 68 | 1380 / 4 | 1495 / 54 | 1399 / 23 | 1495 / 54 | — |
| docs.python.org/3.10/library/abc.html | 1594 / 0 | 2031 / 68 | 2031 / 68 | 1843 / 4 | 1958 / 54 | 1862 / 23 | 1958 / 54 | — |
| docs.python.org/3.10/library/array.html | 1450 / 0 | 1874 / 68 | 1874 / 68 | 1697 / 4 | 1814 / 56 | 1718 / 25 | 1814 / 56 | — |
| docs.python.org/3.10/library/ast.html | 8584 / 0 | 9114 / 68 | 9114 / 68 | 8945 / 4 | 9112 / 54 | 8964 / 23 | 9112 / 54 | — |
| docs.python.org/3.10/library/asynchat.html | 1060 / 0 | 1543 / 68 | 1543 / 68 | 1353 / 4 | 1469 / 55 | 1373 / 24 | 1469 / 55 | — |
| docs.python.org/3.10/library/asyncio-api-index.html | 591 / 0 | 1049 / 68 | 1049 / 68 | 870 / 4 | 983 / 52 | 887 / 21 | 983 / 52 | — |
| docs.python.org/3.10/library/asyncio-task.html | 4157 / 0 | 4762 / 68 | 4762 / 68 | 4544 / 4 | 4659 / 52 | 4561 / 21 | 4659 / 52 | — |
| docs.python.org/3.10/library/asyncio.html | 223 / 0 | 724 / 68 | 724 / 68 | 524 / 4 | 639 / 53 | 542 / 22 | 639 / 53 | — |
| docs.python.org/3.10/library/atexit.html | 579 / 0 | 1062 / 68 | 1062 / 68 | 862 / 4 | 976 / 53 | 880 / 22 | 976 / 53 | — |
| docs.python.org/3.10/library/audioop.html | 1616 / 0 | 2082 / 68 | 2082 / 68 | 1869 / 4 | 1985 / 55 | 1889 / 24 | 1985 / 55 | — |
| docs.python.org/3.10/library/base64.html | 1616 / 0 | 2126 / 68 | 2126 / 68 | 1919 / 4 | 2038 / 57 | 1941 / 26 | 2038 / 57 | — |
| docs.python.org/3.10/library/bdb.html | 2171 / 0 | 2599 / 68 | 2599 / 68 | 2414 / 4 | 2528 / 53 | 2432 / 22 | 2528 / 53 | — |
| docs.python.org/3.10/library/binary.html | 98 / 0 | 677 / 68 | 677 / 68 | 480 / 4 | 593 / 52 | 497 / 21 | 593 / 52 | — |
| docs.python.org/3.10/library/bisect.html | 1347 / 0 | 1876 / 68 | 1876 / 68 | 1640 / 4 | 1758 / 54 | 1659 / 23 | 1758 / 54 | — |
| docs.python.org/3.10/library/builtins.html | 200 / 0 | 658 / 68 | 658 / 68 | 459 / 4 | 573 / 53 | 477 / 22 | 573 / 53 | — |
| docs.python.org/3.10/library/bz2.html | 1666 / 0 | 2187 / 68 | 2187 / 68 | 1981 / 4 | 2100 / 55 | 2001 / 24 | 2100 / 55 | — |
| docs.python.org/3.10/library/cgi.html | 3396 / 0 | 3961 / 68 | 3961 / 68 | 3759 / 4 | 3875 / 55 | 3779 / 24 | 3875 / 55 | — |
| docs.python.org/3.10/library/cgitb.html | 568 / 0 | 1031 / 68 | 1031 / 68 | 827 / 4 | 944 / 56 | 848 / 25 | 944 / 56 | — |
| docs.python.org/3.10/library/cmd.html | 1926 / 0 | 2402 / 68 | 2402 / 68 | 2209 / 4 | 2326 / 56 | 2230 / 25 | 2326 / 56 | — |
| docs.python.org/3.10/library/code.html | 1097 / 0 | 1575 / 68 | 1575 / 68 | 1374 / 4 | 1489 / 54 | 1393 / 23 | 1489 / 54 | — |
| docs.python.org/3.10/library/codecs.html | 8089 / 0 | 8731 / 68 | 8731 / 68 | 8530 / 4 | 8648 / 56 | 8551 / 25 | 8648 / 56 | — |
| docs.python.org/3.10/library/collections.abc.html | 1989 / 0 | 2453 / 68 | 2453 / 68 | 2294 / 4 | 2414 / 56 | 2315 / 25 | 2414 / 56 | — |
| docs.python.org/3.10/library/collections.html | 7020 / 0 | 7592 / 68 | 7592 / 68 | 7389 / 4 | 7533 / 53 | 7407 / 22 | 7533 / 53 | — |
| docs.python.org/3.10/library/colorsys.html | 256 / 0 | 717 / 68 | 717 / 68 | 511 / 4 | 628 / 55 | 531 / 24 | 628 / 55 | — |
| docs.python.org/3.10/library/constants.html | 572 / 0 | 999 / 68 | 999 / 68 | 809 / 4 | 921 / 51 | 825 / 20 | 921 / 51 | — |
| docs.python.org/3.10/library/contextlib.html | 4524 / 0 | 5056 / 68 | 5056 / 68 | 4915 / 4 | 5038 / 55 | 4935 / 24 | 5038 / 55 | — |
| docs.python.org/3.10/library/ctypes.html | 13276 / 0 | 13960 / 68 | 13960 / 68 | 13819 / 4 | 14006 / 57 | 13841 / 26 | 14006 / 57 | — |
| docs.python.org/3.10/library/curses.html | 9380 / 0 | 9874 / 68 | 9874 / 68 | 9702 / 4 | 9819 / 56 | 9723 / 25 | 9819 / 56 | — |
| docs.python.org/3.10/library/dataclasses.html | 4336 / 0 | 4833 / 68 | 4833 / 68 | 4671 / 4 | 4785 / 53 | 4689 / 22 | 4785 / 53 | — |
| docs.python.org/3.10/library/datetime.html | 14043 / 0 | 14623 / 68 | 14623 / 68 | 14458 / 4 | 14601 / 56 | 14479 / 25 | 14601 / 56 | — |
| docs.python.org/3.10/library/debug.html | 261 / 0 | 693 / 68 | 693 / 68 | 496 / 4 | 609 / 52 | 513 / 21 | 609 / 52 | — |
| docs.python.org/3.10/library/decimal.html | 10530 / 0 | 11095 / 68 | 11095 / 68 | 10905 / 4 | 11070 / 58 | 10928 / 27 | 11070 / 58 | — |
| docs.python.org/3.10/library/difflib.html | 4304 / 0 | 4881 / 68 | 4881 / 68 | 4617 / 4 | 4753 / 55 | 4637 / 24 | 4753 / 55 | — |
| docs.python.org/3.10/library/distribution.html | 50 / 0 | 580 / 68 | 580 / 68 | 383 / 4 | 497 / 53 | 401 / 22 | 497 / 53 | — |
| docs.python.org/3.10/library/distutils.html | 323 / 0 | 779 / 68 | 779 / 68 | 578 / 4 | 695 / 56 | 599 / 25 | 695 / 56 | — |
| docs.python.org/3.10/library/email.generator.html | 1903 / 0 | 2374 / 68 | 2374 / 68 | 2158 / 4 | 2272 / 53 | 2176 / 22 | 2272 / 53 | — |
| docs.python.org/3.10/library/email.html | 1130 / 0 | 1660 / 68 | 1660 / 68 | 1467 / 4 | 1585 / 57 | 1489 / 26 | 1585 / 57 | — |
| docs.python.org/3.10/library/email.policy.html | 3961 / 0 | 4388 / 68 | 4388 / 68 | 4222 / 4 | 4339 / 52 | 4239 / 21 | 4339 / 52 | — |
| docs.python.org/3.10/library/email.utils.html | 1462 / 0 | 1908 / 68 | 1908 / 68 | 1703 / 4 | 1816 / 52 | 1720 / 21 | 1816 / 52 | — |
| docs.python.org/3.10/library/ensurepip.html | 718 / 0 | 1220 / 68 | 1220 / 68 | 1019 / 4 | 1135 / 55 | 1039 / 24 | 1135 / 55 | — |
| docs.python.org/3.10/library/enum.html | 5317 / 0 | 6130 / 68 | 6130 / 68 | 5890 / 4 | 6062 / 54 | 5909 / 23 | 6062 / 54 | — |
| docs.python.org/3.10/library/errno.html | 1472 / 0 | 1825 / 68 | 1825 / 68 | 1749 / 4 | 1865 / 55 | 1769 / 24 | 1865 / 55 | — |
| docs.python.org/3.10/library/exceptions.html | 4688 / 0 | 5004 / 68 | 5004 / 68 | 4959 / 4 | 5071 / 51 | 4975 / 20 | 5071 / 51 | — |
| docs.python.org/3.10/library/faulthandler.html | 940 / 0 | 1470 / 68 | 1470 / 68 | 1269 / 4 | 1385 / 55 | 1289 / 24 | 1385 / 55 | — |
| docs.python.org/3.10/library/fileinput.html | 1371 / 0 | 1842 / 68 | 1842 / 68 | 1630 / 4 | 1749 / 58 | 1653 / 27 | 1749 / 58 | — |
| docs.python.org/3.10/library/fractions.html | 785 / 0 | 1238 / 68 | 1238 / 68 | 1050 / 4 | 1168 / 53 | 1068 / 22 | 1168 / 53 | — |
| docs.python.org/3.10/library/frameworks.html | 224 / 0 | 646 / 68 | 646 / 68 | 449 / 4 | 561 / 51 | 465 / 20 | 561 / 51 | — |
| docs.python.org/3.10/library/functions.html | 11862 / 0 | 12437 / 68 | 12437 / 68 | 12219 / 4 | 12350 / 51 | 12235 / 20 | 12350 / 51 | — |
| docs.python.org/3.10/library/gc.html | 1628 / 0 | 2049 / 68 | 2049 / 68 | 1877 / 4 | 1994 / 54 | 1896 / 23 | 1994 / 54 | — |
| docs.python.org/3.10/library/glob.html | 666 / 0 | 1141 / 68 | 1141 / 68 | 933 / 4 | 1052 / 56 | 954 / 25 | 1052 / 56 | — |
| docs.python.org/3.10/library/graphlib.html | 1203 / 0 | 1674 / 68 | 1674 / 68 | 1482 / 4 | 1602 / 57 | 1504 / 26 | 1602 / 57 | — |
| docs.python.org/3.10/library/grp.html | 335 / 0 | 782 / 68 | 782 / 68 | 588 / 4 | 703 / 54 | 607 / 23 | 703 / 54 | — |
| docs.python.org/3.10/library/gzip.html | 1449 / 0 | 1965 / 68 | 1965 / 68 | 1756 / 4 | 1872 / 55 | 1776 / 24 | 1872 / 55 | — |
| docs.python.org/3.10/library/hashlib.html | 3609 / 0 | 4195 / 68 | 4195 / 68 | 3960 / 4 | 4093 / 56 | 3981 / 25 | 4093 / 56 | — |
| docs.python.org/3.10/library/html.html | 193 / 0 | 651 / 68 | 651 / 68 | 450 / 4 | 566 / 55 | 470 / 24 | 566 / 55 | — |
| docs.python.org/3.10/library/html.parser.html | 1522 / 0 | 2027 / 68 | 2027 / 68 | 1833 / 4 | 1957 / 56 | 1854 / 25 | 1957 / 56 | — |
| docs.python.org/3.10/library/http.client.html | 2920 / 0 | 3389 / 68 | 3389 / 68 | 3209 / 4 | 3330 / 54 | 3228 / 23 | 3330 / 54 | — |
| docs.python.org/3.10/library/http.server.html | 2802 / 0 | 3255 / 68 | 3255 / 68 | 3083 / 4 | 3197 / 53 | 3101 / 22 | 3197 / 53 | — |
| docs.python.org/3.10/library/idle.html | 6334 / 0 | 6990 / 68 | 6990 / 68 | 6857 / 4 | 6969 / 50 | 6872 / 19 | 6969 / 50 | — |
| docs.python.org/3.10/library/imghdr.html | 396 / 0 | 862 / 68 | 862 / 68 | 661 / 4 | 780 / 57 | 683 / 26 | 780 / 57 | — |
| docs.python.org/3.10/library/imp.html | 2270 / 0 | 2743 / 68 | 2743 / 68 | 2557 / 4 | 2673 / 55 | 2577 / 24 | 2673 / 55 | — |
| docs.python.org/3.10/library/importlib.html | 9157 / 0 | 9668 / 68 | 9668 / 68 | 9577 / 4 | 9694 / 55 | 9597 / 24 | 9694 / 55 | — |
| docs.python.org/3.10/library/importlib.metadata.html | 1419 / 0 | 1948 / 68 | 1948 / 68 | 1730 / 4 | 1863 / 51 | 1746 / 20 | 1863 / 51 | — |
| docs.python.org/3.10/library/index.html | 2282 / 0 | 2684 / 68 | 2684 / 68 | 2487 / 4 | 2601 / 53 | 2505 / 22 | 2601 / 53 | — |
| docs.python.org/3.10/library/inspect.html | 7199 / 0 | 7738 / 68 | 7738 / 68 | 7554 / 4 | 7678 / 54 | 7573 / 23 | 7678 / 54 | — |
| docs.python.org/3.10/library/io.html | 6375 / 0 | 6949 / 68 | 6949 / 68 | 6766 / 4 | 6885 / 57 | 6788 / 26 | 6885 / 57 | — |
| docs.python.org/3.10/library/itertools.html | 5234 / 0 | 5746 / 68 | 5746 / 68 | 5535 / 4 | 5655 / 57 | 5557 / 26 | 5655 / 57 | — |
| docs.python.org/3.10/library/json.html | 3807 / 0 | 4419 / 68 | 4419 / 68 | 4166 / 4 | 4291 / 55 | 4186 / 24 | 4291 / 55 | — |
| docs.python.org/3.10/library/language.html | 38 / 0 | 636 / 68 | 636 / 68 | 439 / 4 | 552 / 52 | 456 / 21 | 552 / 52 | — |
| docs.python.org/3.10/library/logging.config.html | 5080 / 0 | 5655 / 68 | 5655 / 68 | 5461 / 4 | 5575 / 53 | 5479 / 22 | 5575 / 53 | — |
| docs.python.org/3.10/library/logging.handlers.html | 6934 / 0 | 7443 / 68 | 7443 / 68 | 7281 / 4 | 7395 / 53 | 7299 / 22 | 7395 / 53 | — |
| docs.python.org/3.10/library/logging.html | 9093 / 0 | 9665 / 68 | 9665 / 68 | 9481 / 4 | 9597 / 55 | 9501 / 24 | 9597 / 55 | — |
| docs.python.org/3.10/library/lzma.html | 2417 / 0 | 2960 / 68 | 2960 / 68 | 2748 / 4 | 2865 / 56 | 2769 / 25 | 2865 / 56 | — |
| docs.python.org/3.10/library/mailcap.html | 683 / 0 | 1151 / 68 | 1151 / 68 | 946 / 4 | 1062 / 54 | 965 / 23 | 1062 / 54 | — |
| docs.python.org/3.10/library/markup.html | 360 / 0 | 810 / 68 | 810 / 68 | 613 / 4 | 727 / 53 | 631 / 22 | 727 / 53 | — |
| docs.python.org/3.10/library/mm.html | 37 / 0 | 496 / 68 | 496 / 68 | 299 / 4 | 411 / 51 | 315 / 20 | 411 / 51 | — |
| docs.python.org/3.10/library/mmap.html | 2045 / 0 | 2521 / 68 | 2521 / 68 | 2328 / 4 | 2443 / 54 | 2347 / 23 | 2443 / 54 | — |
| docs.python.org/3.10/library/modulefinder.html | 388 / 0 | 883 / 68 | 883 / 68 | 685 / 4 | 803 / 57 | 707 / 26 | 803 / 57 | — |
| docs.python.org/3.10/library/modules.html | 38 / 0 | 619 / 68 | 619 / 68 | 422 / 4 | 534 / 51 | 438 / 20 | 534 / 51 | — |
| docs.python.org/3.10/library/msilib.html | 2265 / 0 | 2951 / 68 | 2951 / 68 | 2675 / 4 | 2793 / 57 | 2697 / 26 | 2793 / 57 | — |
| docs.python.org/3.10/library/netdata.html | 261 / 0 | 705 / 68 | 705 / 68 | 508 / 4 | 621 / 52 | 525 / 21 | 621 / 52 | — |
| docs.python.org/3.10/library/nntplib.html | 3114 / 0 | 3636 / 68 | 3636 / 68 | 3421 / 4 | 3546 / 54 | 3440 / 23 | 3546 / 54 | — |
| docs.python.org/3.10/library/numbers.html | 1026 / 0 | 1503 / 68 | 1503 / 68 | 1331 / 4 | 1447 / 55 | 1351 / 24 | 1447 / 55 | — |
| docs.python.org/3.10/library/operator.html | 2403 / 0 | 2949 / 68 | 2949 / 68 | 2704 / 4 | 2824 / 55 | 2724 / 24 | 2824 / 55 | — |
| docs.python.org/3.10/library/optparse.html | 10934 / 0 | 11683 / 68 | 11683 / 68 | 11559 / 4 | 11677 / 56 | 11580 / 25 | 11677 / 56 | — |
| docs.python.org/3.10/library/os.html | 24682 / 0 | 25322 / 68 | 25322 / 68 | 25098 / 4 | 25215 / 55 | 25118 / 24 | 25215 / 55 | — |
| docs.python.org/3.10/library/os.path.html | 2744 / 0 | 3193 / 68 | 3193 / 68 | 3011 / 4 | 3132 / 54 | 3030 / 23 | 3132 / 54 | — |
| docs.python.org/3.10/library/pathlib.html | 4727 / 0 | 5624 / 68 | 5624 / 68 | 5380 / 4 | 5569 / 54 | 5399 / 23 | 5569 / 54 | — |
| docs.python.org/3.10/library/pdb.html | 3220 / 0 | 3677 / 68 | 3677 / 68 | 3491 / 4 | 3608 / 54 | 3510 / 23 | 3608 / 54 | — |
| docs.python.org/3.10/library/pickle.html | 7266 / 0 | 7872 / 68 | 7872 / 68 | 7667 / 4 | 7785 / 54 | 7686 / 23 | 7785 / 54 | — |
| docs.python.org/3.10/library/pipes.html | 438 / 0 | 915 / 68 | 915 / 68 | 719 / 4 | 836 / 55 | 739 / 24 | 836 / 55 | — |
| docs.python.org/3.10/library/pkgutil.html | 1566 / 0 | 2034 / 68 | 2034 / 68 | 1833 / 4 | 1948 / 54 | 1852 / 23 | 1948 / 54 | — |
| docs.python.org/3.10/library/platform.html | 1359 / 0 | 1891 / 68 | 1891 / 68 | 1694 / 4 | 1812 / 57 | 1716 / 26 | 1812 / 57 | — |
| docs.python.org/3.10/library/pprint.html | 1887 / 0 | 2411 / 68 | 2411 / 68 | 2172 / 4 | 2295 / 54 | 2191 / 23 | 2295 / 54 | — |
| docs.python.org/3.10/library/py_compile.html | 976 / 0 | 1455 / 68 | 1455 / 68 | 1259 / 4 | 1375 / 55 | 1279 / 24 | 1375 / 55 | — |
| docs.python.org/3.10/library/pyclbr.html | 681 / 0 | 1160 / 68 | 1160 / 68 | 974 / 4 | 1090 / 55 | 994 / 24 | 1090 / 55 | — |
| docs.python.org/3.10/library/queue.html | 1520 / 0 | 1985 / 68 | 1985 / 68 | 1795 / 4 | 1911 / 55 | 1815 / 24 | 1911 / 55 | — |
| docs.python.org/3.10/library/random.html | 3281 / 0 | 3806 / 68 | 3806 / 68 | 3606 / 4 | 3724 / 54 | 3625 / 23 | 3724 / 54 | — |
| docs.python.org/3.10/library/rlcompleter.html | 349 / 0 | 825 / 68 | 825 / 68 | 624 / 4 | 742 / 56 | 645 / 25 | 742 / 56 | — |
| docs.python.org/3.10/library/runpy.html | 1239 / 0 | 1707 / 68 | 1707 / 68 | 1506 / 4 | 1623 / 56 | 1527 / 25 | 1623 / 56 | — |
| docs.python.org/3.10/library/select.html | 3079 / 0 | 3578 / 68 | 3578 / 68 | 3404 / 4 | 3520 / 55 | 3424 / 24 | 3520 / 55 | — |
| docs.python.org/3.10/library/shelve.html | 1303 / 0 | 1792 / 68 | 1792 / 68 | 1586 / 4 | 1701 / 54 | 1605 / 23 | 1701 / 54 | — |
| docs.python.org/3.10/library/shutil.html | 4501 / 0 | 5083 / 68 | 5083 / 68 | 4838 / 4 | 4956 / 54 | 4857 / 23 | 4956 / 54 | — |
| docs.python.org/3.10/library/signal.html | 3708 / 0 | 4214 / 68 | 4214 / 68 | 4045 / 4 | 4162 / 56 | 4066 / 25 | 4162 / 56 | — |
| docs.python.org/3.10/library/sndhdr.html | 308 / 0 | 757 / 68 | 757 / 68 | 559 / 4 | 676 / 56 | 580 / 25 | 676 / 56 | — |
| docs.python.org/3.10/library/socket.html | 11142 / 0 | 11663 / 68 | 11663 / 68 | 11493 / 4 | 11610 / 54 | 11512 / 23 | 11610 / 54 | — |
| docs.python.org/3.10/library/socketserver.html | 3148 / 0 | 3651 / 68 | 3651 / 68 | 3479 / 4 | 3596 / 56 | 3500 / 25 | 3596 / 56 | — |
| docs.python.org/3.10/library/sqlite3.html | 8282 / 0 | 9053 / 68 | 9053 / 68 | 8886 / 4 | 9019 / 57 | 8908 / 26 | 9019 / 57 | — |
| docs.python.org/3.10/library/ssl.html | 14127 / 0 | 14692 / 68 | 14692 / 68 | 14602 / 4 | 14739 / 56 | 14623 / 25 | 14739 / 56 | — |
| docs.python.org/3.10/library/stat.html | 1676 / 0 | 2080 / 68 | 2080 / 68 | 1947 / 4 | 2062 / 54 | 1966 / 23 | 2062 / 54 | — |
| docs.python.org/3.10/library/statistics.html | 4959 / 0 | 5509 / 68 | 5509 / 68 | 5284 / 4 | 5437 / 54 | 5303 / 23 | 5437 / 54 | — |
| docs.python.org/3.10/library/stdtypes.html | 27083 / 0 | 28128 / 68 | 28128 / 68 | 27914 / 4 | 28140 / 51 | 27930 / 20 | 28140 / 51 | — |
| docs.python.org/3.10/library/string.html | 4993 / 0 | 5531 / 68 | 5531 / 68 | 5311 / 4 | 5439 / 54 | 5330 / 23 | 5439 / 54 | — |
| docs.python.org/3.10/library/struct.html | 3237 / 0 | 3793 / 68 | 3793 / 68 | 3574 / 4 | 3702 / 57 | 3596 / 26 | 3702 / 57 | — |
| docs.python.org/3.10/library/subprocess.html | 8197 / 0 | 8859 / 68 | 8859 / 68 | 8676 / 4 | 8795 / 53 | 8694 / 22 | 8795 / 53 | — |
| docs.python.org/3.10/library/superseded.html | 531 / 0 | 981 / 68 | 981 / 68 | 784 / 4 | 896 / 51 | 800 / 20 | 896 / 51 | — |
| docs.python.org/3.10/library/symtable.html | 821 / 0 | 1292 / 68 | 1292 / 68 | 1130 / 4 | 1249 / 57 | 1152 / 26 | 1249 / 57 | — |
| docs.python.org/3.10/library/sys.html | 9831 / 0 | 10228 / 68 | 10228 / 68 | 10086 / 4 | 10204 / 55 | 10106 / 24 | 10204 / 55 | — |
| docs.python.org/3.10/library/sysconfig.html | 1372 / 0 | 1884 / 68 | 1884 / 68 | 1683 / 4 | 1802 / 57 | 1705 / 26 | 1802 / 57 | — |
| docs.python.org/3.10/library/tarfile.html | 6635 / 0 | 7156 / 68 | 7156 / 68 | 7002 / 4 | 7120 / 57 | 7024 / 26 | 7120 / 57 | — |
| docs.python.org/3.10/library/telnetlib.html | 1179 / 0 | 1662 / 68 | 1662 / 68 | 1474 / 4 | 1589 / 53 | 1492 / 22 | 1589 / 53 | — |
| docs.python.org/3.10/library/tempfile.html | 2306 / 0 | 2856 / 68 | 2856 / 68 | 2611 / 4 | 2730 / 56 | 2632 / 25 | 2730 / 56 | — |
| docs.python.org/3.10/library/termios.html | 529 / 0 | 1005 / 68 | 1005 / 68 | 806 / 4 | 922 / 55 | 826 / 24 | 922 / 55 | — |
| docs.python.org/3.10/library/textwrap.html | 1542 / 0 | 2016 / 68 | 2016 / 68 | 1793 / 4 | 1912 / 55 | 1813 / 24 | 1912 / 55 | — |
| docs.python.org/3.10/library/threading.html | 6512 / 0 | 7008 / 68 | 7008 / 68 | 6839 / 4 | 6953 / 53 | 6857 / 22 | 6953 / 53 | — |
| docs.python.org/3.10/library/time.html | 4751 / 0 | 5234 / 68 | 5234 / 68 | 5072 / 4 | 5192 / 55 | 5092 / 24 | 5192 / 55 | — |
| docs.python.org/3.10/library/tkinter.colorchooser.html | 120 / 0 | 577 / 68 | 577 / 68 | 377 / 4 | 492 / 54 | 396 / 23 | 492 / 54 | — |
| docs.python.org/3.10/library/tkinter.html | 6333 / 0 | 6895 / 68 | 6895 / 68 | 6766 / 4 | 6883 / 55 | 6786 / 24 | 6883 / 55 | — |
| docs.python.org/3.10/library/tkinter.messagebox.html | 161 / 0 | 626 / 68 | 626 / 68 | 402 / 4 | 517 / 54 | 421 / 23 | 517 / 54 | — |
| docs.python.org/3.10/library/tkinter.scrolledtext.html | 168 / 0 | 622 / 68 | 622 / 68 | 425 / 4 | 540 / 54 | 444 / 23 | 540 / 54 | — |
| docs.python.org/3.10/library/traceback.html | 2518 / 0 | 3039 / 68 | 3039 / 68 | 2819 / 4 | 2939 / 57 | 2841 / 26 | 2939 / 57 | — |
| docs.python.org/3.10/library/tracemalloc.html | 3466 / 0 | 4008 / 68 | 4008 / 68 | 3849 / 4 | 3964 / 54 | 3868 / 23 | 3964 / 54 | — |
| docs.python.org/3.10/library/tty.html | 159 / 0 | 608 / 68 | 608 / 68 | 408 / 4 | 523 / 54 | 427 / 23 | 523 / 54 | — |
| docs.python.org/3.10/library/types.html | 2140 / 0 | 2633 / 68 | 2633 / 68 | 2467 / 4 | 2588 / 59 | 2491 / 28 | 2588 / 59 | — |
| docs.python.org/3.10/library/typing.html | 10829 / 0 | 11365 / 68 | 11365 / 68 | 11300 / 4 | 11420 / 55 | 11320 / 24 | 11420 / 55 | — |
| docs.python.org/3.10/library/unicodedata.html | 813 / 0 | 1249 / 68 | 1249 / 68 | 1064 / 4 | 1179 / 53 | 1082 / 22 | 1179 / 53 | — |
| docs.python.org/3.10/library/unittest.html | 12854 / 0 | 13518 / 68 | 13518 / 68 | 13265 / 4 | 13382 / 54 | 13284 / 23 | 13382 / 54 | — |
| docs.python.org/3.10/library/unittest.mock-examples.htm | 6546 / 0 | 7369 / 68 | 7369 / 68 | 7099 / 4 | 7287 / 53 | 7117 / 22 | 7287 / 53 | — |
| docs.python.org/3.10/library/urllib.parse.html | 4143 / 0 | 4711 / 68 | 4711 / 68 | 4472 / 4 | 4594 / 55 | 4492 / 24 | 4594 / 55 | — |
| docs.python.org/3.10/library/urllib.robotparser.html | 401 / 0 | 847 / 68 | 847 / 68 | 656 / 4 | 772 / 54 | 675 / 23 | 772 / 54 | — |
| docs.python.org/3.10/library/venv.html | 3268 / 0 | 3798 / 68 | 3798 / 68 | 3598 / 4 | 3714 / 55 | 3618 / 24 | 3714 / 55 | — |
| docs.python.org/3.10/library/winreg.html | 3520 / 0 | 4028 / 68 | 4028 / 68 | 3851 / 4 | 3967 / 54 | 3870 / 23 | 3967 / 54 | — |
| docs.python.org/3.10/library/xdrlib.html | 1244 / 0 | 1700 / 68 | 1700 / 68 | 1531 / 4 | 1648 / 56 | 1552 / 25 | 1648 / 56 | — |
| docs.python.org/3.10/library/xml.sax.handler.html | 2295 / 0 | 2771 / 68 | 2771 / 68 | 2604 / 4 | 2721 / 56 | 2625 / 25 | 2721 / 56 | — |
| docs.python.org/3.10/library/xml.sax.html | 1025 / 0 | 1524 / 68 | 1524 / 68 | 1326 / 4 | 1442 / 55 | 1346 / 24 | 1442 / 55 | — |
| docs.python.org/3.10/library/xmlrpc.client.html | 2693 / 0 | 3224 / 68 | 3224 / 68 | 3038 / 4 | 3153 / 54 | 3057 / 23 | 3153 / 54 | — |
| docs.python.org/3.10/library/xmlrpc.html | 81 / 0 | 541 / 68 | 541 / 68 | 344 / 4 | 461 / 56 | 365 / 25 | 461 / 56 | — |
| docs.python.org/3.10/library/xmlrpc.server.html | 2007 / 0 | 2509 / 68 | 2509 / 68 | 2312 / 4 | 2427 / 54 | 2331 / 23 | 2427 / 54 | — |
| docs.python.org/3.10/library/zipimport.html | 959 / 0 | 1416 / 68 | 1416 / 68 | 1232 / 4 | 1349 / 56 | 1253 / 25 | 1349 / 56 | — |
| docs.python.org/3.10/library/zlib.html | 2078 / 0 | 2527 / 68 | 2527 / 68 | 2331 / 4 | 2447 / 55 | 2351 / 24 | 2447 / 55 | — |
| docs.python.org/3.10/license.html | 6986 / 0 | 7625 / 68 | 7625 / 68 | 7445 / 4 | 7558 / 52 | 7462 / 21 | 7558 / 52 | — |
| docs.python.org/3.10/py-modindex.html | 4026 / 0 | 4420 / 68 | 4420 / 68 | 4208 / 4 | 4324 / 55 | 4228 / 24 | 4324 / 55 | — |
| docs.python.org/3.10/reference/compound_stmts.html | 7246 / 0 | 7950 / 68 | 7950 / 68 | 7742 / 4 | 7859 / 52 | 7759 / 21 | 7859 / 52 | — |
| docs.python.org/3.10/reference/datamodel.html | 16528 / 0 | 17235 / 68 | 17235 / 68 | 17101 / 4 | 17220 / 52 | 17118 / 21 | 17220 / 52 | — |
| docs.python.org/3.10/reference/expressions.html | 10437 / 0 | 11184 / 68 | 11184 / 68 | 10976 / 4 | 11090 / 51 | 10992 / 20 | 11090 / 51 | — |
| docs.python.org/3.10/reference/grammar.html | 1881 / 0 | 2303 / 68 | 2303 / 68 | 2106 / 4 | 2220 / 53 | 2124 / 22 | 2220 / 53 | — |
| docs.python.org/3.10/reference/index.html | 438 / 0 | 844 / 68 | 844 / 68 | 647 / 4 | 761 / 53 | 665 / 22 | 761 / 53 | — |
| docs.python.org/3.10/reference/lexical_analysis.html | 5123 / 0 | 5797 / 68 | 5797 / 68 | 5564 / 4 | 5681 / 52 | 5581 / 21 | 5681 / 52 | — |
| docs.python.org/3.10/search.html | 21 / 0 | 340 / 68 | 340 / 68 | 145 / 4 | 390 / 184 | 294 / 153 | 390 / 184 | — |
| docs.python.org/3.10/tutorial/appendix.html | 693 / 0 | 1187 / 68 | 1187 / 68 | 990 / 4 | 1103 / 51 | 1006 / 20 | 1103 / 51 | — |
| docs.python.org/3.10/tutorial/index.html | 982 / 0 | 1382 / 68 | 1382 / 68 | 1185 / 4 | 1298 / 52 | 1202 / 21 | 1298 / 52 | — |
| docs.python.org/3.10/using/cmdline.html | 4940 / 0 | 5393 / 68 | 5393 / 68 | 5264 / 4 | 5379 / 54 | 5283 / 23 | 5379 / 54 | — |
| docs.python.org/3.10/using/configure.html | 3330 / 0 | 3873 / 68 | 3873 / 68 | 3757 / 4 | 3872 / 52 | 3774 / 21 | 3872 / 52 | — |
| docs.python.org/3.10/using/editors.html | 46 / 0 | 480 / 68 | 480 / 68 | 283 / 4 | 397 / 53 | 301 / 22 | 397 / 53 | — |
| docs.python.org/3.10/using/index.html | 460 / 0 | 870 / 68 | 870 / 68 | 673 / 4 | 787 / 53 | 691 / 22 | 787 / 53 | — |
| docs.python.org/3.10/using/mac.html | 963 / 0 | 1524 / 68 | 1524 / 68 | 1328 / 4 | 1444 / 55 | 1348 / 24 | 1444 / 55 | — |
| docs.python.org/3.10/using/unix.html | 685 / 0 | 1235 / 68 | 1235 / 68 | 1044 / 4 | 1160 / 55 | 1064 / 24 | 1160 / 55 | — |
| docs.python.org/3.10/using/windows.html | 7057 / 0 | 7873 / 68 | 7873 / 68 | 7690 / 4 | 7806 / 54 | 7709 / 23 | 7806 / 54 | — |
| docs.python.org/3.10/whatsnew/2.0.html | 9031 / 0 | 9636 / 68 | 9636 / 68 | 9440 / 4 | 9556 / 54 | 9459 / 23 | 9556 / 54 | — |
| docs.python.org/3.10/whatsnew/2.1.html | 5603 / 0 | 6202 / 68 | 6202 / 68 | 6016 / 4 | 6133 / 54 | 6035 / 23 | 6133 / 54 | — |
| docs.python.org/3.10/whatsnew/2.2.html | 8889 / 0 | 9506 / 68 | 9506 / 68 | 9306 / 4 | 9429 / 54 | 9325 / 23 | 9429 / 54 | — |
| docs.python.org/3.10/whatsnew/2.3.html | 13061 / 0 | 13822 / 68 | 13822 / 68 | 13604 / 4 | 13752 / 54 | 13623 / 23 | 13752 / 54 | — |
| docs.python.org/3.10/whatsnew/2.4.html | 9193 / 0 | 9879 / 68 | 9879 / 68 | 9664 / 4 | 9806 / 54 | 9683 / 23 | 9806 / 54 | — |
| docs.python.org/3.10/whatsnew/2.5.html | 14271 / 0 | 14998 / 68 | 14998 / 68 | 14804 / 4 | 14927 / 54 | 14823 / 23 | 14927 / 54 | — |
| docs.python.org/3.10/whatsnew/2.6.html | 18020 / 0 | 18895 / 68 | 18895 / 68 | 18673 / 4 | 18827 / 54 | 18692 / 23 | 18827 / 54 | — |
| docs.python.org/3.10/whatsnew/2.7.html | 16678 / 0 | 17596 / 68 | 17596 / 68 | 17381 / 4 | 17529 / 54 | 17400 / 23 | 17529 / 54 | — |
| docs.python.org/3.10/whatsnew/3.0.html | 5654 / 0 | 6289 / 68 | 6289 / 68 | 6095 / 4 | 6210 / 54 | 6114 / 23 | 6210 / 54 | — |
| docs.python.org/3.10/whatsnew/3.1.html | 2814 / 0 | 3356 / 68 | 3356 / 68 | 3149 / 4 | 3278 / 54 | 3168 / 23 | 3278 / 54 | — |
| docs.python.org/3.10/whatsnew/3.10.html | 12579 / 0 | 13749 / 68 | 13749 / 68 | 13627 / 4 | 13773 / 54 | 13646 / 23 | 13773 / 54 | — |
| docs.python.org/3.10/whatsnew/3.2.html | 14445 / 0 | 15360 / 68 | 15360 / 68 | 15093 / 4 | 15268 / 54 | 15112 / 23 | 15268 / 54 | — |
| docs.python.org/3.10/whatsnew/3.3.html | 13058 / 0 | 14601 / 68 | 14601 / 68 | 14419 / 4 | 14550 / 54 | 14438 / 23 | 14550 / 54 | — |
| docs.python.org/3.10/whatsnew/3.4.html | 15521 / 0 | 16605 / 68 | 16605 / 68 | 16408 / 4 | 16528 / 54 | 16427 / 23 | 16528 / 54 | — |
| docs.python.org/3.10/whatsnew/3.5.html | 12043 / 0 | 13260 / 68 | 13260 / 68 | 13052 / 4 | 13191 / 54 | 13071 / 23 | 13191 / 54 | — |
| docs.python.org/3.10/whatsnew/3.6.html | 12378 / 0 | 13727 / 68 | 13727 / 68 | 13533 / 4 | 13656 / 54 | 13552 / 23 | 13656 / 54 | — |
| docs.python.org/3.10/whatsnew/3.7.html | 13451 / 0 | 14690 / 68 | 14690 / 68 | 14509 / 4 | 14624 / 54 | 14528 / 23 | 14624 / 54 | — |
| docs.python.org/3.10/whatsnew/3.8.html | 11745 / 0 | 12704 / 68 | 12704 / 68 | 12486 / 4 | 12619 / 54 | 12505 / 23 | 12619 / 54 | — |
| docs.python.org/3.10/whatsnew/3.9.html | 8718 / 0 | 9585 / 68 | 9585 / 68 | 9408 / 4 | 9526 / 54 | 9427 / 23 | 9526 / 54 | — |
| docs.python.org/3.10/whatsnew/changelog.html | 183653 / 0 | 188265 / 68 | 188265 / 68 | 188054 / 4 | 188169 / 50 | 188069 / 19 | 188169 / 50 | — |
| docs.python.org/3.10/whatsnew/index.html | 2172 / 0 | 2587 / 68 | 2587 / 68 | 2389 / 4 | 2503 / 53 | 2407 / 22 | 2503 / 53 | — |
| docs.python.org/3.11 | 188 / 0 | 711 / 68 | 711 / 68 | 522 / 4 | 629 / 47 | 534 / 16 | 629 / 47 | — |
| docs.python.org/3.11/about.html | 207 / 27 | 606 / 68 | 606 / 68 | 410 / 4 | 522 / 52 | 427 / 21 | 522 / 52 | — |
| docs.python.org/3.11/bugs.html | 698 / 32 | 1106 / 68 | 1106 / 68 | 916 / 4 | 1028 / 52 | 933 / 21 | 1028 / 52 | — |
| docs.python.org/3.11/c-api/index.html | 463 / 33 | 842 / 68 | 842 / 68 | 646 / 4 | 759 / 53 | 664 / 22 | 759 / 53 | — |
| docs.python.org/3.11/contents.html | 20504 / 31 | 20856 / 68 | 20856 / 68 | 20659 / 4 | 20771 / 52 | 20676 / 21 | 20771 / 52 | — |
| docs.python.org/3.11/copyright.html | 85 / 27 | 462 / 68 | 462 / 68 | 264 / 4 | 374 / 50 | 279 / 19 | 374 / 50 | — |
| docs.python.org/3.11/distributing/index.html | 34 / 0 | 384 / 68 | 384 / 68 | 188 / 4 | 300 / 52 | 205 / 21 | 300 / 52 | — |
| docs.python.org/3.11/download.html | 261 / 0 | 585 / 68 | 585 / 68 | 391 / 4 | 501 / 50 | 406 / 19 | 501 / 50 | — |
| docs.python.org/3.11/extending/index.html | 613 / 35 | 1110 / 68 | 1110 / 68 | 915 / 4 | 1030 / 55 | 935 / 24 | 1030 / 55 | — |
| docs.python.org/3.11/faq/index.html | 97 / 97 | 456 / 68 | 456 / 68 | 260 / 4 | 373 / 53 | 278 / 22 | 373 / 53 | — |
| docs.python.org/3.11/glossary.html | 8486 / 32 | 8760 / 68 | 8760 / 68 | 8680 / 4 | 8795 / 50 | 8695 / 19 | 8795 / 50 | — |
| docs.python.org/3.11/howto/index.html | 82 / 30 | 556 / 68 | 556 / 68 | 360 / 4 | 471 / 51 | 376 / 20 | 471 / 51 | — |
| docs.python.org/3.11/installing/index.html | 1236 / 27 | 1816 / 68 | 1816 / 68 | 1621 / 4 | 1733 / 52 | 1638 / 21 | 1733 / 52 | — |
| docs.python.org/3.11/library/index.html | 2332 / 29 | 2707 / 68 | 2707 / 68 | 2511 / 4 | 2624 / 53 | 2529 / 22 | 2624 / 53 | — |
| docs.python.org/3.11/license.html | 7696 / 32 | 8309 / 68 | 8309 / 68 | 8130 / 4 | 8242 / 52 | 8147 / 21 | 8242 / 52 | — |
| docs.python.org/3.11/py-modindex.html | 4102 / 0 | 4498 / 68 | 4498 / 68 | 4287 / 4 | 4402 / 55 | 4307 / 24 | 4402 / 55 | — |
| docs.python.org/3.11/reference/index.html | 471 / 33 | 846 / 68 | 846 / 68 | 650 / 4 | 763 / 53 | 668 / 22 | 763 / 53 | — |
| docs.python.org/3.11/search.html | 13 / 0 | 334 / 68 | 334 / 68 | 147 / 4 | 437 / 230 | 342 / 199 | 437 / 230 | — |
| docs.python.org/3.11/tutorial/index.html | 1024 / 28 | 1398 / 68 | 1398 / 68 | 1202 / 4 | 1314 / 52 | 1219 / 21 | 1314 / 52 | — |
| docs.python.org/3.11/using/index.html | 508 / 32 | 888 / 68 | 888 / 68 | 692 / 4 | 805 / 53 | 710 / 22 | 805 / 53 | — |
| docs.python.org/3.11/whatsnew/3.11.html | 13307 / 32 | 14517 / 68 | 14517 / 68 | 14330 / 4 | 14445 / 54 | 14349 / 23 | 14445 / 54 | — |
| docs.python.org/3.11/whatsnew/index.html | 2390 / 34 | 2773 / 68 | 2773 / 68 | 2576 / 4 | 2689 / 53 | 2594 / 22 | 2689 / 53 | — |
| docs.python.org/3.12 | 195 / 4 | 712 / 68 | 712 / 68 | 525 / 4 | 632 / 47 | 537 / 16 | 632 / 47 | — |
| docs.python.org/3.12/about.html | 211 / 26 | 609 / 68 | 609 / 68 | 415 / 4 | 527 / 52 | 432 / 21 | 527 / 52 | — |
| docs.python.org/3.12/bugs.html | 724 / 32 | 1130 / 68 | 1130 / 68 | 942 / 4 | 1054 / 52 | 959 / 21 | 1054 / 52 | — |
| docs.python.org/3.12/c-api/index.html | 447 / 33 | 824 / 68 | 824 / 68 | 630 / 4 | 743 / 53 | 648 / 22 | 743 / 53 | — |
| docs.python.org/3.12/contents.html | 19884 / 30 | 20235 / 68 | 20235 / 68 | 20040 / 4 | 20152 / 52 | 20057 / 21 | 20152 / 52 | — |
| docs.python.org/3.12/deprecations/index.html | 2635 / 28 | 3378 / 68 | 3378 / 68 | 3182 / 4 | 3292 / 50 | 3197 / 19 | 3292 / 50 | — |
| docs.python.org/3.12/download.html | 267 / 3 | 586 / 68 | 586 / 68 | 394 / 4 | 504 / 50 | 409 / 19 | 504 / 50 | — |
| docs.python.org/3.12/extending/index.html | 607 / 35 | 1102 / 68 | 1102 / 68 | 909 / 4 | 1024 / 55 | 929 / 24 | 1024 / 55 | — |
| docs.python.org/3.12/glossary.html | 8740 / 29 | 8999 / 68 | 8999 / 68 | 8909 / 4 | 9039 / 50 | 8924 / 19 | 9039 / 50 | — |
| docs.python.org/3.12/howto/index.html | 177 / 29 | 562 / 68 | 562 / 68 | 368 / 4 | 479 / 51 | 384 / 20 | 479 / 51 | — |
| docs.python.org/3.12/installing/index.html | 1233 / 27 | 1811 / 68 | 1811 / 68 | 1618 / 4 | 1730 / 52 | 1635 / 21 | 1730 / 52 | — |
| docs.python.org/3.12/library/index.html | 2316 / 29 | 2689 / 68 | 2689 / 68 | 2495 / 4 | 2608 / 53 | 2513 / 22 | 2608 / 53 | — |
| docs.python.org/3.12/license.html | 7747 / 32 | 8320 / 68 | 8320 / 68 | 8143 / 4 | 8255 / 52 | 8160 / 21 | 8255 / 52 | — |
| docs.python.org/3.12/py-modindex.html | 3602 / 0 | 3996 / 68 | 3996 / 68 | 3787 / 4 | 3902 / 55 | 3807 / 24 | 3902 / 55 | — |
| docs.python.org/3.12/reference/index.html | 481 / 33 | 854 / 68 | 854 / 68 | 660 / 4 | 773 / 53 | 678 / 22 | 773 / 53 | — |
| docs.python.org/3.12/tutorial/index.html | 1023 / 28 | 1395 / 68 | 1395 / 68 | 1201 / 4 | 1313 / 52 | 1218 / 21 | 1313 / 52 | — |
| docs.python.org/3.12/using/index.html | 534 / 32 | 912 / 68 | 912 / 68 | 718 / 4 | 831 / 53 | 736 / 22 | 831 / 53 | — |
| docs.python.org/3.12/whatsnew/3.12.html | 15327 / 33 | 16742 / 68 | 16742 / 68 | 16524 / 4 | 16660 / 54 | 16543 / 23 | 16660 / 54 | — |
| docs.python.org/3.12/whatsnew/index.html | 2498 / 34 | 2879 / 68 | 2879 / 68 | 2684 / 4 | 2797 / 53 | 2702 / 22 | 2797 / 53 | — |
| docs.python.org/3.13 | 195 / 4 | 712 / 68 | 712 / 68 | 525 / 4 | 632 / 47 | 537 / 16 | 632 / 47 | — |
| docs.python.org/3.13/about.html | 211 / 26 | 609 / 68 | 609 / 68 | 415 / 4 | 527 / 52 | 432 / 21 | 527 / 52 | — |
| docs.python.org/3.13/c-api/index.html | 496 / 33 | 873 / 68 | 873 / 68 | 679 / 4 | 792 / 53 | 697 / 22 | 792 / 53 | — |
| docs.python.org/3.13/contents.html | 20979 / 27 | 21333 / 68 | 21333 / 68 | 21138 / 4 | 21250 / 52 | 21155 / 21 | 21250 / 52 | — |
| docs.python.org/3.13/copyright.html | 85 / 27 | 460 / 68 | 460 / 68 | 264 / 4 | 374 / 50 | 279 / 19 | 374 / 50 | — |
| docs.python.org/3.13/deprecations/index.html | 2811 / 28 | 3671 / 68 | 3671 / 68 | 3475 / 4 | 3585 / 50 | 3490 / 19 | 3585 / 50 | — |
| docs.python.org/3.13/download.html | 152 / 3 | 471 / 68 | 471 / 68 | 279 / 4 | 389 / 50 | 294 / 19 | 389 / 50 | — |
| docs.python.org/3.13/extending/index.html | 566 / 35 | 1062 / 68 | 1062 / 68 | 868 / 4 | 983 / 55 | 888 / 24 | 983 / 55 | — |
| docs.python.org/3.13/glossary.html | 10616 / 29 | 10850 / 68 | 10850 / 68 | 10785 / 4 | 10916 / 50 | 10800 / 19 | 10916 / 50 | — |
| docs.python.org/3.13/howto/index.html | 203 / 29 | 584 / 68 | 584 / 68 | 390 / 4 | 501 / 51 | 406 / 20 | 501 / 51 | — |
| docs.python.org/3.13/installing/index.html | 1010 / 31 | 1548 / 68 | 1548 / 68 | 1353 / 4 | 1465 / 52 | 1370 / 21 | 1465 / 52 | — |
| docs.python.org/3.13/library/index.html | 2153 / 29 | 2526 / 68 | 2526 / 68 | 2332 / 4 | 2445 / 53 | 2350 / 22 | 2445 / 53 | — |
| docs.python.org/3.13/license.html | 7923 / 32 | 8523 / 68 | 8523 / 68 | 8329 / 4 | 8441 / 52 | 8346 / 21 | 8441 / 52 | — |
| docs.python.org/3.13/py-modindex.html | 3489 / 0 | 3883 / 68 | 3883 / 68 | 3674 / 4 | 3789 / 55 | 3694 / 24 | 3789 / 55 | — |
| docs.python.org/3.13/tutorial/index.html | 1057 / 28 | 1429 / 68 | 1429 / 68 | 1235 / 4 | 1347 / 52 | 1252 / 21 | 1347 / 52 | — |
| docs.python.org/3.13/using/index.html | 313 / 32 | 691 / 68 | 691 / 68 | 497 / 4 | 610 / 53 | 515 / 22 | 610 / 53 | — |
| docs.python.org/3.13/whatsnew/3.13.html | 16950 / 33 | 18380 / 68 | 18380 / 68 | 18181 / 4 | 18302 / 54 | 18200 / 23 | 18302 / 54 | — |
| docs.python.org/3.13/whatsnew/index.html | 2572 / 34 | 2953 / 68 | 2953 / 68 | 2758 / 4 | 2871 / 53 | 2776 / 22 | 2871 / 53 | — |
| docs.python.org/3.14 | 195 / 4 | 712 / 68 | 712 / 68 | 525 / 4 | 632 / 47 | 537 / 16 | 632 / 47 | — |
| docs.python.org/3.14/about.html | 211 / 26 | 617 / 68 | 617 / 68 | 495 / 4 | 607 / 52 | 512 / 21 | 607 / 52 | — |
| docs.python.org/3.14/c-api/index.html | 589 / 33 | 974 / 68 | 974 / 68 | 852 / 4 | 965 / 53 | 870 / 22 | 965 / 53 | — |
| docs.python.org/3.14/contents.html | 22218 / 30 | 22582 / 68 | 22582 / 68 | 22454 / 4 | 22566 / 52 | 22471 / 21 | 22566 / 52 | — |
| docs.python.org/3.14/copyright.html | 86 / 28 | 468 / 68 | 468 / 68 | 344 / 4 | 454 / 50 | 359 / 19 | 454 / 50 | — |
| docs.python.org/3.14/deprecations/index.html | 3109 / 30 | 3782 / 68 | 3782 / 68 | 3659 / 4 | 3770 / 50 | 3674 / 19 | 3770 / 50 | — |
| docs.python.org/3.14/download.html | 132 / 3 | 451 / 68 | 451 / 68 | 259 / 4 | 369 / 50 | 274 / 19 | 369 / 50 | — |
| docs.python.org/3.14/extending/index.html | 566 / 35 | 1070 / 68 | 1070 / 68 | 948 / 4 | 1063 / 55 | 968 / 24 | 1063 / 55 | — |
| docs.python.org/3.14/glossary.html | 11351 / 29 | 11582 / 68 | 11582 / 68 | 11600 / 4 | 11731 / 50 | 11615 / 19 | 11731 / 50 | — |
| docs.python.org/3.14/howto/index.html | 207 / 29 | 596 / 68 | 596 / 68 | 474 / 4 | 585 / 51 | 490 / 20 | 585 / 51 | — |
| docs.python.org/3.14/library/index.html | 2236 / 29 | 2617 / 68 | 2617 / 68 | 2495 / 4 | 2608 / 53 | 2513 / 22 | 2608 / 53 | — |
| docs.python.org/3.14/py-modindex.html | 3551 / 0 | 3948 / 68 | 3948 / 68 | 3736 / 4 | 3851 / 55 | 3756 / 24 | 3851 / 55 | — |
| docs.python.org/3.14/reference/index.html | 498 / 33 | 879 / 68 | 879 / 68 | 757 / 4 | 870 / 53 | 775 / 22 | 870 / 53 | — |
| docs.python.org/3.14/tutorial/index.html | 1057 / 28 | 1437 / 68 | 1437 / 68 | 1315 / 4 | 1427 / 52 | 1332 / 21 | 1427 / 52 | — |
| docs.python.org/3.14/using/index.html | 317 / 32 | 703 / 68 | 703 / 68 | 581 / 4 | 694 / 53 | 599 / 22 | 694 / 53 | — |
| docs.python.org/3.14/whatsnew/3.14.html | 19724 / 33 | 21273 / 68 | 21273 / 68 | 21115 / 4 | 21256 / 54 | 21134 / 23 | 21256 / 54 | — |
| docs.python.org/3.14/whatsnew/index.html | 2617 / 34 | 3006 / 68 | 3006 / 68 | 2883 / 4 | 2996 / 53 | 2901 / 22 | 2996 / 53 | — |
| docs.python.org/3.15 | 195 / 4 | 709 / 67 | 709 / 67 | 525 / 4 | 629 / 46 | 537 / 16 | 629 / 46 | — |
| docs.python.org/3.15/about.html | 209 / 26 | 612 / 67 | 612 / 67 | 493 / 4 | 602 / 51 | 510 / 21 | 602 / 51 | — |
| docs.python.org/3.15/bugs.html | 682 / 32 | 1093 / 67 | 1093 / 67 | 980 / 4 | 1089 / 51 | 997 / 21 | 1089 / 51 | — |
| docs.python.org/3.15/c-api/index.html | 595 / 33 | 973 / 67 | 973 / 67 | 854 / 4 | 964 / 52 | 872 / 22 | 964 / 52 | — |
| docs.python.org/3.15/contents.html | 22640 / 32 | 23003 / 67 | 23003 / 67 | 22874 / 4 | 22983 / 51 | 22891 / 21 | 22983 / 51 | — |
| docs.python.org/3.15/deprecations/index.html | 3667 / 30 | 4385 / 67 | 4385 / 67 | 4265 / 4 | 4373 / 49 | 4280 / 19 | 4373 / 49 | — |
| docs.python.org/3.15/download.html | 132 / 3 | 448 / 67 | 448 / 67 | 259 / 4 | 366 / 49 | 274 / 19 | 366 / 49 | — |
| docs.python.org/3.15/extending/index.html | 642 / 35 | 1098 / 67 | 1098 / 67 | 979 / 4 | 1091 / 54 | 999 / 24 | 1091 / 54 | — |
| docs.python.org/3.15/howto/index.html | 208 / 29 | 594 / 67 | 594 / 67 | 475 / 4 | 583 / 50 | 491 / 20 | 583 / 50 | — |
| docs.python.org/3.15/library/index.html | 2256 / 29 | 2634 / 67 | 2634 / 67 | 2515 / 4 | 2625 / 52 | 2533 / 22 | 2625 / 52 | — |
| docs.python.org/3.15/license.html | 8612 / 32 | 9235 / 67 | 9235 / 67 | 9116 / 4 | 9225 / 51 | 9133 / 21 | 9225 / 51 | — |
| docs.python.org/3.15/py-modindex.html | 3588 / 0 | 3984 / 67 | 3984 / 67 | 3773 / 4 | 3885 / 54 | 3793 / 24 | 3885 / 54 | — |
| docs.python.org/3.15/tutorial/index.html | 1065 / 28 | 1442 / 67 | 1442 / 67 | 1323 / 4 | 1432 / 51 | 1340 / 21 | 1432 / 51 | — |
| docs.python.org/3.15/whatsnew/3.15.html | 12088 / 31 | 13352 / 67 | 13352 / 67 | 13197 / 4 | 13326 / 53 | 13216 / 23 | 13326 / 53 | — |
| docs.python.org/3.15/whatsnew/index.html | 2641 / 34 | 3027 / 67 | 3027 / 67 | 2907 / 4 | 3017 / 52 | 2925 / 22 | 3017 / 52 | — |
| docs.python.org/3.2 | 185 / 0 | 298 / 0 | 298 / 0 | — | 324 / 20 | 323 / 20 | 324 / 20 | — |
| docs.python.org/3.3 | 185 / 0 | 298 / 0 | 298 / 0 | — | 324 / 20 | 323 / 20 | 324 / 20 | — |
| docs.python.org/3.3/about.html | 179 / 0 | 319 / 0 | 319 / 0 | — | 338 / 22 | 337 / 22 | 338 / 22 | — |
| docs.python.org/3.3/bugs.html | 596 / 0 | 746 / 0 | 746 / 0 | — | 766 / 21 | 765 / 21 | 766 / 21 | — |
| docs.python.org/3.3/c-api/index.html | 318 / 0 | 416 / 0 | 416 / 0 | — | 436 / 23 | 435 / 23 | 436 / 23 | — |
| docs.python.org/3.3/contents.html | 14428 / 0 | 14515 / 0 | 14515 / 0 | — | 14533 / 22 | 14532 / 22 | 14533 / 22 | — |
| docs.python.org/3.3/copyright.html | 96 / 0 | 192 / 0 | 192 / 0 | — | 207 / 20 | 206 / 20 | 207 / 20 | — |
| docs.python.org/3.3/distutils/index.html | 772 / 0 | 871 / 0 | 871 / 0 | — | 893 / 22 | 892 / 22 | 893 / 22 | — |
| docs.python.org/3.3/download.html | 270 / 0 | 344 / 0 | 344 / 0 | — | 361 / 20 | 360 / 20 | 361 / 20 | — |
| docs.python.org/3.3/extending/index.html | 437 / 0 | 541 / 0 | 541 / 0 | — | 563 / 25 | 562 / 25 | 563 / 25 | — |
| docs.python.org/3.3/faq/index.html | 29 / 29 | 192 / 0 | 192 / 0 | — | 212 / 23 | 211 / 23 | 212 / 23 | — |
| docs.python.org/3.3/genindex.html | 104 / 0 | 216 / 0 | 216 / 0 | — | 233 / 20 | 232 / 20 | 233 / 20 | — |
| docs.python.org/3.3/glossary.html | 5590 / 0 | 5615 / 0 | 5615 / 0 | — | 5717 / 20 | 5712 / 20 | 5717 / 20 | — |
| docs.python.org/3.3/howto/index.html | 95 / 0 | 274 / 0 | 274 / 0 | — | 292 / 21 | 291 / 21 | 292 / 21 | — |
| docs.python.org/3.3/install/index.html | 6793 / 0 | 6931 / 0 | 6931 / 0 | — | 6906 / 22 | 6905 / 22 | 6906 / 22 | — |
| docs.python.org/3.3/library/index.html | 2435 / 0 | 2531 / 0 | 2531 / 0 | — | 2551 / 23 | 2550 / 23 | 2551 / 23 | — |
| docs.python.org/3.3/license.html | 6243 / 0 | 6431 / 0 | 6431 / 0 | — | 6450 / 22 | 6449 / 22 | 6450 / 22 | — |
| docs.python.org/3.3/py-modindex.html | 3758 / 0 | 3897 / 0 | 3897 / 0 | — | 3903 / 25 | 3902 / 25 | 3903 / 25 | — |
| docs.python.org/3.3/reference/index.html | 446 / 0 | 544 / 0 | 544 / 0 | — | 564 / 23 | 563 / 23 | 564 / 23 | — |
| docs.python.org/3.3/search.html | 51 / 0 | 123 / 0 | 123 / 0 | — | 144 / 24 | 143 / 24 | 144 / 24 | — |
| docs.python.org/3.3/tutorial/index.html | 951 / 0 | 1045 / 0 | 1045 / 0 | — | 1064 / 22 | 1063 / 22 | 1064 / 22 | — |
| docs.python.org/3.3/using/index.html | 320 / 0 | 473 / 0 | 473 / 0 | — | 493 / 23 | 492 / 23 | 493 / 23 | — |
| docs.python.org/3.3/whatsnew/3.3.html | 13595 / 0 | 14113 / 0 | 14113 / 0 | — | 14166 / 24 | 14150 / 24 | 14166 / 24 | — |
| docs.python.org/3.3/whatsnew/index.html | 1205 / 0 | 1430 / 0 | 1430 / 0 | — | 1449 / 23 | 1448 / 23 | 1449 / 23 | — |
| docs.python.org/3.4 | 191 / 0 | 336 / 28 | 336 / 28 | — | 361 / 47 | 360 / 47 | 361 / 47 | — |
| docs.python.org/3.4/about.html | 179 / 0 | 347 / 28 | 347 / 28 | — | 365 / 49 | 364 / 49 | 365 / 49 | — |
| docs.python.org/3.4/bugs.html | 596 / 0 | 774 / 28 | 774 / 28 | — | 793 / 48 | 792 / 48 | 793 / 48 | — |
| docs.python.org/3.4/c-api/index.html | 334 / 0 | 460 / 28 | 460 / 28 | — | 479 / 50 | 478 / 50 | 479 / 50 | — |
| docs.python.org/3.4/contents.html | 15636 / 0 | 15751 / 28 | 15751 / 28 | — | 15768 / 49 | 15767 / 49 | 15768 / 49 | — |
| docs.python.org/3.4/copyright.html | 96 / 0 | 220 / 28 | 220 / 28 | — | 234 / 47 | 233 / 47 | 234 / 47 | — |
| docs.python.org/3.4/distributing/index.html | 978 / 0 | 1190 / 28 | 1190 / 28 | — | 1214 / 49 | 1213 / 49 | 1214 / 49 | — |
| docs.python.org/3.4/download.html | 266 / 0 | 368 / 28 | 368 / 28 | — | 384 / 47 | 383 / 47 | 384 / 47 | — |
| docs.python.org/3.4/extending/index.html | 507 / 0 | 758 / 28 | 758 / 28 | — | 780 / 52 | 779 / 52 | 780 / 52 | — |
| docs.python.org/3.4/faq/index.html | 27 / 27 | 211 / 28 | 211 / 28 | — | 230 / 50 | 229 / 50 | 230 / 50 | — |
| docs.python.org/3.4/genindex.html | 27 / 27 | 244 / 28 | 244 / 28 | — | 260 / 47 | 259 / 47 | 260 / 47 | — |
| docs.python.org/3.4/glossary.html | 5774 / 0 | 5818 / 28 | 5818 / 28 | — | 5928 / 47 | 5923 / 47 | 5928 / 47 | — |
| docs.python.org/3.4/howto/index.html | 95 / 0 | 306 / 28 | 306 / 28 | — | 323 / 48 | 322 / 48 | 323 / 48 | — |
| docs.python.org/3.4/installing/index.html | 1136 / 0 | 1404 / 28 | 1404 / 28 | — | 1425 / 49 | 1424 / 49 | 1425 / 49 | — |
| docs.python.org/3.4/library/index.html | 2498 / 0 | 2622 / 28 | 2622 / 28 | — | 2641 / 50 | 2640 / 50 | 2641 / 50 | — |
| docs.python.org/3.4/license.html | 6644 / 0 | 6890 / 28 | 6890 / 28 | — | 6908 / 49 | 6907 / 49 | 6908 / 49 | — |
| docs.python.org/3.4/py-modindex.html | 3846 / 0 | 4013 / 28 | 4013 / 28 | — | 4018 / 52 | 4017 / 52 | 4018 / 52 | — |
| docs.python.org/3.4/reference/index.html | 458 / 0 | 584 / 28 | 584 / 28 | — | 603 / 50 | 602 / 50 | 603 / 50 | — |
| docs.python.org/3.4/search.html | 51 / 0 | 151 / 28 | 151 / 28 | — | 171 / 51 | 170 / 51 | 171 / 51 | — |
| docs.python.org/3.4/tutorial/index.html | 979 / 0 | 1101 / 28 | 1101 / 28 | — | 1119 / 49 | 1118 / 49 | 1119 / 49 | — |
| docs.python.org/3.4/using/index.html | 360 / 0 | 486 / 28 | 486 / 28 | — | 505 / 50 | 504 / 50 | 505 / 50 | — |
| docs.python.org/3.4/whatsnew/3.4.html | 16183 / 0 | 16323 / 28 | 16323 / 28 | — | 16350 / 51 | 16344 / 51 | 16350 / 51 | — |
| docs.python.org/3.4/whatsnew/index.html | 1464 / 0 | 1593 / 28 | 1593 / 28 | — | 1611 / 50 | 1610 / 50 | 1611 / 50 | — |
| docs.python.org/3.5 | 186 / 0 | 371 / 28 | 371 / 28 | — | 353 / 29 | 324 / 29 | 353 / 29 | — |
| docs.python.org/3.5/about.html | 180 / 0 | 397 / 28 | 397 / 28 | — | 374 / 34 | 345 / 34 | 374 / 34 | — |
| docs.python.org/3.5/bugs.html | 631 / 0 | 856 / 28 | 856 / 28 | — | 835 / 34 | 806 / 34 | 835 / 34 | — |
| docs.python.org/3.5/c-api/index.html | 323 / 0 | 535 / 28 | 535 / 28 | — | 513 / 35 | 484 / 35 | 513 / 35 | — |
| docs.python.org/3.5/contents.html | 16248 / 0 | 16441 / 28 | 16441 / 28 | — | 16417 / 34 | 16388 / 34 | 16417 / 34 | — |
| docs.python.org/3.5/copyright.html | 58 / 0 | 269 / 28 | 269 / 28 | — | 242 / 32 | 213 / 32 | 242 / 32 | — |
| docs.python.org/3.5/distributing/index.html | 978 / 0 | 1236 / 28 | 1236 / 28 | — | 1219 / 34 | 1190 / 34 | 1219 / 34 | — |
| docs.python.org/3.5/download.html | 255 / 0 | 413 / 28 | 413 / 28 | — | 389 / 32 | 360 / 32 | 389 / 32 | — |
| docs.python.org/3.5/extending/index.html | 514 / 0 | 811 / 28 | 811 / 28 | — | 792 / 37 | 763 / 37 | 792 / 37 | — |
| docs.python.org/3.5/glossary.html | 6315 / 0 | 6440 / 28 | 6440 / 28 | — | 6518 / 32 | 6485 / 32 | 6518 / 32 | — |
| docs.python.org/3.5/howto/index.html | 52 / 0 | 345 / 28 | 345 / 28 | — | 321 / 33 | 292 / 33 | 321 / 33 | — |
| docs.python.org/3.5/installing/index.html | 1166 / 0 | 1479 / 28 | 1479 / 28 | — | 1459 / 34 | 1430 / 34 | 1459 / 34 | — |
| docs.python.org/3.5/library/index.html | 2476 / 0 | 2685 / 28 | 2685 / 28 | — | 2663 / 35 | 2634 / 35 | 2663 / 35 | — |
| docs.python.org/3.5/license.html | 6671 / 0 | 6993 / 28 | 6993 / 28 | — | 6970 / 34 | 6941 / 34 | 6970 / 34 | — |
| docs.python.org/3.5/py-modindex.html | 3873 / 0 | 4099 / 28 | 4099 / 28 | — | 4063 / 37 | 4034 / 37 | 4063 / 37 | — |
| docs.python.org/3.5/using/index.html | 351 / 0 | 563 / 28 | 563 / 28 | — | 541 / 35 | 512 / 35 | 541 / 35 | — |
| docs.python.org/3.5/whatsnew/3.5.html | 11914 / 0 | 12519 / 28 | 12519 / 28 | — | 12513 / 36 | 12460 / 36 | 12513 / 36 | — |
| docs.python.org/3.5/whatsnew/index.html | 1490 / 0 | 1706 / 28 | 1706 / 28 | — | 1683 / 35 | 1654 / 35 | 1683 / 35 | — |
| docs.python.org/3.6 | 186 / 0 | 371 / 28 | 371 / 28 | — | 353 / 29 | 324 / 29 | 353 / 29 | — |
| docs.python.org/3.6/about.html | 180 / 0 | 397 / 28 | 397 / 28 | — | 374 / 34 | 345 / 34 | 374 / 34 | — |
| docs.python.org/3.6/bugs.html | 631 / 0 | 856 / 28 | 856 / 28 | — | 835 / 34 | 806 / 34 | 835 / 34 | — |
| docs.python.org/3.6/c-api/index.html | 325 / 0 | 537 / 28 | 537 / 28 | — | 515 / 35 | 486 / 35 | 515 / 35 | — |
| docs.python.org/3.6/contents.html | 17414 / 0 | 17607 / 28 | 17607 / 28 | — | 17583 / 34 | 17554 / 34 | 17583 / 34 | — |
| docs.python.org/3.6/copyright.html | 58 / 0 | 269 / 28 | 269 / 28 | — | 242 / 32 | 213 / 32 | 242 / 32 | — |
| docs.python.org/3.6/distributing/index.html | 968 / 0 | 1228 / 28 | 1228 / 28 | — | 1209 / 34 | 1180 / 34 | 1209 / 34 | — |
| docs.python.org/3.6/download.html | 255 / 0 | 413 / 28 | 413 / 28 | — | 389 / 32 | 360 / 32 | 389 / 32 | — |
| docs.python.org/3.6/extending/index.html | 578 / 0 | 875 / 28 | 875 / 28 | — | 856 / 37 | 827 / 37 | 856 / 37 | — |
| docs.python.org/3.6/glossary.html | 7083 / 0 | 7198 / 28 | 7198 / 28 | — | 7286 / 32 | 7253 / 32 | 7286 / 32 | — |
| docs.python.org/3.6/howto/index.html | 52 / 0 | 352 / 28 | 352 / 28 | — | 328 / 33 | 299 / 33 | 328 / 33 | — |
| docs.python.org/3.6/installing/index.html | 1237 / 0 | 1567 / 28 | 1567 / 28 | — | 1545 / 34 | 1516 / 34 | 1545 / 34 | — |
| docs.python.org/3.6/library/index.html | 2487 / 0 | 2696 / 28 | 2696 / 28 | — | 2674 / 35 | 2645 / 35 | 2674 / 35 | — |
| docs.python.org/3.6/license.html | 6672 / 0 | 6994 / 28 | 6994 / 28 | — | 6971 / 34 | 6942 / 34 | 6971 / 34 | — |
| docs.python.org/3.6/py-modindex.html | 3882 / 0 | 4108 / 28 | 4108 / 28 | — | 4072 / 37 | 4043 / 37 | 4072 / 37 | — |
| docs.python.org/3.6/reference/index.html | 428 / 0 | 643 / 28 | 643 / 28 | — | 621 / 35 | 592 / 35 | 621 / 35 | — |
| docs.python.org/3.6/search.html | 51 / 0 | 205 / 28 | 205 / 28 | — | 180 / 32 | 151 / 32 | 180 / 32 | — |
| docs.python.org/3.6/tutorial/index.html | 935 / 0 | 1141 / 28 | 1141 / 28 | — | 1118 / 34 | 1089 / 34 | 1118 / 34 | — |
| docs.python.org/3.6/using/index.html | 346 / 0 | 558 / 28 | 558 / 28 | — | 536 / 35 | 507 / 35 | 536 / 35 | — |
| docs.python.org/3.6/whatsnew/3.6.html | 12608 / 0 | 13340 / 28 | 13340 / 28 | — | 13330 / 36 | 13293 / 36 | 13330 / 36 | — |
| docs.python.org/3.6/whatsnew/index.html | 1657 / 0 | 1873 / 28 | 1873 / 28 | — | 1850 / 35 | 1821 / 35 | 1850 / 35 | — |
| docs.python.org/3.7 | 186 / 0 | 371 / 28 | 371 / 28 | — | 363 / 39 | 334 / 39 | 363 / 39 | — |
| docs.python.org/3.7/about.html | 180 / 0 | 397 / 28 | 397 / 28 | — | 384 / 44 | 355 / 44 | 384 / 44 | — |
| docs.python.org/3.7/bugs.html | 599 / 0 | 824 / 28 | 824 / 28 | — | 813 / 44 | 784 / 44 | 813 / 44 | — |
| docs.python.org/3.7/c-api/index.html | 352 / 0 | 564 / 28 | 564 / 28 | — | 552 / 45 | 523 / 45 | 552 / 45 | — |
| docs.python.org/3.7/contents.html | 16858 / 0 | 17051 / 28 | 17051 / 28 | — | 17037 / 44 | 17008 / 44 | 17037 / 44 | — |
| docs.python.org/3.7/distributing/index.html | 973 / 0 | 1236 / 28 | 1236 / 28 | — | 1227 / 44 | 1198 / 44 | 1227 / 44 | — |
| docs.python.org/3.7/download.html | 241 / 0 | 399 / 28 | 399 / 28 | — | 385 / 42 | 356 / 42 | 385 / 42 | — |
| docs.python.org/3.7/extending/index.html | 578 / 0 | 872 / 28 | 872 / 28 | — | 863 / 47 | 834 / 47 | 863 / 47 | — |
| docs.python.org/3.7/glossary.html | 7203 / 0 | 7317 / 28 | 7317 / 28 | — | 7417 / 42 | 7383 / 42 | 7417 / 42 | — |
| docs.python.org/3.7/installing/index.html | 1237 / 0 | 1567 / 28 | 1567 / 28 | — | 1555 / 44 | 1526 / 44 | 1555 / 44 | — |
| docs.python.org/3.7/library/index.html | 2214 / 0 | 2420 / 28 | 2420 / 28 | — | 2408 / 45 | 2379 / 45 | 2408 / 45 | — |
| docs.python.org/3.7/license.html | 6325 / 0 | 6642 / 28 | 6642 / 28 | — | 6629 / 44 | 6600 / 44 | 6629 / 44 | — |
| docs.python.org/3.7/py-modindex.html | 3898 / 0 | 4124 / 28 | 4124 / 28 | — | 4098 / 47 | 4069 / 47 | 4098 / 47 | — |
| docs.python.org/3.7/reference/index.html | 433 / 0 | 642 / 28 | 642 / 28 | — | 630 / 45 | 601 / 45 | 630 / 45 | — |
| docs.python.org/3.7/tutorial/index.html | 951 / 0 | 1157 / 28 | 1157 / 28 | — | 1144 / 44 | 1115 / 44 | 1144 / 44 | — |
| docs.python.org/3.7/using/index.html | 359 / 0 | 571 / 28 | 571 / 28 | — | 559 / 45 | 530 / 45 | 559 / 45 | — |
| docs.python.org/3.7/whatsnew/3.7.html | 13820 / 0 | 14487 / 28 | 14487 / 28 | — | 14486 / 46 | 14457 / 46 | 14486 / 46 | — |
| docs.python.org/3.7/whatsnew/index.html | 1896 / 0 | 2112 / 28 | 2112 / 28 | — | 2099 / 45 | 2070 / 45 | 2099 / 45 | — |
| docs.python.org/3.8 | 189 / 0 | 551 / 56 | 551 / 56 | — | 484 / 39 | 400 / 12 | 484 / 39 | — |
| docs.python.org/3.9 | 190 / 0 | 580 / 63 | 580 / 63 | — | 504 / 43 | 408 / 12 | 504 / 43 | — |
| docs.python.org/3/bugs.html | — | — | — | 980 / 4 | — | 997 / 21 | — | — |
| docs.python.org/3/license.html | — | — | — | 8679 / 4 | — | 8696 / 21 | — | — |
| docs.python.org/bugs.html | 682 / 32 | 1096 / 68 | 1096 / 68 | — | 1092 / 52 | — | 1092 / 52 | — |
| docs.python.org/license.html | 8187 / 32 | 8801 / 68 | 8801 / 68 | — | 8791 / 52 | — | 8791 / 52 | — |

</details>

## Related Reports

- [RETRIEVAL_COMPARISON.md](RETRIEVAL_COMPARISON.md) — does cleaner extraction
  actually improve retrieval? (Spoiler: modestly, but switching retrieval mode
  helps more than switching crawlers.)
- [SPEED_COMPARISON.md](SPEED_COMPARISON.md) — higher word counts don't mean
  higher quality; see speed vs output size trade-offs.
- [METHODOLOGY.md](METHODOLOGY.md) — full test setup and fairness decisions.

