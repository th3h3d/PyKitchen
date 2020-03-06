pyKnife:
  pyKnife is used for database testing, it is used for comparing two databases (source and target).

How pyKnife works: 
  Script starts reading your connection file.
  Script starts reading mapping file which is defined in connection file.
  Script connects source database which is defined in mapping file.
  Script reads data from source database.
  Script connects target database which is defined in mapping file.
  Script reads data from target database.
  Script compares data.
  Script stores data in report file.
  Whole execution steps are shown on console.
  
How to run:
  pyKnife can be ran with Python 3 and it needs additionally library "Pandas".
  
  run command "python pyKnife.py --help" which will help you.
  
  
  --connection -R:
    Parameter is used for parsing connection file.
    Parameter works with output and onlyexist parameters.

  --example -R:
    Gets certain options (connection/mapping/jsrawreportcode) to generate example file.
    Parameter works alone.

  --output -R:
    Gets certain options (javascript/csv) (p.s. no default)
      javascript: Data is stored in certain javascript structure, which can be integrated other report format.
      csv: Data is stored in csv format.
    Works with connection and onlyexist parameters.

  --onlyonecase
      Parameter is used for execution.
      Gets certain options (<case number>/all)
        <case number>: number of test case which is defined in mapping file.
        all: executes all cases which are defined in mapping file (p.s. option 'all' is defult).
        
  --onlyexist
    Parameter is used for comparing only exist data in both Source and Target
    Gets certain parameters (yes/no) (p.s. option 'no' is default).
      yes: Only data exists in source and in target will be tested and reported.
      no: All data in source will be tested and reported.
    Works together with connection and output parameters.
    
    
  what is -R:
  -R means this parameter is mandatory.

  
  
