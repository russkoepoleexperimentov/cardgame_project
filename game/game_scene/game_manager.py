from game.game_scene.card_line import CardLine


player_first_line: CardLine = None
player_second_line: CardLine = None
enemy_first_line: CardLine = None
enemy_second_line: CardLine = None

turn_count = 0


def is_player_card(card):
    return card.get_game_object().get_parent() == player_first_line.get_game_object() or \
           card.get_game_object().get_parent() == player_second_line.get_game_object()


def is_enemy_card(card):
    return card.get_game_object().get_parent() == enemy_first_line.get_game_object() or \
           card.get_game_object().get_parent() == enemy_second_line.get_game_object()


def enemy_turn():
    if player_first_line.get_game_object().get_children():
        # attack first line
        pass
    else:
        # attack second line
        pass

    end_turn()


def is_player_turn():
    return turn_count % 2 == 0


def end_turn():
    global turn_count
    turn_count += 1


def cards_fight(card1, card2):
    print(card1.card_info, 'vs', card2.card_info)
    #######
    card1.decrease_hit_points(card2.get_damage())
    card2.decrease_hit_points(card1.get_damage())