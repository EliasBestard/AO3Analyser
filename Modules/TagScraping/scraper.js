"use strict";
const puppeteer = require("puppeteer");
const fs = require("fs");

// let tag_to_mine = "Reincarnation";
// tag_to_mine='A lot of past lives' // synned
// tag_to_mine='she lived 4 lives already' // freeform
// tag_to_mine="Alternate Universe - Canon Divergence" //cannonical tag

// let tag_to_mine = ["Reincarnation",'A lot of past lives','she lived 4 lives already',"Alternate Universe - Canon Divergence"]
let tag_to_mine = ["Disability"]

//TODO: Build a CLI
const URLs = {
	site:
		// "https://web.archive.org/web/20170825230518/https://archiveofourown.org/",
		"https://archiveofourown.org/",
	tag:
		process.argv.length > 3 ? process.argv.slice(3) : tag_to_mine,
	file_name:
		process.argv.length > 2 ? process.argv[2] : 'tag_net'
};
// console.log(URLs.tag)

( async () => {	
	const browser = await puppeteer.launch({
		headless: true,
		args: ["--no-sandbox", "--disable-setuid-sandbox"]
	});

	let mined_tags={};
	const page = await browser.newPage();

	// Passing the output to the cmd
	page.on('console', (msg) => console[msg._type]('PAGE LOG:', msg._text));
	
	try{
		for (let index = 0; index < URLs.tag.length; index++) {
			console.log("================= MINING TAG: "+URLs.tag[index]+" =================");
			let temp = await mine_RATAS(URLs.tag[index], page)
			mined_tags[URLs.tag[index]]=temp;
			console.log("===================================================================")
		}		
	}
	catch (e){
		console.log(e);
	}
	finally{
		// strignify the dictionary woth all the mined tags ==> create a JSON of the dictionary
		var dictstring = JSON.stringify(mined_tags);
		// write the JSON 
		fs.writeFile("./"+URLs.file_name+".json", dictstring,function(err, result) {
			if(err) console.log('error', err);
		});

		//Close browser
		await browser.close();
	}
		process.exit(0);
})();

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

		console.log("~~~~~~SubTags~~~~~~~");
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

				// // If it does not have nested elements
				// if (first_child_il.children.length==1){
				// 	// console.log(first_child_il.getElementsByClassName('tag')[0].innerText)
				// 	sub_tags.push(first_child_il.getElementsByClassName('tag')[0].innerText)

				// }
				// else{ //If the subtag has nested tags. It only check for two levels
				// 	let temp=[];
					
				// 	grandchilds_ul=first_child_il.children[1]
				// 	// Iterate for all Nested tags and link only one level to the subtag
				// 	for (let index = 0; index < grandchilds_ul.children.length; index++) {
				// 		//Adds the first element (only the grand child not its nested children)
				// 		temp.push(grandchilds_ul.children[index].firstChild.innerText)
				// 	}
				// 	// //This adds all the nested values ( not only the second level) as the 2nd level
				// 	// for( let i =0; i<first_child_il.getElementsByTagName('li').length; i++){
				// 	// 	temp.push(first_child_il.getElementsByTagName('li')[i].innerText);
				// 	// }

				// 	let temp_2={}; 
				// 	temp_2[first_child_il.children[0].innerText]= temp;
				// 	// console.log(temp_2);
				// 	sub_tags.push(temp_2);
				// }
				ul_list.removeChild(first_child_il);
			}
			// Save the subtags
			my_dic.subtags=sub_tags;

		}
		else
			my_dic.subtags=[""];
		console.log("~~~~~~~~~~~~~");

		console.log("~~~~~~MetaTags~~~~~~~");		
		let list_of_meta_tags =document.getElementsByClassName('meta listbox group').length>0? Array.from(document.getElementsByClassName('meta listbox group')[0].getElementsByTagName('ul')):[''];
		let meta_tags=list_of_meta_tags[0];

		// // soluiton without casting, do not like it, do not like the idea of infinite loop
		// while(list_of_meta_tags.length>1){
			// 	meta_tags.removeChild(list_of_meta_tags[1].parentNode);
			// }
		//cast it as an array for iterate without modify it and delete the dependences in meta_tags

		for (let index = 1; index < list_of_meta_tags.length; index++)
			meta_tags.removeChild(list_of_meta_tags[index].parentNode);
		meta_tags =meta_tags=="" ?[""] : [].map.call(meta_tags.children, (form=>{return form.innerText}));
		my_dic.metatags = meta_tags;
		// console.log(meta_tags);
		console.log("~~~~~~~~~~~~~");

		return my_dic;
	});
	return current_tag
}
