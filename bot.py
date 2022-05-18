from logging.config import valid_ident
from typing import List

from card import Card, RANK, SUIT


def parse_card_arr(cards: List[str]):
    return [Card(card) for card in cards]


def same_suit(card1: Card, card2: Card):
    return card1.suit["value"] == card2.suit["value"]


def get_highest_played_card(played: List[Card]):
    highestCard = played[0]
    for i in range(1, len(played)):
        card = played[i]
        if (
            same_suit(card, highestCard)
            and card.rank["value"] > highestCard.rank["value"]
        ):
            highestCard = card

    return highestCard


def get_play_card(played_str_arr: List[str], cards_str_arr: List[str]):
    played_cards = parse_card_arr(played_str_arr)
    cards = parse_card_arr(cards_str_arr)

    # First turn is ours or we have won last hand.
    # Throw the first card in hand.
    # TODO: maybe play Ace or King here
    if len(played_cards) == 0:
        for card in cards:
            if card.suit != SUIT["SPADE"]:
                if card.rank == RANK["ACE"]:
                    return card
        # S H C D
       # for i in c # RETURNS HIGHEST CARD if your turn always

    selected_card, valid_card = None, None
    highest_card = get_highest_played_card(played_cards)
    # select higher card of same suit
    for card in cards:
        if same_suit(card, highest_card):
            if card.rank["value"] > highest_card.rank["value"]:
                selected_card = card
            else:
                valid_card = card

    # card of same suit exists but not higher than played
    if selected_card is None and valid_card is not None:
        # TODO: maybe play a low-rank card if no winning card exists
        selected_card = valid_card

    # no card of same suit found; use spade
    if selected_card is None:
        opponent_spade = None
        # check first is other players have played spade card
        for card in played_cards:
            if card.suit == SUIT["SPADE"]:
                opponent_spade = card

        for card in cards:
            if opponent_spade:
                if card.rank["value"] > opponent_spade.rank["value"]:
                    selected_card = card
                    break
            else:
                if opponent_spade is None:
                    # TODO: maybe play a low-rank spade card if opponents have not played spade
                    selected_card = card[-1]
                break

    # no spade card in hand; use any card
    if selected_card is None:
        # TODO: maybe play a low-rank card if no winning card exists
        selected_card = cards[0]

    return selected_card



def suitval(suitarr):
    ret_count = 0
    if len(suitarr) > 6:
        ret_count = 0
    else:
        for i in range(len(suitarr)-1):
            if suitarr[i].rank == RANK["ACE"]:
                ret_count += 1
                if suitarr[i+1].rank == RANK["KING"]:
                    ret_count += 1
            elif suitarr[i].rank == RANK["KING"]:
                if suitarr[i+1].rank == RANK["QUEEN"]:
                    ret_count += 1
    return ret_count


def spade_bid(spadearr):
    initial_length = len(spadearr)
    ret_count = 0
    flag = 0

    for i in range(initial_length-1):
        if initial_length >= 1 and spadearr[i].rank == RANK["ACE"]:
            ret_count += 1
            flag += 1
            if initial_length >= 2 and spadearr[i+1].rank == RANK["KING"]:
                ret_count += 1
                flag += 1
                if initial_length >= 3 and spadearr[i+2].rank == RANK["QUEEN"]:
                    ret_count += 1
                    flag += 1
        elif spadearr[i].rank == RANK["KING"]:
            if spadearr[i].rank == RANK["QUEEN"]:
                ret_count += 1
                flag += 1
    if flag != 0:
        adjusted_length = len(spadearr) - flag
        if(adjusted_length <= 2 and flag <= 2):
            ret_count += 1
        elif(adjusted_length == 3 and flag >= 2):
            ret_count += 2
        elif(adjusted_length == 4 and flag >= 2):
            ret_count += 3
    else:
        if(initial_length == 4):
            ret_count += 1
        elif(initial_length == 5):
            ret_count += 2
        if(initial_length == 6):
            ret_count += 3
    return ret_count


def get_bid(cardsStrArr: List[str]):
    count = 0
    cards = parse_card_arr(cardsStrArr)

    clubarr = []
    heartarr = []
    diamondarr = []
    spadearr = []

    # counting the number of cards in each suits
    for card in cards:
        if card.suit == SUIT["SPADE"]:
            spadearr.append(card)
        if card.suit == SUIT["CLUB"]:
            clubarr.append(card)
        if card.suit == SUIT["HEART"]:
            heartarr.append(card)
        if card.suit == SUIT["DIAMOND"]:
            diamondarr.append(card)

    count += suitval(clubarr)
    count += suitval(diamondarr)
    count += suitval(heartarr)
    count += spade_bid(spadearr)

    # 8 is maximum allowed bid
    count = count if count < 8 else 8
    # 1 is minimum allowed bid
    return max(count, 1)
