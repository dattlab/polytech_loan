# Polytech-Loan

> Project for COMP 20073

Prototype software for managing PUP student loans.

## Build

### Requirements

* See `requirements.txt`
* Python <=3.9.X. Install the latest 3.9 version [here](https://www.python.org/downloads/release/python-3913/)

> :warning: PyQt5 (one of the requirements) would not install properly in Python versions >3.10 so better install the
> required version and just create a virtual environment

You can check the default python version installed in your machine by opening terminal and run:

```
python --version
```

### Installing packages

* Open terminal in any directory you like
* Clone this repository
  ```
  C:\Users\YourUsername\...> git clone https://github.com/dattlab/polytech_loan.git
  ```
* Go to folder `polytech_loan`
  ```
  C:\Users\YourUsername\...> cd polytech_loan
  C:\Users\YourUsername\...\polytech_loan>
  ```
* Create virtual environment with Python 3.9.X version:
  ```
  C:\Users\YourUsername\...\polytech_loan> C:\Users\YourUsername\AppData\Local\Programs\Python\Python39\python.exe -m venv venv
  ```

> :information_source: If your default python version is 3.9.X, you might want to change the path
> to `C:\"Program Files"\Python39\python.exe`

* Activate the virtual environment:
  ```
  C:\Users\YourUsername\...\polytech_loan> .\venv\Scripts\activate
  ```
* You should see a `(venv)` in the prompt:
* Check the Python version. It should be 3.9.X:
  ```
  (venv) C:\Users\YourUsername\...\polytech_loan> python --version
  ```
* Install all the required third-party modules:
  ```
  (venv) C:\Users\YourUsername\...\polytech_loan> pip install -r requirements.txt
  ```
* You can now run the main file `polytech_loan.py`

### Tweaking the UI

* You can edit the `.ui` files inside the `ui` directory with Qt Designer located
  at `venv\Lib\site-packages\qt5_applications\Qt\bin\designer.exe`.
* To make `.ui` files as `.py` files:
  ```
  (venv) C:\Users\YourUsername\...\polytech_loan> pyuic5 .\ui\xxxx.ui -o .\ui\xxxx_ui.py
  ```
* The `.qrc` files in `resources` folder must also be in `.py`:
  ```
  (venv) C:\Users\YourUsername\...\polytech_loan> pyrcc5 .\ui\resources\xxxx.qrc -o .\ui\resources\xxxx_rc.py
  ```

### Compiling into `.exe`

Checkout the `build` branch, install `pyinstaller` package and run `pyinstaller polytech_loan.spec`. The binary file will be stored in `dist`
directory.
