# Table of Contents
1. [Problem](README.md#problem)
2. [Approach](README.md#approach)
3. [Run Instructions](README.md#run-instructions)

# Problem

A newspaper editor was researching immigration data trends on H1B(H-1B, H-1B1, E-3) visa application processing over the past years, trying to identify the occupations and states with the most number of approved H1B visas. She has found statistics available from the US Department of Labor and its [Office of Foreign Labor Certification Performance Data](https://www.foreignlaborcert.doleta.gov/performancedata.cfm#dis). But while there are ready-made reports for [2018](https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2018/H-1B_Selected_Statistics_FY2018_Q4.pdf) and [2017](https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2017/H-1B_Selected_Statistics_FY2017.pdf), the site doesn’t have them for past years. 

As a data engineer, you are asked to create a mechanism to analyze past years data, specificially calculate two metrics: **Top 10 Occupations** and **Top 10 States** for **certified** visa applications.

Your code should be modular and reusable for future. If the newspaper gets data for the year 2019 (with the assumption that the necessary data to calculate the metrics are available) and puts it in the `input` directory, running the `run.sh` script should produce the results in the `output` folder without needing to change the code.

To solve this challenge you might pick a programing language of your choice (preferably Python, Scala, Java, or C/C++ because they are commonly used and will help us better assess you), but you are only allowed to use the default data structures that come with that programming language (you may use I/O and other standard libraries). For example, you can code in Python, **but you should not use Pandas or other external libraries**. 

# Approach

To perform the category aggregation and counting in a scalable way for a large amount of data, I broke down the problem into the following pieces:

1. Find the right column names for the fields of interest, i.e., what are the column names for case status, work place state, and occupation name for different years. The names vary for different year ranges. By checking through the documentation on the US DOL website, I noticed that there are limited variants for the column names and created global dictionaries to look them up in the header of the input file to pick the right ones. 

2. Find the indices of the column names identified in step 1 in the list of column names.

3. Extract the field values (state and occupation titles) line by line using the indices found in step 2 and add the values and update their numbers in a dictionary. So far the fields of interest are set to be either state or occupation. The module is readily to be used for the other fields as well.

4. Find the top 10 categories with the largest number of certified h1b visas by sorting the dictionray by values from high to low first, and by the alphabetical order of the keys and then picking out the top 10 records. For the top 10 categories, calculate the percentage for each category.

5. Write out the top 10 records into a formated text file.


# Run Instructions

## Structure of the Code Pipeline
The directory structure of this repo looks like this:
```
      ├── README.md 
      ├── run.sh
      ├── src
      │   └──h1b_counting.py
      ├── input
      │   └──h1b_input.csv
      ├── output
      |   └── top_10_occupations.txt
      |   └── top_10_states.txt
      ├── insight_testsuite
          └── run_tests.sh
          └── tests
              └── test_1
              |   ├── input
              |   │   └── h1b_input.csv
              |   |__ output
              |   |   └── top_10_occupations.txt
              |   |   └── top_10_states.txt
              ├── test_2
                  ├── input
                  │   └── h1b_input.csv
                  |── output
                  |   |   └── top_10_occupations.txt
                  |   |   └── top_10_states.txt
```

## Run the Code

Save or link the input file as ./input/h1b_input.csv and run ./run.sh 

## Run the Tests

1. Create a test folder under ./insight_testsuite/tests with two subfolders: input and output. 
2. Copy or link the input file as h1b_input.csv in the input folder, and place the known output files in the output folder. 
3. Run the ./insight_testsuite/run_tests.sh script and test results will be displayed on screen.

On a failed test, the output of `run_tests.sh` should look like:

    [FAIL]: test_1
    [Thu Mar 30 16:28:01 PDT 2017] 0 of 1 tests passed

On success:

    [PASS]: test_1
    [Thu Mar 30 16:25:57 PDT 2017] 1 of 1 tests passed


