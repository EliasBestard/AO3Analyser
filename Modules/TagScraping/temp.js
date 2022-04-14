"use strict";
const puppeteer = require("puppeteer");
// const moment = require("moment");
// const excel = require('excel4node');
const fs = require("fs");
const { Console } = require("console");

let tag_to_mine = "Reincarnation";
// tag_to_mine='A lot of past lives' // synned
// tag_to_mine='she lived 4 lives already' // freeform
// tag_to_mine="Alternate Universe - Canon Divergence" //cannonical tag

const URLs = 
{
	site:
		"https://archiveofourown.org/",
	tag:
		process.argv.length > 2 ? process.argv.slice(2).join("%20") : tag_to_mine
};

( async () => 
{	
	const browser = await puppeteer.launch(
	{
		headless: false,
		args: ["--no-sandbox", "--disable-setuid-sandbox"]
	});
  
	try
	{
		const page = await browser.newPage();
		await page.goto(URLs.site + 'tags/' + URLs.tag ); 
		
		await page.waitForTimeout(2000);
		await page.$eval('input[id="tos_agree"]', check => check.click());
		await page.waitForTimeout(1000);
		await page.$eval('button[id="accept_tos"]', btn => btn.click());
		
		var works = [];

		







		
		works = works.concat (await page.evaluate(() => 
		{
			console.count("elias");
			console.info("Information");
			console.log("Log");

			let my_dic={};
			console.log("Type of TAG");
			let type_of_tag = document.getElementsByClassName('tag home profile')[0].children[1].innerText;
			console.log(type_of_tag);
			switch (type_of_tag)
			{
				case "This tag belongs to the Additional Tags Category. It's a common tag. You can use it to filter works and to filter bookmarks.":	
					console.log("canonical_tag Tag") 		
					my_dic.type="canonical_tag";
					break;
				case "This tag belongs to the Additional Tags Category.":
					if(document.getElementsByClassName('tag home profile')[0].children[3].innerText =="This tag has not been marked common and can't be filtered on (yet)." ){
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
			console.log("~~~~~~~~~~~~~");

			
			console.log("~~~~~~ParentTags~~~~~~~");
			let parent_tags =document.getElementsByClassName('parent listbox group')[0]? [].map.call(document.getElementsByClassName('parent listbox group')[0].getElementsByClassName('tags'), (form=>{return form.innerText})).join(', '): "";
			my_dic.parent_tags=parent_tags.split(',');
			console.log("~~~~~~~~~~~~~");


			console.log("~~~~~~SynnedTags~~~~~~~");
			let synned_tags =document.getElementsByClassName('synonym listbox group')[0]? [].map.call(document.getElementsByClassName('synonym listbox group')[0].getElementsByClassName('tag'), (form=>{return form.innerText})).join(','):"";
			my_dic.synned_tags=synned_tags.split(',');
			console.log("~~~~~~~~~~~~~");
			

			console.log("~~~~~~SubTags~~~~~~~");
			// let sub_tags = document.getElementsByClassName('sub listbox group')[0]?[].map.call(document.getElementsByClassName('sub listbox group')[0].getElementsByClassName('tag'), (form=>{return form.innerText})).join(','):"";
			let sub_tags = [];
			
			// If there are SUB TAGS
			if(document.getElementsByClassName('sub listbox group').length>0){
				// Get the list of sub tags
				let ul_list=document.getElementsByClassName('sub listbox group')[0].getElementsByTagName('ul')[0];
				// Iterate for all subtags
				while (ul_list.childElementCount>0) {
					let first_child_il =ul_list.firstElementChild; 
					// If it does not have nested elements
					if (first_child_il.getElementsByTagName('ul').length==0){
						// console.log(first_child_il.getElementsByClassName('tag')[0].innerText)
						sub_tags.push(first_child_il.getElementsByClassName('tag')[0].innerText)
	
					}
					else{ //If the subtag has nested tags. It only check for two levels
						let temp=[];
						// Iterate for all Nested tags and link them to the subtag
						for( let i =0; i<first_child_il.getElementsByTagName('li').length; i++){
							temp.push(first_child_il.getElementsByTagName('li')[i].innerText);
						}
	
						let temp_2={}; 
						temp_2[first_child_il.innerText]= temp;
						// console.log(temp_2);
						sub_tags.push(temp_2);
					}
					ul_list.removeChild(first_child_il);
				}
				// Save the subtags
				my_dic.subtags=sub_tags;
								
			}
			else
				my_dic.subtags=[""];
			console.log("~~~~~~~~~~~~~");

			console.log("~~~~~~MetaTags~~~~~~~");
						
			let list_of_meta_tags =document.getElementsByClassName('meta listbox group').length>0? document.getElementsByClassName('meta listbox group')[0].getElementsByTagName('ul'):[''];
			let meta_tags=list_of_meta_tags[0];
			for (let index = 1; index < list_of_meta_tags.length; index++)
				meta_tags.removeChild(list_of_meta_tags[index].parentNode);
			meta_tags =meta_tags=="" ?[""] : [].map.call(meta_tags.children, (form=>{return form.innerText}));
			my_dic.metatags = meta_tags;
			// console.log(meta_tags);
			console.log("~~~~~~~~~~~~~");


			// console.log("~~~~~~ChildTags~~~~~~~");
			// let child_tags = document.getElementsByClassName('child listbox group')[0]?[].map.call(document.getElementsByClassName('child listbox group')[0].getElementsByClassName('tag'), (form=>{return form.innerText})).join(','):"";
			// console.log(child_tags);
			// console.log("~~~~~~~~~~~~~");

			
			return my_dic;
		}));

		let temp={};
		temp[tag_to_mine]=works[0];

		var dictstring = JSON.stringify(temp);
		fs.writeFile("./tag_net.json", dictstring,function(err, result) {
			if(err) console.log('error', err);
		});
	}
	catch (e)
	{
		console.log(e);
	}
	finally
	{
		// await browser.close();
	}
		// process.exit(0);
})
();