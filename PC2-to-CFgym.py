'''
Convert PC2 standings to Codeforces gym ghost file .dat format.
Instructions: 
1. copy report.xml and feed.xml from pc2 into current directory.
2. python3 PC2-to-CFgym.py > contest.dat
'''

import collections
import string
import xml.etree.ElementTree

report_xml = xml.etree.ElementTree.parse('report.xml')
feed_xml = xml.etree.ElementTree.parse('feed.xml')
report = report_xml.getroot()
feed = feed_xml.getroot()
problems = report.findall('problem')
teams = [account for account in report.findall('account') if account.get('type') == 'TEAM']
submissions = feed.findall('run')

print('')
print('@contest', report.find('contest_information').get('title'))
print('@contlen', report.find('contest_time').get('conestLengthMins'))
print('@problems', len(problems))
print('@teams', len(teams))
print('@submissions', len(submissions))

for problem, letter in zip(problems, string.ascii_uppercase):
    print('@p', ','.join([letter, problem.get('name'), '20', '0']))

for index, team in enumerate(teams):
    print('@t', ','.join([str(index), '0', '1', f'"{team.get('name')}"']))

result_map = {
    'AC': 'OK',
    'RTE': 'RT',
    'WA': 'WA',
    'TLE': 'TL',
    'CE': 'CE'
}

submission_counter = collections.Counter()

for submission in submissions:
    team = str(int(submission.find('team').text) - 1)
    problem_num = int(submission.find('problem').text) - 1
    problem = chr(ord('A') + problem_num)
    submission_counter[(team, problem)] += 1
    submission_count = str(submission_counter[(team, problem)])
    time = str(round(float(submission.find('time').text)))
    verdict = result_map[submission.find('result').text]
    print('@s', ','.join([team, problem, submission_count, time, verdict]))
