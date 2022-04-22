"use strict";
const puppeteer = require("puppeteer");
const moment = require("moment");
const excel = require('excel4node');


const URLs = 
{
	site:
		"https://archiveofourown.org/",
	tag:
		process.argv.length > 2 ? process.argv.slice(2).join("%20") : "How%20I%20Met%20Your%20Father%20(TV%202022)"
		// process.argv.length > 2 ? process.argv.slice(2).join("%20") : "Constance%20Raveau"
};

( async () => 
{	
	const browser = await puppeteer.launch(
	{
		headless: false,
		args: ["--no-sandbox", "--disable-setuid-sandbox"],
		// headers:{
		// 	'User-Agent': 'bot'
		//   }
	});
  
	try
	{
	  
		const page = await browser.newPage();
		await page.goto(URLs.site + 'tags/' + URLs.tag + '/works'); 
		
		await page.waitForTimeout(2000);
		await page.$eval('input[id="tos_agree"]', check => check.click());
		await page.waitForTimeout(1000);
		await page.$eval('button[id="accept_tos"]', btn => btn.click());
		await page.waitForTimeout(1000);

		await page.select('select[name="work_search[sort_column]"]', 'kudos_count');
		await page.waitForTimeout(1000);
		await page.click('input[value="Sort and Filter"]');
		await page.waitForTimeout(2000);

		// await page.setUserAgent('bot');
		var works = [];
		let max_stories=100
		// while (true)
		while (max_stories>0)
		{
			works = works.concat (await page.evaluate(() => 
			{
				let elements = document.getElementsByClassName('work blurb group');
				let res = [];
				for (let element of elements)
				{
					function GetInnerTextOfNthElementByClassName(parent, name, n)
					{
						elem = parent.getElementsByClassName(name)[n];
						return elem ? elem.innerText : '';
					}

					work = {};
				
					work.url = element.getElementsByClassName('heading')[0].children[0].href;
					el = element.getElementsByClassName('heading')[0].children[0];
					work.title = el ? el.innerText : '';
//					console.log(work.title);
					el = element.getElementsByClassName('heading')[0].children[1];
					work.author = el ? el.innerText : '';
					work.fandoms = GetInnerTextOfNthElementByClassName(element.getElementsByClassName('fandoms heading')[0], 'tag', 0);
					work.rating = GetInnerTextOfNthElementByClassName(element.getElementsByClassName('required-tags')[0], 'text', 0);
					work.warning = GetInnerTextOfNthElementByClassName(element.getElementsByClassName('required-tags')[0], 'text', 1);
					work.category = GetInnerTextOfNthElementByClassName(element.getElementsByClassName('required-tags')[0], 'text', 2);
					work.updated = GetInnerTextOfNthElementByClassName(element, 'datetime', 0);
					work.characters = [].map.call(element.getElementsByClassName('characters'), (character=>{return character.children[0].innerText})).join(', ');
					work.language = GetInnerTextOfNthElementByClassName(element, 'language', 1);
					work.words = GetInnerTextOfNthElementByClassName(element, 'words', 1);
					work.chapters = GetInnerTextOfNthElementByClassName(element, 'chapters', 1);
					work.comments = GetInnerTextOfNthElementByClassName(element, 'comments', 1);
					work.kudos = GetInnerTextOfNthElementByClassName(element, 'kudos', 1);
					work.bookmarks = GetInnerTextOfNthElementByClassName(element, 'bookmarks', 1);
					work.hits = GetInnerTextOfNthElementByClassName(element, 'hits', 1);
					work.add_tags = [].map.call(element.getElementsByClassName('freeforms'), (form=>{return form.children[0].innerText})).join(', ');
					work.relationships = [].map.call(element.getElementsByClassName('relationships'), (rel=>{return rel.innerText})).join(', ');
					work.series = [].map.call(element.getElementsByClassName('series'), (form=>{return form.children[0].children[1].innerText})).join(', ');
					work.part = [].map.call(element.getElementsByClassName('series'), (form=>{return form.children[0].children[0].innerText})).join(', ');

					res.push(work);
				}
				return res;

			}));
			max_stories -=20 ;
			let next = await page.evaluate(() => 
			{
				let nextEl = document.getElementsByClassName('next')[0];
				return nextEl ? nextEl.children[0].getAttribute('href') : 0;
			})
			
			if (!next)
				break;
			await page.goto(URLs.site + next); 
		}
	
		// useful for debugging
		/* for (let work of works)
		 {
			console.log('title:      ' + work.title);
			console.log('url:        ' + work.url);
			console.log('author:     ' + work.author);
			console.log('fandoms:    ' + work.fandoms);
			console.log('rating:     ' + work.rating);
			console.log('warning:    ' + work.warning);
			console.log('category:   ' + work.category);
			console.log('updated:    ' + work.updated);
			console.log('characters: ' + work.characters);
			console.log('language:   ' + work.language);
			console.log('words:      ' + work.words);
			console.log('chapters:   ' + work.chapters);
			console.log('comments:   ' + work.comments);
			console.log('kudos:      ' + work.kudos);
			console.log('bookmarks:  ' + work.bookmarks);
			console.log('hits:       ' + work.hits);
			console.log('addit. tags:' + work.add_tags);
			console.log('rel-ships:  ' + work.relationships);
			console.log('series:     ' + work.series);
			console.log('part:       ' + work.part);
			console.log('---------------------------');
		} */
		
		var workbook = new excel.Workbook();
		var ws = workbook.addWorksheet('Sheet 1');
	
		for (let n = 0; n <= works.length; n++)
		{
			let w = works[n - 1];
			ws.cell(n + 1, 1).string(n ? w.add_tags	: "Additional Tags:");
			ws.cell(n + 1, 2).string(n ? w.warning 	: "Archive Warning:");
			ws.cell(n + 1, 3).string(n ? w.author 	: "Author:");
			ws.cell(n + 1, 4).string(n ? w.bookmarks 	: "Bookmarks:");
			ws.cell(n + 1, 5).string(n ? w.category 	: "Category:");
			ws.cell(n + 1, 6).string(n ? w.chapters 	: "Chapters:");
			ws.cell(n + 1, 7).string(n ? w.characters 	: "Characters:");
			ws.cell(n + 1, 8).string(n ? w.comments 	: "Comments:");
			ws.cell(n + 1, 9).string(n ? w.fandoms 		: "Fandom:");
			ws.cell(n + 1, 10).string(n ? w.hits 		: "Hits:");
			ws.cell(n + 1, 11).string(n ? w.kudos 		: "Kudos:");
			ws.cell(n + 1, 12).string(n ? w.language	: "Language:");
			ws.cell(n + 1, 13).string(n ? w.rating 		: "Rating:");
			ws.cell(n + 1, 14).string(n ? w.relationships	: "Relationship:");
			ws.cell(n + 1, 15).string(n ? w.series	 	: "Series:");
			ws.cell(n + 1, 16).string(n ? w.part	 	: "Part:");
			ws.cell(n + 1, 17).string(n ? w.url		: "Source URL:");
			ws.cell(n + 1, 18).string(n ? w.title	 	: "Title:");
			ws.cell(n + 1, 19).string(n ? w.updated	 	: "Updated:");
			ws.cell(n + 1, 20).string(n ? w.words	 	: "Words:");
		}
		
		ws.cell(1, 1, 1, 20).style({font: {bold: true}});
	
		// await workbook.write(URLs.tag.replace('%20', ' ') + '_' +
		// 	moment().format('DD_MMM_YYYY') +
		// 	'.xlsx');
		await workbook.write("dascra_output.xlsx");
	}
	catch (e)
	{
		console.log(e);
	}
	finally
	{
		await browser.close();
	}
		// process.exit(0);
})();