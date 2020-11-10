from game import main
from importlib import util

if __name__ == '__main__':
    # load players
    player_modules = ['random_player', 'random_player']
    players = []
    for player_module in player_modules:
        spec = util.spec_from_file_location("module.name", player_module + ".py")
        foo = util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        players.append(foo)
    main(players, False)
