Scraper

scraper.js is a Node.js command line script that gathers some information about fanworks from the site archiveofourown.org by given tag, and saves it in an .xlsx file.

Requirements
- Node.js runtime environment
- Internet connection

How to run
	node scraper.js [tag]
where [tag] may be omitted, or may consist from one or several words separated by spaces. If the tag is omitted, the script would work with the default tag "Constance Raveau".

How the script works
The script runs a headless browser instance and opens the link
	https://archiveofourown.org/tags/[tag]/works
where [tag] is from command line arguments or is the default tag.
The page containing links to Terms of Service and Privacy Policy is opened. The script checks the checkbox "I have read & understood the new Terms of Service and Privacy Policy" and press the button "I agree/consent to its terms".
The first page is opened, from a number of pages containing links to and short descriptions of various fanworks by given tag. The script collects the following attributes of each work, if presented:
	- additional tags
	- archive warning
	- author
	- number of bookmarks
	- category
	- number of chapters
	- number of comments
	- fandom
	- number of hits
	- number of kudos
	- language
	- rating
	- relationship
	- series
	- which part of series
	- URL
	- title
	- date when updated
	- number of words
Then the script proceeds to the next page, while there is one.
After processing all pages, the script creates in the current directory the file with the name
	[tag]_[DD_MMM_YYYY].xlsx
where [tag] is without spaces, and [DD_MMM_YYYY] is the current date, for example
	ConstanceRaveau_09_Jul_2021.xlsx
In the file the script fills a column for each of mentioned attributes. First line of the table contains names of attributes, then are lines for each fanwork.
About
No description, website, or topics provided.
Topics
Resources
 Readme
Releases
No releases published
Create a new release
Packages
No packages published
Publish your first package
Languages
JavaScript
100.0%
