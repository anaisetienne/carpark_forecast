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

# Explanations of data
id: booking number
seller: effia.com (direct booking) or Onepark (indirect booking, we pay a commission)
pocket: id code of the park
product: what type of product has been purchased: hourly fare, weekend/1 week packages...
status: canceled, finished (past booking), progress ()
option: standard or premium (better slot, guest pay an extra fee)
guest_id: guest id (info available only for direct booking with effia.com)
booking_fee:
-for direct bookings: amount of booking fees (some parks are adding fees to the guest who book) and/or premium fees
-for indirect bookings: amount of the booking
