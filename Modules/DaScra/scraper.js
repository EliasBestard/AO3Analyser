"use strict";
const cliProgress = require('cli-progress');
const dascra_cli = require('./dascra_cli')
const puppeteer = require("puppeteer");
const excel = require('exceljs');
const fs = require('fs')




// CLI
let args_mine =dascra_cli.args_mine;

const URLs = 
{
	site:
		"https://archiveofourown.org/",
	tag:
		args_mine.tag,
		// process.argv.length > 2 ? process.argv.slice(2).join("%20") : "How%20I%20Met%20Your%20Father%20(TV%202022)"
		// process.argv.length > 2 ? process.argv.slice(2).join("%20") : "Constance%20Raveau"
};


// ?page=

( async () => 
{	
	const browser = await puppeteer.launch(
	{
		headless: !args_mine.headless,
		args: ["--no-sandbox", "--disable-setuid-sandbox"]
	});
  
	try
	{
		const page = await browser.newPage();
		
		// If continuing an old iteration see where to beguin
		let row_count=0;
		var workbook = new excel.Workbook();
		var ws = NaN;
		
		// If continuing an old iteration scraping a certain tag, and the file exists
		if(args_mine.continue &  fs.existsSync(args_mine.output_path+args_mine.output_file+'.xlsx')){
			// Read the file and get the count of stories
			await workbook.xlsx.readFile(args_mine.output_path+args_mine.output_file+'.xlsx')
			.then(function() {
					if(args_mine.verbose){
						console.log("Reading existing file :"+args_mine.output_path+args_mine.output_file+'.xlsx')
					}
			        ws = workbook.getWorksheet('Sheet 1');
			        const rows = ws.getColumn(1);
					const rowsCount = rows['_worksheet']['_rows'].length;
					row_count= rowsCount-1
			    });
		}else{
			// If it is a new iteration or the file did not extit
			// Creates a new file and adds the header
			if(args_mine.verbose){
				console.log("Creating/Overwriting file :"+args_mine.output_path+args_mine.output_file+'.xlsx')
			}
			ws = workbook.addWorksheet('Sheet 1');
			const headers = [
				{ header: 'Title', key: 'title', width: 15, bold:true },
				{ header: 'AdditionalTags', key: 'at', width: 15 },
				{ header: 'ArchiveWarning', key: 'aw', width: 15 },
				{ header: 'Author', key: 'a', width: 15 },
				{ header: 'Bookmarks', key: 'b', width: 15 },
				{ header: 'Category', key: 'cat', width: 15 },
				{ header: 'Chapters', key: 'chapt', width: 15 },
				{ header: 'Characters', key: 'char', width: 15 },
				{ header: 'Comments', key: 'com', width: 15 },
				{ header: 'Fandom', key: 'fan', width: 15 },
				{ header: 'Hits', key: 'hit', width: 15 },
				{ header: 'Kudos', key: 'k', width: 15 },
				{ header: 'Language', key: 'lang', width: 15 },
				{ header: 'Rating', key: 'rating', width: 15 },
				{ header: 'Relationship', key: 'rel', width: 15 },
				{ header: 'Series', key: 'ser', width: 15 },
				{ header: 'Part', key: 'part', width: 15 },
				{ header: 'SourceURL', key: 'url', width: 15 },
				{ header: 'Updated', key: 'updated', width: 15 },
				{ header: 'Words', key: 'words', width: 15 },
			];
			ws.columns = headers;
			ws.getRow(1).style ={font: {bold: true}};
		}
		// Get the page from where to start to get the data and which story to start geting the data 
		let current_story_number = row_count%20;
		let work_page = Math.floor(row_count/20);
		
		if(args_mine.verbose){
			console.log('======================')
			console.log("stored stories-> "+row_count)
			console.log("starting from page -> "+work_page)
			console.log("current story-> "+current_story_number)
			console.log('======================')
		}
		
		// Go to the URL and accept requirements
		await page.goto(URLs.site + 'tags/' + URLs.tag + '/works?page='+work_page); 
		await page.waitForTimeout(2000);
		await page.$eval('input[id="tos_agree"]', check => check.click());
		await page.waitForTimeout(1000);
		await page.$eval('button[id="accept_tos"]', btn => btn.click());
		await page.waitForTimeout(1000);
		// If it was indicated to sort by kudos
		if( args_mine.kudo_sorting){
			await page.select('select[name="work_search[sort_column]"]', 'kudos_count');
			await page.waitForTimeout(1000);
			await page.click('input[value="Sort and Filter"]');
			await page.waitForTimeout(2000);
		}

		var works = [];
		let max_stories=1200
		
		const bar1 = new cliProgress.SingleBar({}, cliProgress.Presets.rect);
		if(args_mine.verbose){
			console.log('=================== Scraping ===================')
			bar1.start(max_stories, 0);

		}
		// Scraps 1000 stories per iteration
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
			if(args_mine.verbose){
				let actual_number=1200-max_stories
				// update the current value in your application..
				bar1.update(actual_number);
			}
			// GO to the next page
			let next = await page.evaluate(() => 
			{
				let nextEl = document.getElementsByClassName('next')[0];
				return nextEl ? nextEl.children[0].getAttribute('href') : 0;
			})
			
			if (!next)
				break;
			await page.goto(URLs.site + next); 
		}
		const bar2 = new cliProgress.SingleBar({}, cliProgress.Presets.shades_grey);
		
		if(args_mine.verbose){
			// stop the progress bar
			bar1.stop();
			console.log('=================== Writing ===================')
			bar2.start(1200, 0);
		}
		//write the info in the worksheet
		for (let n = current_story_number; n < works.length; n++)
		{
			let w = works[n];
			ws.addRow([
				w.title,
 				w.add_tags,
 				w.warning,
 				w.author,
 				w.bookmarks,
 				w.category,
 				w.chapters,
 				w.characters,
 				w.comments,
				w.fandoms,
				w.hits,
				w.kudos,
				w.language,
				w.rating,
				w.relationships,
				w.series,
				w.part,
				w.url,
				w.updated,
				w.words])
				if(args_mine.verbose & n%100==0){
					bar2.update(n);
					// let lenght_p=process.stdout.columns-15
					// console.log('='.repeat(Math.floor((n*lenght_p)/1000))+ n +'/1000')
			}
		}

		
		// ws.getCell(1, 1, 1, 20).style({font: {bold: true}});
	
		await workbook.xlsx.writeFile(args_mine.output_path+args_mine.output_file+".xlsx").then(() => {
			if(args_mine.verbose){
				bar2.update(1200)
				bar2.stop()
				console.log("========== Successfully stored =========")
			}
		  });
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