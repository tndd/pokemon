from dataclasses import dataclass
from math import ceil

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


def attack_efficiency(type_atk, pokemon_def):
    data_type = pd.read_csv('type.csv', index_col=0)
    effect = data_type.loc[type_atk][pokemon_def['Type1']]
    if not pd.isnull(pokemon_def['Type2']):
        effect *= data_type.loc[type_atk][pokemon_def['Type2']]
    return effect


def calc_damage(atk_method, atk_type, pokemon_def):
    move_dmg = 120
    pokemon_def_value = pokemon_def[atk_method.def_category]
    base_dmg = move_dmg * atk_method.value // pokemon_def_value
    damage = ((22 * base_dmg) // 50) + 2
    efficiency = attack_efficiency(atk_type, pokemon_def)
    return int(damage * efficiency)


def calc_damage_best(pokemon_atk, pokemon_def):
    atk_method = determine_atk_method(pokemon_atk)
    dmg_best = calc_damage(atk_method, pokemon_atk['Type1'], pokemon_def)
    if not pd.isnull(pokemon_atk['Type2']):
        dmg_best = max(dmg_best, calc_damage(atk_method, pokemon_atk['Type2'], pokemon_def))
    return dmg_best


def calc_beat_num(pokemon_atk, pokemon_def):
    dmg = calc_damage_best(pokemon_atk, pokemon_def)
    n = ceil(pokemon_def['HP'] / dmg)
    return n


def main():
    d_pokemon = get_data_pokemon()
    print(d_pokemon)


if __name__ == '__main__':
    main()
