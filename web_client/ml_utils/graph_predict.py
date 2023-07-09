from datetime import datetime, timedelta

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


def get_past_year_weekday(date_reference: datetime) -> datetime:
    """
    Calculate the date one year earlier, adjusted to correspond to the same day of the week as the reference date.
    Args:
        date_reference (datetime): The reference date.
    Returns:
        datetime: The adjusted date one year earlier, or None if the date is out of the valid range.
    Raises:
        pd.errors.OutOfBoundsDatetime: If the adjusted date is out of the valid range.
    """
    # Calculate the date one year earlier
    try:
        date_annee_precedente = date_reference - pd.DateOffset(years=1)
    except pd.errors.OutOfBoundsDatetime:
        print("La date un an auparavant est en dehors de la plage valide.")
        date_annee_precedente = None

    if date_annee_precedente:
        # Check that the days of the week match
        if date_annee_precedente.weekday() != date_reference.weekday():
            # Adjust the date one year earlier to correspond to the same day of the week as the reference date
            while date_annee_precedente.weekday() != date_reference.weekday():
                date_annee_precedente -= pd.DateOffset(days=1)

            # Print results
            print("Date de référence :", date_reference)
            print("Date un an auparavant (ajustée) :", date_annee_precedente)
        else:
            print("La date de référence et la date un an auparavant ont le même jour de la semaine.")
    else:
        print("La date de référence est en dehors de la plage valide.")
    return date_annee_precedente


def get_data_past_two_weeks(date_reference: datetime.date, period: int, df: pd.DataFrame):
    days_range = pd.date_range(end=date_reference, periods=period)
    df_filtered = df[df['date'].isin(days_range)]
    data_to_plot = df_filtered['nb_cars']
    return data_to_plot


def prepare_forecast_data_for_plotting(date_reference: datetime.date, period: int, predictions: list) -> pd.DataFrame:
    date_reference_plus_1_day = date_reference + timedelta(days=1)
    dates = pd.date_range(start=date_reference_plus_1_day, periods=period)
    df_future = pd.DataFrame(index=dates)
    df_future_values = pd.DataFrame(predictions, columns=['nb_cars'], index=pd.date_range(start=date_reference_plus_1_day, periods=len(predictions)))
    return df_future_values

def get_data_from_last_year(date_reference_past: datetime.date, df: pd.DataFrame, period:int) -> pd.DataFrame:
    days_range_past = pd.date_range(end=date_reference_past, periods=period)
    df_filtered_past = df[df['date'].isin(days_range_past)]
    return df_filtered_past


def plot_graph(past_two_weeks_data, forecast_two_weeks_data, last_year_data, date_reference) -> None:
    fig, ax = plt.subplots(figsize=(24, 8))

    width = 0.35  # Largeur des barres

    # Position of bars for the first data set (Past)
    positions_past = range(len(past_two_weeks_data))
    bars_past = ax.bar(positions_past, past_two_weeks_data, width=width, label='Past two weeks')


    # Position of bars for the second data set (Future)
    positions_future = [p + len(past_two_weeks_data) + width for p in range(len(forecast_two_weeks_data))]
    bars_future = ax.bar(positions_future, forecast_two_weeks_data['nb_cars'], width=width, label='Forecast')

    # Line plot with data from the previous year at the same start date(adjust to weekday)
    ax.plot(list(range(29)), last_year_data['nb_cars'].iloc[1:], color='red', label='Last year')

    # Adjust x-axis labels
    dates_bis = pd.date_range(end=date_reference, periods=15)
    formatted_dates = [date.strftime('%Y-%m-%d') for date in dates_bis]
    formatted_dates_future = [date.strftime('%Y-%m-%d') for date in forecast_two_weeks_data.index]

    ax.set_xticks(list(positions_past) + list(positions_future))
    ax.set_xticklabels(formatted_dates + list(formatted_dates_future), rotation=90)

    ax.set_ylabel('Nb reservations')
    ax.set_xlabel('Forecast horizon')
    ax.legend(loc='best')

    return fig

def plot_graph_plotly(past_two_weeks_data, forecast_two_weeks_data, last_year_data, date_reference) -> None:
    width = 0.35  # Largeur des barres
    fig = px.bar()

    # Position of bars for the first data set (Past)
    positions_past = list(range(len(past_two_weeks_data)))
    fig.add_bar(x=positions_past, y=past_two_weeks_data, name='Past two weeks')

    # Position of bars for the second data set (Future)
    positions_future = [p + len(past_two_weeks_data) + width for p in range(len(forecast_two_weeks_data))]
    fig.add_bar(x=positions_future, y=forecast_two_weeks_data['nb_cars'], name='Forecast')

    # Line plot with data from the previous year at the same start date (adjusted to weekday)
    fig.add_trace(px.line(x=list(range(29)), y=last_year_data['nb_cars'].iloc[1:], labels='Last year').data[0])

    # Adjust x-axis labels
    dates_bis = pd.date_range(end=date_reference, periods=15)
    formatted_dates = [date.strftime('%Y-%m-%d') for date in dates_bis]
    formatted_dates_future = [date.strftime('%Y-%m-%d') for date in forecast_two_weeks_data.index]

    fig.update_layout(xaxis=dict(
        tickmode='array',
        tickvals=list(positions_past) + list(positions_future),
        ticktext=formatted_dates + formatted_dates_future,
        tickangle=90
    ))

    fig.update_layout(
        yaxis_title='Number of cars',
        xaxis_title='Forecast horizon',
        legend=dict(
            x=0,
            y=1,
            traceorder="normal",
            font=dict(family="sans-serif", size=12),
        )
    )

    return fig
