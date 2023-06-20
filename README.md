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
- id: booking number
- pocket: id code of the park (one parking, can have several pockets. The pockets of one park, can have the same prices, or different prices)
- product: what type of product has been purchased: hourly fare: H10, weekend/1 week packages : Fxx...
- status: canceled, finished (past booking), progress & completed (futur booking),
- option: standard or premium (better slot, guest pay an extra fee)
- guest_id: guest id
- booking_fees: for direct bookings: amount of booking fees (some parks are adding fees to the guest who book) and/or premium fees
- amount: amount paid for the parking without booking fees
- total amount: booking fees + amount - discount
- discount: amount of promotion
- creation_date_hour: date & time when the booking has been made
- beginning_date_hour: date & time of the beginning of the booking
- beginning slice: time slot of the entry of the guest: 0-6h/6-9h/9-12h/12-15h/15-18h/18-24h
- end_date_jour: ending date & time of the booking
- max_date_hour: the date & hour until the guest can leave without paying an additional fee. For example, if he booked a weekend or a 7 days package, he can stay in the park until the end of package, even if he made a booking for a shorter period
- cxl_date_hour: date & hour of cancelation
- los: length of stay: 0-30min/30min-6h/6h-24h/+24h
- lead_time_hour: nb of hours between the purchase and the arrival
- promo_name: name of the promotional code
- promo_amount: amount of the promotion. May not be equal to "discount", if the guest benefits of 2 or more promotional codes -> this also create duplicates, if the guest has 2+ promo codes. The only differences are in these last 2 colums, all the other columns are equal
