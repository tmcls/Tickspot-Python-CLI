#!/usr/bin/env python

import urllib2
import sys
import datetime
import getpass
from xml.dom.minidom import parseString
from calendar import monthrange

ERROR = '\033[91m'
LIST = '\033[95m'
CONFIRMATION = '\033[92m'
QUESTION = '\033[96m'
ENDC = '\033[0m'
API_ENDPOINT = "https://citylive.tickspot.com/api"

# Fetch Username input
username = raw_input("%s\nYour tickspot email address:%s\n" % (QUESTION, ENDC))
if not username:
    print "%sERROR: Please fill in a email adress!%s" % (ERROR, ENDC)
    sys.exit()

# Fetch password input
password = getpass.getpass("%s\nYour tickspot password:%s\n" % (QUESTION, ENDC))
if not password:
    print "%sERROR: Please fill in a password!%s" % (ERROR, ENDC)
    sys.exit()

# Get List of all projects
print "Loading all your projects from tickspot...\n"
try:
    result = urllib2.urlopen("%s/clients_projects_tasks?email=%s&password=%s" % (
        API_ENDPOINT,
        username,
        password)
    )
    data = result.read()
    result.close()
    clients = parseString(data).getElementsByTagName('clients')[0]
    for client in clients.getElementsByTagName('client'):
        print "\n%s" % (
            client.getElementsByTagName('name')[0].firstChild.nodeValue.upper()
        )

        projects = client.getElementsByTagName('projects')[0]
        for project in projects.getElementsByTagName('project'):
            print "[%s%s%s] %s" % (
                LIST, project.getElementsByTagName('id')[0].firstChild.nodeValue,
                ENDC,
                project.getElementsByTagName('name')[0].firstChild.nodeValue
            )

    project_id = raw_input("\n%sChoose a project ID:\n(Default: 945423)%s\n" % (
        QUESTION,
        ENDC
    ))
    if not project_id:
        project_id = 945423
except:
    print "%sERROR in projects: Check your login details!%s" % (
        ERROR,
        ENDC
    )
    sys.exit()

# Get List of all taks for a project
print "Loading all your tasks from tickspot...\n"
try:
    result = urllib2.urlopen("%s/projects?email=%s&password=%s&project_id=%s" % (
        API_ENDPOINT,
        username,
        password,
        project_id)
    )
    data = result.read()
    result.close()
    tasks = parseString(data).getElementsByTagName('tasks')[0]
    for task in tasks.getElementsByTagName('task'):
        print "[%s%s%s] %s" % (
            LIST,
            task.getElementsByTagName('id')[0].firstChild.nodeValue,
            ENDC,
            task.getElementsByTagName('name')[0].firstChild.nodeValue
        )

    task_id = raw_input("\n%sChoose a task ID:\n(Default: 5325389)%s\n" % (
        QUESTION,
        ENDC
    ))
    if not task_id:
        task_id = 5325389
except:
    print "%sERROR in tasks: Check your login details or project ID!%s" % (
        ERROR,
        ENDC
    )
    sys.exit()

# Get from & till date
current_month = int(datetime.datetime.now().strftime("%m"))
current_year = int(datetime.datetime.now().strftime("%Y"))
current_daysinmonth = monthrange(current_year, current_month)[1]

# Ask for date from
date_from_str = raw_input("\n%sDate from:\n(Default: %s/%s/%s)%s\n" % (
    QUESTION,
    "01",
    current_month,
    current_year,
    ENDC
))

# Check Data from
if date_from_str:
    date_from = datetime.datetime.strptime(date_from_str, '%d/%m/%Y').date()
else:
    date_from = datetime.datetime(current_year, current_month, 1).date()

# Ask for date till
date_till_str = raw_input("\n%sDate till:\n(Default: %s/%s/%s)%s\n" % (
    QUESTION,
    current_daysinmonth,
    current_month,
    current_year, ENDC
))

# Check date till
if date_till_str:
    date_till = datetime.datetime.strptime(date_till_str, '%d/%m/%Y').date()
else:
    date_till = datetime.datetime(current_year, current_month, current_daysinmonth).date()

# Preparing some more data
delta = datetime.timedelta(days=1)
date_from2 = date_from
diff = 0
weekend = {5, 6}

# Create entries
print "Saving......\n"
while date_from2 <= date_till:
    if date_from2.weekday() not in weekend:
        diff += 1
        print " - You worked hard (8 hours) on %s " % (date_from2.strftime("%d/%m/%Y"))

        result = urllib2.urlopen("%s/create_entry?email=%s&password=%s&project_id=%s&task_id=%s&hours=%s&date=%s" % (
            API_ENDPOINT,
            username,
            password,
            project_id,
            task_id,
            8,
            date_from2.strftime("%Y%m%d")
        ))
        data = result.read()
        result.close()

    date_from2 += delta

print "\nCompleted !"