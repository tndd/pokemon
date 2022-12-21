import pandas as pd


def get_data_pokemon():
    d_pokemon = pd.read_csv('pokemon.csv', index_col=0)
    # add column unique_name for index
    unique_name = d_pokemon['Name'] + '/' + d_pokemon['Variation'].fillna('')
    d_pokemon['unique_name'] = unique_name.str.rstrip('/') # remove right excess "/"
    return d_pokemon.set_index('unique_name')


def determine_atk_method(pokemon):
    if pokemon['Attack'] > pokemon['Sp. Atk']:
        atk_method = (pokemon['Attack'], 'Defense') # 1: atk value, 2: def or sp.def for receive
    elif pokemon['Attack'] <= pokemon['Sp. Atk']: # sp.atk has priority over atk
        atk_method = (pokemon['Sp. Atk'], 'Sp. Def') # 1: atk value, 2: def or sp.def for receive
    return atk_method


def main():
    d_pokemon = get_data_pokemon()
    print(d_pokemon)


if __name__ == '__main__':
    main()
