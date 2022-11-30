from django.shortcuts import render
from django.http import HttpResponseNotFound
from .models import Poll, Candidate, Criteria, Score
from urllib.parse import unquote
from string import ascii_letters, digits
from random import choice
from .AHP import normalize_table, ahp
# Create your views here.

alphabet = ascii_letters + digits


def random_string(length):
    '''Generate a random string of given length'''
    return ''.join([choice(alphabet) for i in range(length)])


def index(request):
    '''Index page'''
    if request.method == 'GET':
        return render(request, 'decision_maker/index.html')


def create(request):
    '''Create page'''
    if request.method == 'GET':
        return render(request, 'decision_maker/create.html')
    elif request.method == 'POST':
        data = request.body.decode('utf-8').split('&data=')[1]
        question, candidates, criterias, scores = unquote(data).replace('+', ' ').split(',\r\n')

        new_code = random_string(5)
        while Poll.objects.filter(code=new_code):
            new_code = random_string(5)

        new_admin_code = new_code + random_string(5)

        poll_obj = Poll(code=new_code, admin_code=new_admin_code, question=question, isopen=True)
        poll_obj.save()

        candidate_objs = []
        criteria_objs = []
        for c in candidates.split(','):
            t = Candidate(poll=poll_obj, text=c, vote=0)
            t.save()
            candidate_objs.append(t)
        for c in criterias.split(','):
            t = Criteria(poll=poll_obj, text=c)
            t.save()
            criteria_objs.append(t)

        i = 0
        j = 0
        k = 0
        scores_arr = scores.split(',')
        while i < len(criteria_objs):
            crit = criteria_objs[i]
            cand = candidate_objs[j]
            score_obj = Score(candidate=cand, criteria=crit, score=float(scores_arr[k]))
            score_obj.save()

            k += 1
            j += 1
            if j >= len(candidate_objs):
                j = 0
                i += 1

        print(scores)
        return render(request, 'decision_maker/create_success.html', context={'public_code': new_code, 'private_code': new_admin_code})


def poll(request, code):
    '''Poll/Vote page'''
    if request.method == 'GET':
        if len(code) == 5:
            try:
                poll = Poll.objects.get(code=code)
            except Exception:
                return HttpResponseNotFound('Page not found')
            crit_objs = poll.criteria_set.all()
            cand_objs = poll.candidate_set.all()
            crits = []
            cands = []
            for c in crit_objs:
                crits.append(c.text)
            for c in cand_objs:
                cands.append(c.text)
            return render(request, 'decision_maker/vote.html', context={'question': poll.question, 'criterias': crits, 'candidates': cands})
        elif len(code) == 10:
            poll = Poll.objects.filter(admin_code=code).first()
            if poll is None:
                return HttpResponseNotFound('Page not found')
            question = poll.question
            cand_objs = poll.candidate_set.all()
            cands = [['Candidates', 'Votes']]
            total = 0
            for c in cand_objs:
                cands.append([c.text, c.vote])
                total += c.vote

            return render(request, 'decision_maker/result.html', context={'question': question, 'total': total, 'data': cands})
        else:
            return HttpResponseNotFound('Page not found')
    elif request.method == 'POST' and len(code) == 5:
        try:
            poll = Poll.objects.get(code=code)
        except Exception:
            return HttpResponseNotFound('Page not found')
        data = request.body.decode('utf-8').split('&data=')[1]
        data = unquote(data).split(',')
        data.pop()
        for i, n in enumerate(data):
            data[i] = float(n)
        crit_objs = poll.criteria_set.all()
        cand_objs = poll.candidate_set.all()

        table = normalize_table(data, crit_objs.count())
        weight = ahp(table)

        best = -1
        winner = None
        for cand in cand_objs:
            total_score = 0
            for i, crit in enumerate(crit_objs):
                score_obj = Score.objects.filter(candidate=cand, criteria=crit).first()
                total_score += score_obj.score * weight[i]

            if total_score > best:
                best = total_score
                winner = cand

        winner.vote += 1
        winner.save()
        return render(request, 'decision_maker/vote_success.html')
