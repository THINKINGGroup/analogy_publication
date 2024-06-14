# Analogy

**A**utomated A**na**lytics for Epidemio**logy** (ANALOGY) is an open-source python cli application to run Incidence and Prevalence analysis.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites
The project requires python 3.9 or above. We recommend using Anaconda for open source python distribution. Go to https://www.anaconda.com/ for installation.

### Installing

1. Clone the repository to your local system.
```bash
git clone https://github.com/aditya02acharya/analogy_publication.git
```

2. Move to the project directory.
```bash
cd analogy_publication
```

3. Run the command below to install the package and all the dependency. 
```bash
python -m pip install .
```

### Running the application

To see all available arguments, use the command below.
```bash
analogy incprev --help
```

Run the command below to start the analysis.
```bash
analogy incprev ./src/analogy/data/sample.csv . "2001-01-01 00:00:00.0" "2021-12-31 00:00:00.0" "%Y-%m-%d %H:%M:%S.%f" START_DATE END_DATE 1000 12
```
Running the command above will be followed up with the prompts below. 
```bash
Enter the list of conditions columns to analyse (col1, col2, ...): CONDITION
Enter the list of demography columns for subgroup analyse or leave empty if none (col1, col2, ...): SEX, ETHNICITY
```
The command expects the following:
1. path to the .csv dataset: **./src/analogy/data/sample.csv**
2. the destination folder to store outputs: **.** (current directory)
3. Study start date: **2001-01-01 00:00:00.0**
4. Study end date: **2021-12-31 00:00:00.0**
5. Date formate in dataset and user provided: **%Y-%m-%d %H:%M:%S.%f**
6. Patient follow-up start date column in dataset: **START_DATE**
7. Patient follow-up end date column in dataset: **END_DATE**
8. Per person years scale for the result reporting: **1000**
9. Regular interval at which incidence and prevalence to be calculated: **12**
10. List of condition to calculate incidence and prevalence on: **CONDITION**
11. List of demography variables for subgroup analysis: **SEX, ETHNICITY**

### CSV File Format
The command takes csv files as input and expects the following format:
1. Each row should correspond to one observation
2. Each column should represent one variable
3. The first row should be a list of column names
4. Each observation must have a start and end date

   
## FAQ
**Q: Where should I run the code blocks in the readme?**

These should be run in the Python command line.


**Q: Are column names necessary or do they need to be excluded?**

Column names are necessary and the command line will take column names as inputs to identify observation start and end dates, conditions, and any subgroup analyses that are desired for stratified analysis.

**Q: Do the values need to be quoted in case there are spaces in them?**

Values in the command line need to be quoted to provide those data points as "string" formats. Without quote marks, the software reads inputs as pre-defined variables. The dates should be provided in the same format as in the data, and this format should be provided to the command line as an input e.g. "%Y-%m-%d %H:%M:%S.%f". The 9th character in that string is a space, which also reflects the character 9 space between data and time in "2001-01-01 00:00:00.0"
