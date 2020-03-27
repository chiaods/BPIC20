from pm4py.objects.conversion.log import factory as log_conv_factory
from pm4py.objects.log.log import EventLog
import constants
from pm4py.util import constants as xes_constants
from pm4py.algo.filtering.log.attributes import attributes_filter
import copy
import Exploration as util


def filter_cases_before_2018(log):
    log_filtered = EventLog([case for case in log if case[0]['time:timestamp'].year >= 2018])
    util.print_filtered_cases_count(len(log), len(log_filtered))
    return log_filtered


def filter_open_cases(log):
    log_selected = attributes_filter.apply(log, ["Payment Handled"],
                                           parameters={xes_constants.PARAMETER_CONSTANT_ATTRIBUTE_KEY: constants.concept_key,
                                                       "positive": True})
    util.print_filtered_cases_count(len(log), len(log_selected))
    return log_selected


def filter_abnormal_cases(log, criteria):
    # Shift+Alt+Insert to disable multi caret
    tofilter_log = copy.deepcopy(log)
    for key, values in criteria.items():
        for value in values:
            tofilter_log = attributes_filter.apply(tofilter_log, [value],
                                                   parameters={xes_constants.PARAMETER_CONSTANT_ATTRIBUTE_KEY: key,
                                                   "positive": True})
    tofilter_cases = [case.attributes[constants.concept_key] for case in tofilter_log]
    log_filtered = EventLog([case for case in log if case.attributes[constants.concept_key] not in tofilter_cases])
    util.print_filtered_cases_count(len(log), len(log)-len(tofilter_log))
    return log_filtered


def determine_stage(words):
    stages = ['declaration', 'permit', 'request', 'trip']
    for word in words:
        if word.lower() in stages:
            return stages[stages.index(word.lower())]
    else:
        return ' '.join(words)


def determine_action(words):
    for word in words:
        if word.isupper():
            return word
    else:
        return ' '.join(words)


def determine_decision(words):
    for word in words:
        if word.isupper():
            if 'REJECTED' in word:
                return 'rejection'
            elif 'APPROVED' in word:
                return 'approval'


def decode_event_concept(log):
    stages = ['declaration', 'permit', 'request', 'trip']
    stream = log_conv_factory.apply(log, variant=log_conv_factory.TO_EVENT_STREAM)
    for event in stream:
        words = event[constants.concept_key].split('by')[0].strip().split(' ')
        event['stage'] = determine_stage(words)
        event['decision'] = determine_decision(words) if event['stage'] in stages else None
        event['action'] = determine_action(words)


def convert_event_attr_to_concept(log, attr_keys):
    stream = log_conv_factory.apply(log, variant=log_conv_factory.TO_EVENT_STREAM)
    for event in stream:
        values = [event[key] for key in attr_keys]
        event[constants.concept_key] = '+'.join(values)


