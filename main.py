from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.log.exporter.xes import factory as xes_exporter
from pm4py.objects.log.exporter.csv import factory as csv_exporter
import Exploration as explorer
import Preprocess as util
import constants
from datetime import datetime, timedelta, timezone

analysis_path = 'C://Users//li//Desktop//WorkPlace//Research//BPIC20//Dataset//'
dataset_path = 'C://Users//li//Desktop//WorkPlace//Dataset//BPIC20_TripAdmin//'
file_names = ['DomesticDeclarations', 'InternationalDeclarations', 'PermitLog', 'PrepaidTravelCost',
              'RequestForPayment']
idx_dataset = 2
#
# """
# Preprocess:
# filter cases start before 2018
# filter ongoing cases by existence of Payment Handled
# decode the event concept name into stage, action, and decision
# """
#
log_origin = xes_importer.apply(dataset_path + 'Original//' + file_names[idx_dataset] + '.xes')
# log_complete = util.filter_open_cases(log_origin)
# log_from2018 = util.filter_cases_before_2018(log_complete)
#
selection = {constants.concept_key: ['Start trip', 'End trip'],
             constants.time_key: [datetime(2018,4,10,0,0, tzinfo=timezone(timedelta(seconds=3600*2))),
                                  datetime(2018,4,13,0,0, tzinfo=timezone(timedelta(seconds=3600*2)))]}
log = util.filter_abnormal_cases(log_origin, selection)
# print(len(log))
util.decode_event_concept(log)
#
# """
# Rename event concept name for analysis
# """
util.convert_event_attr_to_concept(log, ['stage', 'action'])
xes_exporter.apply(log, analysis_path+file_names[idx_dataset]+'_stageAction.xes')
#
#
#
# from pm4py.objects.log.util import sampling
# sampled_log = sampling.sample(log_origin, n=50)
# csv_exporter.apply(sampled_log, analAysis_path+file_names[1]+'.csv')



