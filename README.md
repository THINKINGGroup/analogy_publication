# Analogy

**A**utomated A**na**lytics for Epidemio**logy** (ANALOGY) is an open-source python cli application to run Incidence and Prevalence analysis.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites
The project requires python 3.9 or above. We recommend using Anaconda for open source python distribution. Goto https://www.anaconda.com/ for installation.

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

To see all available argument, use the command below.
```bash
analogy incprev --help
```

Run the command below to start the analysis.
```bash
analogy incprev ./src/analogy/data/sample.csv . "2001-01-01 00:00:00.0" "2021-12-31 00:00:00.0" "%Y-%m-%d %H:%M:%S.%f" START_DATE END_DATE 1000 12
```
The command expects the following:
1. path to the .csv dataset: **./src/analogy/data/sample.csv**
2. the destination folder to store outputs: **.** (current directory)
3. Study start date: **2001-01-01 00:00:00.0**
4. Study end date: **2021-12-31 00:00:00.0**
5. Date formate in dataset and user provided: **%Y-%m-%d %H:%M:%S.%f**
6. Patient follow-up start date column in dataset: **START_DATE**
7. Patient follow-up end date column in dataset: **END_DATE**
8. Pre person years scale for the result reporting: **1000**
9. Regualr interval at witch incidence and prevalence to be calculated: **12**

## FAQ
