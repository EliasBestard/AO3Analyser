"use strict";
const puppeteer = require("puppeteer");
const fs = require("fs");
const tagscra_cli = require('./Utils/tagscra_cli');
const { mine_non_canonicals } = require("./Utils/utils_scraper");
const mine_RATAS = require('./Utils/utils_scraper').mine_RATAS


let args_mine = tagscra_cli.args_mine;

//TODO: Build a CLI
const URLs = {
	site:
		args_mine.AO3_version== 'current'? "https://archiveofourown.org/":"https://web.archive.org/web/20170825230518/https://archiveofourown.org/",
	tag:
		args_mine.tags,
		// process.argv.length > 3 ? process.argv.slice(3) : tag_to_mine,
};

switch (args_mine.AO3_version) {
	case 'current':
	  URLs.site = "https://archiveofourown.org/";
	  break;
	case '2021':
		URLs.site = "https://web.archive.org/web/20210125165441/https://archiveofourown.org/";
		// Ableism
		// URLs.site = "https://web.archive.org/web/20210125101651/https://archiveofourown.org/";
		break;
	case '2018':
		URLs.site = "https://web.archive.org/web/20180205161503/https://archiveofourown.org/";
		break;
	case '2017':
		URLs.site = "https://web.archive.org/web/20170723141339/https://archiveofourown.org/";
		break;
	case '2016':
		URLs.site = "https://web.archive.org/web/20160217094435/https://archiveofourown.org/";
		break;
	case '2015':
		URLs.site = "https://web.archive.org/web/20150105080944/https://archiveofourown.org/";
		// Ableism
		// URLs.site = "https://web.archive.org/web/20151122021416/https://archiveofourown.org/";
		break;
	case '2014':
		URLs.site = "https://web.archive.org/web/20140911124210/https://archiveofourown.org/";
		break;
	case '2013':
		URLs.site = "https://web.archive.org/web/20130907212114/https://archiveofourown.org/";
		break;
	// Ableism
	case '2011':
		URLs.site = "https://web.archive.org/web/20111128133119/https://archiveofourown.org/";
		break;
	default:
	  text = "https://archiveofourown.org/";
  }

// If only mining the non-canonical tags from a TAG
if(args_mine.freeforms){
	URLs.site="https://archiveofourown.org/tags/search?tag_search%5Bname%5D="+URLs.tag+"&tag_search%5Bfandoms%5D=&tag_search%5Btype%5D=Freeform&tag_search%5Bcanonical%5D=F&tag_search%5Bsort_column%5D=name&tag_search%5Bsort_direction%5D=asc&commit=Search+Tags"
}

// console.log(URLs.tag)


//  https://archiveofourown.org/tags/search?tag_search%5Bname%5D=Disability&tag_search%5Bfandoms%5D=&tag_search%5Btype%5D=Freeform&tag_search%5Bcanonical%5D=F&tag_search%5Bsort_column%5D=name&tag_search%5Bsort_direction%5D=asc&commit=Search+Tags

( async () => {	
	const browser = await puppeteer.launch({
		headless: args_mine.headless,
		args: ["--no-sandbox", "--disable-setuid-sandbox"]
	});
	
	if(args_mine.freeforms){
		let non_can_tags=[];
		try {
			if(args_mine.verbose)
			    console.log("========================= Scraping NonCanonical Tags ================================");
			const page = await browser.newPage();
			non_can_tags= await mine_non_canonicals(URLs.site,page);		
		} catch (error) {
			console.error(error);
		}
		finally{
			fs.writeFile(args_mine.output_path+args_mine.output_file+".json", non_can_tags.toString(),function(err, result) {
				if(err) console.log('error', err);
			});
			//Close browser
			// await browser.close();
			return;
			// process.exit(0);
		}
	}
	
	let mined_tags={};
	if (args_mine.continue & fs.existsSync(args_mine.output_path+args_mine.output_file+'.json')){
		if(args_mine.verbose)
			console.log("Reading existing JSON :"+args_mine.output_path+args_mine.output_file+'.json')
		// fs.readFile(args_mine.output_path+args_mine.output_file+'.json', (err, data) => {
		// 	if (err) throw err;
		// 	mined_tags = JSON.parse(data);
		// });
		let rawdata = fs.readFileSync(args_mine.output_path+args_mine.output_file+'.json');
		mined_tags = JSON.parse(rawdata);
	}
	else{
		// If it is a new iteration or the file did not extit
		// Creates a new file and adds the header
		if(args_mine.verbose)
			console.log("Creating/Overwriting JSON :"+args_mine.output_path+args_mine.output_file+'.json')
	}
	
	
	
	const page = await browser.newPage();

	// Passing the output to the cmd
	// page.on('console', (msg) => console[msg._type]('PAGE LOG:', msg._text));
	
	try{
		for (let index = 0; index < URLs.tag.length; index++) {
			if(Object.keys(mined_tags).includes(URLs.tag[index])){
				if(args_mine.verbose){
					console.log("================= "+(index+1)+"/"+URLs.tag.length+" =================");
					console.log("================= ALREADY MINNED TAG: "+URLs.tag[index]+" =================");	
					console.log("====================================================================")
				}
				continue;
			}
			
			// verbose
			if(args_mine.verbose){
				console.log("================= "+(index+1)+"/"+URLs.tag.length+" =================");
				console.log("================= MINING TAG: "+URLs.tag[index]+" =================");	
			}
			
			// let temp = await mine_RATAS(URLs.tag[index], page, true)
			let temp = await mine_RATAS(URLs.site + 'tags/' +URLs.tag[index], page, true)
			if(temp==NaN)
				continue;
			mined_tags[URLs.tag[index]]= temp;
			
			if(args_mine.verbose)
				console.log("====================================================================")

			// if(index%51==0 & index>0){
			// 	if(args_mine.verbose)
			// 		console.log("========================== Waiting 4 mins ==========================")
			// 	await page.waitForTimeout(40000);
			// }
			// if(index>99 &index%25==0){
			// 	if(args_mine.verbose)
			// 		console.log("========================== Waiting 4 mins ==========================");
			// 	await page.waitForTimeout(40000);
			// }

		}		
	}
	catch (e){
		console.log(e);
	}
	finally{
		// strignify the dictionary woth all the mined tags ==> create a JSON of the dictionary
		var dictstring = JSON.stringify(mined_tags);
		// write the JSON 
		
		// fs.writeFile("./"+URLs.file_name+".json", dictstring,function(err, result) {
		fs.writeFile(args_mine.output_path+args_mine.output_file+".json", dictstring,function(err, result) {
			if(err) console.log('error', err);
		});

		//Close browser
		await browser.close();
	}
	
	process.exit(0);
})();
