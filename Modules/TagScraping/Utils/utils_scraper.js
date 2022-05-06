"use strict";


/**
 * Builds the RATAS of the tag to mine in the URL
 * @param {String} url_tag_to_mine URL of the tag to get the RATA
 * @param {*} page pupet
 * @param {Boolean} verbose 
 * @returns {dict} 
 */
async function mine_RATAS (url_tag_to_mine, page, verbose){
	//go to "https://archiveofourown.org/tag_to mine"
	await page.goto(url_tag_to_mine ); 

	//conditions
	// await page.waitForTimeout(2000);
	// await page.$eval('input[id="tos_agree"]', check => check.click());
	await page.waitForTimeout(1000);
	// await page.$eval('button[id="accept_tos"]', btn => btn.click());
	
	// Mine the RATAS of the current tag
	let current_tag = await page.evaluate( verbose=>{
        
        /**
         * 
         * @param {html element} node the node to get the children list from
         * @returns  {dict { subtags:[subsubtags:[].....] }}
         */
        const getNodeTree= node=>{
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


        if(document.getElementById('error')){
            if(verbose)
                console.log('========= Page ERROR =========')
            return NaN
        }
        
		let my_dic={};
        
		let type_of_tag = document.getElementsByClassName('tag home profile')[0].children[1].innerText;
        if(verbose)
            console.log("Type of TAG");
		switch (type_of_tag)
		{
			case "This tag belongs to the Additional Tags Category. It's a common tag. You can use it to filter works and to filter bookmarks.":	
                my_dic.type="canonical_tag";
                if(verbose)
                    console.log("canonical_tag Tag") 		
				break;
			case "This tag belongs to the Additional Tags Category.":
				if(
					document.getElementsByClassName('tag home profile')[0].children[3].innerText =="This tag has not been marked common and can't be filtered on (yet)."
					||
					document.getElementsByClassName('tag home profile')[0].children[2].innerText =="This tag has not been marked common and can't be filtered on (yet)."
					){
					my_dic.type="freeform_tag";
                    if(verbose)
                        console.log("FreeForm Tag");
				}
				else{
                    if(verbose)
			        	console.log("SYNNED Tag");
				  my_dic.type="synned_tag";
                  my_dic.cannonical_tag= document.getElementsByClassName('merger module')[0].children[1].innerText.split(".")[0].split("has been made a synonym of")[1]
				  my_dic.cannonical_tag=my_dic.cannonical_tag.trim()
			}

			break;
	   
	   	default: 
			my_dic.type="NAN";
		}

		// console.log("~~~~~~ParentTags~~~~~~~");
		let parent_tags =document.getElementsByClassName('parent listbox group')[0]? [].map.call(document.getElementsByClassName('parent listbox group')[0].getElementsByClassName('tags'), (form=>{return form.innerText})).join(', '): "";
		my_dic.parent_tags=parent_tags.split(',');


		// console.log("~~~~~~SynnedTags~~~~~~~");
		let synned_tags =document.getElementsByClassName('synonym listbox group')[0]? [].map.call(document.getElementsByClassName('synonym listbox group')[0].getElementsByClassName('tag'), (form=>{return form.innerText})).join(','):"";
		my_dic.synned_tags=synned_tags.split(',');
		
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

		// console.log("~~~~~~MetaTags~~~~~~~");		
		let list_of_meta_tags =document.getElementsByClassName('meta listbox group').length>0? Array.from(document.getElementsByClassName('meta listbox group')[0].getElementsByTagName('ul')):[''];
		let meta_tags=list_of_meta_tags[0];

		for (let index = 1; index < list_of_meta_tags.length; index++)
			list_of_meta_tags[index].parentNode.parentNode==meta_tags? meta_tags.removeChild(list_of_meta_tags[index].parentNode):NaN;
		meta_tags =meta_tags=="" ?[""] : [].map.call(meta_tags.children, (form=>{return form.innerText}));
		my_dic.metatags = meta_tags;

		return my_dic;
	}  ) ;
	return current_tag
}

/**
 * 
 * @param {String} url_tag_to_mine URL for the tag to mine all the non canonical tags
 * @param {*} page 
 * @param {*} verbose 
 * @returns {[]} all the tags separated by commas
 */
async function mine_non_canonicals (url_tag_to_mine, page, verbose){
	//go to "https://archiveofourown.org/tag_to mine"
	await page.goto(url_tag_to_mine ); 

	//conditions
	// await page.waitForTimeout(2000);
	// await page.$eval('input[id="tos_agree"]', check => check.click());
	await page.waitForTimeout(1000);
	// await page.$eval('button[id="accept_tos"]', btn => btn.click());
	
	let result_tags=[]
	while (true) {
		result_tags =result_tags.concat(await page.evaluate( verbose=>{

			if(document.getElementById('error')){
				if(verbose)
					console.log('========= Page ERROR =========')
				return NaN
			}	

			let tags_list = document.getElementsByClassName('tag').length>0? Array.from(document.getElementsByClassName('tag')):[];
			if(verbose)
				console.log("Type of TAG");
	
			tags_list=tags_list.slice(1);
			let temp = tags_list.map((x=>{ return x.innerText}));
			return temp;
			
		}));	
		// GO to the next page
		let next = await page.evaluate(() => 
		{
			let nextEl = document.getElementsByClassName('next')[0];
			return nextEl ? nextEl.children[0].getAttribute('href') : 0;
		})
		if (!next)
			break;
		await page.goto('https://archiveofourown.org' + next); 
		// await page.waitForTimeout(2000);
	}
	// Mine the tags of the current tag search
	console.log(result_tags)
	return result_tags
}

module.exports ={
    mine_RATAS,
	mine_non_canonicals
  }