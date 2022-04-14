import argparse
import os

parser = argparse.ArgumentParser(prog="")
parser.add_argument("-f", "--file",
                    help="The path of the file to analize")
# parser.add_argument("-o","--out", help="Name of the result of the procces")

parser.add_argument("-dg", "--data_generator", help='''To Generate many files of data to analize, depends of the parse of your choice ex:'p_label_value,p_series_list' ''',
                    type=str)

def parse():
    args = parser.parse_args()
    config = Config()
    config.set_available_parsers_graphs(args.parser,args.graph)
    config.set_data_generated_list(args.data_generator)
    config.set_output_file(args.out)
    config.set_parsers_help(args.parsers_help)
    
    if args.parsers_help:
        parsers_help()
        return []
    elif args.parsers_list:
        [print(item) for item in config.parsers]
        return []
    elif args.graphs_list:
        [print(item) for item in config.graphs]
        return []
    elif args.data_generator:
        data_generator()
        return []
    
    #adquiriendo los valores a procesar en data=STRING
    data=""
    # args.file = "text.txt"
    if args.file:   #Si recibo los datos de un FILE
        data=[]
        if os.path.isdir(args.file):
            for item in os.listdir(args.file):
                temp = open(args.file+item, "r")
                data.append(temp.read())
                temp.close()
        else:
            data = [open(args.file, "r").read()]
    else:   #Si recibo los datos por la consola hasta que no escriba una linea en blanco
        print("write the data. To finish it write a blank line")
        temp = input()
        while not temp=="":
            data+=temp
            temp=input()
            data+="\n" if not temp=="" else ""
            data=[data]
    #ya con data lleno
    
    return data

def parsers_help():
    ''' Lista todos los parsers definidos y un ejemplo de los mismos '''
    print("="*20)
    for item in Config().prarsers_help:
        class_name = Config().get_parser_class_name(item)
        print(item)
        import_module = compile(
            "from api.parsers."+item+" import "+class_name, 'e', mode='exec')
        exec(import_module)
        print(eval(str(class_name+"().help()")))
        print("="*20)

def data_generator(amount=5, on_top=50, below=100):
    ''' Lista todos los parsers definidos y un ejemplo de los mismos '''
    print("="*20)
    #Recorrer todos los parsers que quiere ser procesados
    for item in Config().data_generated:
        #Adquirir el nombre de la clase dentro del file item
        print(item)
        class_name = Config().get_parser_class_name(item)
        import_module = compile(
            "from api.parsers."+item+" import "+class_name, 'e', mode='exec')
        exec(import_module)
        try:
            eval(str(class_name+"().data_generator(amount, on_top,below)"))
        except:
            print("WARNING-- THE PARSER "+item+" DOES NOT HAVE THE METHOD data_generator")
        print("="*20)
