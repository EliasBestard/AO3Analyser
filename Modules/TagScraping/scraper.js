"use strict";
const puppeteer = require("puppeteer");
const fs = require("fs");
const { ArgumentParser } = require('argparse');


const parser = new ArgumentParser({
	description: 'Argparse example'
});

parser.add_argument('-of', '--output_file', {
	type:'str',
	default:'tag_net',
	help: 'Name of the output JSON file'
  });

parser.add_argument('-t', '--tags', {
	nargs:'+',
  	required: true,
  	help: 'Set of tags to scrap',
  });

parser.add_argument('-op', '--output_path', { 
    type:'str',
    default:'./OutputFiles/', 
    help: 'Path to save the output JSON'
  });

  parser.add_argument('-av', '--AO3_version', { 
    type:'str',
    default:'current', 
    help: 'verison of AO3 using the waytime machine'
  });

parser.add_argument('--headless', { 
    type:'int',
    default:1, 
    help: ''
  });

   
//   console.dir(parser.parse_args());

let args_mine = parser.parse_args();

// let tag_to_mine = ["Reincarnation",'A lot of past lives','she lived 4 lives already',"Alternate Universe - Canon Divergence"]
let tag_to_mine = ["Disability"]

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
		// URLs.site = "https://web.archive.org/web/20210125165441/https://archiveofourown.org/";
		// Ableism
		URLs.site = "https://web.archive.org/web/20210125101651/https://archiveofourown.org/";
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
		// URLs.site = "https://web.archive.org/web/20150105080944/https://archiveofourown.org/";
		// Ableism
		URLs.site = "https://web.archive.org/web/20151122021416/https://archiveofourown.org/";
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


// console.log(URLs.tag)




( async () => {	
	const browser = await puppeteer.launch({
		headless: args_mine.headless,
		args: ["--no-sandbox", "--disable-setuid-sandbox"]
	});

	let mined_tags={};
	const page = await browser.newPage();

	// Passing the output to the cmd
	page.on('console', (msg) => console[msg._type]('PAGE LOG:', msg._text));
	
	try{
		for (let index = 0; index < URLs.tag.length; index++) {
			console.log("================= "+(index+1)+"/"+URLs.tag.length+" =================");
			console.log("================= MINING TAG: "+URLs.tag[index]+" =================");
			
			let temp = await mine_RATAS(URLs.tag[index], page)
			if(temp==NaN)
				continue;
			mined_tags[URLs.tag[index]]= temp;
			
			console.log("===================================================================")
			if(index%50==0 & index>0)
				await delay(60000);
			console.log("================= Waiting 3min =================");
			if(index>99){
				if(index%10==0)
					delay(5000);
				if(index%50==0)
					delay(60000);
			}	
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
		fs.writeFile(args_mine.output_path+args_mine.output_file+"_"+args_mine.AO3_version+".json", dictstring,function(err, result) {
			if(err) console.log('error', err);
		});

		//Close browser
		await browser.close();
	}
		process.exit(0);
})();





function delay(time) {
	return new Promise(resolve => setTimeout(resolve, time));
  }




async function mine_RATAS (tag_to_mine, page){
	//go to "https://archiveofourown.org/tag_to mine"
	await page.goto(URLs.site + 'tags/' + tag_to_mine ); 

	

	//conditions
	// await page.waitForTimeout(2000);
	// await page.$eval('input[id="tos_agree"]', check => check.click());
	await page.waitForTimeout(1000);
	// await page.$eval('button[id="accept_tos"]', btn => btn.click());
	
	// Mine the RATAS of the current tag
	let current_tag = await page.evaluate(() => {
		let my_dic={};

		if(document.getElementById('error'))
			return NaN
		console.log("Type of TAG");
		let type_of_tag = document.getElementsByClassName('tag home profile')[0].children[1].innerText;
		// console.log(type_of_tag);
		switch (type_of_tag)
		{
			case "This tag belongs to the Additional Tags Category. It's a common tag. You can use it to filter works and to filter bookmarks.":	
				console.log("canonical_tag Tag") 		
				my_dic.type="canonical_tag";
				break;
			case "This tag belongs to the Additional Tags Category.":
				if(
					document.getElementsByClassName('tag home profile')[0].children[3].innerText =="This tag has not been marked common and can't be filtered on (yet)."
					||
					document.getElementsByClassName('tag home profile')[0].children[2].innerText =="This tag has not been marked common and can't be filtered on (yet)."
					){
					my_dic.type="freeform_tag";
					console.log("FreeForm Tag");
				}
				else{
				console.log("SYNNED Tag");
				  my_dic.type="synned_tag";
				my_dic.cannonical_tag= document.getElementsByClassName('merger module')[0].children[1].innerText.split(".")[0].split("has been made a synonym of")[1]
			}

			break;
	   
	   	default: 
			my_dic.type="NAN";
		}
		// console.log("~~~~~~~~~~~~~");

	
		// console.log("~~~~~~ParentTags~~~~~~~");
		let parent_tags =document.getElementsByClassName('parent listbox group')[0]? [].map.call(document.getElementsByClassName('parent listbox group')[0].getElementsByClassName('tags'), (form=>{return form.innerText})).join(', '): "";
		my_dic.parent_tags=parent_tags.split(',');
		// console.log("~~~~~~~~~~~~~");


		// console.log("~~~~~~SynnedTags~~~~~~~");
		let synned_tags =document.getElementsByClassName('synonym listbox group')[0]? [].map.call(document.getElementsByClassName('synonym listbox group')[0].getElementsByClassName('tag'), (form=>{return form.innerText})).join(','):"";
		my_dic.synned_tags=synned_tags.split(',');
		// console.log("~~~~~~~~~~~~~");
		function getNodeTree(node) {
			if (node.children.length>1) {
				var children = [];
				for (var j = 0; j < node.childNodes[1].childNodes.length; j++) {
					children.push(getNodeTree(node.childNodes[1].childNodes[j]));
				}
				let temp={}
				temp[node.firstChild.innerText]=children
				return temp
			}
		
			return node.firstChild.innerText;
		}

		// console.log("~~~~~~SubTags~~~~~~~");
		let sub_tags = [];
		// If there are SUB TAGS
		if(document.getElementsByClassName('sub listbox group').length>0){
			// Get the list of sub tags
			let ul_list=document.getElementsByClassName('sub listbox group')[0].getElementsByTagName('ul')[0];
			// Iterate for all subtags
			while (ul_list.childElementCount>0) {
				let first_child_il =ul_list.firstElementChild; 
				
				let temp=getNodeTree(first_child_il)
				sub_tags.push(temp)

				ul_list.removeChild(first_child_il);
			}
			// Save the subtags
			my_dic.subtags=sub_tags;

		}
		else
			my_dic.subtags=[""];
		// console.log("~~~~~~~~~~~~~");

		// console.log("~~~~~~MetaTags~~~~~~~");		
		let list_of_meta_tags =document.getElementsByClassName('meta listbox group').length>0? Array.from(document.getElementsByClassName('meta listbox group')[0].getElementsByTagName('ul')):[''];
		let meta_tags=list_of_meta_tags[0];

		for (let index = 1; index < list_of_meta_tags.length; index++)
			list_of_meta_tags[index].parentNode.parentNode==meta_tags? meta_tags.removeChild(list_of_meta_tags[index].parentNode):NaN;
		meta_tags =meta_tags=="" ?[""] : [].map.call(meta_tags.children, (form=>{return form.innerText}));
		my_dic.metatags = meta_tags;
		// console.log(meta_tags);
		// console.log("~~~~~~~~~~~~~");

		return my_dic;
	});
	return current_tag
}
