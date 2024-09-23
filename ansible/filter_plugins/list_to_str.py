#!/usr/bin/python3
import re

def convert_list_to_string(source_list, seperator="\n"):
    return seperator.join(source_list)

class FilterModule(object):
    filter_map = {
        'list_to_string': convert_list_to_string,
    }
    def filters(self):
        return self.filter_map

# Test
#check_for =  ['^ip access-list extended test', '^\\spermit ip host 192\\.0\\.2\\.1 any log', '^\\spermit ip host 192\\.0\\.2\\.2 any log']
#full_str = convert_list_to_string(check_for)
#print(full_str)
