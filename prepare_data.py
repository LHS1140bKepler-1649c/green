import numpy as np
import pandas as pd
import json
from profiler import profile

df_green_house_gases = pd.read_csv('greenhouse_emissions.csv', engine='python', error_bad_lines=False)
df_co2 = pd.read_csv('co2_emissions_in_kt.csv', engine='python', error_bad_lines=False)
df_methane = pd.read_csv('methane_emissions_kt_of_co2_equivalent.csv', engine='python', error_bad_lines=False)
df_gdp = pd.read_csv('gdp_const_2015_usd.csv', engine='python', error_bad_lines=False)
df_population = pd.read_csv('population.csv', engine='python', error_bad_lines=False)
df_nuclear = pd.read_csv('nuclear_energy_percent_of_total_electricity.csv', engine='python', error_bad_lines=False)
df_municipal_waste = pd.read_csv('municipal_waste_oecd.csv', engine='python', error_bad_lines=False)
df_land = pd.read_csv('land_area.csv', engine='python', error_bad_lines=False)
df_forest = pd.read_csv('forest_percentage_of_land_area.csv', engine='python', error_bad_lines=False)
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
        self.emission_land_ratio = list()
        self.population = list()
        self.land_area = list()
        self.forest = list()
        self.forest_size = list()
        self.emission_forest_ratio = list()
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
            country.emission_land_ratio.append(None)
            country.population.append(None)
            country.land_area.append(None)
            country.forest.append(None)
            country.forest_size.append(None)
            country.emission_forest_ratio.append(None)
            country.gdp.append(None)
            country.gdp_per_capita.append(None)

    numpy_df_header = np.array(list(df))
    numpy_df = df.to_numpy()
    numpy_df_population_header = np.array(list(df_population))
    numpy_df_population = df_population.to_numpy()
    numpy_df_gdp_header = np.array(list(df_gdp))
    numpy_df_gdp = df_gdp.to_numpy()
    numpy_df_co2_header = np.array(list(df_co2))
    numpy_df_co2 = df_co2.to_numpy()
    numpy_df_methane_header = np.array(list(df_methane))
    numpy_df_methane = df_methane.to_numpy()
    numpy_df_nuclear_header = np.array(list(df_nuclear))
    numpy_df_nuclear = df_nuclear.to_numpy()
    numpy_df_land_header = np.array(list(df_land))
    numpy_df_land = df_land.to_numpy()
    numpy_df_forest_header = np.array(list(df_forest))
    numpy_df_forest = df_forest.to_numpy()

    for country in countries:
        create_data(numpy_df, numpy_df_header, country, country.green_house_gas_emission)
        create_data(numpy_df_population, numpy_df_population_header, country, country.population)
        create_data(numpy_df_gdp, numpy_df_gdp_header, country, country.gdp)
        create_data(numpy_df_co2, numpy_df_co2_header, country, country.co2_emission)
        create_data(numpy_df_methane, numpy_df_methane_header, country, country.methane_emission)
        create_data(numpy_df_nuclear, numpy_df_nuclear_header, country, country.nuclear)
        create_data(numpy_df_land, numpy_df_land_header, country, country.land_area)
        create_data(numpy_df_forest, numpy_df_forest_header, country, country.forest)
    
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
            if country.green_house_gas_emission[index] != None and country.land_area[index] != None:
                country.emission_land_ratio[index] = to_tree(country.green_house_gas_emission[index]*1000) / country.land_area[index]
            if country.forest[index] != None and country.land_area[index] != None:
                country.forest_size[index] = country.land_area[index] * (country.forest[index] / 100)
            if country.green_house_gas_emission[index] != None and country.forest_size[index] != None and country.forest_size[index] != 0.0:
                country.emission_forest_ratio[index] = to_tree(country.green_house_gas_emission[index]*1000) / country.forest_size[index]


def add_oecd_data(df):
    numpy_header = np.array(list(df_municipal_waste))
    numpy_df = df_municipal_waste.to_numpy()
    _index_time = np.where(numpy_header == 'TIME')
    _index_measure = np.where(numpy_header == 'MEASURE')
    _index_value = np.where(numpy_header == 'Value')
    for country in countries:
        for arr in numpy_df:
            if country.code in arr:
                if arr[_index_time] in country.year:
                    index = country.year.index(arr[_index_time])
                    if arr[_index_measure] == 'THND_TONNE':
                        country.municipal_waste[index] = arr[_index_value][0]
                    if arr[_index_measure] == 'KG_CAP':
                        country.municipal_waste_per_capita[index] = arr[_index_value][0]


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
                                        'emission_land_ratio': country.emission_land_ratio,
                                        'population': country.population,
                                        'land_area': country.land_area,
                                        'forest': country.forest,
                                        'forest_size': country.forest_size,
                                        'emission_forest_ratio': country.emission_forest_ratio,
                                        'gdp': country.gdp,
                                        'year': country.year}
    return countries_dict

# Give the gas emmision data in tonns.
def to_tree(gas):
    acre = 2500
    km2 = 247.10538146717*acre
    return (gas / km2)*1000

def create_data(np_df, np_header, country, output_data):
    _index = np.where(np_df == country.name)[0][0]
    _index2 = np.where(np_header == str(country.year[0]))[0]
    for year in country.year:
        index = country.year.index(year)
        if not np.isnan(np_df[_index][_index2][0]):
            output_data[index] = np_df[_index][_index2][0]
        _index2 += 1


if __name__ == '__main__':
    create_database(df_green_house_gases, df_population, df_gdp)
    add_oecd_data(df_municipal_waste)
    # _show('Hungary')
    countries_to_json = create_dict(countries)
    with open('data_green_advanced_profiled.json', 'w') as f:
        json.dump(countries_to_json, f, indent = 2)