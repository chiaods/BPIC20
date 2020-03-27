import re
import constants
from pm4py.algo.filtering.log.attributes import attributes_filter
from pm4py.util import constants as xes_constants
from pm4py.objects.conversion.log import factory as log_conv_factory


def verify_resource(log):
    stream = log_conv_factory.apply(log, variant=log_conv_factory.TO_EVENT_STREAM)
    for event in stream:
        if 'by' in event[constants.concept_key] and \
                event[constants.concept_key].split('by')[-1].strip() != event[constants.res_key]:
            print('Resource info. inconsistent.')
            return False
    else:
        return True

def is_caseid_conceptname(stream):
    for event in stream:
        if event['case:id'] != event['case:'+constants.concept_key]:
            return False
    else:
        return True

def longest_substring_by_type(str):
    letter = max(re.findall(r'\D+', str), key=len)
    digit = max(re.findall(r'\d+', str), key=len)
    return letter, digit


def print_filtered_cases_count(original_len, filtered_len):
    print(original_len-filtered_len, end=' ')
    print('cases are filtered.')


def is_same_event(event1, event2):
    event1_keys = set([key for key in event1.keys() if 'case' not in key])
    event2_keys = set([key for key in event2.keys() if 'case' not in key])
    if event1_keys != event2_keys:
        return False
    else:
        for key in event1_keys:
            if key not in event2.keys() or event1[key] != event2[key]:
                return False
        else:
            return True


def is_same_event(event1, event2):
    event1_keys = set([key for key in event1.keys() if 'case' not in key and 'log' not in key])
    event2_keys = set([key for key in event2.keys() if 'case' not in key and 'log' not in key])
    if event1_keys != event2_keys:
        return False
    else:
        for key in event1_keys:
            if key not in event2.keys() or event1[key] != event2[key]:
                return False
        else:
            return True


def is_unique_event_attr(stream, attr):
    return len(stream) == len(set([event[attr] for event in stream]))

def differnt_case_attributes(event1, event2):
    case_attributes = set()
    case1_keys = [key for key in event1.keys() if 'case' in key and constants.concept_key not in key and 'log' not in key]
    case2_keys = [key for key in event2.keys() if 'case' in key and constants.concept_key not in key and 'log' not in key]
    mutual_keys = set(case1_keys).intersection(case2_keys)
    for key in mutual_keys:
        if event1[key] != event2[key]:
            case_attributes.add(key)
    return case_attributes


def verify_unique_event_across_processes(log_names, streams):

    events_dict = dict()
    for stream in streams:
        for event in stream:
            if event['id'] not in events_dict.keys():
                events_dict[event['id']] = []
            events_dict[event['id']].append(event)

    diff_case_attributes = dict()
    for key, events in events_dict.items():
        for i in range(1, len(events)):
            if not is_same_event(events[0], events[i]):
                print('Not the same event.')
                return False
            else:
                case_attributes = differnt_case_attributes(events[0], events[i])
                for attr in case_attributes:
                    if attr not in diff_case_attributes.keys():
                        diff_case_attributes[attr] = set()
                    diff_case_attributes[attr].add(log_names[events[0]['log']])
                    diff_case_attributes[attr].add(log_names[events[1]['log']])

    for key, values in diff_case_attributes.items():
        print(key, end=' ')
        print('has different values in logs ', end ='')
        for log in values:
            print(log, end=' ')
        print('')

