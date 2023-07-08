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
    print(df.info())
    # Count the number of bookings and cancellations for each date
    booking_counts = df.loc[df['status'] != 'canceled', 'beginning_date_hour'].dt.date.value_counts()
    cancellation_counts = df.loc[df['status'] == 'canceled', 'beginning_date_hour'].dt.date.value_counts()

    # Update nb_bookings column
    df_days['nb_bookings'] = df_days['date'].map(booking_counts).fillna(0).astype(int)

    # Update nb_bookings_cxl column
    df_days['nb_bookings_cxl'] = df_days['date'].map(cancellation_counts).fillna(0).astype(int)

    return df_days
