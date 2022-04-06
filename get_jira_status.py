#!/usr/bin/python3

# https://jira.readthedocs.io/examples.html
# https://jira.readthedocs.io/jirashell.html
# https://jira.readthedocs.io/api.html

import sys
import json

from jira import JIRA

jira = JIRA(server="https://jira.atlassian.com")

project = "ABC123"

affected_versions = [
    "0.1",
    "1.0",
    "1.1",
]

statuses = [
    "Open",
    # "Accepted",
    # "In Progress",
    # "Resolved",
    # "In Review",
    # "Closed",
    # "Reopened",
]

nested_fields = [
    "assignee",
    # "attachment",  # AttributeError: 'PropertyHolder' object has no attribute
    # "comment",  # AttributeError: 'PropertyHolder' object has no attribute
    "components",  # object JIRA Component
    "created",
    "creator",
    "description",
    "duedate",
    "environment",
    "fixVersions",
    "issuelinks",
    "issuetype",
    "labels",
    "lastViewed",
    "priority",
    "project",
    "reporter",
    "resolution",
    "resolutiondate",
    "status",
    "subtasks",
    "summary",
    "updated",
    "versions",  # object JIRA Version
    # "votes",
    # "watches",
    # "workratio",
    "customfield_10000",
]

custom_fields = {
    "customfield_10000": "my_custom_field",
    "customfield_11111": "my_other_custom_field",
}

status_string = ", ".join(map(lambda x: '"' + x + '"', statuses))
affected_versions_string = ", ".join(map(lambda x: '"' + x + '"', affected_versions))

JQL = (
    f"project = {project} "
    f"AND status in ({status_string}) "
    f"AND affectedVersion in ({affected_versions_string}) "
    f"ORDER BY key ASC"
)

issues = jira.search_issues(JQL)
response = []

for found_issue in issues:

    issue_dict = {}

    for field in ["id", "key"]:
        value = found_issue.__getattr__(field)
        issue_dict[field] = value

    for nested_field in nested_fields:
        try:
            value = found_issue.fields.__getattribute__(nested_field)
            if value:
                # if value is dict and value.__len__ == 0:
                #     next
                # print(type(value).__name__, file=sys.stderr)
                value = str(value)
                value = json.dumps(value, indent=2, sort_keys=True)
                # Remove characters
                value = value.replace('"', "").replace("\\", "")
                if value:
                    issue_dict[nested_field] = value
        except TypeError as e:
            print("{}: {}".format(type(e).__name__, str(e)), file=sys.stderr)
            pass

    # Rename custom fields in dict
    for key in custom_fields.keys():
        if key in issue_dict.keys():
            issue_dict[custom_fields[key]] = issue_dict.pop(key)

    response.append(issue_dict)

print(json.dumps(response, indent=2, sort_keys=True))
