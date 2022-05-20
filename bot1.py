from logging.config import valid_ident
from operator import and_
from secrets import token_urlsafe
from typing import List

from soupsieve import select

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
        for i in range(len(cards)-1):
            if cards[i].suit != SUIT["SPADE"]:
                if cards[i].rank == RANK["ACE"]:
                    return cards[i]
                elif cards[i].rank == RANK["KING"] and cards[i+1].rank == RANK["QUEEN"]:
                    return cards[i]
                try:
                    if cards[i].suit != cards[i+1].suit and cards[i+1].suit != cards[i+2].suit:
                        return cards[i+1]

                except IndexError:
                    if cards[i].suit != cards[i+1].suit:
                        return cards[i+1]
                        
#choose smallest card available
        ret_card = cards[0]
        for card in cards:
            if card.suit != SUIT["SPADE"]:
                   if ret_card.rank["value"] > card.rank["value"]:
                       ret_card = card

        for card in cards:
            if card.suit == RANK["SPADE"]:
                count += 1

        if count == len(cards):
            for card in cards:
                if card.rank["value"] < ret_card.rank["value"]:
                    ret_card = card
        return ret_card 

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
        for card in played_cards:
           if same_suit(card,highest_card):
               if card.suit["value"] == highest_card.suit["value"]:
                   if card.rank["value"] < valid_card.rank["value"]:
                       valid_card = card
        selected_card = valid_card

    # no card of same suit found; use spade
    if selected_card is None:
        opponent_spade = None
        # check first is other players have played spade card
        for card in played_cards:
            if card.suit == SUIT["SPADE"]:
                opponent_spade = card

        for i in range(len(cards)-1):
            if opponent_spade:
                if card[i].rank["value"] > opponent_spade.rank["value"]:
                    selected_card = cards[i]
                    break
            else:
                # TODO: maybe play a low-rank spade card if opponents have not played spade
                try:
                    if cards[i].suit["value"] != cards[i+1].suit["value"]:
                        selected_card = cards[i]
                        break
                except IndexError:
                    selected_card = cards[i]

    # no spade card in hand; use any card
    if selected_card is None:
        # TODO: maybe play a low-rank card if no winning card exists
        token =cards[0]
        for card in cards:
            if card.rank["value"] < token.rank["value"]:
                token = card
        selected_card =token
        
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
                flag += 2
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


