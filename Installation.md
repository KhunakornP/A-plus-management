# How to install

## Prerequisite requirements

- python 3.11 or newer
  - If your using windows you can check your python version by typing ```python --version```
  - For mac/linux use ```python3 --version``` <br>
  if you don't have a suitable version of python or you don't have python
  installed visit https://www.python.org/downloads/
- [Node.js](https://nodejs.org/en) to run Javascript tests (Optional)
  - You can run the server without Node.js, but you won't have access to JavaScript tests for our project.
- [Git](https://git-scm.com/downloads) for running git commands (Optional)<br>

## Installation instructions
Depending on if you have git or not the instructions may differ. \
For this guide replace all `python` commands with your OS equivalent if you're
not using windows.

1. clone the repository with the following command
    - make sure you are in a suitable directory before cloning
    - alternatively download and extract the .zip file into the desired directory
   [here](https://github.com/KhunakornP/A-plus-management/releases)
```
git clone https://github.com/KhunakornP/A-plus-management.git
```

2. change the directory to the A-plus-management directory
```
cd A-plus-management
```

3. create a virtual environment
```
python -m venv env
```

4. activate the virtual environment
```
# on Mac/Linux use
.env/bin/activate

# on Windows use
.\env\scripts\activate
```

5. install required python packages
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

9. get your [google credentials](https://support.google.com/cloud/answer/6158849?hl=en) and put them into .env
    - detailed instructions [here](google_auth_setup_guide.md#Setting-up-Google-OAuth-2.0)
    - **DO NOT** publish your client id and secret on the internet.

## How to run tests
1. Django tests:
  ```
  python manage.py runserver
  ```
2. JavaScript tests:
  ```
  npm install
  npm run test
  ```