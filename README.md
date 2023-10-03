# ATS Puzzles

Solving ATS ants and signal processing challenge.

## Setup
1) Clone the repo
> Optional but recommended: create a virtual environment
2) Install the requirements: `pip install -r requirements.txt`


## Possible Issues
Within JP Morgan, getting the distfit package might require the user to follow these steps:
1) Download the whl file from here: https://pypi.org/project/distfit/#files
2) `pip install {whl file path}`

## Question 1: Ants
To run the code for ants, run the following commands (once this repo has been cloned):

`cd ants`

`python main.py`

To configure the test, please make changes in the `config.py` file, with the main parameter `N=10_000` defining how many runs to perform for each test case.

The results summary can be found in the `ants/README.md` file

## Question 2: Signal Processing
To run the code for the signal processing, run the following commands (once this repo has been cloned):

`cd signal_processing`

`python main.py`

The results summary can be found in the `signal_processing/README.md` file


## Future Work

Time permitting, future work recommended is as follows:
1) Utilize parallel compute in python (or other languages) to increase number of simulations for ants.
2) Write unit tests for all code.
