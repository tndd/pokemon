import json
from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations
from math import ceil, floor

import numpy as np
import pandas as pd


@dataclass
class AtkMethod:
    value: int
    def_category: str


def get_data_pokemon():
    d_pokemon = pd.read_csv('data/pokemon.csv', index_col=0)
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
    data_type = pd.read_csv('data/type.csv', index_col=0)
    effect = data_type.loc[type_atk][pokemon_def['Type1']]
    if not pd.isnull(pokemon_def['Type2']):
        effect *= data_type.loc[type_atk][pokemon_def['Type2']]
    return effect


def calc_damage(
        atk_method,
        atk_type,
        pokemon_def,
        move_dmg = 80,
        base_stats_atk = 31,
        base_stats_def = 31,
        effort_value_atk = 0,
        effort_value_def = 0,
        nature_atk = 1,
        nature_def = 1
    ):
    pokemon_atk_value = floor((atk_method.value + (base_stats_atk / 2) + (effort_value_atk / 8) + 5) * nature_atk)
    pokemon_def_value = floor((pokemon_def[atk_method.def_category] + (base_stats_def / 2) + (effort_value_def / 8) + 5) * nature_def)
    base_dmg = floor(22 * move_dmg * pokemon_atk_value / pokemon_def_value)
    damage = np.round(floor((base_dmg / 50) + 2) * 1.5)
    efficiency = attack_efficiency(atk_type, pokemon_def)
    return floor(damage * efficiency)


def calc_damage_best(pokemon_atk, pokemon_def):
    atk_method = determine_atk_method(pokemon_atk)
    dmg_best = calc_damage(atk_method, pokemon_atk['Type1'], pokemon_def)
    if not pd.isnull(pokemon_atk['Type2']):
        dmg_best = max(dmg_best, calc_damage(atk_method, pokemon_atk['Type2'], pokemon_def))
    if dmg_best == 0:
        # case of zero damage
        dmg_best = 0.1
    return dmg_best


def calc_damage_percentage(
        pokemon_atk,
        pokemon_def,
        base_stat_hp = 31,
        effort_value_hp = 0,
    ):
    dmg = calc_damage_best(pokemon_atk, pokemon_def)
    pokemon_def_hp = pokemon_def['HP'] + floor((base_stat_hp / 2) + (effort_value_hp / 8)) + 60
    return (dmg / pokemon_def_hp)


def battle_report(pokemon_alfa, pokemon_bravo):
    # calc inflict damage percentage
    dmg_from_alfa_to_bravo = calc_damage_percentage(pokemon_alfa, pokemon_bravo)
    dmg_from_bravo_to_alfa = calc_damage_percentage(pokemon_bravo, pokemon_alfa)
    # calc beat num
    beat_num_alfa = ceil(1 / dmg_from_alfa_to_bravo)
    beat_num_bravo = ceil(1 / dmg_from_bravo_to_alfa)
    # calc speed diff
    spd_offset_based_on_alfa = pokemon_bravo['Speed'] - pokemon_alfa['Speed']
    # judge battle: win = 1, lose = -1, draw = 0
    win_pokemon = None
    act_num_lose_pokemon = None
    winner_remain_hp = None
    if spd_offset_based_on_alfa < 0:
        # alfa is faster than bravo
        if beat_num_alfa <= beat_num_bravo:
            win_pokemon = pokemon_alfa.name
            act_num_lose_pokemon = beat_num_alfa - 1
            winner_remain_hp = 1 - dmg_from_bravo_to_alfa * act_num_lose_pokemon
        elif beat_num_alfa > beat_num_bravo:
            win_pokemon = pokemon_bravo.name
            act_num_lose_pokemon = beat_num_bravo
            winner_remain_hp = 1 - dmg_from_alfa_to_bravo * act_num_lose_pokemon
    elif spd_offset_based_on_alfa > 0:
        # bravo is faster than alfa
        if beat_num_bravo <= beat_num_alfa:
            win_pokemon = pokemon_bravo.name
            act_num_lose_pokemon = beat_num_bravo - 1
            winner_remain_hp = 1 - dmg_from_alfa_to_bravo * act_num_lose_pokemon
        elif beat_num_bravo > beat_num_alfa:
            win_pokemon = pokemon_alfa.name
            act_num_lose_pokemon = beat_num_alfa
            winner_remain_hp = 1 - dmg_from_bravo_to_alfa * act_num_lose_pokemon
    else:
        # speed of alfa & bravo is equal
        if beat_num_alfa < beat_num_bravo:
            win_pokemon = pokemon_alfa.name
            act_num_lose_pokemon = beat_num_alfa - 0.5
            winner_remain_hp = dmg_from_bravo_to_alfa * act_num_lose_pokemon
        elif beat_num_alfa > beat_num_bravo:
            win_pokemon = pokemon_bravo.name
            act_num_lose_pokemon = beat_num_bravo - 0.5
            winner_remain_hp = dmg_from_alfa_to_bravo * act_num_lose_pokemon
        else:
            # battle is DRAW
            pass
    return {
        'pokemon_alfa': pokemon_alfa.name,
        'pokemon_bravo': pokemon_bravo.name,
        'win_pokemon': win_pokemon,
        'winner_remain_hp': winner_remain_hp
    }


def simulate_battle():
    d_pokemon = get_data_pokemon()
    battle_results = defaultdict(
        lambda: {
            'win': defaultdict(float),  # received damage until win
            'lose': defaultdict(float), # inflict damage until lose
            'draw': []
        }
    )
    for poke_alfa, poke_bravo in combinations(list(d_pokemon.index), 2):
        r = battle_report(d_pokemon.loc[poke_alfa], d_pokemon.loc[poke_bravo])
        if r['win_pokemon'] == poke_alfa:
            battle_results[poke_alfa]['win'][poke_bravo] = r['winner_remain_hp']
            battle_results[poke_bravo]['lose'][poke_alfa] = r['winner_remain_hp']
        elif r['win_pokemon'] == poke_bravo:
            battle_results[poke_bravo]['win'][poke_alfa] = r['winner_remain_hp']
            battle_results[poke_alfa]['lose'][poke_bravo] = r['winner_remain_hp']
        else:
            battle_results[poke_bravo]['draw'].append(poke_alfa)
            battle_results[poke_alfa]['draw'].append(poke_bravo)
        print(f"{poke_alfa:32}\t{poke_bravo:32}\t{str(poke_alfa == r['win_pokemon']):16}\t{r['winner_remain_hp']}")
    with open('out/battle_results.json', 'w') as f:
        json.dump(battle_results, f, indent=4)


def main():
    simulate_battle()


if __name__ == '__main__':
    main()
