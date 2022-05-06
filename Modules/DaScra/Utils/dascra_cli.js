const { ArgumentParser } = require('argparse');


const parser = new ArgumentParser({
	description: 'Argparse example'
});

parser.add_argument('-t', '--tag', {
  	required: true,
  	help: 'Tag to scrap',
  });

parser.add_argument('-of', '--output_file', {
	type:'str',
	default:'dascra_output',
	help: 'Name of the output file'
  });

parser.add_argument('-c', '--continue', {
    action:'store_true',
    help: 'Indicates if it should continue from where it left'
  });

parser.add_argument('-ks', '--kudo_sorting', {
	  type:'int',
    default:0,
    help: 'Indicates if it should sort the works by kudos or not'
  });

parser.add_argument('-op', '--output_path', { 
    type:'str',
    default:'./OutputFiles/', 
    help: 'Path to save the output file'
  });

parser.add_argument('--headless', { 
    action:'store_true',
    help: "To show the scraper's browser"
  });
parser.add_argument('-v', '--verbose', {
    action:'store_true',	
    help: 'Log into the console',
  });

   
//   console.dir(parser.parse_args());

const args_mine = parser.parse_args();

module.exports ={
  args_mine
}
