from debate.adjudicator import Allocator
from debate.adjudicator.stab import StabAllocator

from munkres import Munkres

class HungarianAllocator(Allocator):

    def calc_cost(self, debate, adj):
        cost = 0

        cost += 1000000 * adj.conflict_with(debate.aff_team)
        cost += 1000000 * adj.conflict_with(debate.neg_team)
        cost += 10000 * adj.seen_team(debate.aff_team, debate.round)
        cost += 10000 * adj.seen_team(debate.neg_team, debate.round)

        cost += (10 - debate.bracket) * adj.score

        return cost

    def allocate(self):
        from debate.models import AdjudicatorAllocation

        print "running Stab"
        initial = StabAllocator(self.debates,
                                self.adjudicators).allocate(avoid_conflicts=False)

        print "calculating costs"

        chairs_only = [a for a in initial if len(a.panel) == 0]
        panels = [a for a in initial if len(a.panel) > 0]

        chair_debates = [a.debate for a in chairs_only]
        chairs = [a.chair for a in chairs_only]

        n = len(chairs)

        cost_matrix = [[0] * n for i in range(n)]

        for i, debate in enumerate(chair_debates):
            for j, adj in enumerate(chairs):
                cost_matrix[i][j] = self.calc_cost(debate, adj)

        print "optimizing"

        m = Munkres()
        indexes = m.compute(cost_matrix)

        total_cost = 0
        for r, c in indexes:
            total_cost += cost_matrix[r][c]

        print 'total cost', total_cost
        print n

        result = ((chair_debates[i], chairs[j]) for i, j in indexes)
        alloc = [AdjudicatorAllocation(d, c) for d, c in result]

        print [(a.debate, a.chair) for a in alloc]

        # do panels
        n = len(panels)

        from itertools import chain
        debates = [a.debate for a in panels]
        panellists = []
        for p in panels:
            panellists.extend(tuple(a[1] for a in p))
        

        print "costing panellists"

        cost_matrix = [[0] * n * 3 for i in range(n*3)]
        for i, debate in enumerate(debates):
            for j in range(3):
                for k, adj in enumerate(panellists):
                    cost_matrix[3*i+j][k] = self.calc_cost(debate, adj)

        print "optimizing"

        indexes = m.compute(cost_matrix)

        cost = 0
        for r, c in indexes:
            cost += cost_matrix[r][c]

        p = [[] for i in range(n)]
        for r, c in indexes:
            p[r // 3].append(panellists[c])

        for i, d in enumerate(debates):
            a = AdjudicatorAllocation(d)
            p[i].sort(key=lambda a: a.score, reverse=True)
            a.chair = p[i].pop(0)
            a.panel = p[i]
            alloc.append(a)

        return alloc 

def test():
    from debate.models import Round
    r = Round.objects.get(pk=4)
    debates = r.debates()
    adjs = list(r.active_adjudicators.all())

    HungarianAllocator(debates, adjs).allocate()

if __name__ == '__main__':
    test()

