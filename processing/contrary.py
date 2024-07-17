import re
import processing.rules as r

# Checks the length of the ## Thesis and ## Summary to ensure they fit within a certain length. Use regex to find the specific sections and count the number of words and characters. Use `entire_text = r.unite_valid_lines(text)` to process through the entire text if needed.

# Check if the following sections exist: "## Thesis", "## Founding Story", "## Product", "## Market", "### Customer", "### Market Size", "## Competition", "## Business Model", "## Traction", "## Valuation", "#Key Opportunities", "## Key Risks", "## Summary".

# “When using quotes. Periods go after the quotation marks”.

# Don't start sentence with However or Because.

# Don't use "this study found" or "this paper found" or "this source found"... Just link directly

# Passive voice detector... "has been, has become, has shown, has seen, that included, that plays, as well as, has the..., would need, etc" - is there a better algorithm for this?

# Implement Canonical dates. Find "currently has, current, currently, is in a place, as of now, recently, has recently, over the past few years, over the past, over the next, within the next, in the past, this year, this month, last month, last year, next year, next month, etc" and prompt to replace with specific dates.

# Only third person: there should be no use of “I”, “you”, “we”, "our", etc...

# Regex for all dates to flag for refresh updates... all years "xxxx" or months in a list.

# Regex for all numbers to follow the Notion guidelines: https://www.notion.so/contrary/Number-Formatting-FAQs-7f87f95f8d9d4755aa352232a1c8779f?pvs=4

# Check for the use of banned words: "unicorn, flourish, disrupt, ultimately, so, according to, overall, "impressive", "excellent", "hard-to-replicate", "industry-leading", "flourish", "tapestry", "vastly improved", "benefit tremendously", "explosion in companies using the open-source tool", "exponential growth", "ton of potential", "revolutionized", "renowned", etc" These are fluffly or filler language. Also check for commonly GPT words.

# Capitalize "Series" in "Series A, Series B, etc"

# Flag "they" to ensure it isn't referring to the company, which should be "it".

# Regex to enforce Oxford commas?

# For longer podcasts and videos and PDFs, ensure timestamps are included in the hyperlink.

# Ensure hyperlinks are within 1-3 words.

# Regex to ensure hyperlinks don't have: "#:~:text="

# Refer to all mentions of COVID-19 as "the COVID-19 pandemic"