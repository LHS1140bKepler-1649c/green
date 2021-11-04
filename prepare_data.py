import numpy as np
import pandas as pd
import json

df_green_house_gases = pd.read_csv('greenhouse_emissions.csv', engine='python', error_bad_lines=False)
df_co2 = pd.read_csv('co2_emissions_in_kt.csv', engine='python', error_bad_lines=False)
df_methane = pd.read_csv('methane_emissions_kt_of_co2_equivalent.csv', engine='python', error_bad_lines=False)
df_gdp = pd.read_csv('gdp_const_2015_usd.csv', engine='python', error_bad_lines=False)
df_population = pd.read_csv('population.csv', engine='python', error_bad_lines=False)
df_nuclear = pd.read_csv('nuclear_energy_percent_of_total_electricity.csv', engine='python', error_bad_lines=False)
df_municipal_waste = pd.read_csv('municipal_waste_oecd.csv', engine='python', error_bad_lines=False)
countries = list()


class Country:
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.green_house_gas_emission = list()
        self.green_house_gas_emission_per_capita = list()
        self.co2_emission = list()
        self.co2_emission_per_capita = list()
        self.methane_emission = list()
        self.methane_emission_per_capita = list()
        self.municipal_waste = list()
        self.municipal_waste_per_capita = list()
        self.nuclear = list()
        self.nuclear_per_capita = list()
        self.population = list()
        self.gdp = list()
        self.gdp_per_capita = list()
        self.year = set()

    def fill(self, ghge, pop, gdp, year):
        '''
        Fill up features of the specific country with values.
        '''
        self.green_house_gas_emission.append(ghge)
        self.population.append(pop)
        self.gdp.append(gdp)
        self.year.add(year)

    def __repr__(self) -> str:
        return str(self.name)


def create_database(df, df_population, gdp):

    temp_country = list()
    time = list(range(1970, 2018+1))
    for i, row in df.iterrows():
        temp_country.append((row['Country Name'], row['Country Code']))
    temp_country = sorted(set(temp_country))
    # print(temp_country)
    for country, code in temp_country:
        new_country = Country(country, code)
        countries.append(new_country)
        new_country.year = time

    for country in countries:
        for i, time in enumerate(country.year):
            country.green_house_gas_emission.append(None)
            country.green_house_gas_emission_per_capita.append(None)
            country.co2_emission.append(None)
            country.co2_emission_per_capita.append(None)
            country.methane_emission.append(None)
            country.methane_emission_per_capita.append(None)
            country.municipal_waste.append(None)
            country.municipal_waste_per_capita.append(None)
            country.nuclear.append(None)
            country.nuclear_per_capita.append(None)
            country.population.append(None)
            country.gdp.append(None)
            country.gdp_per_capita.append(None)

    for country in countries:
        for i, row in df.iterrows():
            if row['Country Name'] == country.name:
                for year in country.year:
                    index = country.year.index(year)
                    # print(f"{row['Country Name']} at {year}: {row[str(year)]}")
                    if not np.isnan(row[str(year)]):
                        country.green_house_gas_emission[index] = row[str(year)]
        for i, row in df_population.iterrows():
            if row['Country Name'] == country.name:
                for year in country.year:
                    index = country.year.index(year)
                    # print(f"{row['Country Name']} at {year}: {row[str(year)]}")
                    if not np.isnan(row[str(year)]):
                        country.population[index] = row[str(year)]
        for i, row in df_gdp.iterrows():
            if row['Country Name'] == country.name:
                for year in country.year:
                    index = country.year.index(year)
                    # print(f"{row['Country Name']} at {year}: {row[str(year)]}")
                    if not np.isnan(row[str(year)]):
                        country.gdp[index] = row[str(year)]

        for i, row in df_co2.iterrows():
            if row['Country Name'] == country.name:
                for year in country.year:
                    index = country.year.index(year)
                    # print(f"{row['Country Name']} at {year}: {row[str(year)]}")
                    if not np.isnan(row[str(year)]):
                        country.co2_emission[index] = row[str(year)]

        for i, row in df_methane.iterrows():
            if row['Country Name'] == country.name:
                for year in country.year:
                    index = country.year.index(year)
                    # print(f"{row['Country Name']} at {year}: {row[str(year)]}")
                    if not np.isnan(row[str(year)]):
                        country.methane_emission[index] = row[str(year)]

        for i, row in df_nuclear.iterrows():
            if row['Country Name'] == country.name:
                for year in country.year:
                    index = country.year.index(year)
                    # print(f"{row['Country Name']} at {year}: {row[str(year)]}")
                    if not np.isnan(row[str(year)]):
                        country.nuclear[index] = row[str(year)]
    
    for country in countries:
        for year in country.year:
            index = country.year.index(year)
            if country.green_house_gas_emission[index] != None and country.population[index] != None:
                country.green_house_gas_emission_per_capita[index] = country.green_house_gas_emission[index] / country.population[index]
            # country.gdp_per_capita[index] = country.gdp[index] / country.population[index]
            if country.co2_emission[index] != None and country.population[index] != None:
                country.co2_emission_per_capita[index] = country.co2_emission[index] / country.population[index]
            if country.methane_emission[index] != None and country.population[index] != None:
                country.methane_emission_per_capita[index] = country.methane_emission[index] / country.population[index]
            if country.nuclear[index] != None and country.population[index] != None:
                country.nuclear_per_capita[index] = country.nuclear[index] / country.population[index]

def add_oecd_data(df):
    for country in countries:
        for i, row in df.iterrows():
            if row['LOCATION'] == country.code:
                if row['TIME'] in country.year:
                    index = country.year.index(row['TIME'])
                    if row['MEASURE'] == 'THND_TONNE':
                        country.municipal_waste[index] = row['Value']
                    if row['MEASURE'] == 'KG_CAP':
                        country.municipal_waste_per_capita[index] = row['Value']


def _show(ctry):
    for country in countries:
        if str(ctry) == str(country):
            print(f'{country.name} at \t {country.year[-1]}: {country.green_house_gas_emission[-1]} \t with population \t\t{country.population[-1]} \t\t and emission per capita \t\t{country.green_house_gas_emission_per_capita[-1]} \t\t kt of CO2 equivalent with {country.gdp[-1]}.')


def create_dict(data) -> dict:
    countries_dict = dict()
    for country in data:
        countries_dict[country.name] = {'code': country.code, 
                                        'green_house_gas_emission': country.green_house_gas_emission,
                                        'green_house_gas_emission_per_capita': country.green_house_gas_emission_per_capita,
                                        'co2_emission': country.co2_emission,
                                        'co2_emission_per_capita': country.co2_emission_per_capita,
                                        'methane_emission': country.methane_emission,
                                        'methane_emission_per_capita': country.methane_emission_per_capita,
                                        'nuclear': country.nuclear,
                                        'nuclear_per_capita': country.nuclear_per_capita,
                                        'municipal_waste': country.municipal_waste,
                                        'municipal_waste_per_capita': country.municipal_waste_per_capita,
                                        'population': country.population,
                                        'gdp': country.gdp,
                                        'year': country.year}
    return countries_dict


if __name__ == '__main__':
    create_database(df_green_house_gases, df_population, df_gdp)
    add_oecd_data(df_municipal_waste)
    _show('Netherlands')
    _show('Hungary')
    _show('Germany')
    countries_to_json = create_dict(countries)
    with open('data_green_advanced.json', 'w') as f:
        json.dump(countries_to_json, f, indent = 2)