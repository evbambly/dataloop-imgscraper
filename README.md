# dataloop-imgscraper

Built with these specifications:


The goal of this exercise is to build a web crawler CLI. 

The CLI is a node.js/python/typescript application. 

CLI usage: 

	node crawler.js <start_url: string> <depth: number>
  
Description:

Given a url, the crawler will scan the webpage for any images, and continue to every link inside that page and scan it as well. 

The crawling should stop once <depth> is reached. depth=3 means we can go as deep as 3 pages from the source url (denoted by the < start_url > param), and depth=0 is just the first page. 

  
Results should be saved into a results.json file in the following format:
  
	results: [
  
		{
  
			imageUrl: string,
  
			sourceUrl: string // the page url this image was found on
  
			depth: number // the depth of the source at which this image was found on
  
		}
  
	]

Web crawler introduction can be found here: https://en.wikipedia.org/wiki/Web_crawler
