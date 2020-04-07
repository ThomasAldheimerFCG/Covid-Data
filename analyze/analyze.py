#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Get covid daily data from ecdc url
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

today = str(date.today()).replace('-', '')
country_codes = pd.read_pickle('country_codes')
df = pd.read_pickle('../get/data/covid_cases_'+today).drop('dateRep', axis=1)
df['date'] = pd.to_datetime(df[['year', 'month', 'day']])


def plot_country_list(country_list, start_date, threshold, deaths=False):
    """ Plot country list of cases or deaths """
    plt.figure(figsize=(18, 9))
    for country in country_list:
        df1 = df[df.countryterritoryCode == country]
        if deaths:
            df1 = df1[['date', 'deaths']]
            df1 = df1.sort_values(by='date', ascending=True)
            df1['total'] = df1.deaths.cumsum()
            df1['seven_days_avg'] = df1.deaths.rolling(window=7).mean()
            label = 'deaths'
        else:
            df1 = df1[['date', 'cases']]
            df1 = df1.sort_values(by='date', ascending=True)
            df1['total'] = df1.cases.cumsum()
            df1['seven_days_avg'] = df1.cases.rolling(window=7).mean()
            label = 'cases'

        df1 = df1[df1['date'] >= start_date]
        try:
            latest_tot = df1.total.iat[-1]
        except IndexError:
            continue
        if latest_tot < threshold:
            continue
        latest_new = df1.seven_days_avg.iat[-1]

        plt.loglog(df1.total, df1.seven_days_avg, 'k-')
        plt.scatter(latest_tot, latest_new, c='red', edgecolors='red', s=8)
        plt.text(latest_tot + 1.0, latest_new + 1.0, country, fontsize=9, color='red')
        plt.xlabel('Total '+label)
        plt.ylabel('7-day-average new '+label)
    plt.show()
    return None


def plot_single_country(country):
    """ Plot single country statistics """
    df1 = df[df.countryterritoryCode == country]
    df1 = df1[['date', 'cases', 'deaths']]
    df1 = df1.sort_values(by='date', ascending=True)
    df1['total_cases'] = df1.cases.cumsum()
    df1['total_deaths'] = df1.deaths.cumsum()
    df1['cases_seven_days_avg'] = df1.cases.rolling(window=7).mean()
    df1['deaths_seven_days_avg'] = df1.deaths.rolling(window=7).mean()

    latest_cases = df1.cases.iat[-1]
    latest_deaths = df1.deaths.iat[-1]
    latest_total_cases = df1.total_cases.iat[-1]
    latest_total_deaths = df1.total_deaths.iat[-1]
    latest_avg_cases = df1.cases_seven_days_avg.iat[-1]
    latest_avg_deaths = df1.deaths_seven_days_avg.iat[-1]

    plt.figure(figsize=(18, 9))
    plt.subplot(131)
    plt.loglog(df1.total_cases, df1.cases_seven_days_avg, 'k-', label=country+' cases')
    plt.scatter(latest_total_cases, latest_avg_cases, c='red', edgecolors='red', s=8)
    plt.scatter(latest_total_cases, latest_cases, marker='x', c='red', edgecolors='red', s=8, label='latest value')
    plt.text(latest_total_cases - 1, latest_cases + 1.0, str(latest_cases), fontsize=9, color='red')

    plt.loglog(df1.total_deaths, df1.deaths_seven_days_avg, 'k--', label=country+' deaths')
    plt.scatter(latest_total_deaths, latest_avg_deaths, c='red', edgecolors='red', s=8)
    plt.scatter(latest_total_deaths, latest_deaths, marker='x', c='red', edgecolors='red', s=8)
    plt.text(latest_total_deaths - 1, latest_deaths + 1.0, str(latest_deaths), fontsize=9, color='red')

    plt.xlabel('Total')
    plt.ylabel('7-day-average')
    plt.title(country_codes[country_codes.countryterritoryCode == country].countriesAndTerritories.values[0])
    plt.legend(loc='lower right')

    plt.subplot(132)
    plt.bar(np.arange(df1.cases.shape[0]), df1.cases, label='New cases')
    plt.xlabel('Time')
    plt.title(country_codes[country_codes.countryterritoryCode == country].countriesAndTerritories.values[0])
    plt.grid()
    plt.legend(loc='upper left')

    plt.subplot(133)
    plt.bar(np.arange(df1.deaths.shape[0]), df1.deaths, label='New deaths', color='red')
    plt.xlabel('Time')
    plt.title(country_codes[country_codes.countryterritoryCode == country].countriesAndTerritories.values[0])
    plt.grid()
    plt.legend(loc='upper left')
    plt.show()
    return None


def plot_world(start_date):
    df1 = df
    df1 = df1[['date', 'cases', 'deaths']]
    df1 = df1.groupby('date').sum().reset_index()
    df1 = df1.sort_values(by='date', ascending=True)
    df1['total_cases'] = df1.cases.cumsum()
    df1['total_deaths'] = df1.deaths.cumsum()
    df1['cases_seven_days_avg'] = df1.cases.rolling(window=7).mean()
    df1['deaths_seven_days_avg'] = df1.deaths.rolling(window=7).mean()

    latest_cases = df1.cases.iat[-1]
    latest_deaths = df1.deaths.iat[-1]
    latest_total_cases = df1.total_cases.iat[-1]
    latest_total_deaths = df1.total_deaths.iat[-1]
    latest_avg_cases = df1.cases_seven_days_avg.iat[-1]
    latest_avg_deaths = df1.deaths_seven_days_avg.iat[-1]

    df1 = df1[df1['date'] >= start_date]

    plt.figure(figsize=(18, 9))
    plt.subplot(131)
    plt.loglog(df1.total_cases, df1.cases_seven_days_avg, 'k-', label='Cases')
    plt.scatter(latest_total_cases, latest_avg_cases, c='red', edgecolors='red', s=8)
    plt.scatter(latest_total_cases, latest_cases, marker='x', c='red', edgecolors='red', s=8, label='latest value')
    plt.text(latest_total_cases - 1, latest_cases + 1.0, str(latest_cases), fontsize=9, color='red')

    plt.loglog(df1.total_deaths, df1.deaths_seven_days_avg, 'k--', label='Deaths')
    plt.scatter(latest_total_deaths, latest_avg_deaths, c='red', edgecolors='red', s=8)
    plt.scatter(latest_total_deaths, latest_deaths, marker='x', c='red', edgecolors='red', s=8)
    plt.text(latest_total_deaths - 1, latest_deaths + 1.0, str(latest_deaths), fontsize=9, color='red')

    plt.xlabel('Total')
    plt.ylabel('7-day-average')
    plt.title('World')
    plt.legend(loc='lower right')

    plt.subplot(132)
    plt.bar(np.arange(df1.cases.shape[0]), df1.cases, label='New cases')
    plt.xlabel('Time')
    plt.title('World')
    plt.grid()
    plt.legend(loc='upper left')

    plt.subplot(133)
    plt.bar(np.arange(df1.deaths.shape[0]), df1.deaths, label='New deaths', color='red')
    plt.xlabel('Time')
    plt.title('World')
    plt.grid()
    plt.legend(loc='upper left')
    plt.show()
    return None


africa = ['AGO', 'BDI', 'BEN', 'BFA', 'BWA', 'CAF', 'CIV', 'CMR', 'COD', 'COG', 'COM', 'CPV', 'DJI', 'DZA',
          'EGY', 'ERI', 'ESH', 'ETH', 'GAB', 'GIN', 'GMB', 'GNB', 'GNQ', 'KEN', 'LBR', 'LBY', 'LSO', 'MAR',
          'MDG', 'MLI', 'MOZ', 'MRT', 'MUS', 'MWI', 'MYT', 'NAM', 'NER', 'NGA', 'REU', 'RWA', 'SDN', 'SEN',
          'SHN', 'SLE', 'SOM', 'SSD', 'STP', 'SWZ', 'SYC', 'TCD', 'TGO', 'TUN', 'TZA', 'UGA', 'ZAF', 'ZMB', 'ZWE']

EU = ['ITA', 'DEU', 'GBR', 'FRA', 'GRC', 'CHE', 'NLD', 'UKR', 'POL', 'AUT', 'NOR', 'ISL', 'HRV',
      'SWE', 'FIN', 'CZE', 'BEL', 'DNK', 'BGR', 'IRL', 'SVN', 'LTU', 'EST', 'SVK', 'LVA']

world_countries = country_codes.countryterritoryCode.dropna().values.tolist()
african_countries = np.intersect1d(world_countries, africa)
eu_countries = np.intersect1d(world_countries, EU)



plot_single_country('USA')
#plot_country_list(eu_countries, start_date='2020-03-01', threshold=50, deaths=True)
#plot_world(start_date='2020-03-01')

