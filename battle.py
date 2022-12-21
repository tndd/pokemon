from dataclasses import dataclass

import pandas as pd


@dataclass
class AtkMethod:
    value: int
    def_category: str


def get_data_pokemon():
    d_pokemon = pd.read_csv('pokemon.csv', index_col=0)
    # add column unique_name for index
    unique_name = d_pokemon['Name'] + '/' + d_pokemon['Variation'].fillna('')
    d_pokemon['unique_name'] = unique_name.str.rstrip('/') # remove right excess "/"
    return d_pokemon.set_index('unique_name')


def determine_atk_method(pokemon):
    if pokemon['Attack'] > pokemon['Sp. Atk']:
        atk_method = AtkMethod(pokemon['Attack'], 'Defense')
    elif pokemon['Attack'] <= pokemon['Sp. Atk']: # sp.atk has priority over atk
        atk_method = AtkMethod(pokemon['Sp. Atk'], 'Sp. Def')
    return atk_method


def calc_damage(atk_method, pokemon_def):
    base_move_damage = 120
    pokemon_def_value = pokemon_def[atk_method.def_category]
    move_damage = base_move_damage * atk_method.value // pokemon_def_value
    damage = ((22 * move_damage) // 50) + 2
    return damage


def main():
    d_pokemon = get_data_pokemon()
    print(d_pokemon)


if __name__ == '__main__':
    main()
