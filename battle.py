from dataclasses import dataclass
from math import floor, ceil

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


def calc_damage(
        atk_method,
        atk_type,
        pokemon_def,
        move_dmg = 120,
        base_stats_atk = 0,
        base_stats_def = 0,
        effort_value_atk = 0,
        effort_value_def = 0,
        nature_atk = 1,
        nature_def = 1
    ):
    pokemon_atk_value = floor((atk_method.value + (base_stats_atk // 2) + (effort_value_atk // 8) + 5) * nature_atk)
    pokemon_def_value = floor((pokemon_def[atk_method.def_category] + (base_stats_def // 2) + (effort_value_def // 8) + 5) * nature_def)
    base_dmg = move_dmg * pokemon_atk_value // pokemon_def_value
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
    n = ceil((pokemon_def['HP'] + 60) / dmg)
    return n


def battle(pokemon_me, pokemon_enemy):
    print(f"Me: {pokemon_me['unique_name']}, Enemy: {pokemon_enemy['unique_name']}')")
    beat_num_me = calc_beat_num(pokemon_me, pokemon_enemy)
    beat_num_enemy = calc_beat_num(pokemon_enemy, pokemon_me)
    # win = 1, lose = -1, draw = 0
    if beat_num_me < beat_num_enemy:
        return 1
    elif beat_num_me > beat_num_enemy:
        return -1
    else:
        if pokemon_me['Speed'] > pokemon_enemy['Speed']:
            return 1
        elif pokemon_me['Speed'] < pokemon_enemy['Speed']:
            return -1
        else:
            return 0


def main():
    d_pokemon = get_data_pokemon()
    miraidon = d_pokemon.loc['Miraidon']
    garchomp = d_pokemon.loc['Garchomp']
    mimikyu = d_pokemon.loc['Mimikyu']
    print(calc_damage_best(garchomp, mimikyu))
    print(calc_beat_num(garchomp, mimikyu))


if __name__ == '__main__':
    main()
