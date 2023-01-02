from os import makedirs
from shutil import rmtree
from itertools import combinations, zip_longest
from collections import defaultdict
from concurrent import futures
from glob import glob

import pandas as pd


def party_combinations(top, unit):
    df = pd.read_csv(f'out/battle_results/avg.csv')[:top]
    return list(combinations(df['Self'], unit))


def get_party_score(battle_results, party):
    print(' | '.join(party))
    party_score = defaultdict(float)
    for pokemon_pty in party:
        r = battle_results.loc[pokemon_pty]
        for pokemon, score in r.items():
            party_score[pokemon] += score
    return (party, party_score)


def get_df_party_scores(battle_results, parties):
    scores = {}
    for party in parties:
        r = get_party_score(battle_results, party)
        party_name = '|'.join(r[0])
        scores[party_name] = r[1]
    df = pd.DataFrame.from_dict(data=scores, orient="index")
    df.index.name = 'Party'
    return df


def get_df_party_scores_multi_process(battle_results, parties, max_workers):
    chunk_size = max(1, len(parties) // max_workers)
    parties_splited = [parties[i:i + chunk_size] for i in range(0, len(parties), chunk_size)]
    with futures.ProcessPoolExecutor(max_workers=max_workers) as executer:
        fts = [executer.submit(get_df_party_scores, battle_results, parties) for parties in parties_splited]
    dfs = [f.result() for f in fts]
    df_score = pd.concat(dfs)
    return df_score


def party_score(top, unit, max_workers=8, segment=100000):
    # make tmp dir
    path_tmp_dir = f'out/party/score_top{top}_unit{unit}'
    makedirs(path_tmp_dir, exist_ok=True)
    try:
        # calc party scores
        parties = party_combinations(top, unit)
        br = pd.read_csv('out/battle_results/avg.csv').set_index('Self').drop('score', axis=1)
        for n, parties_part in enumerate(zip_longest(*[iter(parties)] * segment)):
            partyies_part_exclude_none = [party for party in parties_part if party is not None]
            df_score = get_df_party_scores_multi_process(br, partyies_part_exclude_none, max_workers)
            df_score.to_pickle(f'{path_tmp_dir}/{n}.pkl')
        # concat completed tmp party scores csv
        df = pd.concat([pd.read_pickle(path) for path in glob(f'{path_tmp_dir}/*.pkl')])
        # remove tmp csv files after store full party score csv file
        df.to_pickle(f'{path_tmp_dir}.gz')
    except Exception as e:
        print(e)
    finally:
        rmtree(path_tmp_dir)


def main() -> None:
    party_score(top=100, unit=6)


if __name__ == '__main__':
    main()
