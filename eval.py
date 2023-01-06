import pandas as pd
from os import makedirs
from glob import glob
from concurrent import futures

from frequency import get_frequency


def get_poke_weight():
    freq = get_frequency()
    values_sum = sum(freq['freq'].values())
    poke_weight = {}
    for poke, freq_num in freq['freq'].items():
        poke_weight[poke] = (freq_num / values_sum) * 100
    return poke_weight


def parties_weighted(parties, poke_weight):
    for pokemon, weight in poke_weight.items():
        print(pokemon)
        parties[pokemon] = parties[pokemon].mul(weight)
    return parties


def parties_weighted_multi_process(parties, poke_weight, max_workers=8):
    chunk_size = max(1, len(parties) // max_workers)
    parties_splited = [parties[i:i + chunk_size] for i in range(0, len(parties), chunk_size)]
    with futures.ProcessPoolExecutor(max_workers=max_workers) as executer:
        fts = [executer.submit(parties_weighted, pty, poke_weight) for pty in parties_splited]
    dfs = [f.result() for f in fts]
    return pd.concat(dfs)


def party_rank(path):
    parties = pd.read_pickle(path)
    poke_weight = get_poke_weight()
    parties_w = parties_weighted_multi_process(parties, poke_weight)
    parties_w['score'] = parties_w.sum(axis=1)
    parties_w = parties_w.sort_values(by='score', ascending=False)
    # store parties rank
    score_dir = 'out/rank'
    makedirs(score_dir, exist_ok=True)
    filename = path.split('/')[-1][:-3]
    parties_w['score'].to_csv(f'{score_dir}/{filename}.csv')


def party_ranks():
    for path in glob('out/party/*.gz'):
        print(path)
        party_rank(path)


def main() -> None:
    party_ranks()


if __name__ == '__main__':
    main()
