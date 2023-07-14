Branch solely for compiling the program into one `.exe` file.

# Polytech-Loan

> Project for COMP 20073

Prototype software for managing PUP student loans.

## Build

### Requirements

* For third-party modules, see `requirements.txt`
* Qt Designer for editing `.ui` files

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
* (Recommended) Create virtual environment:
  ```
  C:\Users\YourUsername\...\polytech_loan> python -m venv venv
  ```

 Activate the virtual environment:
  ```
  C:\Users\YourUsername\...\polytech_loan> .\venv\Scripts\activate
  ```
* You should see a `(venv)` in the prompt:
  ```
  (venv) C:\Users\YourUsername\...\polytech_loan>
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

Checkout the `build` branch, install `pyinstaller` package
```bash
pip install pyinstaller
```
and run
```bash
pyinstaller polytech_loan.spec
```
The binary file will be stored in `dist` directory.
>>>>>>> main
