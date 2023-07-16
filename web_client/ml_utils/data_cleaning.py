import pandas as pd


# This code is defining a dictionary called `custom_dtype` that maps column names to their respective data types.
# The keys of the dictionary are the column names and the values are the data types.
# The data types include `str` for string, and `float` for floating-point numbers.
# This dictionary can be used to specify the data types of columns when reading data from a file or database.

custom_dtype = {'id': int,
                'pocket':str,
                'product':str,
                'status':str,
                'option':str,
                'guest_id':str,
                'booking_fees':float,
                'amount':float,
                'total_amount':float,
                'discount':float,
                'creation_date_hour':str,
                'beginning_date_hour':str,
                'begining_slice':str,
                'end_date_hour':str,
                'max_date_hour':str,
                'cxl_date_hour':str,
                'los':str,
                'lead_time_hours':float
                }

# This is a function definition in Python that takes two arguments: `filename` and `new_filename`, both of which are strings.
# The function reads the content of an Excel file using the pandas library's `read_excel` function and stores it in a dataframe object.
# It then writes the contents of the dataframe object to a CSV file using the `to_csv` function,
# with the `index` parameter set to `None` and `header` parameter set to `True`.
# The function returns `None`. This function can be used to convert an Excel file to a CSV file.

def transform_xls_to_csv(filename: str, new_filename: str) -> None:
    # Read and store content of an excel file
    read_file = pd.read_excel(filename)
    # Write the dataframe object into csv file
    read_file.to_csv(new_filename, index = None, header=True)


def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    # Drop the 'entry_date_hour' and 'exit_date_hour' columns
    df = df.drop(['entry_date_hour', 'exit_date_hour','promo_code','amount_promo','max_date_hour'], axis=1)
    # Check for duplicates based on the 'id' column
    duplicates = df.duplicated(subset=['id'])

    # Count the number of duplicates
    duplicate_count = duplicates.sum()

    # Print the number of duplicates
    print("Number of duplicates:", duplicate_count)

    # Drop the duplicates based on the 'id' column
    df = df.drop_duplicates(subset=['id'])

    # Check for nan values and transform them to unknown to count them and to 0 after
    df = df.fillna('unknown')
    df.isin(['unknown']).sum()
    df.replace({'unknown': 0})

    # remove electrique option
    df = df.drop(df[df['option'] == 'electrique'].index)

    # Count the occurrences of each product and store it in a new DataFrame
    product_counts = df['product'].value_counts().reset_index()

    # Rename the columns in the new DataFrame
    product_counts.columns = ['product', 'count']

    # Count the occurrences of each pocket and store it in a new DataFrame
    pocket_counts = df['pocket'].value_counts().reset_index()

    # Rename the columns in the new DataFrame
    pocket_counts.columns = ['pocket', 'count']

    # Count the occurrences of each option
    options = df['option'].value_counts().reset_index()

    # Replace the names of the products
    df['product'] = df['product'].replace({'H10': 'hourly rate',
                                        'F397':'WE package',
                                        'F398': '1 week package',
                                        'F44': '1 week package',
                                        'F98':'WE package',
                                        'F60': '1 month package',
                                        'F63' : '2 weeks package',
                                        'F109': 'other package',
                                        'F132': 'other package',
                                        'F139': '1 month package',
                                        'F400':'1 month package',
                                        'F414': '2 weeks package',
                                        'F150': 'other package',
                                        'F54': '1 week package',
                                        'F67': 'other package',
                                        'F343': 'WE package',
                                        'F138': '1 week package',
                                        'F7': 'other package',
                                        'F33': '2 weeks package',
                                        'F319':'1 week package',
                                        'F70': '1 month package',
                                        'F100': 'other package',
                                        'F110': 'other package',
                                        'F227': 'other package',
                                        'F137': 'other package',
                                        'F58': 'other package',
                                        'F5' : '1 month package',
                                        'F215': 'other package'
                                        })
    # Count the occurrences of each product and store it in a new DataFrame
    product_counts = df['product'].value_counts().reset_index()

    # Rename the columns in the new DataFrame
    product_counts.columns = ['product', 'count']

    return df

def create_time_series_df(df: pd.DataFrame) -> pd.DataFrame:
    # Creation of a DataFrame with 1 car for each day, cancellations (cxl),
    # and nb of bookings and cancellations by days of arrival
    df_days = pd.DataFrame({
        'date': pd.date_range(start='2021-06-01', end='2023-06-20'),
        'nb_cars': 0,
        'nb_cars_cxl': 0,
        'nb_bookings': 0,
        'nb_bookings_cxl': 0
    })

    # Iterate through each row of the DataFrame `df`
    for _, row in df.iterrows():
        start = row['beginning_date_hour']
        end = row['end_date_hour']
        status = row['status']

        # Update nb_cars column
        df_days.loc[(df_days['date'] >= start) & (df_days['date'] <= end) & (status != 'canceled'), 'nb_cars'] += 1

        # Update nb_cars_canceled column
        df_days.loc[(df_days['date'] >= start) & (df_days['date'] <= end) & (status == 'canceled'), 'nb_cars_cxl'] += 1
    # Count the number of bookings and cancellations for each date
    booking_counts = df.loc[df['status'] != 'canceled', 'beginning_date_hour'].dt.date.value_counts()
    cancellation_counts = df.loc[df['status'] == 'canceled', 'beginning_date_hour'].dt.date.value_counts()

    # Update nb_bookings column
    df_days['nb_bookings'] = df_days['date'].map(booking_counts).fillna(0).astype(int)

    # Update nb_bookings_cxl column
    df_days['nb_bookings_cxl'] = df_days['date'].map(cancellation_counts).fillna(0).astype(int)

    # Convert 'date' column to datetime data type
    df_days['date'] = pd.to_datetime(df_days['date'])

    # Reshape the DataFrame using melt
    df_melted = df_days.melt(id_vars='date', value_vars=['nb_cars', 'nb_cars_cxl', 'nb_bookings', 'nb_bookings_cxl'])

    # Creation of df_products with the nb of cars per days by products (w/o cancellations)
    df_products = pd.DataFrame({
    'date': pd.date_range(start='2021-06-01', end='2023-06-20'),
    'hourly rate': 0,
    'WE package': 0,
    '1 week package': 0,
    '1 month package':0,
    'other package': 0,
    '2 weeks package': 0,
})
    # Iterate through each row of the DataFrame `df`
    for _, row in df.iterrows():
        start = row['beginning_date_hour']
        end = row['end_date_hour']
        status = row['status']
        product = row['product']  # Retrieve the product value from the row

        # Update the count for the respective product
        df_products.loc[(df_products['date'] >= start) & (df_products['date'] <= end) & (status != 'canceled'), product] += 1

    # Creation of df_turnover
    # Initialize the DataFrame with the date column
    df_turnover = pd.DataFrame({
        'date': pd.date_range(start='2021-06-01', end='2023-06-20')
    })

    # Calculate turnover by date
    df['date'] = pd.to_datetime(df['beginning_date_hour']).dt.date  # Convert 'beginning_date_hour' to date
    turnover_data = df.loc[df['status'] != 'canceled'].groupby('date').agg({'amount': 'sum'}).reset_index()
    turnover_data = turnover_data.rename(columns={'amount': 'turnover'})
    turnover_data['date'] = pd.to_datetime(turnover_data['date'])  # Convert 'date' to datetime

    # Calculate discount by date
    discount_data = df.loc[df['status'] != 'canceled'].groupby('date').agg({'discount': 'sum'}).reset_index()
    discount_data['date'] = pd.to_datetime(discount_data['date'])  # Convert 'date' to datetime

    # Calculate booking fees by date
    booking_fees_data = df.loc[df['status'] != 'canceled'].groupby('date').agg({'booking_fees': 'sum'}).reset_index()
    booking_fees_data['date'] = pd.to_datetime(booking_fees_data['date'])  # Convert 'date' to datetime

    # Calculate mean of lead_time_hours by date
    mean_lead_time_data = df.groupby('date')['lead_time_hours'].mean().reset_index()
    mean_lead_time_data['date'] = pd.to_datetime(mean_lead_time_data['date'])  # Convert 'date' to datetime

    # Merge the data into the df_turnover DataFrame
    df_turnover = df_turnover.merge(turnover_data, on='date', how='left')
    df_turnover = df_turnover.merge(discount_data, on='date', how='left')
    df_turnover = df_turnover.merge(booking_fees_data, on='date', how='left')
    df_turnover = df_turnover.merge(mean_lead_time_data, on='date', how='left')

    # Fill NaN values with 0
    df_turnover[['turnover', 'discount', 'booking_fees', 'lead_time_hours']] = df_turnover[['turnover', 'discount', 'booking_fees', 'lead_time_hours']].fillna(0)

    # Multiply the discount column by -1 to make it negative
    df_turnover['discount'] = df_turnover['discount'] * -1

    # Reshape the DataFrame using melt
    df_melted_turnover = df_turnover[['date', 'turnover', 'booking_fees', 'discount']].melt(id_vars='date', var_name='category', value_name='amount')

    #Adding the last columns of the original dataset
    # Creation of a DataFrame with 1 car for each day without cancellations, displayed by products

    df_option = pd.DataFrame({
        'date': pd.date_range(start='2021-06-01', end='2023-06-20'),
        'standard': 0,
        'premium': 0,
        '6H à 9H': 0,
        '15H à 18H': 0,
        '9H à 12H': 0,
        '12H à 15H': 0,
        '0H à 6H': 0,
        '18H à 24H': 0,
        '+24h': 0,
        '06:00 24:00': 0,
        '00:30 06:00': 0,
        '00:00 00:30': 0
    })

    # Iterate through each row of the DataFrame `df`
    for _, row in df.iterrows():
        start = row['beginning_date_hour']
        end = row['end_date_hour']
        status = row['status']
        option = row['option']  # Retrieve the option value from the row
        begining_slice = row['begining_slice']  # Retrieve the option value from the row
        los = row['los']  # Retrieve the option value from the row

        # Update the count for the respective option
        df_option.loc[(df_option['date'] >= start) & (df_option['date'] <= end) & (status != 'canceled'), option] += 1
        df_option.loc[(df_option['date'] >= start) & (df_option['date'] <= end) & (status != 'canceled'), begining_slice] += 1
        df_option.loc[(df_option['date'] >= start) & (df_option['date'] <= end) & (status != 'canceled'), los] += 1

    new_df = df_days.merge(df_products, left_index=True, right_index=True, suffixes=('_days', '_products'))
    new_df = new_df.merge(df_turnover, left_index=True, right_index=True, suffixes=('_merged', '_turnover'))
    new_df = new_df.merge(df_option, left_index=True, right_index=True, suffixes=('_merged', '_option'))

    new_df = new_df.drop(['date_products', 'date_merged', 'date_option' ], axis=1)
    new_df = new_df.rename(columns={'date_days': 'date'})

    # Adding strikes, holidays... to new_df

    new_df['strike'] = 0  # Initialize 'strike' column with 0
    dates_of_strike = ['2021-08-05', '2021-11-17',
                    '2022-08-06', '2022-09-29',
                    '2023-01-19','2023-01-31',
                    '2023-02-07','2023-02-11','2023-02-16',
                    '2023-03-07','2023-03-11','2023-03-15','2023-03-21','2023-03-30',
                    '2023-04-06','2023-04-13',
                    '2023-06-06']
    new_df.loc[new_df['date'].isin(dates_of_strike), 'strike'] = 1

    # Add the dates of holidays
    new_df['holidays'] = 0  # Initialize 'holidays' column with 0
    dates_of_holidays = ['2023-01-01', '2023-04-10','2023-05-01','2023-05-08','2023-05-18','2023-05-19','2023-05-29','2023-07-14','2023-08-15','2023-11-01','2023-11-11','2023-12-25',
                    '2022-01-01', '2022-04-18','2022-05-01','2022-05-08','2022-05-26','2022-05-27','2022-06-06','2022-07-14','2022-08-15','2022-11-01','2022-11-11','2022-12-25',
                    '2021-07-14','2021-08-15','2021-11-01','2021-11-11','2021-12-25',
                    ]
    new_df.loc[new_df['date'].isin(dates_of_holidays), 'holidays'] = 1  # Set 'holidays' to 1 for the specified dates

    # Add the vacations

    new_df['vacation'] = 0  # Initialize 'vacation' column with 0
    new_df['date'] = pd.to_datetime(new_df['date'])


    # Define vacation date ranges
    vacation_ranges = [
        ('2021-07-06', '2021-09-01'),
        ('2021-10-23', '2021-11-07'),
        ('2021-12-18', '2022-01-02'),
        ('2022-02-05', '2022-03-06'),
        ('2022-04-09', '2022-08-05'),
        ('2022-07-07', '2022-08-31'),
        ('2022-10-22', '2022-11-06'),
        ('2022-12-17', '2023-01-02'),
        ('2023-02-04', '2023-03-05'),
        ('2023-04-08', '2023-05-08'),
        ('2023-07-08', '2023-09-03'),
        ('2023-10-21', '2023-11-05'),
        ('2023-12-23', '2024-01-07'),
    ]

    # Iterate over each vacation range
    for start_date, end_date in vacation_ranges:
        # Generate a list of dates within the range
        vacation_dates = pd.date_range(start=start_date, end=end_date, freq='D').date
        # Set 'vacation' to 1 for the dates in the vacation range
        new_df.loc[new_df['date'].isin(vacation_dates), 'vacation'] = 1

    return new_df
