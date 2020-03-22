'''
Convert DOMjudge standings to Codeforces gym ghost file .dat format.
Instructions: 
1. Install requests.
2. Run the DOMjudge server.
3. Change the constants below.
4. python3 DOMjudge-to-CFgym.py > contest.dat
'''

import collections
import datetime
import requests

BASE_URL = 'http://localhost:12345'
CONTEST_ID = 3
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'dGlKouosIJJENVMz'

contest = requests.get(f'{BASE_URL}/api/contests/{CONTEST_ID}').json()
teams = requests.get(f'{BASE_URL}/api/contests/{CONTEST_ID}/teams').json()
valid_team_ids = set(team['id'] for team in teams)
problems = requests.get(f'{BASE_URL}/api/contests/{CONTEST_ID}/problems').json()
problems_dict = {problem['id']: problem for problem in problems}
auth = requests.auth.HTTPBasicAuth(ADMIN_USERNAME, ADMIN_PASSWORD)
submissions = requests.get(f'{BASE_URL}/api/contests/{CONTEST_ID}/submissions', auth=auth).json()
judgements = requests.get(f'{BASE_URL}/api/contests/{CONTEST_ID}/judgements', auth=auth).json()
judgements_dict = {judgement['submission_id']: judgement for judgement in judgements}

def to_timedelta(duration_string):
    return datetime.datetime.strptime(duration_string, '%H:%M:%S.%f') - datetime.datetime(1900, 1, 1)

print('')
print('@contest', contest['name'])
print('@contlen', int(to_timedelta(contest['duration']).total_seconds()) // 60)
print('@problems', len(problems))
print('@teams', len(teams))
print('@submissions', len(submissions))

for problem in problems:
    print('@p', ','.join([problem['label'], problem['name'], '20', '0']))

for team in teams:
    print('@t', ','.join([team['id'], '0', '1', f"\"{team['name']} ({team['affiliation']})\""]))

result_map = {
    'AC': 'OK',
    'RTE': 'RT',
    'WA': 'WA',
    'TLE': 'TL',
    'CE': 'CE',
    'NO': 'WA'
}

submission_counter = collections.Counter()

for submission in submissions:
    team_id = submission['team_id']
    if team_id in valid_team_ids:
        problem_id = problems_dict[submission['problem_id']]['label']
        submission_counter[(team_id, problem_id)] += 1
        print('@s', ','.join([team_id,
                            problem_id,
                            str(submission_counter[(team_id, problem_id)]),
                            str(int(to_timedelta(submission['contest_time']).total_seconds())),
                            result_map[judgements_dict[submission['id']]['judgement_type_id']]]))
