"""Adds randomly generated side allocations to teams."""

import header
import debate.models as m
import random
import argparse

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("rounds", type=int, nargs="+", help="Round to generate for.")
parser.add_argument("-d", "--delete", action="store_true", help="Delete allocations, don't create any.")
parser.add_argument("-q", "--quiet", action="store_true", help="Don't print the allocations.")
args = parser.parse_args()

for seq in args.rounds:
    round = m.Round.objects.get(seq=seq)
    teams = list(m.Team.objects.all())
    assert len(teams) % 2 == 0, "There aren't an even number of teams ({0})".format(len(teams))
    random.shuffle(teams)
    affs = teams[:len(teams)/2]
    negs = teams[len(teams)/2:]
    m.TeamPositionAllocation.objects.filter(round=round).delete()
    if not args.quiet:
        print(str(round))
        print("Affirmative:                   Negative:")
        for aff, neg in zip(sorted(affs), sorted(negs)):
            print("{0:30} {1:30}".format(aff.short_name, neg.short_name))
    if args.delete:
        continue
    for team in affs:
        m.TeamPositionAllocation(round=round, team=team, position=m.TeamPositionAllocation.POSITION_AFFIRMATIVE).save()
    for team in negs:
        m.TeamPositionAllocation(round=round, team=team, position=m.TeamPositionAllocation.POSITION_NEGATIVE).save()
