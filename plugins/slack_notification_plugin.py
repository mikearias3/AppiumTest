import os
import glob
import json
import requests
import xml.etree.ElementTree as ET

CIRCLE_BUILD_NUM = os.environ['CIRCLE_BUILD_NUM']
CIRCLE_PROJECT_USERNAME = os.environ['CIRCLE_PROJECT_USERNAME']
CIRCLE_PROJECT_REPONAME = os.environ['CIRCLE_PROJECT_REPONAME']
CIRCLE_USERNAME = os.getenv("USER") or os.environ['CIRCLE_USERNAME']
CIRCLE_BUILD_URL = os.environ['CIRCLE_BUILD_URL']
TOKEN = os.environ['TOKEN']
slack_api = os.environ['SLACK_API']
CIRCLE_BRANCH = os.environ['CIRCLE_BRANCH']
'''
CIRCLE_BUILD_NUM = '117'
CIRCLE_PROJECT_USERNAME = 'VICEMedia'
CIRCLE_PROJECT_REPONAME = 'qa-fe'
CIRCLE_USERNAME = 'xiaohanc'
CIRCLE_BUILD_URL = 'https://circleci.com/gh/VICEMedia/qa-fe/116'
TOKEN = "82a5789605435e65018571a25067f98425ae4ccf"
slack_api = "https://hooks.slack.com/services/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"
# slack_api = "https://hooks.slack.com/services/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"
'''

circle_repo_url = CIRCLE_BUILD_URL.replace(CIRCLE_BUILD_NUM, '')


# convert milliseconds to human readable
def convert_millis(time):
    s = time / 1000
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return h, m, s


# capture information from current build via circleci API
api_url = "https://circleci.com/api/v1.1/project/"
vcs_type = "github"
current_circleci_api_url = api_url + vcs_type + '/' + CIRCLE_PROJECT_USERNAME \
    + '/' + CIRCLE_PROJECT_REPONAME + '/' + CIRCLE_BUILD_NUM + '?circle-token=' + TOKEN
response = requests.get(current_circleci_api_url)
data = json.loads(response.text)

test_suite_name = "Perform Tests"
for i in data['steps']:
    for action in i['actions']:
        if action['bash_command'] is not None \
                and 'run_env.py' in action['bash_command']:
            test_suite_name = i['name']

PLATFORM = os.getenv("PLATFORM") or "Windows-10-Chrome-61"
VERTICAL = os.getenv("VERTICAL") or "tonic"

for git in data['all_commit_details']:
    commit_url = git['commit_url']
    author_name = git['author_name']
git_commit = data['subject']
build_start_time = data['author_date']
branch = data['branch']
belong = ': ' + CIRCLE_USERNAME + "'s build" + CIRCLE_BUILD_NUM + ' in <' + circle_repo_url + '|' + CIRCLE_PROJECT_USERNAME \
    + '/' + CIRCLE_PROJECT_REPONAME + '>'

if data['why'] == "retry":
    why = " ; retry by " + CIRCLE_USERNAME
elif data['why'] == "github":
    why = " ; triggered by git commit "
elif data['why'] == "api":
    why = " ; triggered by api "

# capture BASE_URL from test file
with open('./android_simple.py') as f:
    for line in f:
        if 'BASE_URL = ' in line:
            exec(line)
            break

test_suites_name = "Mobile Automation Test"


# requests get the allure artifact url via circleci api
def get_current_allure_url():

    api_url = "https://circleci.com/api/v1.1/project/"
    vcs_type = "github"
    CIRCLE_PREVIOUS_BUILD_NUM = '100'
    url = api_url + vcs_type + '/' + CIRCLE_PROJECT_USERNAME + '/' +\
        CIRCLE_PROJECT_REPONAME + '/' + CIRCLE_PREVIOUS_BUILD_NUM

    response = requests.get(url + "/artifacts?circle-token=" + TOKEN)
    data = json.loads(response.text)
    header = 'https://' + CIRCLE_PREVIOUS_BUILD_NUM
    for i in data:
        if header in i['url'] and '/index.html' in i['path']:
            allure_artifact_url = i['url']
            html_path = i['path']
    allure_url = allure_artifact_url.replace(
        CIRCLE_PREVIOUS_BUILD_NUM, str(CIRCLE_BUILD_NUM), 1)
    current_allure_url = allure_url.replace(
        html_path, "test-reports/" + VERTICAL + "/index.html")

    return current_allure_url

last_status = 'None'
# get last test status
with open('./test-reports/' + VERTICAL + '/history/history-trend.json', 'r') as file:
    trend = json.load(file)
if len(trend) > 1:
    if trend[1]['data']['failed'] > 0:
        last_status = 'Failure'
    else:
        last_status = 'Success'

# Get last build status
try:
    CIRCLE_PREVIOUS_BUILD_NUM = os.environ['CIRCLE_PREVIOUS_BUILD_NUM']
    CIRCLE_ALLURE_REPORT = get_current_allure_url()
    last_url = circle_repo_url + CIRCLE_PREVIOUS_BUILD_NUM
    last_build = "build" + '<' + last_url + '|#' + \
        str(data['previous']['build_num']) + '>: ' + last_status

except:
    last_build = "This is the first build for current stage"
    CIRCLE_ALLURE_REPORT = ""

# capture information from report xml file
for xml in glob.glob('test-report/' + VERTICAL + '/*.xml'):
    root = ET.parse(xml).getroot()
start_time = root.get('start')
stop_time = root.get('stop')
run_time = int(stop_time) - int(start_time)
test_name = root.find('name').text

time = '%d hours %d minutes %d seconds' % convert_millis(run_time)


# capture information from summary json file
with open('./test-reports/' + VERTICAL + '/widgets/summary.json', 'r') as file:
    summary = json.load(file)
passed = summary['statistic']['passed']
skipped = summary['statistic']['skipped']
failed = summary['statistic']['failed']
total = summary['statistic']['total']
if failed == 0:
    status = "Success"
    color = "#36a64f"
else:
    status = "Failure"
    color = "#ff0000"
results = "Passed: " + str(passed) + " Failed: " + \
    str(failed) + " Skipped: " + str(skipped)
text = status + belong + why


# Post custom json data to slack notification
with open('slack.json', 'r') as file:
    slack_message = json.load(file)

for slack in slack_message["attachments"]:
    slack["color"] = color
    slack["author_name"] = CIRCLE_USERNAME + " build at " + build_start_time
    slack["title"] = "Allure report build#" + CIRCLE_BUILD_NUM
    slack["title_link"] = CIRCLE_ALLURE_REPORT
    slack["text"] = text + "\nLastest commit - <" + commit_url + '|' + git_commit + '> by ' + author_name
    slack["actions"][0]["name"] = "{ 'build_parameters': { 'VERTICAL': " + VERTICAL + ", 'PLATFORM': " + PLATFORM + "}}"

    for filed in slack["fields"]:
        if filed['title'] == "Test suits name":
            filed['value'] = test_suites_name
        if filed['title'] == "running time":
            filed['value'] = time
        if filed['title'] == "Test results":
            filed['title'] = "Test results ( Total: " + str(total) + " )"
            filed['value'] = results
        if filed['title'] == "Last build status":
            filed['value'] = last_build
        if filed['title'] == "Circle ci build":
            filed['value'] = '<' + CIRCLE_BUILD_URL + '|#' + CIRCLE_BUILD_NUM + '> - build at ' + CIRCLE_BRANCH


requests.post(slack_api, data=str(slack_message))
