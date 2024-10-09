# How to install

## Prerequisite requirements

- python 3.11 or newer
  - If your using windows you can check your python version by typing ```python --version```
  - For mac/linux use ```python3 --version``` <br>
  if you don't have a suitable version of python or you don't have python
  installed visit https://www.python.org/downloads/
- Git for running git commands (optional)<br>
If you don't have git you can download it here: https://git-scm.com/downloads
in order to use and run git commands

## Installation instructions
Depending on if you have git or not the instructions may differ. \
For this guide replace all `python` commands with your OS equivalent if you're
not using windows.

1. clone the repository with the following command
    - make sure you are in a suitable directory before cloning
    - alternatively download and extract the .zip file into the desired directory
   [here](https://github.com/KhunakornP/ku-polls/releases)
```
git clone https://github.com/KhunakornP/A-plus-management.git
```

2. change the directory to the ku-polls directory
```
cd ku-polls
```

3. create a virtual environment
```
python -m venv env
```

4. activate the virtual environment
```
.env/bin/activate

# on windows use
.\env\scripts\activate
```

5. install required python pakages
```
pip install -r requirements.txt
```

6. migrate the database
```
python manage.py migrate
```

7. import data

```
#TODO update this when the data fixture is finalized
```

8. create a .env file <br>
note: Decide if we want a sample.env or if we will use testing.env