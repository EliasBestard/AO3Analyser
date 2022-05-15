import Utils.ao3_analyser_cli as analyser
import os
analyser.parse()
os.remove("test.log") if os.path.isfile('test.log') else None