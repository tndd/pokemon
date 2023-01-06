import json
from datetime import datetime


def store_frequency(freq):
    with open('data/frequency.json', 'w') as f:
        json.dump(freq, f, indent=4)


def init_frequency():
    with open('data/paldea.json', 'r') as f:
        d = json.load(f)
    freq = {}
    freq['freq'] = {}
    freq['hist'] = {}
    for pokemon in d['legal']:
        freq['freq'][pokemon] = 1
    store_frequency(freq)


def get_frequency():
    with open('data/frequency.json', 'r') as f:
        d = json.load(f)
    return d


def update_frequency(pokemons):
    freq = get_frequency()
    # is exist pokemons in frequency
    if not all(poke in freq['freq'] for poke in pokemons):
        raise Exception("Detects doesn't exist pokemon")
    for pokemon in pokemons:
        freq['freq'][pokemon] += 1
    freq['hist'][datetime.now().strftime('%Y-%m-%d|%H:%M:%S')] = pokemons
    store_frequency(freq)


def rollback_frequency():
    freq = get_frequency()
    latest_key = max(freq['hist'], key=lambda x: freq['hist'][x])
    pokemons_latest = freq['hist'][latest_key]
    for pokemon in pokemons_latest:
        freq['freq'][pokemon] -= 1
    del freq['hist'][latest_key]
    store_frequency(freq)
    print(f'Rollback | key:{latest_key}, pokemons: {pokemons_latest}')


def main() -> None:
    # init_frequency()
    update_frequency(['Sprigatito', 'Iron Thorns', 'Iron Moth'])
    # rollback_frequency()


if __name__ == '__main__':
    main()
