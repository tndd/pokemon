import json
import time
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
    key = datetime.now().isoformat(sep=' ', timespec='milliseconds')
    freq['hist'][key] = pokemons
    store_frequency(freq)
    print(f'Update | key:{key}, pokemons: {pokemons}')
    time.sleep(0.001)


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
    init_frequency()
    update_frequency(['Dragapult', 'Hydreigon', 'Gholdengo', 'Dragonite', 'Meowscarada', 'Garchomp', 'Azumarill', 'Kingambit', 'Volcarona', 'Baxcalibur', 'Dondozo', 'Amoonguss', 'Hippowdon', 'Garganacl', 'Annihilape', 'Toedscruel', 'Amoonguss'])
    update_frequency(['Dragapult', 'Hydreigon', 'Gholdengo', 'Dragonite', 'Meowscarada', 'Garchomp', 'Azumarill', 'Kingambit', 'Volcarona', 'Baxcalibur', 'Dondozo', 'Amoonguss', 'Hippowdon', 'Garganacl', 'Annihilape', 'Toedscruel', 'Amoonguss'])
    update_frequency(['Dragapult', 'Hydreigon', 'Gholdengo', 'Dragonite', 'Meowscarada', 'Garchomp', 'Azumarill', 'Kingambit', 'Volcarona', 'Baxcalibur', 'Dondozo', 'Amoonguss', 'Hippowdon', 'Garganacl', 'Annihilape', 'Toedscruel', 'Amoonguss'])
    update_frequency(['Dragapult', 'Hydreigon', 'Gholdengo', 'Dragonite', 'Meowscarada', 'Garchomp', 'Azumarill', 'Kingambit', 'Volcarona', 'Baxcalibur', 'Dondozo', 'Rotom/Wash Rotom', 'Skeledirge', 'Mimikyu', 'Amoonguss', 'Hippowdon', 'Garganacl', 'Clodsire', 'Annihilape', 'Toedscruel', 'Amoonguss'])
    update_frequency(['Dragapult', 'Hydreigon', 'Gholdengo', 'Dragonite', 'Meowscarada', 'Garchomp', 'Azumarill', 'Kingambit', 'Volcarona', 'Baxcalibur', 'Dondozo', 'Rotom/Wash Rotom', 'Skeledirge', 'Mimikyu', 'Amoonguss', 'Hippowdon', 'Garganacl', 'Clodsire', 'Annihilape', 'Toedscruel', 'Amoonguss'])
    update_frequency(['Hippowdon', 'Azumarill', 'Salamence', 'Noivern', 'Toxtricity/Amped Form', 'Scizor'])
    update_frequency(['Grimmsnarl', 'Scizor', 'Toxtricity/Amped Form', 'Mimikyu', 'Dragonite', 'Dragapult'])
    update_frequency(['Baxcalibur', 'Garganacl', 'Amoonguss', 'Rotom/Wash Rotom', 'Dragapult', 'Scizor'])
    update_frequency(['Hippowdon', 'Gholdengo', 'Dragonite', 'Hydreigon', 'Azumarill', 'Skeledirge'])
    update_frequency(['Arcanine', 'Corviknight', 'Garchomp', 'Rotom/Wash Rotom', 'Meowscarada', 'Tyranitar'])


if __name__ == '__main__':
    main()
