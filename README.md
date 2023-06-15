# Data analysis
- Document here the project: carpark_forecast
- Description: Make predictions of numbers of bookings for car parks
- Data Source:
- Type of analysis:

Please document the project the better you can.

# Startup the project

The initial setup.

Create virtualenv and install the project:
```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt
```

Unittest test:
```bash
make clean install test
```

Check for carpark_forecast in github.com/anaisetienne. If your project is not set please add it:

Create a new project on github.com/anaisetienne/carpark_forecast
Then populate it:

```bash
##   e.g. if group is "anaisetienne" and project_name is "carpark_forecast"
git remote add origin git@github.com:anaisetienne/carpark_forecast.git
git push -u origin master
git push -u origin --tags
```

Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
carpark_forecast-run
```

# Install

Go to `https://github.com/anaisetienne/carpark_forecast` to see the project, manage issues,
setup you ssh public key, ...

Create a python3 virtualenv and activate it:

```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
```

Clone the project and install it:

```bash
git clone git@github.com:anaisetienne/carpark_forecast.git
cd carpark_forecast
pip install -r requirements.txt
make clean install test                # install and test
```
Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
carpark_forecast-run
```
