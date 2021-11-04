import numpy as np
import pandas as pd
import plotly
import plotly.express as px
import plotly.offline as po
import plotly.graph_objs as pg
import matplotlib.pyplot as plt
import json

def get_population(data, country, plot=False) -> tuple:
    years, population = get_data(data, country, 'population')
    if plot:
        plt.plot(years, np.array(population) / 1000000)
        plt.title('Population')
        plt.xlabel('Years')
        plt.ylabel('Million people')
        plt.show()
    return (years, population)

def get_it(data, country, indicator, _title, _ylabel, plot=False) -> tuple:
    years, temp_data = get_data(data, country, indicator)
    if plot:
        plt_plot(years, temp_data, _title, _ylabel)
    return (years, temp_data)

def get_green_house_gas_emission(data, country, plot=False) -> tuple:
    years, green_house_gas_emission = get_data(data, country, 'green_house_gas_emission')
    if plot:
        plt_plot(years, green_house_gas_emission, 'Greenhouse Gas Emission', 'kt of co2 equivalent')
    return (years, green_house_gas_emission)

def get_green_house_gas_emission_per_capita(data, country, plot=False) -> tuple:
    years, green_house_gas_emission_per_capita = get_data(data, country, 'green_house_gas_emission_per_capita')
    if plot:
        plt_plot(years, green_house_gas_emission_per_capita, 'Greenhouse Gas Emission Per Capita', 'kt of co2 equivalent')
    return (years, green_house_gas_emission_per_capita)

def get_co2_emission(data, country, plot=False) -> tuple:
    years, co2_emission = get_data(data, country, 'co2_emission')
    if plot:
        plt_plot(years, co2_emission, 'CO2 Emission', 'kt of co2')
    return (years, co2_emission)

def get_co2_emission_per_capita(data, country, plot=False) -> tuple:
    years, co2_emission_per_capita = get_data(data, country, 'co2_emission_per_capita')
    if plot:
        plt_plot(years, co2_emission_per_capita, 'CO2 Emission Per Capita', 'kt of co2')
    return (years, co2_emission_per_capita)

def get_methane_emission(data, country, plot=False) -> tuple:
    years, methane_emission = get_data(data, country, 'methane_emission')
    if plot:
        plt_plot(years, methane_emission, 'Methane Emission', 'kt of co2 equvalent')
    return (years, methane_emission)

def get_methane_emission_per_capita(data, country, plot=False) -> tuple:
    years, methane_emission_per_capita = get_data(data, country, 'methane_emission_per_capita')
    if plot:
        plt_plot(years, methane_emission_per_capita, 'Methane Emission Per Capita', 'kt of co2 equvalent')
    return (years, methane_emission_per_capita)

def get_nuclear(data, country, plot=False) -> tuple:
    years, nuclear = get_data(data, country, 'nuclear')
    if plot:
        plt_plot(years, nuclear, 'Nuclear Power Percantage', 'percentage of all electricity')
    return (years, nuclear)

def get_nuclear_power_per_capita(data, country, plot=False) -> tuple:
    years, nuclear_per_capita = get_data(data, country, 'nuclear_per_capita')
    if plot:
        plt_plot(years, nuclear_per_capita, 'Nuclear Power Per Capita', 'percentage of total electricity per capita')
    return (years, nuclear_per_capita)

def get_data_at_specific_year(data, years, year) -> float:
    index = None
    for i, y in enumerate(years):
        if y == year:
            index = i
            return data[index]

def get_data_of_countries(data, countries, year, func, _plot=False) -> list:
    out = list()
    for country in countries:
        years, data_of_country = func(data, country, plot=_plot)
        out.append(get_data_at_specific_year(data_of_country, years, year))
    return out

def get_codes(data, countries) -> list:
    codes = list()
    for country in countries:
        codes.append(data[country]['code'])
    return codes

def _plot(_locations, _z, _text, _title, _colorbar_title):
    data_dict = dict(type = 'choropleth',
            locations = _locations,
            z = _z,
            text = _text,
            colorscale = 'oranges',
            colorbar = {'title' : _colorbar_title})
    layout = dict(title = {'text': _title, 'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                geo = dict(scope='europe',
                        showlakes = True,
                        showframe = False,
                        lakecolor = 'rgb(0,191,255)'))
    x = pg.Figure(data = [data_dict],
                layout = layout)
    po.iplot(x)

def plt_plot(years, _data, _title, _ylabel):
    plt.plot(years, np.array(_data))
    plt.title(_title)
    plt.xlabel('Years')
    plt.ylabel(_ylabel)
    plt.show()

def get_data(data, country, _data) -> tuple:
    nones = [i for i, x in enumerate(data[country][_data]) if x == None]
    temp_data = [float(x) for i, x in enumerate(data[country][_data]) if i not in nones]
    years = [int(x) for i, x in enumerate(data[country]['year']) if i not in nones]
    return (years, temp_data)


# Give the gas emmision data in tonns.
def to_tree(gas):
    acre = 2500
    km2 = 247.10538146717*acre
    return (gas / km2)*1000



if __name__ == '__main__':
    
    with open('data_greenhouse_emission.json') as f:
        data = json.load(f)

    countries = ['Hungary', 'Netherlands', 'Germany', 'Denmark', 'Sweden', 'Norway', 'Finland', 'Belgium', 'Poland', 'Slovak Republic',
                'Czech Republic', 'Slovenia', 'Austria', 'Romania', 'France', 'Switzerland', 'Italy', 'Spain', 'Portugal', 'Luxembourg',
                'Ireland', 'Croatia', 'Bulgaria', 'Greece', 'Iceland', 'United Kingdom', 'Estonia', 'Latvia', 'Lithuania', 'Cyprus',
                'Bulgaria', 'Malta']

    # countries = ['Afghanistan', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Argentina', 'Armenia', 
    #             'Australia', 'Austria', 'Azerbaijan', 'Bahamas, The', 'Bahrain', 'Bangladesh', 'Barbados', 
    #             'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bolivia', 'Bosnia and Herzegovina', 
    #             'Botswana', 'Brazil', 'British Virgin Islands', 'Bulgaria', 'Burkina Faso', 
    #             'Cambodia', 'Cameroon', 'Canada', 'Cayman Islands', 
    #             'Central African Republic', 'Chad','Chile', 'China', 
    #             'Colombia', 'Congo, Dem. Rep.', 'Congo, Rep.', 'Costa Rica', "Cote d'Ivoire", 'Croatia', 'Cuba', 
    #             'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 
    #             'Ecuador', 'Egypt, Arab Rep.', 'El Salvador',
    #             'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Faroe Islands', 'Fiji', 'Finland', 
    #             'France', 'French Polynesia', 'Gabon', 'Gambia, The', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 
    #             'Greece', 'Greenland', 'Grenada', 'Guam', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 
    #             'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Rep.', 'Iraq', 'Ireland', 
    #             'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 
    #             "Korea, Dem. People's Rep.", 'Korea, Rep.', 'Kosovo', 'Kuwait', 'Kyrgyz Republic', 'Lao PDR', 
    #             'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 
    #             'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 
    #             'Mauritius', 'Mexico', 'Micronesia, Fed. Sts.', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 
    #             'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 
    #             'Nicaragua', 'Niger', 'Nigeria', 'North Macedonia', 'Northern Mariana Islands', 'Norway', 'Oman', 
    #             'Pakistan', 'Palau', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 
    #             'Puerto Rico', 'Qatar', 'Romania', 'Russian Federation', 'Rwanda', 'Samoa', 'San Marino', 
    #             'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 
    #             'Slovak Republic', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Asia', 
    #             'South Sudan', 'Spain', 'Sri Lanka', 'St. Kitts and Nevis', 'St. Lucia', 'St. Vincent and the Grenadines', 
    #             'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Tajikistan', 'Tanzania', 'Thailand', 
    #             'Timor-Leste', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 
    #             'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 
    #             'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela, RB', 'Vietnam', 'Virgin Islands (U.S.)', 
    #             'West Bank and Gaza', 'Yemen, Rep.', 'Zambia', 'Zimbabwe']

    emissions_per_capita = get_data_of_countries(data, countries, 2018, get_green_house_gas_emission_per_capita)
    codes = get_codes(data, countries)
    d = zip(countries, codes, emissions_per_capita)
    df_emission = pd.DataFrame(d, columns =['Country', 'Code', 'Emission per Capita'])

    nuclear_per_capita = get_data_of_countries(data, countries, 2014, get_nuclear)
    nuc = zip(countries, codes, nuclear_per_capita)
    df_nuclear = pd.DataFrame(nuc, columns =['Country', 'Code', 'Nuclear Power'])

    emissions_total= get_data_of_countries(data, countries, 2018, get_green_house_gas_emission)
    em = zip(countries, codes, emissions_total)
    df_emission_total = pd.DataFrame(em, columns =['Country', 'Code', 'Emission'])

    # print(df_emission.head())

    # print(list(data))

    print(to_tree(60920*1000) / 93030)

    # _plot(df_emission['Code'], df_emission['Emission per Capita'], df_emission['Country'], 'Greenhouse Gas Emission per Capita', 'kt of co2 equivalent per capita')
    # _plot(df_nuclear['Code'], df_nuclear['Nuclear Power'], df_nuclear['Country'], 'Nuclear Energy Percentage of Total Electricity', 'percentage of total electricity')
    # _plot(df_emission_total['Code'], df_emission_total['Emission'], df_emission_total['Country'], 'Greenhouse Gas Emission', 'kt of co2 equivalent')

    

    