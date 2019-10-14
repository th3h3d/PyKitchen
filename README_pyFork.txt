pyFork:
  It enables people who needs to test data which is coming with CSV format. 23 diffirent test types can be executed over CSV files.
  All test type can be define with diffirent parameters and saves in testcase file which has to be JSON file format.

How pyFork works: 
  

  +------------+                                 +------------+
  |            |                                 |            |
  | JSON file  |                                 | CSV File   |
  | Testcases  |                                 | Report     |
  |            |         +--------------+        |            |
  |            |         |              |        |            |
  |            |         |   pyFork.py  |        |            |
  |            +-------->+   Script     +<-------+            |
  |            |         |              |        |            |
  |            |         |              |        |            |
  +------------+         |              |        +------------+      +-----------+
                         |              |                            | logger.py |
                         |              +<---------------------------+ Script    |
                         +--------------+                            |           |
                          |           |            +-----------+     |           |
                          |           |            |           |     +-----------+
                          |           +------------+ Log File  |
                          |                        | Logs      |
                          |                        |           |
                          |                        +-----------+
                          v
           +------------------------------+
           |                              |
           |  Output CSV or JSON format   |
           |                              |
           +------------------------------+

How to run:
  pyFork can be ran with Python 3 and it needs additionally library "Pandas".
  
  run command "python pyFork.py --help" which will help you.
  
Test Types:
  ISINTEGER-0
    -check that column has only integer value(s)
    
  ISNEGATIVEINTEGER-0
    -check that column has only negative integer value(s)
    
  ISDOUBLE-0
    -check that column has only double(floating) value(s)
    
  ISNEGATIVEDOUBLE-0
    -check that column has only negative double(floating) value(s)
    
  ISNULL-0
    -check that column has only null value(s)
    
  ISNOTNULL-0
    -check that column has only non-null value(s)
    
  ISALPHANUMERIC-0
    -check that column has only alphanumeric value(s)
    
  ISALPHABETIC-0
    -check that column has only alphabetic value(s)
    
  ISSPACE-0
    -check that column has only space value(s)
    
  ISREGEX-1
    -check that column has only specific regex value(s)
    -arg1 should be defined in quotes and also escape character should be used example: "^\\d$"
    
  ISLESSTHAN-1
    -check that column has only value(s) less than -arg1-
    
  ISGREATERTHAN-1
    -check that column has only value(s) greater than -arg1-
    
  ISLESSTHANOREQUALSTO-1
    -check that column has only value(s) less than -arg1- or equals to -arg1-
    
  ISGREATERTHANOREQUALSTO-1
    -check that column has only value(s) greater than -arg1- or equals to -arg1-
    
  ISINBETWEEN-2
    -check that column has only value(s) in between -arg1- and -arg2-
    
  ISINBETWEENOREQUALSTO-2
    -check that column has only value(s) in between -arg1- and -arg2- or equals to -arg1- and -arg2-
    
  ISMAXLENGTH-1
    -check that column has only max char length -arg1-
    
  ISMINLENGTH-1
    -check that column has only min char length -arg1-
    
  ISEXACTLENGTH-1
    -check that column has only exact char length -arg1-
    
  ISLENGTHINBETWEEN-2
    -check that column has only char length between -arg1- and -arg1-
    
  ISLENGTHINBETWEENOREQUALSTO-2
    -check that column has only char length between -arg1- and -arg1- or equals to -arg1- and -arg1-
     
  ISVALUERANGE-1
    -check that column has only defined values range -arg1-
    -arg1 should be defined with quote in parentheses and separeted with pipe symbol example: "(A|B|C)"
    
  ISUNIQUE-0
    -check that column has only unique values

  
  What does -0, -1, 2 mean?
    -0 means test type does not take any parameter
    -1 means test type takes only 1 parameter which is arg1
    -2 means test type takes 2 paramters which are arg1 and arg2
 
  
  Example testcase "testcase.json", file can be got via command "python pyFork.py --example testcase"
  ---------------------------------------------------------
  [ 
   { 
      "case":"1",
      "column":"Region",
      "type":"IsNotNull",
      "arg1":null,
      "arg2":null
   },
   { 
      "case":"2",
      "column":"Order Priority",
      "type":"IsValueRange",
      "arg1":"(M|C)",
      "arg2":null
   },
   { 
      "case":"3",
      "column":"Order Priority",
      "type":"IsMinLength",
      "arg1":"1",
      "arg2":null
   }
  ]
  -------------------------------------------------------


  Example report file "report.csv", file can be got via command "python pyFork.py --example report"
  -----------------------------------------------------
  Region,Country,Item Type,Sales Channel,Order Priority
  Asia,Singapore,Snacks,Online,C
  Sub-Saharan Africa,Ethiopia,Cosmetics,Online,M
  Africa,Tanzania,Cosmetics,Offline,M
  -----------------------------------------------------
  
  
  Example output execution:
  -----------------------------------------------------
  run command "python pyFork.py --report report.csv --testcase.json --output csv"
  or
  run command "python pyFork.py --report report.csv --testcase.json --output json"