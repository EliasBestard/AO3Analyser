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


let args_mine = parser.parse_args();

module.exports ={
  args_mine
}
