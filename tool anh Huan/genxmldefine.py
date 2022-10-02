#==========================================
# Title:  define file
# Author: Nguyen Vu Huan  -  NHY2HC 
# Date:   7 Jan 2019
#==========================================

from xml.etree.ElementTree import Element, SubElement, Comment, tostring, fromstring, ElementTree
from xml.dom import minidom
import re
import os
import win32api
import subprocess
import Function1
import logging
import time
from threading import Lock
log_handle = logging.getLogger('ToolHuan')
class ProgressValue(object):
    def __init__(self):
        self.value = 0
        self.mutex = Lock()

    def setValue(self, value_in):
        self.mutex.acquire(True)
        self.value = value_in
        self.mutex.release()

    def getValue(self):
        self.mutex.acquire(True)
        temp = self.value
        self.mutex.release()
        return temp



from threading import Condition
class ProgressValue_1(object):
    def __init__(self):
        self.value = 0
        self.condition_variable = Condition()

    def setValue(self, value_in):
        self.condition_variable.acquire(True)
        self.value = value_in
        self.condition_variable.release()
        self.condition_variable.notify_all()

    def getValue(self):
        self.condition_variable.wait()
        self.condition_variable.acquire(False)
        temp = self.value
        self.condition_variable.release()
        return temp

ProgressValue_obj = ProgressValue()
ProgressValue_obj_2 = ProgressValue()
ProgressValue_obj_xml = ProgressValue()
#define keyword
myglobal = 0
cycletimeReg = 'cycletime'
dlc_okReg = 'dlc_ok'

WaitForAlltxMessage_Req = 'WaitForAlltxMessage'
WaitForNoAlltxMessage_Req = 'WaitForNoAlltxMessage'
envvarReg = 'envvar\((.+)\)'


CalculatePVCForMessageReq = 'CalculatePVCForMessage\((.*)[ ]*,[ ]*(.*)[ ]*\)'

RequestResponseReg = 'RequestResponse\((.*)[ ]*,[ ]*(.*)[ ]*,[ ]*(.*)\)'
RequestResponse_SPRB_Req ='RequestResponse_SPRB\((.*)[ ]* [ ]*(.*)[ ]* [ ]*(.*)\)'
FunctionalMessageReg = 'FunctionalMessage\((.*)[ ]*,[ ]*(.*)[ ]*,[ ]*(.*)\)'

RequestResponseCanMsgIdReg = 'RequestResponseCanMsgId\([ ]*(.*),[ ]*(.*),[ ]*(.*),[ ]*(.*),[ ]*(.*)[ ]*\)'


setenv_CRC_BZ_Req = r'(setenv_CRC_BZ)\s*\(\s*(.+)\)'   #setenv_CRC_BZ(string  E_pubc_GW_GW_1CB_IBCU_RollingCounter_1CB_wrongvalctr, int  -1, int  0)
Check_Eventmessage_failure_Req = r'(Check_Eventmessage_failure)\s*\(\s*(.+)\)' #Check_Eventmessage_failure(string MsgEnvVar E_pric_RadarFrontCenter_RDR1Header_tx, int Nrofevents 4)
waitReg = 'wait\s*\(([0-9]+)\)'

CalcCRCReg = 'CalcCRC[ ]?\((.+),[ ]?\'(.+)\',[ ]?([0-9]+)\)'
CRCReg =  'CRC[ ]?\((.+),[ ]?([0-9]+)\)'
DiagSessionCtrlReg = 'DiagSessionCtrl[ ]?\((.+)\)'
normalTestcaseReg = '^[ ]?[0-9]+[ ]?\) +(.*)'
SetVoltageReg = '[sS]et_?[vV]oltage\((.*)\)'

SetSpeedReg = '[sS]et[sS]peed\((.+)[ ]*,[ ]*(.+)\)'

loginReg = '[lL]ogin[ ]?\((.+)\)'
Measurement_value_test_Reg = '[mM]easurement_value_test[ ]?\((.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+)\)'  # exactly 8 parameter
Adaption_value_test_Reg = '[aA]daption_value_test[ ]?\((.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+)[ ]?\)'  # 9 parameter
SaveSignalValue_Req = 'SaveSignalValue[ ]?\([ ]?(.+)\)'
RestoreSignalValue_Req = 'RestoreSignalValue[ ]?\([ ]?(.+)\)'

DTC_check_Timeout_Req = 'DTC_check_Timeout[ ]?\([ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+)\)'  # message name, envvar name of cyclic tx switch, DTC_number, qualification time, healing time, priority
DTC_check_DLC_Req = 'DTC_check_DLC[ ]?\([ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+)\)'  # message name, envvar name of'Enable for wrong DLC' checkbox, envvar name of wrong DLC number, DTC_number, qualification time, healing time, priority
DTC_check_CRC_Req = 'DTC_check_CRC[ ]?\([ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+)\)'  # message name, envvar name of CRC field, DTC_number, multiplier for qualification time, multiplier for healing time, priority
DTC_check_BZ_Req = 'DTC_check_BZ[ ]?\([ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+)\)'  # message name, envvar name of BZ field, DTC_number, multiplier for qualification time, multiplier for healing time, priority
DTC_check_Signal_Req = 'DTC_check_Signal[ ]?\([ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+)\)'  # message name, envvar name of signal field, value of signal, DTC_number, qualification time, healing time, priority
# DTC_check_Timeout_Msg_handle_Req = 'DTC_check_Timeout_Msg_handle[ ]?\(' # message name(max ql), number of message, msgTM, DTC_number, qualification time, healing time, priority
DTC_check_Timeout_Msg_handle_Req = 'DTC_check_Timeout_Msg_handle[ ]?\([ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+)\)'  # message name, message ON, Message off, DTC_number, qualification time, healing time, priority
DTC_check_Timeout_Monitoring_Global_Timeout_Req = 'DTC_check_Timeout_Monitoring_Global_Timeout[ ]?\([ ]?(.+),[ ]?(.+),[ ]?(.+)\)'  # envvar name of cyclic tx switch, DTC_number, qualification time
Timeout_Monitoring_Start_Req = 'Timeout_Monitoring_Start[ ]?\([ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+)\)'  # envvar name of cyclic tx switch, DTC_number, qualification time, PreconditionType (KL15/0V/7V/18V), Retriggering
Signal_Monitoring_Start_Req = 'Signal_Monitoring_Start[ ]?\([ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+)\)'  # envvar name of signal field, value of signal, DTC_number, qualification time, PreconditionType (KL15/0V/7V/18V), Retriggering
Timeout_Monitoring_Start_BusOff_Req = 'Timeout_Monitoring_Start_BusOff[ ]?\([ ]?(.+),[ ]?(.+),[ ]?(.+)\)'  # envvar name of cyclic tx switch, DTC_number, qualification time,

FID_Test_Timeout_Req = 'FID_Test_Timeout[ ]?\([ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+)\)'  # message name, envvar name of cyclic tx switch, DTC_number, qualification time, Mapped FIDs, Safety relevant failure
FID_Test_DLC_Req = 'FID_Test_DLC[ ]?\([ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+)\)'  # message name, envvar name of'Enable for wrong DLC' checkbox, envvar name of wrong DLC number, DTC_number, qualification time, Mapped FIDs, Safety relevant failure
FID_Test_CRC_Req = 'FID_Test_CRC[ ]?\([ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+)\)'  # message name, envvar name of CRC field, DTC_number, multiplier for qualification time, Mapped FIDs, Safety relevant failure
FID_Test_BZ_Req = 'FID_Test_BZ[ ]?\([ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+)\)'  # message name, envvar name of BZ field, DTC_number, multiplier for qualification time, Mapped FIDs, Safety relevant failure
FID_Test_Signal_Req = 'FID_Test_Signal[ ]?\([ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+)\)'  # message name, envvar name of signal field, value of signal, DTC_number, qualification time, Mapped FIDs, Safety relevant failure
DTC_Check_FID_Req = 'DTC_Check_FID[ ]?\([ ]?(.+)\)'  # FID String

safeStateCheck_Req = 'safeStateCheck'
SearchPDM_Req = 'SearchPDM[ ]?\([ ]?(.+),[ ]?(.+),[ ]?(.+)\)'  # PDM ID, PDM Length, DTC number
CheckPdmContent_Req = 'CheckPdmContent[ ]?\([ ]?(.+),[ ]?(.+)\)'  # Expected data, Start byte of expected data
Repeat_ignition_cycles_10_Req = "ignition_cycles_10"
Repeat_ignition_cycles_9_Req = "ignition_cycles_9"

WriteCoding_Req = 'WriteCoding[ ]?\([ ]?(.+)\)'  # coding value



MeasureEntryTime_Req = 'MeasureEntryTime[ ]?\([ ]?(.+), [ ]?(.+)\)'  # DTC number. quantity of'n'
MeasuringQualificationTime_Req = 'MeasuringQualificationTime[ ]?\([ ]?(.+), [ ]?(.+)\)'  # DTC number. qualification time
Cycletime_and_DLC_Req = 'Cycletime_and_DLC[ ]?\([ ]?(.+), [ ]?(.+)\)'  # Message name, CAN channel
Repeat_Req = 'Repeat[ ]?\([ ]?(.+),[ ]?(.+),[ ]?(.+)\)'  # envvar name, DTC_number, sum of iterations
DTC_check_CRC_Event_Req = "DTC_check_CRC_Event[ ]?\([ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+)\)" #message name, send msg, envvar name of CRC field, DTC_number, qualification_ev, healing_ev, priority
DTC_check_BZ_Event_Req =  "DTC_check_BZ_Event[ ]?\([ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+)\)" #message name,  send msg, envvar name of BZ field, DTC_number, qualification_ev, healing_ev,priority
DTC_check_invalid_signal_Event_Req =  "DTC_check_invalid_signal_Event[ ]?\([ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+)\)" # //message name, send msg,envvar name of signal field, value of signal, DTC_number, qualification_ev , qualification_ev , priority
DTC_check_DLC_Event_Req = 'DTC_check_DLC_Event[ ]?\([ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+)\)'  # message name ,send msg,envvar name of'Enable for wrong DLC' checkbox envvar name of wrong DLC number, DTC_number, qualification_ev, qualification_ev, priority
# For CAN_TP:
SendDiagFrame_Req = 'SendDiagFrame\((.*)[ ]*,[ ]*(.*)[ ]*,[ ]*(.*)[ ]*,[ ]*(.*)\)'    #SendDiagFrame(messageID,DLC,frame,deltaT)
SetUseFC_Req = 'SetUseFC\((.*)[ ]*\)'   #SetUseFC(value)
Check_Diagnosis_Trace_Req = 'Check_Diagnosis_Trace\(\)'  #Check_Diagnosis_Trace()
StartPerformanceTest_Req = 'StartPerformanceTest\(\)'   #StartPerformanceTest()
StartTimeoutTest_Req = 'StartTimeoutTest\((.*)[ ]*\)'   #StartTimeoutTest(timeoutpar)
#  test new template qualification time and healing time:
DTC_check_Timeout_NTem_Req = 'DTC_check_Timeout_NTem[ ]?\([ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+)\)'  # message name, envvar name of cyclic tx switch, DTC_number, qualification time, healing time, priority, monitoring task
DTC_check_DLC_NTem_Req = 'DTC_check_DLC_NTem[ ]?\([ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+)\)'  # message name, envvar name of'Enable for wrong DLC' checkbox, envvar name of wrong DLC number, DTC_number, qualification time, healing time, priority, cycle message
DTC_check_CRC_NTem_Req = 'DTC_check_CRC_NTem[ ]?\([ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+)\)'  # message name, envvar name of CRC field, DTC_number, multiplier for qualification time, multiplier for healing time, priority, cycle message
DTC_check_BZ_NTem_Req = 'DTC_check_BZ_NTem[ ]?\([ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+)\)'  # message name, envvar name of BZ field, DTC_number, multiplier for qualification time, multiplier for healing time, priority, cycle message
DTC_check_Signal_NTem_Req = 'DTC_check_Signal_NTem[ ]?\([ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+)\)'  # message name, envvar name of signal field, value of signal, DTC_number, qualification time, healing time, priority, cycle message
write_variant_ntime_Req = 'write_variant_ntime[ ]?\([ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+)\)'  #request, response, type, time


# message name, envvar name of'Enable for wrong DLC' checkbox, envvar name of wrong DLC number, DTC_number, qualification counter, healing counter, priority, Fault level, evar name of turn off message, , message transmit
DTC_check_DLC_EventCount_Req = 'DTC_check_DLC_EventCount[ ]?\([ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+)\)'

# message name, envvar name of CRC field, DTC_number, qualification counter, healing counter, priority, Fault level, evar name of turn off message, message transmit
DTC_check_CRC_EventCount_Req = 'DTC_check_CRC_EventCount[ ]?\([ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+)\)'

# message name, envvar name of BZ field, DTC_number, qualification counter, healing counter, priority, Fault level, evar name of turn off message, message transmit
DTC_check_BZ_EventCount_Req = 'DTC_check_BZ_EventCount[ ]?\([ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+)\)'

# message name, envvar name of signal field, value of signal, DTC_number, qualification counter, healing counter, priority, Fault level, evar name of turn off message, message transmit
DTC_check_Signal_EventCount_Req = 'DTC_check_Signal_EventCount[ ]?\([ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+),[ ]?(.+)\)'

#update function keyword:

# for specific case
Checking_Configuration_Req = 'Checking_Configuration\((.*)[ ]*,[ ]*(.*)[ ]*,[ ]*(.*)[ ]*,[ ]*(.*)\)'    #SendDiagFrame(messageID,DLC,frame,deltaT)
# tatecheck([message], [signal], [channel], [node], [value])
# e.g. statecheck(Camera_Display_Status, HhBmCntSta, E_can, CSM, 0)
statecheck_Reg =  'statecheck[ ]*\([ ]*([^ ]*?)[ ]*,[ ]*([^ ]*?)[ ]*,[ ]*([^ ]*?)[ ]*,[ ]*([^ ]*?)[ ]*,[ ]*([^ ]*?)[ ]*\)'
AvoidSignalValue_Req =  r'(AvoidSignalValue)\s*\(\s*(.+)\)'
# WaitForSignalValue_Req = r'(WaitForSignalValue)\s?\(\s?(.+)\)'
WaitForSignalValue_Req = r'(WaitForSignalValue)\s*\(\s*([\w\s,]+)\)'
DeactivateFunction_Req = r'(DeactivateFunction)\s*\(\s*(.+)\)'
ActivateFunction_Req = r'(ActivateFunction)\s*\(\s*(.+)\)'
TesterConfirm_Req = r'(TesterConfirm)\s*\(\s*(.+)\)'
TimeNowStart_Req = 'TimeNowStart'
TimeNowEnd_Req = 'TimeNowEnd[ ]?\([ ]?(.+), [ ]?(.+)\)'  # min time, max time
CheckSignalValueIsPermanentStart_Req = r'(CheckSignalValueIsPermanentStart)\s*\(\s*(.+)\)'
CheckSignalValueIsPermanentStop_Req = r'(CheckSignalValueIsPermanentStop)\s*\(\s*(.+)\)'
startVideo_Req = r'(startVideo)\(\s*(.+)\)'
stopVideo_Req = r'(stopVideo)\s*\(\s*(.*)\)'
WaitForSignalValueOutsideRange_Req = r'(WaitForSignalValueOutsideRange)\s*\(\s*(.+)\)'
CheckSignalValueIsNotTaken_START_Req = r'(CheckSignalValueIsNotTaken_START)\s*\(\s*(.+)\)'
CheckSignalValueIsNotTaken_STOP_Req  = r'(CheckSignalValueIsNotTaken_STOP)\s*\(\s*(.+)\)'
StartLoggingCANtrace_Req = r'(StartLoggingCANtrace)\s*\(\s*(.+)\)'
StopLoggingCANtrace_Req = r'(StopLoggingCANtrace)\s*\(\s*(.+)\)'
SendMsg_Req = r'(SendMsg)\s*\(\s*(.+)\)'
class hierarchy_check():
    element =0;
    parent = 0
class hierarchy():
    def __init__(self):
        self.contains = list()
        self.fullName  = list()
        self.parent = list()
        self.id = 0
        self.rank = 0


class object_heading():
    def __init__(self):
        self.hierarchy = 0
        self.ID = list()
        self.prefix = list()
        self.suffix = list()

class Step_by_step_keyw():
    def __init__(self):
        self.step_count = 0
        self.step_check = list()
        self.step_contain = list()

class Step_by_test_step():
    def __init__(self):
        self.step_count = 0
        self.step_check = list()
        self.step_contain = list()

class Step_by_test_response():
    def __init__(self):
        self.step_count = 0
        self.step_check = list()
        self.step_contain = list()

#**************************************** EM check****************************************
# ***************************Measuring method parameter define****************************
class Tiout_ms():
    def __init__(self):
        self.msname_p = 0
        self.envarcycl_p = 1
        self.dtcnum_p = 2
        self.qtime_p = 3
        self.htime_p = 4
        self.priority_p = 5

class Dlc_ms():
    def __init__(self):
        self.msname_p = 0
        self.envarset_p = 1
        self.envardlc_p = 2
        self.dtcnum_p = 3
        self.qtime_p = 4
        self.htime_p = 5
        self.priority_p = 6

class Crc_ms():
    def __init__(self):
        self.msname_p = 0
        self.envarcrc_p = 1
        self.dtcnum_p = 2
        self.qtime_p = 3
        self.htime_p = 4
        self.priority_p = 5

class Bz_ms():
    def __init__(self):
        self.msname_p = 0
        self.envarbz_p = 1
        self.dtcnum_p = 2
        self.qtime_p = 3
        self.htime_p = 4
        self.priority_p = 5

class Invalid_ms():
    def __init__(self):
        self.msname_p = 0
        self.envarsig_p = 1
        self.valueinv_p = 2
        self.dtcnum_p = 3
        self.qtime_p = 4
        self.htime_p = 5
        self.priority_p = 6

# ********************************events counter method parameter define:**************
class Dlc_ec():
    def __init__(self):
        self.msname_p = 0
        self.envarset_p = 1
        self.envardlc_p = 2
        self.mscycl = 3
        self.mstrs_p = 4
        self.dtcnum_p = 5
        self.Fup_p = 6
        self.Fdown_p = 7
        self.Flv_p = 8
        self.priority_p = 9

class Crc_ec():
    def __init__(self):
        self.msname_p = 0
        self.envarcrc_p = 1
        self.mscycl = 2
        self.mstrs_p = 3
        self.dtcnum_p = 4
        self.Fup_p = 5
        self.Fdown_p = 6
        self.Flv_p = 7
        self.priority_p = 8


class Bz_ec():
    def __init__(self):
        self.msname_p = 0
        self.envarbz_p = 1
        self.mscycl = 2
        self.mstrs_p = 3
        self.dtcnum_p = 4
        self.Fup_p = 5
        self.Fdown_p = 6
        self.Flv_p = 7
        self.priority_p = 8


class Invalid_ec():
    def __init__(self):
        self.msname_p = 0
        self.envarsig_p = 1
        self.mscycl = 2
        self.mstrs_p = 3
        self.dtcnum_p = 4
        self.Fup_p = 5
        self.Fdown_p = 6
        self.Flv_p = 7
        self.valueinv_p = 8
        self.priority_p = 9


def write_xml(t_data_w, t_step_by_step_keyw_arr, t_step_by_test_step_arr, t_step_by_test_response_arr, t_path_output, object_heading_arr,t_ECAN_main_node, t_SFCAN_main_node, t_measure_type, t_test_module,t_execute_option):
    # =======================================================
    # =========Create index of parameter=====================
    global t_progress
    t_progress = 0
    tiout_ms =  Tiout_ms()
    dlc_ms = Dlc_ms()
    crc_ms = Crc_ms()
    bz_ms = Bz_ms()
    invalid_ms = Invalid_ms()

    dlc_ec = Dlc_ec()
    crc_ec = Crc_ec()
    bz_ec = Bz_ec()
    invalid_ec = Invalid_ec()
    # =======================================================
    # Create the begining of XLM file
    testmodule = Element('testmodule', title= t_test_module, version="1.0")
    comment = Comment('Generated for PyMOTW')
    testmodule.append(comment)
    #RequestResponseReg = 'RequestResponse\((.*)[ ]*,[ ]*(.*)[ ]*,[ ]*(.*)\)'
    # =======================================================
    # Write XLM file
    # =======================================================
    # //aaa = re.findall(RequestResponseReg, t_step_by_step_keyw_arr[i].step_contain[2])
    # log_handle.info(aaa)
    main_cl = hierarchy()
    main_cl.fullName  =""
    temp_cl = main_cl
    lenght = len(main_cl.fullName )
    for i in range (1, t_data_w.end_row):
        if (object_heading_arr[i]):
            if (object_heading_arr[i].prefix) and (len(object_heading_arr[i].prefix[0]) > lenght):
                arr1 = hierarchy()
                arr1.fullName  = object_heading_arr[i].prefix
                arr1.parent = temp_cl
                arr1.id = i
                arr1.rank = len(object_heading_arr[i].prefix[0])
                temp_cl.contains.append(arr1)
                temp_cl = temp_cl.contains[len(temp_cl.contains) - 1]
                lenght = len(object_heading_arr[i].prefix[0])
            elif (object_heading_arr[i].prefix) and (len(object_heading_arr[i].prefix[0]) == lenght):
                arr2 = hierarchy()
                arr2.fullName = object_heading_arr[i].prefix
                arr2.parent = temp_cl.parent
                arr2.id = i
                arr2.rank = len(object_heading_arr[i].prefix[0])
                temp_cl.parent.contains.append(arr2)
                temp_cl = temp_cl.parent.contains[len(temp_cl.parent.contains) - 1]
            else:
                arr3 = hierarchy()
                arr3.fullName = object_heading_arr[i].prefix
                com = temp_cl.parent
                while len(object_heading_arr[i].prefix[0]) <= len(com.fullName[0]):
                    com = com.parent
                arr3.parent = com
                arr3.id = i
                arr3.rank = len(object_heading_arr[i].prefix[0])
                com.contains.append(arr3)
                temp_cl = com.contains[len(com.contains) - 1]
                lenght = len(arr3.fullName[0])



    arr_rank = [None] * 200
    hierarchy_check.element=0
    global ProgressValue_obj
    ProgressValue_obj.setValue(21)
    # for i in range (t_data_w.begin_ID, t_data_w.end_ID):
    def get_out_data(main_cl,t_data_w, t_step_by_step_keyw_arr, t_step_by_test_step_arr, t_step_by_test_response_arr, t_path_output, object_heading_arr,t_ECAN_main_node, t_SFCAN_main_node):
        i = main_cl.id
        global myglobal
        if t_data_w.object_type_arr[i]== "Test group" and myglobal == 0:
            myglobal = myglobal + 1
            variants = SubElement(testmodule, 'variants')
            variant = SubElement(variants, "variant", aka1_name="Automated")
            variant.text = (re.findall("[a-z].*", (t_data_w.Component_name_arr[i]), re.IGNORECASE))[0] + "Automated Testcase"
            arr_rank[main_cl.rank] = SubElement(testmodule, 'testgroup', title=(re.findall("[a-z].*", (t_data_w.Component_name_arr[i]), re.IGNORECASE))[0] + "Automated Testcase")
            # todo ---> ADD LINK DOOR
            externalref = SubElement(arr_rank[main_cl.rank], 'externalref', aka1_type="doors", aka2_owner="TAE - DOORS extension", aka3_title=t_data_w.TC_ID_arr[i])
        elif t_data_w.object_type_arr[i]== "Test group":
            arr_rank[main_cl.rank] = SubElement(arr_rank[main_cl.parent.rank], 'testgroup', title=(re.findall("[a-z].*", (t_data_w.Component_name_arr[i]), re.IGNORECASE))[0])
            # todo ---> ADD LINK DOOR
            externalref = SubElement(arr_rank[main_cl.rank], 'externalref', aka1_type="doors", aka2_owner="TAE - DOORS extension", aka3_title=t_data_w.TC_ID_arr[i])
        if (i>= t_data_w.begin_ID) and (i< t_data_w.end_ID):
            if (t_data_w.object_type_arr[i] == "Automated Testcase" and (t_data_w.test_status_arr[i]== "implemented" or t_data_w.test_status_arr[i]== "specified")):
                aka007 = (re.findall("[a-z].*$", (t_data_w.Component_name_arr[i]), re.IGNORECASE))[0]
                if arr_rank[main_cl.parent.rank] != None:
                    arr_rank[main_cl.rank] = SubElement(arr_rank[main_cl.parent.rank], 'testgroup', title=(re.findall("[a-z].*$", (t_data_w.Component_name_arr[i]), re.IGNORECASE))[0])
                elif arr_rank[main_cl.parent.rank-1] != None:
                    arr_rank[main_cl.rank] = SubElement(arr_rank[main_cl.parent.rank-1], 'testgroup', title=(re.findall("[a-z].*$", (t_data_w.Component_name_arr[i]), re.IGNORECASE))[0])
                elif arr_rank[main_cl.parent.rank-2] != None:
                    arr_rank[main_cl.rank] = SubElement(arr_rank[main_cl.parent.rank-2], 'testgroup', title=(re.findall("[a-z].*$", (t_data_w.Component_name_arr[i]), re.IGNORECASE))[0])
                else:
                    catch_error = "Please check the test hierarchy in row: " + str(i + 1) + "  Parent of that not have or should be add in to Test group object type"
                    win32api.MessageBox(0,catch_error , 'ERROR')
                # todo ---> ADD LINK DOOR
                externalref = SubElement(arr_rank[main_cl.rank], 'externalref', aka1_type="doors", aka2_owner="TAE - DOORS extension", aka3_title=t_data_w.TC_ID_arr[i])

                for j in range(0, len(t_step_by_step_keyw_arr[i].step_check)):
                    # log_handle.info(t_step_by_step_keyw_arr[i].step_contain[j])
                    # Request Response ===============================
                    MSG_NAME = ""
                    check_error = None
                    catch_error = None
                    # ===================================================================================================================
                    # ================================== For FUNCTION keyword ===========================================================
                    if (re.findall(statecheck_Reg, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(statecheck_Reg, t_step_by_step_keyw_arr[i].step_contain[j])
                        MSG_NAME = regex[0][0]
                        testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j], aka4_variants= "Automated")
                        Function.statecheck_f(testcase,regex,t_step_by_test_response_arr[i].step_contain[j])



                    if (re.findall(AvoidSignalValue_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(AvoidSignalValue_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        t_split = re.split (",\s+", regex[0][1]) #regex[0][1].split(",")
                        if (t_split==None):
                            check_error = 1
                            catch_error = "Generate may be error, Please check Test step keyword row: " + str(i + 1) + ", step " +  str(j + 1)
                            Function.checkerror_f(check_error,catch_error)
                        else:
                            try:
                                signalNames = re.findall("([\w\d]+)\s+([\w\d]+).*\(\s*(.+)\)", t_split[0])
                                # signalNames_split = re.split("\s+", signalNames[0][2])  # signalNames[0][2].split(" ")
                                signalNames_split = re.split("\s+;?\s*", signalNames[0][2])  # signalNames[0][2].split(" ")
                                # signalNames_split.remove(";")
                                signalValue = re.findall("([\w\d]+)\s+([\w\d]+)\s+([\w\d]+)", t_split[1])
                                timeout = re.findall("([\w\d]+)\s+([\w\d]+)\s+([\w\d]+)", t_split[2])
                                t_msg_name = MSG_NAME
                                temp_node = t_ECAN_main_node
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="AvoidSignalValue", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j], aka4_variants="Automated")
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name=signalNames[0][1], aka2_type=signalNames[0][0])
                                cansignal = SubElement(caplparam, 'cansignal', aka1_bus=signalNames_split[3], aka2_name=re.sub(";", "", signalNames_split[1]), aka3_msg=t_msg_name, aka4_node=temp_node)
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name=signalValue[0][1], aka2_type=signalValue[0][0])
                                caplparam.text = signalValue[0][2]
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name=timeout[0][1], aka2_type=timeout[0][0])
                                caplparam.text = timeout[0][2]
                            except:
                                log_handle.info("Error: please check parameter in test step keword AvoidSignalValue, row: " + str(i + 1) + ", step " +  str(j + 1))

                    if (re.findall(SendMsg_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(SendMsg_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        t_split = re.split (",\s+", regex[0][1]) #regex[0][1].split(",")
                        if (t_split==None):
                            check_error = 1
                            catch_error = "Generate may be error, Please check Test step keyword row: " + str(i + 1) + ", step " +  str(j + 1)
                            Function.checkerror_f(check_error,catch_error)
                        else:
                            try:
                                signalNames_split = re.split("\s+", t_split[0])  # signalNames[0][2].split(" ")
                                timout_split = re.split("\s+", t_split[1])
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="SendMsg", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j], aka4_variants="Automated")
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name=signalNames_split[1], aka2_type=signalNames_split[0])
                                caplparam.text = signalNames_split[2]
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name=timout_split[1], aka2_type=timout_split[0])
                                caplparam.text = timout_split[2]
                            except:
                                log_handle.info("Error: please check parameter in test step keword SendMsg, row: " + str(i + 1) + ", step " +  str(j + 1))

                    if (re.findall(WaitForSignalValue_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+","",t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(WaitForSignalValue_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        t_split = regex[0][1].split(",")
                        if (t_split == None):
                            check_error = 1
                            catch_error = "Generate may be error, Please check Test step keyword row: " + str(i + 1) + ", step " + str(j + 1)
                            Function.checkerror_f(check_error, catch_error)
                        else:
                            try:
                                t_msg_name = MSG_NAME
                                temp_node = t_ECAN_main_node
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase',aka1_name="WaitForSignalValue" ,aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j],aka3_ident="-",aka4_variants="Automated")
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name="signalName",aka2_type="signal")
                                cansignal = SubElement(caplparam, 'cansignal', aka1_name=t_split[0],aka2_bus=t_split[1])
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name="signalValue", aka2_type="float")
                                caplparam.text = t_split[2]
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Timeout", aka2_type="int")
                                caplparam.text = t_split[3]
                            except:
                                log_handle.info("Error: please check parameter in test step keword WaitForSignalValue, row: " + str(i + 1) + ", step " + str(j + 1))

                    if (re.findall(DeactivateFunction_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(DeactivateFunction_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        t_split = re.split("\s+",regex[0][1])#regex[0][1].split(" ")
                        if (t_split == None):
                            check_error = 1
                            catch_error = "Generate may be error, Please check Test step keyword row: " + str(i + 1) + ", step " + str(j + 1)
                            Function.checkerror_f(check_error, catch_error)
                        else:
                            try:
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name ="DeactivateFunction", aka2_title=str(j + 1)+"- " +  t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j], aka4_variants= "Automated")
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name=t_split[1], aka2_type=t_split[0])
                                caplparam.text= t_split[2]
                            except:
                                log_handle.info("Error: please check parameter in test step keword DeactivateFunction, row: " + str(i + 1) + ", step " + str(j + 1))

                    if (re.findall(ActivateFunction_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(ActivateFunction_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        t_split = re.split("\s+",regex[0][1])#regex[0][1].split(" ")
                        if (t_split == None):
                            check_error = 1
                            catch_error = "Generate may be error, Please check Test step keyword row: " + str(i + 1) + ", step " + str(j + 1)
                            Function.checkerror_f(check_error, catch_error)
                        else:
                            try:
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name ="ActivateFunction", aka2_title=str(j + 1)+"- " +  t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j], aka4_variants= "Automated")
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name=t_split[1], aka2_type=t_split[0])
                                caplparam.text= t_split[2]
                            except:
                                log_handle.info("Error: please check parameter in test step keword ActivateFunction, row: " + str(i + 1) + ", step " + str(j + 1))



                    if (re.findall(TesterConfirm_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(TesterConfirm_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title=str(j + 1)+"- " +  t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j], aka4_variants= "Automated")
                        testerconfirmation = SubElement(testcase, 'testerconfirmation', aka1_title=t_step_by_test_step_arr[i].step_contain[j], )
                        testerconfirmation.text=t_step_by_test_step_arr[i].step_contain[j]


                    if (re.findall(TimeNowStart_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(TimeNowStart_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name ="TimeNowStart", aka2_title=str(j + 1)+"- " +  t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j], aka4_variants= "Automated")

                    if (re.findall(TimeNowEnd_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(TimeNowEnd_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="TimeNowEnd", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j], aka4_variants="Automated")
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="aTime1", aka2_type="string")
                            caplparam.text = regex[0][0]
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="aTime2", aka2_type="string")
                            caplparam.text = regex[0][1]
                        except:
                            log_handle.info("Error: please check parameter in test step keword TimeNowEnd, row: " + str(i + 1) + ", step " + str(j + 1))

                    if (re.findall(Occurance_Counter_100_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(Occurance_Counter_100_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        if (regex == None):
                            check_error = 1
                            catch_error = "Generate may be error, Please check Test step keyword row: " + str(i + 1) + ", step " + str(j + 1)
                            Function.checkerror_f(check_error, catch_error)
                        else:
                            try:
                                t_split = re.split(",\s+", regex[0][1])
                                t_Variable = re.split("\s+", t_split[0])
                                t_Counter_Req =  re.split("\s+", t_split[1])
                                t_Counter_resp = re.split("\s+", t_split[2])
                                t_compareMod = re.split("\s+", t_split[3])
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="Occurance_Counter_100", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j], aka4_variants="Automated")
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name=t_Variable[1], aka2_type=t_Variable[0])
                                caplparam.text = t_Variable[2]
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name=t_Counter_Req[1], aka2_type=t_Counter_Req[0])
                                caplparam.text = t_Counter_Req[2]
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name=t_Counter_resp[1], aka2_type=t_Counter_resp[0])
                                caplparam.text = t_Counter_resp[2]
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name=t_compareMod[1], aka2_type=t_compareMod[0])
                                caplparam.text = t_compareMod[2]
                            except:
                                log_handle.info("Error: please check parameter in test step keword Occurance_Counter_100_Req, row: " + str(i + 1) + ", step " + str(j + 1))

                    if (re.findall(Occurance_Counter_50_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(Occurance_Counter_50_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        if (regex == None):
                            check_error = 1
                            catch_error = "Generate may be error, Please check Test step keyword row: " + str(i + 1) + ", step " + str(j + 1)
                            Function.checkerror_f(check_error, catch_error)
                        else:
                            try:
                                t_split = re.split(",\s+", regex[0][1])
                                t_Variable = re.split("\s+", t_split[0])
                                t_Counter_Req =  re.split("\s+", t_split[1])
                                t_Counter_resp = re.split("\s+", t_split[2])
                                t_compareMod = re.split("\s+", t_split[3])
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="Occurance_Counter_50", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j], aka4_variants="Automated")
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name=t_Variable[1], aka2_type=t_Variable[0])
                                caplparam.text = t_Variable[2]
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name=t_Counter_Req[1], aka2_type=t_Counter_Req[0])
                                caplparam.text = t_Counter_Req[2]
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name=t_Counter_resp[1], aka2_type=t_Counter_resp[0])
                                caplparam.text = t_Counter_resp[2]
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name=t_compareMod[1], aka2_type=t_compareMod[0])
                                caplparam.text = t_compareMod[2]
                            except:
                                log_handle.info("Error: please check parameter in test step keword Occurance_Counter_50_Req, row: " + str(i + 1) + ", step " + str(j + 1))

                    if (re.findall(Occurance_Counter_4_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(Occurance_Counter_4_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        if (regex == None):
                            check_error = 1
                            catch_error = "Generate may be error, Please check Test step keyword row: " + str(i + 1) + ", step " + str(j + 1)
                            Function.checkerror_f(check_error, catch_error)
                        else:
                            try:
                                t_split = re.split(",\s+", regex[0][1])
                                t_Variable = re.split("\s+", t_split[0])
                                t_Counter_Req =  re.split("\s+", t_split[1])
                                t_Counter_resp = re.split("\s+", t_split[2])
                                t_compareMod = re.split("\s+", t_split[3])
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="Occurance_Counter_4", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j], aka4_variants="Automated")
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name=t_Variable[1], aka2_type=t_Variable[0])
                                caplparam.text = t_Variable[2]
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name=t_Counter_Req[1], aka2_type=t_Counter_Req[0])
                                caplparam.text = t_Counter_Req[2]
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name=t_Counter_resp[1], aka2_type=t_Counter_resp[0])
                                caplparam.text = t_Counter_resp[2]
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name=t_compareMod[1], aka2_type=t_compareMod[0])
                                caplparam.text = t_compareMod[2]
                            except:
                                log_handle.info("Error: please check parameter in test step keword Occurance_Counter_4_Req, row: " + str(i + 1) + ", step " + str(j + 1))



                    if (re.findall(CheckSignalValueIsPermanentStart_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(CheckSignalValueIsPermanentStart_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        if (regex == None):
                            check_error = 1
                            catch_error = "Generate may be error, Please check Test step keyword row: " + str(i + 1) + ", step " + str(j + 1)
                            Function.checkerror_f(check_error, catch_error)
                        else:
                            try:
                                t_split = re.split(",\s+", regex[0][1])
                                t_signal = re.split("\s+", t_split[0])
                                t_value =  re.split("\s+", t_split[1])
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="CheckSignalValueIsPermanentStart", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j], aka4_variants="Automated")
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name=t_signal[1], aka2_type=t_signal[0])
                                caplparam.text = t_signal[2]
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name=t_value[1], aka2_type=t_value[0])
                                caplparam.text = t_value[2]
                            except:
                                log_handle.info("Error: please check parameter in test step keword CheckSignalValueIsPermanentStart, row: " + str(i + 1) + ", step " + str(j + 1))

                    if (re.findall(CheckSignalValueIsPermanentStop_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(CheckSignalValueIsPermanentStop_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        t_split = re.split("\s+", regex[0][1])
                        if (t_split == None):
                            check_error = 1
                            catch_error = "Generate may be error, Please check Test step keyword row: " + str(i + 1) + ", step " + str(j + 1)
                            Function.checkerror_f(check_error, catch_error)
                        else:
                            try:
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="CheckSignalValueIsPermanentStop", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j], aka4_variants="Automated")
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name=t_split[1], aka2_type=t_split[0])
                                caplparam.text = t_split[2]
                            except:
                                log_handle.info("Error: please check parameter in test step keword CheckSignalValueIsPermanentStop, row: " + str(i + 1) + ", step " + str(j + 1))


                    if (re.findall(startVideo_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(startVideo_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        t_split = re.split(",\s+", regex[0][1])
                        if (t_split == None):
                            check_error = 1
                            catch_error = "Generate may be error, Please check Test step keyword row: " + str(i + 1) + ", step " + str(j + 1)
                            Function.checkerror_f(check_error, catch_error)
                        else:
                            try:
                                t_link = re.split("\s+", t_split[0])
                                t_config1 = re.split("\s+", t_split[1])
                                t_config2 = re.split("\s+", t_split[2])
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="startVideo", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j], aka4_variants="Automated")
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name=t_link[1], aka2_type=t_link[0])
                                caplparam.text = re.sub(r"\\\\",r"\\",t_link[2])
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name=t_config1[1], aka2_type=t_config1[0])
                                caplparam.text = t_config1[2]
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name=t_config2[1], aka2_type=t_config2[0])
                                caplparam.text = t_config2[2]
                            except:
                                log_handle.info("Error: please check parameter in test step keword startVideo,  row: " + str(i + 1) + ", step " + str(j + 1))

                    if (re.findall(stopVideo_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(stopVideo_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="stopVideo", aka2_title=str(j + 1) + "- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident="-", aka4_variants="Automated")

                    if (re.findall(WaitForSignalValueOutsideRange_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(WaitForSignalValueOutsideRange_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        t_split = re.split(",\s+", regex[0][1])
                        if (t_split == None):
                            check_error = 1
                            catch_error = "Generate may be error, Please check Test step keyword row: " + str(i + 1) + ", step " + str(j + 1)
                            Function.checkerror_f(check_error, catch_error)
                        else:
                            try:
                                signalNames = re.findall("([\w\d]+)\s+([\w\d]+).*\(\s?(.+)\)", t_split[0])
                                signalNames_split = re.split("\s+", signalNames[0][2])  # signalNames[0][2].split(" ")
                                LowLimit = re.findall("([\w\d]+)\s+([\w\d]+)\s+([\w\d]+)", t_split[1])
                                HighLimit = re.findall("([\w\d]+)\s+([\w\d]+)\s+([\w\d]+)", t_split[2])
                                Timeout = re.findall("([\w\d]+)\s+([\w\d]+)\s+([\w\d]+)", t_split[3])

                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForSignalValueOutsideRange", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j], aka4_variants="Automated")
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name=signalNames[0][1], aka2_type=signalNames[0][0])
                                cansignal = SubElement(caplparam, 'cansignal', aka1_bus=signalNames_split[3], aka2_name=re.sub(";", "", signalNames_split[1]))
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name=LowLimit[0][1], aka2_type=LowLimit[0][0])
                                caplparam.text = LowLimit[0][2]
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name=HighLimit[0][1], aka2_type=HighLimit[0][0])
                                caplparam.text = HighLimit[0][2]
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name=Timeout[0][1], aka2_type=Timeout[0][0])
                                caplparam.text = Timeout[0][2]
                            except:
                                log_handle.info("Error: please check parameter in test step keword WaitForSignalValueOutsideRange, row: " + str(i + 1) + ", step " + str(j + 1))



                    if (re.findall(CheckSignalValueIsNotTaken_START_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(CheckSignalValueIsNotTaken_START_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        t_split = re.split(",\s+", regex[0][1])
                        if (t_split == None):
                            check_error = 1
                            catch_error = "Generate may be error, Please check Test step keyword row: " + str(i + 1) + ", step " + str(j + 1)
                            Function.checkerror_f(check_error, catch_error)
                        else:
                            try:
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="CheckSignalValueIsNotTaken_START", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j], aka4_variants="Automated")
                                for temp in  t_split:
                                    temp_split = re.split("\s+", temp)
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name=temp_split[1], aka2_type=temp_split[0])
                                    caplparam.text = temp_split[2]
                            except:
                                log_handle.info("Error: please check parameter in test step keword CheckSignalValueIsNotTaken_START, row: " + str(i + 1) + ", step " + str(j + 1))


                    if (re.findall(CheckSignalValueIsNotTaken_STOP_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(CheckSignalValueIsNotTaken_STOP_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        t_split = re.split(",\s+", regex[0][1])
                        if (t_split == None):
                            check_error = 1
                            catch_error = "Generate may be error, Please check Test step keyword row: " + str(i + 1) + ", step " + str(j + 1)
                            Function.checkerror_f(check_error, catch_error)
                        else:
                            try:
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="CheckSignalValueIsNotTaken_STOP", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j], aka4_variants="Automated")
                                for temp in  t_split:
                                    temp_split = re.split("\s+", temp)
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name=temp_split[1], aka2_type=temp_split[0])
                                    caplparam.text = temp_split[2]
                            except:
                                log_handle.info("Error: please check parameter in test step keword CheckSignalValueIsNotTaken_STOP, row: " + str(i + 1) + ", step " + str(j + 1))

                    if (re.findall(StartLoggingCANtrace_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(StartLoggingCANtrace_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        t_split = re.split(",\s+", regex[0][1])
                        if (t_split == None):
                            check_error = 1
                            catch_error = "Generate may be error, Please check Test step keyword row: " + str(i + 1) + ", step " + str(j + 1)
                            Function.checkerror_f(check_error, catch_error)
                        else:
                            try:
                                # t_link = re.split("\s+", t_split[0])
                                t_config1 = re.split("\s+", t_split[0])
                                t_config2 = re.split("\s+", t_split[1])
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="StartLoggingCANtrace", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j], aka4_variants="Automated")
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name=t_config1[1], aka2_type=t_config1[0])
                                caplparam.text = t_config1[2]
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name=t_config2[1], aka2_type=t_config2[0])
                                caplparam.text = t_config2[2]
                            except:
                                log_handle.info("Error: please check parameter in test step keword startVideo,  row: " + str(i + 1) + ", step " + str(j + 1))

                    if (re.findall(StopLoggingCANtrace_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(StopLoggingCANtrace_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        t_split = re.split("\s+", regex[0][1])
                        if (t_split == None):
                            check_error = 1
                            catch_error = "Generate may be error, Please check Test step keyword row: " + str(i + 1) + ", step " + str(j + 1)
                            Function.checkerror_f(check_error, catch_error)
                        else:
                            try:
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="StopLoggingCANtrace", aka2_title=str(j + 1) + "- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j], aka4_variants="Automated")
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name=t_split[1], aka2_type=t_split[0])
                                caplparam.text = t_split[2]
                            except:
                                log_handle.info("Error: please check parameter in test step keword startVideo,  row: " + str(i + 1) + ", step " + str(j + 1))

                    # =============================================================================================================================
                    # ============================================= For EM testing ==============================================================
                    # if (re.findall(CalculateCRCForMessageReg, t_step_by_step_keyw_arr[i].step_contain[j])):
                    #     t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                    #     regex = re.findall(CalculateCRCForMessageReg, t_step_by_step_keyw_arr[i].step_contain[j])
                    #     try:
                    #         capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="CalculateCRCForMessage", aka2_title=str(j + 1)+"- " + "CRC Testing", aka3_ident="CRC Testing")
                    #         caplparam = SubElement(capltestcase, 'caplparam', aka1_name="MessageName", aka2_type="string", )
                    #         caplparam.text = regex[0][0]
                    #         caplparam = SubElement(capltestcase, 'caplparam', aka1_name="NrOfExecution", aka2_type="int")
                    #         caplparam.text = regex[0][1]
                    #     except:
                    #         log_handle.info("Error: please check parameter in test step keword CalculateCRCForMessage, row: " + str(i + 1) + ", step " + str(j + 1))

                    if (re.findall(CalculatePVCForMessageReq, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(CalculatePVCForMessageReq, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="CalculatePVCForMessage", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j] , aka3_ident="PVC Testing")
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="MessageName", aka2_type="string", )
                            caplparam.text = regex[0][0]
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="NrOfExecution", aka2_type="int")
                            caplparam.text = regex[0][1]
                        except:
                            log_handle.info("Error: please check parameter in test step keword CalculatePVCForMessage, row: " + str(i + 1) + ", step " + str(j + 1))

                    elif (re.findall(cycletimeReg, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall('cycletime\((.*),[ ]*(.*),[ ]*(.*),[ ]*(.*)\)', t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka2_ident=t_step_by_test_response_arr[i].step_contain[j])
                            conditions = SubElement(testcase, 'conditions')
                            cycletime_rel = SubElement(conditions, 'cycletime_rel', aka1_min=regex[0][2], aka2_max=regex[0][3])
                            if (regex[0][1] == "E_can"):
                                temp_node = t_ECAN_main_node
                            elif (regex[0][1] == "SF_can"):
                                temp_node = t_SFCAN_main_node
                            else:
                                temp_node = ""
                            canmsg = SubElement(cycletime_rel, 'canmsg', aka1_id=regex[0][0], aka2_bus=regex[0][1], aka3_node=temp_node)
                            wait = SubElement(testcase, 'wait', aka1_time='3000', aka2_title='wait')
                        except:
                            log_handle.info("Error: please check parameter in test step keword cycletime, row: " + str(i + 1) + ", step " + str(j + 1))

                    #
                    elif (re.findall(dlc_okReg, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall('dlc_ok\((.*),[ ]*(.*)\)', t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka2_ident=t_step_by_test_response_arr[i].step_contain[j])
                            conditions = SubElement(testcase, 'conditions')
                            dlc_ok = SubElement(conditions, 'dlc_ok', aka1_title='Check DLC')
                            title = Function.msgName(object_heading_arr[i].suffix[0])
                            if (regex[0][1] == "E_can"):
                                temp_node = t_ECAN_main_node
                            elif (regex[0][1] == "SF_can"):
                                temp_node = t_SFCAN_main_node
                            else:
                                temp_node = ""
                            canmsg = SubElement(dlc_ok, 'canmsg', aka1_id=title, aka3_bus=regex[0][1], aka4_node=temp_node)
                            wait = SubElement(testcase, 'wait', aka1_time='3000', aka2_title='wait')
                        except:
                            log_handle.info("Error: please check parameter in test step keword dlc, row: " + str(i + 1) + ", step " + str(j + 1))
                    # todo -->  Not yet test
                    elif (re.findall(Cycletime_and_DLC_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall('cycletime\((.*),[ ]*(.*),[ ]*(.*),[ ]*(.*)\)', t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka2_ident=t_step_by_test_response_arr[i].step_contain[j])
                            conditions = SubElement(testcase, 'conditions')
                            cycletime_rel = SubElement(conditions, 'cycletime_rel', aka1_min='0.9', aka2_max='1.1')
                            canmsg = SubElement(cycletime_rel, 'canmsg', aka1_id=regex[0][0], aka2_bus=regex[0][1], aka3_node='MPC2')
                            wait = SubElement(testcase, 'wait', aka1_time='3000', aka2_time='wait')

                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title=t_step_by_test_step_arr[i].step_contain[j], aka2_ident=t_step_by_test_response_arr[i].step_contain[j])
                            conditions = SubElement(testcase, 'conditions')
                            dlc_ok = SubElement(conditions, 'dlc_ok', aka1_title='Check DLC')
                            # //-->todo implement objHeading
                            title = Function.msgName(object_heading_arr[i].suffix[0])
                            canmsg = SubElement(cycletime_rel, 'canmsg', aka1_id=title, aka3_bus="E_can", aka4_node='MPC2')
                            wait = SubElement(testcase, 'wait', aka1_time='3000', aka2_time='wait')
                        except:
                            log_handle.info("Error: please check parameter in test step keword Cycletime_and_DLC, row: " + str(i + 1) + ", step " + str(j + 1))

                    # elif (re.findall(CheckAliveCounterReg, t_step_by_step_keyw_arr[i].step_contain[j])):
                    #     t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                    #     regex = re.findall(CheckAliveCounterReg, t_step_by_step_keyw_arr[i].step_contain[j])
                    #     try:
                    #         capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="CheckAliveCounter", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                    #         caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CanName", aka2_type="string")
                    #         caplparam.text = regex[0][0]
                    #         caplparam = SubElement(capltestcase, 'caplparam', aka1_name="NodeName", aka2_type="string")
                    #         caplparam.text = regex[0][1]
                    #         caplparam = SubElement(capltestcase, 'caplparam', aka1_name="MessageName", aka2_type="string")
                    #         caplparam.text = regex[0][2]
                    #         caplparam = SubElement(capltestcase, 'caplparam', aka1_name="SignalName", aka2_type="string")
                    #         caplparam.text = regex[0][3]
                    #     except:
                    #         log_handle.info("Error: please check parameter in test step keword CheckAliveCounter, row: " + str(i + 1) + ", step " + str(j + 1))



                    # todo -->  Not yet test
                    elif (re.findall(Repeat_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(Repeat_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        na = int(regex[0][2])
                        wait_time = 0
                        for i in range(na):
                            # set CRC fault with setting the CRC field to -1
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title=str(j + 1)+"- " + "Set CRC error for message", aka3_ident='DTC 0x' + regex[0][2] + " is qualifying (0x01)")
                            set = SubElement(testcase, 'set', aka1_title=regex[0][1])
                            envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][1])
                            envvar.text = "-1"

                            # wait 150 ms
                            wait_time = 150
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 10 ms for PDM writing ", aka3_ident='-')
                            wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka1_title="wait")

                            # RequestResponse: DTC is active
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][1] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][1] + "09")
                            Function.clearDTC_f(capltestcase,regex[0][1],"09.*")

                            # wait 150 ms
                            wait_time = 150
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 10 ms for PDM writing ", aka3_ident='-')
                            wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka1_title="wait")

                            # RequestResponse: DTC is active
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][1] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][1] + "08")
                            Function.request_response_DTC_f(capltestcase,regex[0][1], ".{1}[0|8|e].*")
                    elif (re.findall(WaitForAlltxMessage_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(WaitForAlltxMessage_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForAlltxMessage", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                    elif (re.findall(WaitForNoAlltxMessage_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(WaitForNoAlltxMessage_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForNoAlltxMessage", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))

                    elif (re.findall(ignition_cycles_9_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(ignition_cycles_9_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="ignition_cycles_9", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                    elif (re.findall(ignition_cycles_10_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(ignition_cycles_10_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="ignition_cycles_10", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))

                    elif (re.findall(RequestResponseReg, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(RequestResponseReg, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                            Function.RequestResponseReg_f(capltestcase, regex)
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                    elif (re.findall(FunctionalMessageReg, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(FunctionalMessageReg, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="FunctionalMessage", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                            Function.FunctionalMessageReg_f(capltestcase, regex)
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))

                    elif (re.findall(FunctionalMessage_SPRB_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        # t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(FunctionalMessage_SPRB_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="FunctionalMessage_SPRB", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                            Function.FunctionalMessage_SPRB_f(capltestcase, regex)
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))

                    elif (re.findall(RequestResponse_SPRB_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        # t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(RequestResponse_SPRB_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse_SPRB", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                            Function.RequestResponse_SPRB_f(capltestcase, regex)
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                    elif (re.findall(SaveSignalValue_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(SaveSignalValue_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="SaveSignalValue",aka2_title=str(j + 1)+"- " + "Save Signal Value",aka3_ident="-")
                            Function.SaveSignalValueReq_f(capltestcase, regex)
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                    elif (re.findall(RestoreSignalValue_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(RestoreSignalValue_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RestoreSignalValue",aka2_title=str(j + 1)+"- " + "Set signal to default value",aka3_ident="-")
                            Function.RestoreSignalValueReq_f(capltestcase, regex)
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                    # envvar value with one or more parameter ========
                    elif (re.findall(envvarReg, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(envvarReg, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            keyword = regex[0]
                            function = '(.+),[ ]?(.+)'
                            param = '(.+)\((.*)\)'
                            envvarName = ''
                            envvarVariable = ''

                            xy = re.findall(function, regex[0])
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka2_ident=t_step_by_test_response_arr[i].step_contain[j])
                            while (keyword):
                                # todo --> This case is temporary and must be test later
                                if (re.findall(function, keyword)):
                                    temp_regex = re.findall(function, keyword)
                                    temp = temp_regex[0][0]
                                    keyword = temp_regex[0][1]
                                    temp = re.findall(param, temp)
                                    envvarName = temp[0][0]
                                    envvarVariable = temp[0][1]
                                elif (re.findall(param, keyword)):
                                    keyword = re.findall(param, keyword)
                                    envvarName = keyword[0][0]
                                    envvarVariable = keyword[0][1]
                                    keyword = None
                                else:
                                    keyword = None
                                    catch_error = r'Please check the envvar parameter ' + r", test step keyword column row : " + str(i + 1)
                                    win32api.MessageBox(0, catch_error, 'ERROR')

                                waitTimeRegexp = '(.+);[ ]?(.+)'
                                tempresult = None
                                if (re.findall(waitTimeRegexp, envvarVariable)):
                                    t_regex = re.findall(waitTimeRegexp, envvarVariable)
                                    set = SubElement(testcase, 'set', aka1_title=envvarName)
                                    envvar = SubElement(set, 'envvar', aka1_name=envvarName)
                                    envvar.text = t_regex[0][0]
                                    wait = SubElement(testcase, 'wait', aka1_time=t_regex[0][1], aka2_title='wait')
                                else:
                                    set = SubElement(testcase, 'set', aka1_title=envvarName)
                                    envvar = SubElement(set, 'envvar', aka1_name=envvarVariable)
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))

                    elif (re.findall(SetEnvVar_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(SetEnvVar_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        t_split = re.split(",\s*", regex[0][1])
                        if (t_split == None):
                            check_error = 1
                            catch_error = "Generate may be error, Please check Test step keyword row: " + str(i + 1) + ", step " + str(j + 1)
                            Function.checkerror_f(check_error, catch_error)
                        else:
                            try:
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="SetEnvVar", aka2_title=str(j + 1) + "- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j], aka4_variants="Automated")
                                for temp in t_split:
                                    temp_split = re.split("\s+", temp)
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name=temp_split[1], aka2_type=temp_split[0])
                                    caplparam.text = temp_split[2]
                            except:
                                log_handle.info("Error: please check parameter in test step keword SetEnvVar, row: " + str(i + 1) + ", step " + str(j + 1))

                    # elif (re.findall(ResetCameraReg, t_step_by_step_keyw_arr[i].step_contain[j])):
                    #     t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                    #     regex = re.findall(ResetCameraReg, t_step_by_step_keyw_arr[i].step_contain[j])
                    #     try:
                    #         capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="ResetCamera", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                    #         Function.ResetCameraReg_f(capltestcase, regex)
                    #     except:
                    #         log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                    # todo -->  Not yet test
                    elif (re.findall(RequestResponseCanMsgIdReg, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(RequestResponseCanMsgIdReg, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponseCanMsgId", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                            Function.RequestResponseCanMsgIdReg_f(capltestcase, regex)
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))

                    elif (re.findall(waitReg, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(waitReg, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka2_ident=t_step_by_test_response_arr[i].step_contain[j])
                            Function.waitReg_f(testcase, regex)
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                    elif (re.findall(Wait_Reg, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(Wait_Reg, t_step_by_step_keyw_arr[i].step_contain[j])
                        t_split = re.split(",\s+", regex[0][1])
                        if (t_split == None):
                            check_error = 1
                            catch_error = "Generate may be error, Please check Test step keyword row: " + str(i + 1) + ", step " + str(j + 1)
                            Function.checkerror_f(check_error, catch_error)
                        else:
                            try:
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="Wait", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                                for temp in t_split:
                                    temp_split = re.split("\s+", temp)
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name=temp_split[1], aka2_type=temp_split[0])
                                    caplparam.text = temp_split[2]
                            except:
                                log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))


                    elif (re.findall(ResetCamera_REQ, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(ResetCamera_REQ, t_step_by_step_keyw_arr[i].step_contain[j])
                        t_split = re.split(",\s+", regex[0][1])
                        if (t_split == None):
                            check_error = 1
                            catch_error = "Generate may be error, Please check Test step keyword row: " + str(i + 1) + ", step " + str(j + 1)
                            Function.checkerror_f(check_error, catch_error)
                        else:
                            try:
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="ResetCamera", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                                for temp in t_split:
                                    temp_split = re.split("\s+", temp)
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name=temp_split[1], aka2_type=temp_split[0])
                                    caplparam.text = temp_split[2]
                            except:
                                if (re.findall(ResetCameraReg, t_step_by_step_keyw_arr[i].step_contain[j])):
                                    t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                                    regex = re.findall(ResetCameraReg, t_step_by_step_keyw_arr[i].step_contain[j])
                                    try:
                                        # capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="ResetCamera", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                                        Function.ResetCameraReg_f(capltestcase, regex)
                                    except:
                                        log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                                else:
                                    log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))

                    elif (re.findall(SecurityunlockLevel1_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(SecurityunlockLevel1_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        t_split = re.split(",\s+", regex[0][1])
                        if (t_split == None):
                            check_error = 1
                            catch_error = "Generate may be error, Please check Test step keyword row: " + str(i + 1) + ", step " + str(j + 1)
                            Function.checkerror_f(check_error, catch_error)
                        else:
                            try:
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="SecurityunlockLevel1", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                                for temp in t_split:
                                    temp_split = re.split("\s+", temp)
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name=temp_split[1], aka2_type=temp_split[0])
                                    caplparam.text = temp_split[2]
                            except:
                                log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))

                    elif (re.findall(CheckMessageCycletime_REQ, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(CheckMessageCycletime_REQ, t_step_by_step_keyw_arr[i].step_contain[j])
                        t_split = re.split(",\s+", regex[0][1])
                        if (t_split == None):
                            check_error = 1
                            catch_error = "Generate may be error, Please check Test step keyword row: " + str(i + 1) + ", step " + str(j + 1)
                            Function.checkerror_f(check_error, catch_error)
                        else:
                            try:
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="CheckMessageCycletime", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                                for temp in t_split:
                                    temp_split = re.split("\s+", temp)
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name=temp_split[1], aka2_type=temp_split[0])
                                    caplparam.text = temp_split[2]
                            except:
                                log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))


                    elif (re.findall(CalculateCRCForMessage_REQ, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(CalculateCRCForMessage_REQ, t_step_by_step_keyw_arr[i].step_contain[j])
                        t_split = re.split(",\s+", regex[0][1])
                        if (t_split == None):
                            check_error = 1
                            catch_error = "Generate may be error, Please check Test step keyword row: " + str(i + 1) + ", step " + str(j + 1)
                            Function.checkerror_f(check_error, catch_error)
                        else:
                            try:
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="CalculateCRCForMessage", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                                for temp in t_split:
                                    temp_split = re.split("\s+", temp)
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name=temp_split[1], aka2_type=temp_split[0])
                                    caplparam.text = temp_split[2]
                            except:
                                if (re.findall(CalculateCRCForMessageReg, t_step_by_step_keyw_arr[i].step_contain[j])):
                                    t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                                    regex = re.findall(CalculateCRCForMessageReg, t_step_by_step_keyw_arr[i].step_contain[j])
                                    try:
                                        # capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="CalculateCRCForMessage", aka2_title=str(j + 1)+"- " + "CRC Testing", aka3_ident="CRC Testing")
                                        caplparam = SubElement(capltestcase, 'caplparam', aka1_name="MessageName", aka2_type="string", )
                                        caplparam.text = regex[0][0]
                                        caplparam = SubElement(capltestcase, 'caplparam', aka1_name="NrOfExecution", aka2_type="int")
                                        caplparam.text = regex[0][1]
                                    except:
                                        log_handle.info("Error: please check parameter in test step keword CalculateCRCForMessage, row: " + str(i + 1) + ", step " + str(j + 1))
                                else:
                                 log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))


                    elif (re.findall(CheckAliveCounter_REQ, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(CheckAliveCounter_REQ, t_step_by_step_keyw_arr[i].step_contain[j])
                        t_split = re.split(",\s+", regex[0][1])
                        if (t_split == None):
                            check_error = 1
                            catch_error = "Generate may be error, Please check Test step keyword row: " + str(i + 1) + ", step " + str(j + 1)
                            Function.checkerror_f(check_error, catch_error)
                        else:
                            try:
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="CheckAliveCounter", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                                for temp in t_split:
                                    temp_split = re.split("\s+", temp)
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name=temp_split[1], aka2_type=temp_split[0])
                                    caplparam.text = temp_split[2]
                            except:
                                if (re.findall(CheckAliveCounterReg, t_step_by_step_keyw_arr[i].step_contain[j])):
                                    t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                                    regex = re.findall(CheckAliveCounterReg, t_step_by_step_keyw_arr[i].step_contain[j])
                                    try:
                                        # capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="CheckAliveCounter", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                                        caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CanName", aka2_type="string")
                                        caplparam.text = regex[0][0]
                                        caplparam = SubElement(capltestcase, 'caplparam', aka1_name="NodeName", aka2_type="string")
                                        caplparam.text = regex[0][1]
                                        caplparam = SubElement(capltestcase, 'caplparam', aka1_name="MessageName", aka2_type="string")
                                        caplparam.text = regex[0][2]
                                        caplparam = SubElement(capltestcase, 'caplparam', aka1_name="SignalName", aka2_type="string")
                                        caplparam.text = regex[0][3]
                                    except:
                                        log_handle.info("Error: please check parameter in test step keword CheckAliveCounter, row: " + str(i + 1) + ", step " + str(j + 1))
                                else:
                                    log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                    elif (re.findall(CheckBlockCounter_REQ, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(CheckBlockCounter_REQ, t_step_by_step_keyw_arr[i].step_contain[j])
                        t_split = re.split(",\s+", regex[0][1])
                        if (t_split == None):
                            check_error = 1
                            catch_error = "Generate may be error, Please check Test step keyword row: " + str(i + 1) + ", step " + str(j + 1)
                            Function.checkerror_f(check_error, catch_error)
                        else:
                            try:
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="CheckBlockCounter", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                                for temp in t_split:
                                    temp_split = re.split("\s+", temp)
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name=temp_split[1], aka2_type=temp_split[0])
                                    caplparam.text = temp_split[2]
                            except:
                                log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))

                    elif (re.findall(CheckInitalSignalValue_REQ, t_step_by_step_keyw_arr[i].step_contain[j])):
                        regex = re.findall(CheckInitalSignalValue_REQ, t_step_by_step_keyw_arr[i].step_contain[j])
                        t_split = re.split(",\s+", regex[0][1])
                        if (t_split == None):
                            check_error = 1
                            catch_error = "Generate may be error, Please check Test step keyword row: " + str(i + 1) + ", step " + str(j + 1)
                            Function.checkerror_f(check_error, catch_error)
                        else:
                            try:
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="CheckInitalSignalValue", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                                for temp in t_split:
                                    temp_split = re.split("\s+", temp)
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name=temp_split[1], aka2_type=temp_split[0])
                                    caplparam.text = temp_split[2]
                            except:
                                if (re.findall(CheckInitalSignalValueReg, t_step_by_step_keyw_arr[i].step_contain[j])):
                                    t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                                    messageNameReg = '\((.+)\((.+)\)\)'
                                    ValueReg = '(.*),[ ]*(.+)[ ]?=[ ]?(.+)?'
                                    regex = re.findall(messageNameReg, t_step_by_step_keyw_arr[i].step_contain[j])
                                    try:
                                        messageName = regex[0][0]
                                        keyword = regex[0][1]
                                        ValuesName = [None] * 200
                                        ValuesInitialNumber = [None] * 200
                                        db = 0
                                        while (keyword):
                                            if (re.findall(ValueReg, keyword)):
                                                temp = re.findall(ValueReg, keyword)
                                                ValuesName[db] = temp[0][1]
                                                ValuesInitialNumber[db] = temp[0][2]
                                                db = db + 1
                                                keyword = temp[0][0]
                                            else:
                                                Value2Reg = '(.+)[ ]?=[ ]?(.+)'
                                                temp = re.findall(Value2Reg, keyword)
                                                ValuesName[db] = temp[0][0]
                                                ValuesInitialNumber[db] = temp[0][1]
                                                keyword = None
                                        # log_handle.info("Error: huanaka", t_step_by_test_response_arr[i].step_contain[j])
                                        # capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="CheckInitalSignalValue", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                                        caplparam = SubElement(capltestcase, 'caplparam', aka1_name="MessageName", aka2_type="string")
                                        caplparam.text = messageName
                                        temp = ''
                                        k = 0
                                        for k in range(db, 0, -1):
                                            temp = temp + str(ValuesName[k]) + ','
                                        temp = temp + str(ValuesName[0])
                                        caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Signals", aka2_type="string")
                                        caplparam.text = temp
                                        temp = ''
                                        for k in range(db, 0, -1):
                                            temp = temp + str(ValuesInitialNumber[k]) + ','
                                        temp = temp + str(ValuesInitialNumber[0])
                                        caplparam = SubElement(capltestcase, 'caplparam', aka1_name="ExpectedResults", aka2_type="string")
                                        caplparam.text = temp
                                    except:
                                        log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                                else:
                                    log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                    # todo -->  Not yet test
                    elif (re.findall(CalcCRCReg, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(CalcCRCReg, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="CalculateCRCForMessage", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                            Function.CalcCRCReg_f(capltestcase, regex)
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))

                    elif (re.findall(DiagSessionCtrlReg, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(DiagSessionCtrlReg, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="DiagSessionCtrl", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                            Function.DiagSessionCtrlReg_f(capltestcase, regex)
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                    # todo -->  Not yet test
                    elif (re.findall(SetVoltageReg, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(SetVoltageReg, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title=str(j + 1)+"- " + "Set battery voltage to " + regex[0] + "V", aka2_ident=t_step_by_test_response_arr[i].step_contain[j])
                            Function.SetVoltageReg_f(testcase, regex)
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                        # todo -->  Not yet test
                    elif (re.findall(SetSpeedReg, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(SetSpeedReg, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka2_ident=t_step_by_test_response_arr[i].step_contain[j])
                            Function.SetSpeedReg_f(testcase, regex)
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                    # todo -->  Not yet test *****************************************
                    # elif (re.findall(CheckInitalSignalValueReg, t_step_by_step_keyw_arr[i].step_contain[j])):
                    #     t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                    #     messageNameReg = '\((.+)\((.+)\)\)'
                    #     ValueReg = '(.*),[ ]*(.+)[ ]?=[ ]?(.+)?'
                    #     regex = re.findall(messageNameReg, t_step_by_step_keyw_arr[i].step_contain[j])
                    #     try:
                    #         messageName = regex[0][0]
                    #         keyword = regex[0][1]
                    #         ValuesName = [None] * 200
                    #         ValuesInitialNumber = [None] * 200
                    #         db = 0
                    #         while (keyword):
                    #             if (re.findall(ValueReg, keyword)):
                    #                 temp = re.findall(ValueReg, keyword)
                    #                 ValuesName[db] = temp[0][1]
                    #                 ValuesInitialNumber[db] = temp[0][2]
                    #                 db = db + 1
                    #                 keyword = temp[0][0]
                    #             else:
                    #                 Value2Reg = '(.+)[ ]?=[ ]?(.+)'
                    #                 temp = re.findall(Value2Reg, keyword)
                    #                 ValuesName[db] = temp[0][0]
                    #                 ValuesInitialNumber[db] = temp[0][1]
                    #                 keyword = None
                    #         # log_handle.info("Error: huanaka", t_step_by_test_response_arr[i].step_contain[j])
                    #         capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="CheckInitalSignalValue", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                    #         caplparam = SubElement(capltestcase, 'caplparam', aka1_name="MessageName", aka2_type="string")
                    #         caplparam.text = messageName
                    #         temp = ''
                    #         k = 0
                    #         for k in range(db, 0, -1):
                    #             temp = temp + str(ValuesName[k]) + ','
                    #         temp = temp + str(ValuesName[0])
                    #         caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Signals", aka2_type="string")
                    #         caplparam.text = temp
                    #         temp = ''
                    #         for k in range(db, 0, -1):
                    #             temp = temp + str(ValuesInitialNumber[k]) + ','
                    #         temp = temp + str(ValuesInitialNumber[0])
                    #         caplparam = SubElement(capltestcase, 'caplparam', aka1_name="ExpectedResults", aka2_type="string")
                    #         caplparam.text = temp
                    #     except:
                    #         log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))

                    # todo -->  Not yet test *****************************************
                    # elif (re.findall(statecheckReg, t_step_by_step_keyw_arr[i].step_contain[j])):
                    #     testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title=t_step_by_test_step_arr[i].step_contain[j], aka2_ident=t_step_by_test_response_arr[i].step_contain[j])
                    #     statecheck = SubElement(testcase, 'statecheck', aka1_wait="MessageName", aka2_title="string")
                    #     expected = SubElement(statecheck, 'expected')
                    #     regex = re.findall(statecheckReg, t_step_by_step_keyw_arr[i].step_contain[j])
                    #     while (regex):
                    #         cansignal = SubElement(expected, 'cansignal', aka1_name=regex[0][1], aka2_msg=regex[0][0])
                    #         temp = re.findall('.*', regex)
                    #         # todo --> will be update
                    #         regex = regex[0][2]

                    # todo -->  Not yet test *****************************************
                    elif (re.findall(loginReg, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(loginReg, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="Login", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                            Function.loginReg_f(capltestcase, regex)
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))

                    # todo -->  Not yet test *****************************************
                    elif (re.findall(Measurement_value_test_Reg, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(Measurement_value_test_Reg, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="Measurement_value_test", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                            Function.Measurement_value_test_Reg_f(capltestcase, regex)
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                    # todo -->  Not yet test *****************************************
                    elif (re.findall(Adaption_value_test_Reg, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(Adaption_value_test_Reg, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="Adaption_value_test", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                            Function.Adaption_value_test_Reg_f(capltestcase, regex)
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                    # todo --> check wait for 100% of qualification time *2 or not
                    elif (re.findall(DTC_check_Timeout_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        if (t_measure_type == "Measuring_auto"):
                            regex = re.findall(DTC_check_Timeout_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                            try:
                                q_time = int(regex[0][tiout_ms.qtime_p])
                                q_min_time = q_time * 9 / 10
                                q_max_time = q_time * 11 / 10
                                # if (q_time <= 100):
                                #     q_max_time = q_time * 12 / 10
                                #     q_min_time = q_time * 8 / 10
                                h_time = int(regex[0][tiout_ms.htime_p])
                                h_min_time = h_time * 9 / 10
                                h_max_time = h_time * 11 / 10
                                wait_time = 0

                                # clear DTC
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                                Function.clearDTC_f(capltestcase)

                                # wait for 100% of qualification time
                                wait_time = q_time * 2;
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 2 times 100% of qualification time (" + str(wait_time) + "ms)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka2_title="wait")

                                # RequestResponse: DTC not present
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][tiout_ms.dtcnum_p] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][tiout_ms.dtcnum_p] + "), DTC not present")
                                if (re.findall("SAIC", t_test_module, re.IGNORECASE)):
                                    Function.request_response_DTC_f(capltestcase, regex[0][tiout_ms.dtcnum_p], ".0.*")
                                else:
                                    Function.request_response_DTC_f(capltestcase, regex[0][tiout_ms.dtcnum_p], ".0")
                                # t_regex = re.findall(RequestResponseReg,t)

                                # wait for message sending
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][tiout_ms.msname_p], aka3_ident='Message arrived')
                                Function.wait_msgsend_f(capltestcase, regex[0][tiout_ms.msname_p])

                                # switch off cyclic sending of message with envvar set to 0
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Disable Cyclic Tx for the message", aka3_ident='DTC 0x' + regex[0][tiout_ms.dtcnum_p] + " is qualifying (0x01)")
                                set = SubElement(testcase, 'set', aka1_title=regex[0][tiout_ms.envarcycl_p])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][tiout_ms.envarcycl_p])
                                envvar.text = "0"

                                # RequestResponse: Measuring qualification time
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponseTimeElapsed", aka2_title="Measuring qualification time of the 0x" + regex[0][tiout_ms.dtcnum_p] + "DTC", aka3_ident='The DTC is qualified in qualification time (+10ms for PDM writting)')
                                Function.measuringtime_f(capltestcase,regex[0][tiout_ms.dtcnum_p],q_min_time,int(q_max_time)+10,".{1}[f|b|9].*")
                                # //RequestResponse: Priority check. If the priority in the parameters is set to 0 no priority check will be requested. If the priority is a valid number a RequestResponse will ba added.
                                priority = int(regex[0][tiout_ms.priority_p])
                                if (priority > 10):
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][tiout_ms.dtcnum_p] + '01', aka3_ident='Field #8 contains DTC priority ' + regex[0][tiout_ms.priority_p])
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                                    caplparam.text = "1906" + regex[0][tiout_ms.dtcnum_p] + "01"
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                                    caplparam.text = "5906" + regex[0][tiout_ms.dtcnum_p] + "09.{2}0" + regex[0][tiout_ms.priority_p] + '.*'
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                                    caplparam.text = "Regexp"

                                # //switch on cyclic sending of message with envvar set to 1
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Enable Cyclic Tx for the message", aka3_ident='DTC 0x' + regex[0][tiout_ms.dtcnum_p] + " is healing")
                                set = SubElement(testcase, 'set', aka1_title=regex[0][tiout_ms.envarcycl_p])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][tiout_ms.envarcycl_p])
                                envvar.text = "1"

                                if (t_execute_option == "Add_waiting_msg"):
                                    # wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][dlc_ms.msname_p], aka3_ident='Message arrived')
                                    Function.wait_msgsend_f(capltestcase, regex[0][tiout_ms.msname_p])

                                # RequestResponse: Measuring healing time
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponseTimeElapsed", aka2_title="Measuring healing time of the 0x" + regex[0][tiout_ms.dtcnum_p] + "DTC", aka3_ident='The DTC is qualified in healing time (+10ms for PDM writting)')
                                Function.measuringtime_f(capltestcase, regex[0][tiout_ms.dtcnum_p], h_min_time, int(h_max_time) + 10, ".{1}[8|e|a].*")
                            except:
                                log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))

                        elif (t_measure_type == "Measuring_manual"):
                            regex = re.findall(DTC_check_Timeout_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                            try:
                                q_time = int(regex[0][tiout_ms.qtime_p])
                                q_min_time = q_time * 89 / 100
                                q_max_time = q_time * 11 / 10
                                h_time = int(regex[0][tiout_ms.htime_p])
                                h_min_time = h_time * 89 / 100
                                h_max_time = h_time * 11 / 10
                                # if (q_time <= 100):
                                #     q_max_time = q_time * 12 / 10
                                #     q_min_time = q_time * 8 / 10
                                # if (h_time > 100):
                                #     h_min_time = h_time * 9 / 10;
                                #     h_max_time = h_time * 11 / 10;

                                wait_time = 0
                                # max time
                                # clear DTC
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                                Function.clearDTC_f(capltestcase)

                                # wait for 100% of qualification time
                                wait_time = q_time * 2;
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 2 times 100% of qualification time (" + str(wait_time) + "ms)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka2_title="wait")

                                # RequestResponse: DTC not present
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][tiout_ms.dtcnum_p] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][tiout_ms.dtcnum_p] + "), DTC not present")
                                # Function.request_response_DTC_f(capltestcase, regex[0][tiout_ms.dtcnum_p], ".0")
                                if (re.findall("SAIC", t_test_module, re.IGNORECASE)):
                                    Function.request_response_DTC_f(capltestcase, regex[0][tiout_ms.dtcnum_p], ".0.*")
                                else:
                                    Function.request_response_DTC_f(capltestcase, regex[0][tiout_ms.dtcnum_p], ".0")
                                # t_regex = re.findall(RequestResponseReg,t)

                                # wait for message sending
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][tiout_ms.msname_p], aka3_ident='Message arrived')
                                Function.wait_msgsend_f(capltestcase, regex[0][tiout_ms.msname_p])

                                # switch off cyclic sending of message with envvar set to 0
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Disable Cyclic Tx for the message", aka3_ident='DTC 0x' + regex[0][tiout_ms.dtcnum_p] + " is qualifying (0x01)")
                                set = SubElement(testcase, 'set', aka1_title=regex[0][tiout_ms.envarcycl_p])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][tiout_ms.envarcycl_p])
                                envvar.text = "0"

                                # RequestResponse: Measuring qualification time with manual
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait ~110% of qualification time (" + str(q_max_time+10) + " ms) (+10ms for write PDM items)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(q_max_time+10), aka1_title="wait")

                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][tiout_ms.dtcnum_p] + '01', aka3_ident='Positive response is returned (0x5906' + regex[0][tiout_ms.htime_p])
                                Function.request_response_DTC_f(capltestcase, regex[0][tiout_ms.dtcnum_p], ".{1}[f|b|9].*")

                                # //RequestResponse: Priority check. If the priority in the parameters is set to 0 no priority check will be requested. If the priority is a valid number a RequestResponse will ba added.
                                priority = int(regex[0][tiout_ms.priority_p])
                                if (priority > 10):
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][tiout_ms.dtcnum_p] + '01', aka3_ident='Field #8 contains DTC priority ' + regex[0][tiout_ms.priority_p])
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                                    caplparam.text = "1906" + regex[0][tiout_ms.dtcnum_p] + "01"
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                                    caplparam.text = "5906" + regex[0][tiout_ms.dtcnum_p] + "09.{2}0" + regex[0][tiout_ms.priority_p] + '.*'
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                                    caplparam.text = "Regexp"
                                #  Check healing time
                                # //switch on cyclic sending of message with envvar set to 1
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Enable Cyclic Tx for the message", aka3_ident='DTC 0x' + regex[0][tiout_ms.dtcnum_p] + " is healing")
                                set = SubElement(testcase, 'set', aka1_title=regex[0][tiout_ms.envarcycl_p])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][tiout_ms.envarcycl_p])
                                envvar.text = "1"

                                if (t_execute_option == "Add_waiting_msg"):
                                    # wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][dlc_ms.msname_p], aka3_ident='Message arrived')
                                    Function.wait_msgsend_f(capltestcase, regex[0][tiout_ms.msname_p])

                                wait_time = h_max_time +10
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait ~110% of healing time (" + str(int(wait_time)) + "ms)(+10ms for PDM writing)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(int(wait_time)), aka1_title="wait")
                                # // RequestResponse: DTC is not present
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][tiout_ms.dtcnum_p] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][tiout_ms.dtcnum_p] + "), DTC is not present")
                                Function.request_response_DTC_f(capltestcase, regex[0][tiout_ms.dtcnum_p], ".{1}[0|e|8].*")

                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait 2000 ms before run next TC ", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(2000), aka1_title="wait")

                                # todo :check  update this after confirm from test and dev
                                # check Healing time = 89%
                                # clear DTC
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                                Function.clearDTC_f(capltestcase)
                                # wait for 200% of qualification time
                                wait_time = q_time * 2;
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 2 times 100% of qualification time (" + str(wait_time) + "ms)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka2_title="wait")
                                # wait for message sending
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][tiout_ms.msname_p], aka3_ident='Message arrived')
                                Function.wait_msgsend_f(capltestcase, regex[0][tiout_ms.msname_p])

                                # switch off cyclic sending of message with envvar set to 0
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Disable Cyclic Tx for the message", aka3_ident='DTC 0x' + regex[0][tiout_ms.dtcnum_p] + " is qualifying (0x01)")
                                set = SubElement(testcase, 'set', aka1_title=regex[0][tiout_ms.envarcycl_p])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][tiout_ms.envarcycl_p])
                                envvar.text = "0"

                                # RequestResponse: Measuring qualification time with manual
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait ~110% of qualification time (" + str(q_max_time+10) + " ms)(+10 ms for PDM writing)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(q_max_time+10), aka1_title="wait")


                                # //switch on cyclic sending of message with envvar set to 1
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Enable Cyclic Tx for the message", aka3_ident='DTC 0x' + regex[0][tiout_ms.dtcnum_p] + " is healing")
                                set = SubElement(testcase, 'set', aka1_title=regex[0][tiout_ms.envarcycl_p])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][tiout_ms.envarcycl_p])
                                envvar.text = "1"

                                if (t_execute_option == "Add_waiting_msg"):
                                    # wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][dlc_ms.msname_p], aka3_ident='Message arrived')
                                    Function.wait_msgsend_f(capltestcase, regex[0][tiout_ms.msname_p])

                                # if (h_time < 50):
                                #     wait_time = 10;
                                #     testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 10 ms for PDM writing ", aka3_ident='-')
                                #     wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka1_title="wait")
                                # //wait 89% of healing time
                                wait_time = h_min_time
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait ~89% of healing time (" + str(int(wait_time)) + "ms)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(int(wait_time)), aka1_title="wait")
                                # // RequestResponse: DTC is  present
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][tiout_ms.dtcnum_p] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][tiout_ms.dtcnum_p] + "), DTC is not present")
                                Function.request_response_DTC_f(capltestcase, regex[0][tiout_ms.dtcnum_p], ".{1}[f|b|9].*")

                                # mintime
                                # clear DTC
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                                Function.clearDTC_f(capltestcase)

                                # wait for 100% of qualification time
                                wait_time = q_time * 2;
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 2 times 100% of qualification time (" + str(wait_time) + "ms)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka2_title="wait")

                                # RequestResponse: DTC not present
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][tiout_ms.dtcnum_p] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][tiout_ms.dtcnum_p] + "), DTC not present")
                                # Function.request_response_DTC_f(capltestcase, regex[0][tiout_ms.dtcnum_p], ".0")
                                if (re.findall("SAIC", t_test_module, re.IGNORECASE)):
                                    Function.request_response_DTC_f(capltestcase, regex[0][tiout_ms.dtcnum_p], ".0.*")
                                else:
                                    Function.request_response_DTC_f(capltestcase, regex[0][tiout_ms.dtcnum_p], ".0")
                                # t_regex = re.findall(RequestResponseReg,t)

                                # wait for message sending
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][tiout_ms.msname_p], aka3_ident='Message arrived')
                                Function.wait_msgsend_f(capltestcase, regex[0][tiout_ms.msname_p])

                                # switch off cyclic sending of message with envvar set to 0
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Disable Cyclic Tx for the message", aka3_ident='DTC 0x' + regex[0][tiout_ms.dtcnum_p] + " is qualifying (0x01)")
                                set = SubElement(testcase, 'set', aka1_title=regex[0][tiout_ms.envarcycl_p])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][tiout_ms.envarcycl_p])
                                envvar.text = "0"


                                # RequestResponse: Measuring qualification time with manual
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait ~89% of qualification time (" + str(q_min_time) + " ms)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(q_min_time), aka1_title="wait")

                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][tiout_ms.dtcnum_p] + '01', aka3_ident='Positive response is returned (0x5906' + regex[0][tiout_ms.htime_p])
                                Function.request_response_DTC_f(capltestcase, regex[0][tiout_ms.dtcnum_p], ".{1}[0|e|8].*")

                                # //RequestResponse: Priority check. If the priority in the parameters is set to 0 no priority check will be requested. If the priority is a valid number a RequestResponse will ba added.
                                priority = int(regex[0][tiout_ms.priority_p])
                                if (priority > 10):
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][tiout_ms.dtcnum_p] + '01', aka3_ident='Field #8 contains DTC priority ' + regex[0][tiout_ms.priority_p])
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                                    caplparam.text = "1906" + regex[0][tiout_ms.dtcnum_p] + "01"
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                                    caplparam.text = "5906" + regex[0][tiout_ms.dtcnum_p] + "09.{2}0" + regex[0][tiout_ms.priority_p] + '.*'
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                                    caplparam.text = "Regexp"

                                # //switch on cyclic sending of message with envvar set to 1
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Enable Cyclic Tx for the message", aka3_ident='DTC 0x' + regex[0][tiout_ms.dtcnum_p] + " is healing")
                                set = SubElement(testcase, 'set', aka1_title=regex[0][tiout_ms.envarcycl_p])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][tiout_ms.envarcycl_p])
                                envvar.text = "1"

                                # //wait for message sending
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][tiout_ms.msname_p], aka3_ident='Message arrived')
                                Function.wait_msgsend_f(capltestcase, regex[0][tiout_ms.msname_p])
                            except:
                                log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                        testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait 2345ms before run next TC ", aka3_ident='-')
                        wait = SubElement(testcase, 'wait', aka1_time=str(2000), aka1_title="wait")


                    elif (re.findall(DTC_check_DLC_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        if (t_measure_type == "Measuring_auto"):
                            regex = re.findall(DTC_check_DLC_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                            try:
                                q_time = int(regex[0][dlc_ms.qtime_p])
                                q_min_time = q_time * 90 / 100
                                q_max_time = q_time * 11 / 10
                                # if (q_time <= 100):
                                #     q_max_time = q_time * 12 / 10
                                #     q_min_time = q_time * 8 / 10

                                h_time = int(regex[0][dlc_ms.htime_p])
                                h_min_time = h_time * 90 / 100
                                h_max_time = h_time * 11 / 10
                                wait_time = 0
                                # clear DTC
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                                Function.clearDTC_f(capltestcase)
                                # wait for 200% of qualification time
                                wait_time = q_time * 2;
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 2 times 100% of qualification time (" + str(wait_time) + "ms)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka2_title="wait")

                                # RequestResponse: DTC not present
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][dlc_ms.dtcnum_p] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][dlc_ms.dtcnum_p] + "), DTC not present")
                                # Function.request_response_DTC_f(capltestcase, regex[0][dlc_ms.dtcnum_p], ".0")
                                if (re.findall("SAIC", t_test_module, re.IGNORECASE)):
                                    Function.request_response_DTC_f(capltestcase, regex[0][dlc_ms.dtcnum_p], ".0.*")
                                else:
                                    Function.request_response_DTC_f(capltestcase, regex[0][dlc_ms.dtcnum_p], ".0")

                                # wait for message sending
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][dlc_ms.msname_p], aka3_ident='Message arrived')
                                Function.wait_msgsend_f(capltestcase, regex[0][dlc_ms.msname_p])

                                # set "Enable for wrong DLC" to 1 and set DLC number to 7
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Enable wrong DLC for the message", aka2_ident='DTC 0x' + regex[0][dlc_ms.dtcnum_p] + ' is qualifying (0x01)')
                                set = SubElement(testcase, 'set', aka1_title=regex[0][dlc_ms.envarset_p])
                                envvar = SubElement(set, 'envvar', aka1_name=regex[0][dlc_ms.envarset_p])
                                envvar.text = "1"
                                set = SubElement(testcase, 'set', aka1_title=regex[0][dlc_ms.envardlc_p])
                                envvar = SubElement(set, 'envvar', aka1_name=regex[0][dlc_ms.envardlc_p])
                                envvar.text = "0"
                                if (t_execute_option == "Add_waiting_msg"):
                                    # wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][dlc_ms.msname_p], aka3_ident='Message arrived')
                                    Function.wait_msgsend_f(capltestcase, regex[0][dlc_ms.msname_p])
                                # RequestResponse: Measuring qualification time
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponseTimeElapsed", aka2_title="Measuring qualification time of the 0x" + regex[0][dlc_ms.dtcnum_p] + "DTC", aka3_ident='The DTC is qualified in qualification time (+10ms for PDM writting)')
                                Function.measuringtime_f(capltestcase, regex[0][dlc_ms.dtcnum_p], q_min_time, int(q_max_time) + 10, ".{1}[f|b|9].*")
                                # //RequestResponse: Priority check. If the priority in the parameters is set to 0 no priority check will be requested. If the priority is a valid number a RequestResponse will ba added.
                                priority = int(regex[0][dlc_ms.priority_p])
                                if (priority > 10):
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][dlc_ms.dtcnum_p] + '01', aka3_ident='Field #8 contains DTC priority ' + regex[0][dlc_ms.priority_p])
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                                    caplparam.text = "1906" + regex[0][dlc_ms.dtcnum_p] + "01"
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                                    caplparam.text = "5906" + regex[0][dlc_ms.dtcnum_p] + "09.{2}0" + regex[0][dlc_ms.priority_p] + '.*'
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                                    caplparam.text = "Regexp"

                                # //wait for message sending
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][dlc_ms.msname_p], aka3_ident='Message arrived')
                                Function.wait_msgsend_f(capltestcase, regex[0][dlc_ms.msname_p])

                                # clear "Enable for wrong DLC"
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Disable wrong DLC for the message", aka2_ident='DTC 0x' + regex[0][dlc_ms.dtcnum_p] + ' is healing')
                                set = SubElement(testcase, 'set', aka1_title=regex[0][dlc_ms.envarset_p])
                                envvar = SubElement(set, 'envvar', aka1_name=regex[0][dlc_ms.envarset_p])
                                envvar.text = "0"
                                ## old template
                                # //wait for message sending
                                # capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][dlc_ms.msname_p], aka3_ident='Message arrived')
                                # caplparam = SubElement(capltestcase, 'caplparam', aka1_name="MessageName", aka2_type="string")
                                # caplparam.text = regex[0][dlc_ms.msname_p]
                                # caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Timeout", aka2_type="int")
                                # caplparam.text = "5000"
                                # check healing time
                                # # //wait 110% of healing time
                                # wait_time = h_time * 11 / 10
                                # testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait ~110% of healing time (" + str(int(wait_time)) + "ms)", aka3_ident='-')
                                # wait = SubElement(testcase, 'wait', aka1_time=str(int(wait_time)), aka1_title="wait")
                                #
                                # if (h_time < 50):
                                #     wait_time = 10;
                                #     testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 10 ms for PDM writing ", aka3_ident='-')
                                #     wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka1_title="wait")
                                #
                                # # // RequestResponse: DTC present with passive state
                                # capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][dlc_ms.dtcnum_p] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][dlc_ms.dtcnum_p] + "), DTC is not present")
                                # caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                                # caplparam.text = "1906" + regex[0][dlc_ms.dtcnum_p] + "01"
                                # caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                                # caplparam.text = "5906" + regex[0][dlc_ms.dtcnum_p] + ".{1}[0|8|e].*"
                                # caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                                # caplparam.text = "Regexp"
                                if (t_execute_option == "Add_waiting_msg"):
                                    # wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][dlc_ms.msname_p], aka3_ident='Message arrived')
                                    Function.wait_msgsend_f(capltestcase, regex[0][dlc_ms.msname_p])
                                # RequestResponse: Measuring healing time
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponseTimeElapsed", aka2_title="Measuring healing time of the 0x" + regex[0][dlc_ms.dtcnum_p] + "DTC", aka3_ident='The DTC is qualified in healing time (+10ms for PDM writting)')
                                Function.measuringtime_f(capltestcase, regex[0][dlc_ms.dtcnum_p], h_min_time, int(h_max_time) + 10, ".{1}[8|e|a].*")
                            except:
                                log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))


                        elif (t_measure_type == "Measuring_manual"):
                            regex = re.findall(DTC_check_DLC_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                            try:
                                q_time = int(regex[0][dlc_ms.qtime_p])
                                h_time = int(regex[0][dlc_ms.htime_p])
                                q_min_time = q_time * 89 / 100
                                q_max_time = q_time * 11 / 10
                                h_min_time = h_time * 89 / 100
                                h_max_time = h_time * 11 / 10

                                wait_time = 0
                                # MAX TIME
                                # clear DTC
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                                Function.clearDTC_f(capltestcase)
                                # wait for 100% of qualification time
                                wait_time = q_time * 2;
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 2 times 100% of qualification time (" + str(wait_time) + "ms)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka2_title="wait")

                                # RequestResponse: DTC not present
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][dlc_ms.dtcnum_p] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][dlc_ms.dtcnum_p] + "), DTC not present")
                                # Function.request_response_DTC_f(capltestcase, regex[0][dlc_ms.dtcnum_p], ".0")
                                if (re.findall("SAIC", t_test_module, re.IGNORECASE)):
                                    Function.request_response_DTC_f(capltestcase, regex[0][dlc_ms.dtcnum_p], ".0.*")
                                else:
                                    Function.request_response_DTC_f(capltestcase, regex[0][dlc_ms.dtcnum_p], ".0")

                                # wait for message sending
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][dlc_ms.msname_p], aka3_ident='Message arrived')
                                Function.wait_msgsend_f(capltestcase, regex[0][dlc_ms.msname_p])

                                # set "Enable for wrong DLC" to 1 and set DLC number to 7
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Enable wrong DLC for the message", aka2_ident='DTC 0x' + regex[0][dlc_ms.dtcnum_p] + ' is qualifying (0x01)')
                                set = SubElement(testcase, 'set', aka1_title=regex[0][dlc_ms.envarset_p])
                                envvar = SubElement(set, 'envvar', aka1_name=regex[0][dlc_ms.envarset_p])
                                envvar.text = "1"
                                set = SubElement(testcase, 'set', aka1_title=regex[0][dlc_ms.envardlc_p])
                                envvar = SubElement(set, 'envvar', aka1_name=regex[0][dlc_ms.envardlc_p])
                                envvar.text = "7"

                                if (t_execute_option == "Add_waiting_msg"):
                                    # wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][dlc_ms.msname_p], aka3_ident='Message arrived')
                                    Function.wait_msgsend_f(capltestcase, regex[0][dlc_ms.msname_p])
                                # RequestResponse: Measuring qualification time with manual
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait ~110% of qualification time (" + str(q_max_time) + " ms)(+10ms for writing PDM)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(q_max_time+10), aka1_title="wait")

                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][dlc_ms.dtcnum_p] + '01', aka3_ident='Positive response is returned (0x5906' + regex[0][dlc_ms.dtcnum_p])
                                Function.request_response_DTC_f(capltestcase, regex[0][dlc_ms.dtcnum_p], ".{1}[f|b|9].*")

                                # //RequestResponse: Priority check. If the priority in the parameters is set to 0 no priority check will be requested. If the priority is a valid number a RequestResponse will ba added.
                                priority = int(regex[0][dlc_ms.priority_p])
                                if (priority > 10):
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][dlc_ms.dtcnum_p] + '01', aka3_ident='Field #8 contains DTC priority ' + regex[0][dlc_ms.priority_p])
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                                    caplparam.text = "1906" + regex[0][dlc_ms.dtcnum_p] + "01"
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                                    caplparam.text = "5906" + regex[0][dlc_ms.dtcnum_p] + "09.{2}0" + regex[0][dlc_ms.priority_p] + '.*'
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                                    caplparam.text = "Regexp"

                                # //wait for message sending
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][dlc_ms.msname_p], aka3_ident='Message arrived')
                                Function.wait_msgsend_f(capltestcase, regex[0][dlc_ms.msname_p])

                                # clear "Enable for wrong DLC"
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Disable wrong DLC for the message", aka2_ident='DTC 0x' + regex[0][dlc_ms.dtcnum_p] + ' is healing')
                                set = SubElement(testcase, 'set', aka1_title=regex[0][dlc_ms.envarset_p])
                                envvar = SubElement(set, 'envvar', aka1_name=regex[0][dlc_ms.envarset_p])
                                envvar.text = "0"

                                # //wait 110% of healing time
                                # check healing time
                                # healing timke 110%
                                # if (h_time < 50):
                                #     wait_time = 10;
                                #     testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 10 ms for PDM writing ", aka3_ident='-')
                                #     wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka1_title="wait")
                                if (t_execute_option == "Add_waiting_msg"):
                                    # wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][dlc_ms.msname_p], aka3_ident='Message arrived')
                                    Function.wait_msgsend_f(capltestcase, regex[0][dlc_ms.msname_p])

                                # RequestResponse: Measuring healing time :  Wait ~110% of healing time
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait ~110% of healing time (" + str(int(h_max_time)) + "ms)(+10ms for writing PDM)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(int(h_max_time+10)), aka1_title="wait")

                                #  RequestResponse: DTC present with passive state
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][dlc_ms.dtcnum_p] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][dlc_ms.dtcnum_p] + "), DTC is not present")
                                Function.request_response_DTC_f(capltestcase, regex[0][dlc_ms.dtcnum_p], ".{1}[0|e|8].*")
                                #	wait 2s before run next TC
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait 2000ms before run next TC ", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(2000), aka1_title="wait")

                                #  update for new template
                                # healing time 99%
                                # clear DTC
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                                Function.clearDTC_f(capltestcase)
                                # wait for 100% of qualification time
                                wait_time = q_time * 2;
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 2 times 100% of qualification time (" + str(wait_time) + "ms)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka2_title="wait")

                                # wait for message sending
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][dlc_ms.msname_p], aka3_ident='Message arrived')
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name="MessageName", aka2_type="string")
                                caplparam.text = regex[0][dlc_ms.msname_p]
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Timeout", aka2_type="int")
                                caplparam.text = "5000"

                                # set "Enable for wrong DLC" to 1 and set DLC number to 7
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Enable wrong DLC for the message", aka2_ident='DTC 0x' + regex[0][dlc_ms.dtcnum_p] + ' is qualifying (0x01)')
                                set = SubElement(testcase, 'set', aka1_title=regex[0][dlc_ms.envarset_p])
                                envvar = SubElement(set, 'envvar', aka1_name=regex[0][dlc_ms.envarset_p])
                                envvar.text = "1"
                                set = SubElement(testcase, 'set', aka1_title=regex[0][dlc_ms.envardlc_p])
                                envvar = SubElement(set, 'envvar', aka1_name=regex[0][dlc_ms.envardlc_p])
                                envvar.text = "7"
                                if (t_execute_option == "Add_waiting_msg"):
                                    # wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][dlc_ms.msname_p], aka3_ident='Message arrived')
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="MessageName", aka2_type="string")
                                    caplparam.text = regex[0][dlc_ms.msname_p]
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Timeout", aka2_type="int")
                                    caplparam.text = "5000"

                                # RequestResponse: Measuring qualification time with manual
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait ~110% of qualification time (" + str(q_max_time) + " ms)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(q_max_time), aka1_title="wait")

                                # wait for message sending
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][dlc_ms.msname_p], aka3_ident='-')
                                Function.wait_msgsend_f(capltestcase, regex[0][dlc_ms.msname_p])
                                # clear "Enable for wrong DLC"
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Disable wrong DLC for the message", aka2_ident='DTC 0x' + regex[0][dlc_ms.dtcnum_p] + ' is healing')
                                set = SubElement(testcase, 'set', aka1_title=regex[0][dlc_ms.envarset_p])
                                envvar = SubElement(set, 'envvar', aka1_name=regex[0][dlc_ms.envarset_p])
                                envvar.text = "0"
                                if (t_execute_option == "Add_waiting_msg"):
                                    # //wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][dlc_ms.msname_p], aka3_ident='Message arrived')
                                    Function.wait_msgsend_f(capltestcase, regex[0][dlc_ms.msname_p])
                                #
                                # if (h_time < 50):
                                #     wait_time = 10;
                                #     testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 10 ms for PDM writing ", aka3_ident='-')
                                #     wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka1_title="wait")
                                # RequestResponse: Measuring healing time :  Wait ~99% of healing time
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait ~99% of healing time (" + str(int(h_min_time * 99 / 100)) + "ms)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(int(h_min_time * 99 / 100)), aka1_title="wait")

                                #  RequestResponse: DTC present with passive state
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][dlc_ms.dtcnum_p] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][dlc_ms.dtcnum_p] + "), DTC is not present")
                                Function.request_response_DTC_f(capltestcase, regex[0][dlc_ms.dtcnum_p], ".{1}[f|b|9].*")

                                # MIN TIME
                                # clear DTC
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                                Function.clearDTC_f(capltestcase)
                                # wait for 100% of qualification time
                                wait_time = q_time * 2;
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 2 times 100% of qualification time (" + str(wait_time) + "ms)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka2_title="wait")

                                # RequestResponse: DTC not present
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][dlc_ms.dtcnum_p] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][dlc_ms.dtcnum_p] + "), DTC not present")
                                # Function.request_response_DTC_f(capltestcase, regex[0][dlc_ms.dtcnum_p], ".0")
                                if (re.findall("SAIC", t_test_module, re.IGNORECASE)):
                                    Function.request_response_DTC_f(capltestcase, regex[0][dlc_ms.dtcnum_p], ".0.*")
                                else:
                                    Function.request_response_DTC_f(capltestcase, regex[0][dlc_ms.dtcnum_p], ".0")

                                # wait for message sending
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][dlc_ms.msname_p], aka3_ident='Message arrived')
                                Function.wait_msgsend_f(capltestcase, regex[0][dlc_ms.msname_p])

                                # set "Enable for wrong DLC" to 1 and set DLC number to 7
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Enable wrong DLC for the message", aka2_ident='DTC 0x' + regex[0][dlc_ms.dtcnum_p] + ' is qualifying (0x01)')
                                set = SubElement(testcase, 'set', aka1_title=regex[0][dlc_ms.envarset_p])
                                envvar = SubElement(set, 'envvar', aka1_name=regex[0][dlc_ms.envarset_p])
                                envvar.text = "1"
                                set = SubElement(testcase, 'set', aka1_title=regex[0][dlc_ms.envardlc_p])
                                envvar = SubElement(set, 'envvar', aka1_name=regex[0][dlc_ms.envardlc_p])
                                envvar.text = "7"
                                if (t_execute_option == "Add_waiting_msg"):
                                    # wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][dlc_ms.msname_p], aka3_ident='Message arrived')
                                    Function.wait_msgsend_f(capltestcase, regex[0][dlc_ms.msname_p])

                                # RequestResponse: Measuring qualification time with manual
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait ~89% of qualification time (" + str(q_min_time) + " ms)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(q_min_time), aka1_title="wait")

                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][dlc_ms.dtcnum_p] + '01', aka3_ident='Positive response is returned (0x5906' + regex[0][dlc_ms.dtcnum_p])
                                Function.request_response_DTC_f(capltestcase, regex[0][dlc_ms.dtcnum_p], ".{1}[[f|9].*")

                                # //RequestResponse: Priority check. If the priority in the parameters is set to 0 no priority check will be requested. If the priority is a valid number a RequestResponse will ba added.
                                priority = int(regex[0][dlc_ms.priority_p])
                                if (priority > 10):
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][dlc_ms.dtcnum_p] + '01', aka3_ident='Field #8 contains DTC priority ' + regex[0][dlc_ms.priority_p])
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                                    caplparam.text = "1906" + regex[0][dlc_ms.dtcnum_p] + "01"
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                                    caplparam.text = "5906" + regex[0][dlc_ms.dtcnum_p] + "09.{2}0" + regex[0][dlc_ms.priority_p] + '.*'
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                                    caplparam.text = "Regexp"

                                # //wait for message sending
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][dlc_ms.msname_p], aka3_ident='Message arrived')
                                Function.wait_msgsend_f(capltestcase, regex[0][dlc_ms.msname_p])

                                # clear "Enable for wrong DLC"
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Disable wrong DLC for the message", aka2_ident='DTC 0x' + regex[0][dlc_ms.dtcnum_p] + ' is healing')
                                set = SubElement(testcase, 'set', aka1_title=regex[0][dlc_ms.envarset_p])
                                envvar = SubElement(set, 'envvar', aka1_name=regex[0][dlc_ms.envarset_p])
                                envvar.text = "0"
                                if (t_execute_option == "Add_waiting_msg"):
                                    # //wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][dlc_ms.msname_p], aka3_ident='Message arrived')
                                    Function.wait_msgsend_f(capltestcase, regex[0][dlc_ms.msname_p])
                                #	wait 2s before run next TC
                            except:
                                log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                        testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait 2000ms before run next TC ", aka3_ident='-')
                        wait = SubElement(testcase, 'wait', aka1_time=str(2000), aka1_title="wait")


                    elif (re.findall(DTC_check_CRC_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        if (t_measure_type == 'Measuring_auto'):
                            regex = re.findall(DTC_check_CRC_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                            try:
                                q_time = int(regex[0][crc_ms.qtime_p])
                                q_min_time = q_time * 90 / 100
                                q_max_time = q_time * 11 / 10
                                h_time = int(regex[0][crc_ms.htime_p])
                                h_min_time = h_time * 90 / 100
                                h_max_time = h_time * 11 / 10
                                wait_time = 0
                                # clear DTC
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                                Function.clearDTC_f(capltestcase)

                                # wait for 100% of qualification time
                                wait_time = q_time * 2;
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 2 times 100% of qualification time (" + str(wait_time) + "ms)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka2_title="wait")

                                # RequestResponse: DTC not present
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][crc_ms.dtcnum_p] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][crc_ms.dtcnum_p] + "), DTC not present")
                                Function.request_response_DTC_f(capltestcase, regex[0][crc_ms.dtcnum_p], ".{1}[0|e|8].*")
                                # t_regex = re.findall(RequestResponseReg,t)

                                # wait for message sending
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][crc_ms.msname_p], aka3_ident='-')
                                Function.wait_msgsend_f(capltestcase, regex[0][crc_ms.msname_p])

                                # set CRC fault with setting the CRC field to -1
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Set CRC error for message", aka3_ident='DTC 0x' + regex[0][crc_ms.dtcnum_p] + " is qualifying (0x01)")
                                set = SubElement(testcase, 'set', aka1_title=regex[0][crc_ms.envarcrc_p])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][crc_ms.envarcrc_p])
                                envvar.text = "-1"
                                if (t_execute_option == "Add_waiting_msg"):
                                    # wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][crc_ms.msname_p], aka3_ident='-')
                                    Function.wait_msgsend_f(capltestcase, regex[0][crc_ms.msname_p])

                                # RequestResponse: Measuring qualification time
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponseTimeElapsed", aka2_title="Measuring qualification time of the 0x" + regex[0][crc_ms.dtcnum_p] + "DTC", aka3_ident='The DTC is qualified in qualification time (+10ms for PDM writting)')
                                Function.measuringtime_f(capltestcase, regex[0][crc_ms.dtcnum_p], q_min_time, int(q_max_time) + 10, ".{1}[f|b|9].*")
                                # //RequestResponse: Priority check. If the priority in the parameters is set to 0 no priority check will be requested. If the priority is a valid number a RequestResponse will ba added.
                                priority = int(regex[0][crc_ms.priority_p])
                                if (priority > 10):
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][crc_ms.dtcnum_p] + '01', aka3_ident='Field #8 contains DTC priority ' + regex[0][crc_ms.priority_p])
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                                    caplparam.text = "1906" + regex[0][crc_ms.dtcnum_p] + "01"
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                                    caplparam.text = "5906" + regex[0][crc_ms.dtcnum_p] + "09.{2}0" + regex[0][crc_ms.priority_p] + '.*'
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                                    caplparam.text = "Regexp"

                                # //wait for message sending
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][crc_ms.msname_p], aka3_ident='-')
                                Function.wait_msgsend_f(capltestcase, regex[0][crc_ms.msname_p])

                                # clear CRC fault with setting the CRC field to 0
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Clear CRC error for message", aka3_ident='DTC 0x' + regex[0][crc_ms.dtcnum_p] + " is healing")
                                set = SubElement(testcase, 'set', aka1_title=regex[0][crc_ms.envarcrc_p])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][crc_ms.envarcrc_p])
                                envvar.text = "0"

                                if (t_execute_option == "Add_waiting_msg"):
                                    # wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][crc_ms.msname_p], aka3_ident='-')
                                    Function.wait_msgsend_f(capltestcase, regex[0][crc_ms.msname_p])
                                # RequestResponse: Measuring healing time
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponseTimeElapsed", aka2_title="Measuring healing time of the 0x" + regex[0][crc_ms.dtcnum_p] + "DTC", aka3_ident='The DTC is qualified in healing time (+10ms for PDM writting)')
                                Function.measuringtime_f(capltestcase, regex[0][crc_ms.dtcnum_p], h_min_time, int(h_max_time) + 10, ".{1}[8|e|a].*")
                            except:
                                log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))

                        elif (t_measure_type == "Measuring_manual"):
                            regex = re.findall(DTC_check_CRC_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                            try:
                                q_time = int(regex[0][crc_ms.qtime_p])
                                q_min_time = q_time * 89 / 100
                                q_max_time = q_time * 11 / 10
                                h_time = int(regex[0][crc_ms.htime_p])
                                h_min_time = h_time * 89 / 100
                                h_max_time = h_time * 11 / 10
                                wait_time = 0
                                # MAX TIME
                                # clear DTC
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                                Function.clearDTC_f(capltestcase)

                                # wait for 100% of qualification time
                                wait_time = q_time * 2;
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 2 times 100% of qualification time (" + str(wait_time) + "ms)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka2_title="wait")

                                # RequestResponse: DTC not present
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][crc_ms.dtcnum_p] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][crc_ms.dtcnum_p] + "), DTC not present")
                                # Function.request_response_DTC_f(capltestcase, regex[0][crc_ms.dtcnum_p], ".0")
                                if (re.findall("SAIC", t_test_module, re.IGNORECASE)):
                                    Function.request_response_DTC_f(capltestcase, regex[0][crc_ms.dtcnum_p], ".0.*")
                                else:
                                    Function.request_response_DTC_f(capltestcase, regex[0][crc_ms.dtcnum_p], ".0")
                                # t_regex = re.findall(RequestResponseReg,t)

                                # wait for message sending
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][crc_ms.msname_p], aka3_ident='-')
                                Function.wait_msgsend_f(capltestcase, regex[0][crc_ms.msname_p])

                                # set CRC fault with setting the CRC field to -1
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Set CRC error for message", aka3_ident='DTC 0x' + regex[0][crc_ms.dtcnum_p] + " is qualifying (0x01)")
                                set = SubElement(testcase, 'set', aka1_title=regex[0][crc_ms.envarcrc_p])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][crc_ms.envarcrc_p])
                                envvar.text = "-1"
                                if (t_execute_option == "Add_waiting_msg"):
                                    # wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][crc_ms.msname_p], aka3_ident='-')
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="MessageName", aka2_type="string")
                                    caplparam.text = regex[0][crc_ms.msname_p]
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Timeout", aka2_type="int")
                                    caplparam.text = "5000"

                                # RequestResponse: Measuring qualification time with manual
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait ~110% of qualification time (" + str(q_max_time+10) + " ms) (+10ms for writing PDM)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(q_max_time+10), aka1_title="wait")
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][crc_ms.dtcnum_p] + '01', aka3_ident='Positive response is returned (0x5906' + regex[0][crc_ms.htime_p])
                                Function.request_response_DTC_f(capltestcase, regex[0][crc_ms.dtcnum_p], ".{1}[f|b|9].*")

                                # //RequestResponse: Priority check. If the priority in the parameters is set to 0 no priority check will be requested. If the priority is a valid number a RequestResponse will ba added.
                                priority = int(regex[0][crc_ms.priority_p])
                                if (priority > 10):
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][crc_ms.dtcnum_p] + '01', aka3_ident='Field #8 contains DTC priority ' + regex[0][crc_ms.priority_p])
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                                    caplparam.text = "1906" + regex[0][crc_ms.dtcnum_p] + "01"
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                                    caplparam.text = "5906" + regex[0][crc_ms.dtcnum_p] + "09.{2}0" + regex[0][crc_ms.priority_p] + '.*'
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                                    caplparam.text = "Regexp"

                                # //wait for message sending
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][crc_ms.msname_p], aka3_ident='-')
                                Function.wait_msgsend_f(capltestcase, regex[0][crc_ms.msname_p])

                                # clear CRC fault with setting the CRC field to 0
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Clear CRC error for message", aka3_ident='DTC 0x' + regex[0][crc_ms.dtcnum_p] + " is healing")
                                set = SubElement(testcase, 'set', aka1_title=regex[0][crc_ms.envarcrc_p])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][crc_ms.envarcrc_p])
                                envvar.text = "0"
                                if (t_execute_option == "Add_waiting_msg"):
                                    # //wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][crc_ms.msname_p], aka3_ident='')
                                    Function.wait_msgsend_f(capltestcase, regex[0][crc_ms.msname_p])
                                # check healing time
                                # //wait 110% of healing time
                                # wait 10 ms for PDM writing
                                # if (h_time < 50):
                                #     wait_time = 10
                                #     testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 10 ms for PDM writing ", aka3_ident='-')
                                #     wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka1_title="wait")
                                # //wait 110% of healing time
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait ~110% of healing time (" + str(int(h_max_time)) + "ms)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(int(h_max_time)), aka1_title="wait")
                                # // RequestResponse: DTC is not present
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][crc_ms.dtcnum_p] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][crc_ms.dtcnum_p] + "), DTC is not present")
                                Function.request_response_DTC_f(capltestcase, regex[0][crc_ms.dtcnum_p], ".{1}[0|e|8].*")
                                # wait 2s before run next TC
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait 2000ms before run next TC ", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(2000), aka1_title="wait")

                                # update for new template
                                # check 99% healing time
                                # clear DTC
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                                Function.clearDTC_f(capltestcase)

                                # wait for 100% of qualification time
                                wait_time = q_time * 2;
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 2 times 100% of qualification time (" + str(wait_time) + "ms)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka2_title="wait")

                                # wait for message sending
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][crc_ms.msname_p], aka3_ident='-')
                                Function.wait_msgsend_f(capltestcase, regex[0][crc_ms.msname_p])

                                # set CRC fault with setting the CRC field to -1
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Set CRC error for message", aka3_ident='DTC 0x' + regex[0][crc_ms.dtcnum_p] + " is qualifying (0x01)")
                                set = SubElement(testcase, 'set', aka1_title=regex[0][crc_ms.envarcrc_p])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][crc_ms.envarcrc_p])
                                envvar.text = "-1"
                                if (t_execute_option == "Add_waiting_msg"):
                                    # wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][crc_ms.msname_p], aka3_ident='-')
                                    Function.wait_msgsend_f(capltestcase, regex[0][crc_ms.msname_p])

                                # RequestResponse: qualification time with manual
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait ~110% of qualification time (" + str(q_max_time) + " ms)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(q_max_time), aka1_title="wait")

                                # wait for message sending
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][crc_ms.msname_p], aka3_ident='-')
                                Function.wait_msgsend_f(capltestcase, regex[0][crc_ms.msname_p])
                                # clear CRC fault with setting the CRC field to 0
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Clear CRC error for message", aka3_ident='DTC 0x' + regex[0][crc_ms.dtcnum_p] + " is healing")
                                set = SubElement(testcase, 'set', aka1_title=regex[0][crc_ms.envarcrc_p])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][crc_ms.envarcrc_p])
                                envvar.text = "0"
                                if (t_execute_option == "Add_waiting_msg"):
                                    # wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][crc_ms.msname_p], aka3_ident='')
                                    Function.wait_msgsend_f(capltestcase, regex[0][crc_ms.msname_p])
                                #
                                # # wait 10 ms for PDM writing
                                # if (h_time < 50):
                                #     wait_time = 10
                                #     testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 10 ms for PDM writing ", aka3_ident='-')
                                #     wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka1_title="wait")
                                # //wait 99% of healing time
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait ~99% of healing time (" + str(int(h_min_time * 99 / 100)) + "ms)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(int(h_min_time * 99 / 100)), aka1_title="wait")
                                # // RequestResponse: DTC is not present
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][crc_ms.dtcnum_p] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][crc_ms.dtcnum_p] + "), DTC is not present")
                                Function.request_response_DTC_f(capltestcase, regex[0][crc_ms.dtcnum_p], ".{1}[f|b|9].*")
                                # wait 2s before run next TC
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait 2000ms before run next TC ", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(2000), aka1_title="wait")

                                # MIN TIME
                                # clear DTC
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                                Function.clearDTC_f(capltestcase)

                                # wait for 100% of qualification time
                                wait_time = q_time * 2;
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 2 times 100% of qualification time (" + str(wait_time) + "ms)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka2_title="wait")

                                # RequestResponse: DTC not present
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][crc_ms.dtcnum_p] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][crc_ms.dtcnum_p] + "), DTC not present")
                                # Function.request_response_DTC_f(capltestcase, regex[0][crc_ms.dtcnum_p], ".0")
                                if (re.findall("SAIC", t_test_module, re.IGNORECASE)):
                                    Function.request_response_DTC_f(capltestcase, regex[0][crc_ms.dtcnum_p], ".0.*")
                                else:
                                    Function.request_response_DTC_f(capltestcase, regex[0][crc_ms.dtcnum_p], ".0")
                                # t_regex = re.findall(RequestResponseReg,t)

                                # wait for message sending
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][crc_ms.msname_p], aka3_ident='-')
                                Function.wait_msgsend_f(capltestcase, regex[0][crc_ms.msname_p])

                                # set CRC fault with setting the CRC field to -1
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Set CRC error for message", aka3_ident='DTC 0x' + regex[0][crc_ms.dtcnum_p] + " is qualifying (0x01)")
                                set = SubElement(testcase, 'set', aka1_title=regex[0][crc_ms.envarcrc_p])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][crc_ms.envarcrc_p])
                                envvar.text = "-1"
                                if (t_execute_option == "Add_waiting_msg"):
                                    # wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][crc_ms.msname_p], aka3_ident='-')
                                    Function.wait_msgsend_f(capltestcase, regex[0][crc_ms.msname_p])

                                # RequestResponse: Measuring qualification time with manual
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait ~89% of qualification time (" + str(q_min_time) + " ms)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(q_min_time), aka1_title="wait")
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][crc_ms.dtcnum_p] + '01', aka3_ident='Positive response is returned (0x5906' + regex[0][crc_ms.htime_p])
                                Function.request_response_DTC_f(capltestcase, regex[0][crc_ms.dtcnum_p], ".{1}[0|e|8].*")

                                # //RequestResponse: Priority check. If the priority in the parameters is set to 0 no priority check will be requested. If the priority is a valid number a RequestResponse will ba added.
                                priority = int(regex[0][crc_ms.priority_p])
                                if (priority > 10):
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][crc_ms.dtcnum_p] + '01', aka3_ident='Field #8 contains DTC priority ' + regex[0][crc_ms.priority_p])
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                                    caplparam.text = "1906" + regex[0][crc_ms.dtcnum_p] + "01"
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                                    caplparam.text = "5906" + regex[0][crc_ms.dtcnum_p] + "09.{2}0" + regex[0][crc_ms.priority_p] + '.*'
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                                    caplparam.text = "Regexp"

                                # //wait for message sending
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][crc_ms.msname_p], aka3_ident='-')
                                Function.wait_msgsend_f(capltestcase, regex[0][crc_ms.msname_p])

                                # clear CRC fault with setting the CRC field to 0
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Clear CRC error for message", aka3_ident='DTC 0x' + regex[0][crc_ms.dtcnum_p] + " is healing")
                                set = SubElement(testcase, 'set', aka1_title=regex[0][crc_ms.envarcrc_p])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][crc_ms.envarcrc_p])
                                envvar.text = "0"
                                if (t_execute_option == "Add_waiting_msg"):
                                    # //wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][crc_ms.msname_p], aka3_ident='')
                                    Function.wait_msgsend_f(capltestcase, regex[0][dlc_ms.msname_p])
                                # wait 2s before run next TC
                            except:
                                log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                        testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait 2000ms before run next TC ", aka3_ident='-')
                        wait = SubElement(testcase, 'wait', aka1_time=str(2000), aka1_title="wait")

                    elif (re.findall(DTC_check_BZ_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        if (t_measure_type == "Measuring_auto"):
                            regex = re.findall(DTC_check_BZ_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                            try:
                                q_time = int(regex[0][bz_ms.qtime_p])
                                q_min_time = q_time * 90 / 100
                                q_max_time = q_time * 11 / 10
                                h_time = int(regex[0][bz_ms.htime_p])
                                h_min_time = h_time * 90 / 100
                                h_max_time = h_time * 11 / 10

                                wait_time = 0
                                # clear DTC
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                                Function.clearDTC_f(capltestcase)

                                # wait for 200% of qualification time
                                wait_time = q_time * 2;
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 2 times 100% of qualification time (" + str(wait_time) + "ms)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka2_title="wait")

                                # RequestResponse: DTC not present
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][bz_ms.dtcnum_p] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][bz_ms.dtcnum_p] + "), DTC not present")
                                # Function.request_response_DTC_f(capltestcase, regex[0][bz_ms.dtcnum_p], ".0")
                                if (re.findall("SAIC", t_test_module, re.IGNORECASE)):
                                    Function.request_response_DTC_f(capltestcase, regex[0][bz_ms.dtcnum_p], ".0.*")
                                else:
                                    Function.request_response_DTC_f(capltestcase, regex[0][bz_ms.dtcnum_p], ".0")

                                # wait for message sending
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][bz_ms.msname_p], aka3_ident='-')
                                Function.wait_msgsend_f(capltestcase, regex[0][bz_ms.msname_p])

                                # set BZ fault with setting the BZ field to -1
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Set BZ error for message", aka3_ident='DTC 0x' + regex[0][bz_ms.dtcnum_p] + " is qualifying (0x01)")
                                set = SubElement(testcase, 'set', aka1_title=regex[0][bz_ms.envarbz_p])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][bz_ms.envarbz_p])
                                envvar.text = "-1"
                                if (t_execute_option == "Add_waiting_msg"):
                                    # wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][bz_ms.msname_p], aka3_ident='-')
                                    Function.wait_msgsend_f(capltestcase, regex[0][bz_ms.msname_p])

                                # RequestResponse: Measuring qualification time
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponseTimeElapsed", aka2_title="Measuring qualification time of the 0x" + regex[0][bz_ms.dtcnum_p] + "DTC", aka3_ident='The DTC is qualified in qualification time (+10ms for PDM writting)')
                                Function.measuringtime_f(capltestcase, regex[0][bz_ms.dtcnum_p], q_min_time, int(q_max_time) + 10, ".{1}[f|b|9].*")
                                # //RequestResponse: Priority check. If the priority in the parameters is set to 0 no priority check will be requested. If the priority is a valid number a RequestResponse will ba added.
                                priority = int(regex[0][bz_ms.priority_p])
                                if (priority > 10):
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][bz_ms.dtcnum_p] + '01', aka3_ident='Field #8 contains DTC priority ' + regex[0][bz_ms.priority_p])
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                                    caplparam.text = "1906" + regex[0][bz_ms.dtcnum_p] + "01"
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                                    caplparam.text = "5906" + regex[0][bz_ms.dtcnum_p] + "09.{2}0" + regex[0][bz_ms.priority_p] + '.*'
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                                    caplparam.text = "Regexp"

                                # //wait for message sending
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][bz_ms.msname_p], aka3_ident='-')
                                Function.wait_msgsend_f(capltestcase, regex[0][bz_ms.msname_p])

                                # clear BZ fault with setting the CRC field to 0
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Clear BZ error for message", aka3_ident='DTC 0x' + regex[0][bz_ms.dtcnum_p] + " is healing")
                                set = SubElement(testcase, 'set', aka1_title=regex[0][bz_ms.envarbz_p])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][bz_ms.envarbz_p])
                                envvar.text = "0"
                                if (t_execute_option == "Add_waiting_msg"):
                                    # wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][bz_ms.msname_p], aka3_ident='-')
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="MessageName", aka2_type="string")
                                    caplparam.text = regex[0][bz_ms.msname_p]
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Timeout", aka2_type="int")
                                    caplparam.text = "5000"
                                # RequestResponse: Measuring healing time
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponseTimeElapsed", aka2_title="Measuring healing time of the 0x" + regex[0][bz_ms.dtcnum_p] + "DTC", aka3_ident='The DTC is qualified in healing time (+10ms for PDM writting)')
                                Function.measuringtime_f(capltestcase, regex[0][bz_ms.dtcnum_p], h_min_time, int(h_max_time) + 10, ".{1}[8|a|e].*")
                            except:
                                log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))

                        elif (t_measure_type == "Measuring_manual"):
                            regex = re.findall(DTC_check_BZ_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                            try:
                                q_time = int(regex[0][bz_ms.qtime_p])
                                q_min_time = q_time * 89 / 100
                                q_max_time = q_time * 11 / 10
                                h_time = int(regex[0][bz_ms.htime_p])
                                h_min_time = h_time * 89 / 100
                                h_max_time = h_time * 11 / 10

                                wait_time = 0

                                # MAX TIME
                                # clear DTC
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                                Function.clearDTC_f(capltestcase)

                                # wait for 100% of qualification time
                                wait_time = q_time * 2;
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 2 times 100% of qualification time (" + str(wait_time) + "ms)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka2_title="wait")

                                # RequestResponse: DTC not present
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][bz_ms.dtcnum_p] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][bz_ms.dtcnum_p] + "), DTC not present")
                                # Function.request_response_DTC_f(capltestcase, regex[0][bz_ms.dtcnum_p], ".0")
                                if (re.findall("SAIC", t_test_module, re.IGNORECASE)):
                                    Function.request_response_DTC_f(capltestcase, regex[0][bz_ms.dtcnum_p], ".0.*")
                                else:
                                    Function.request_response_DTC_f(capltestcase, regex[0][bz_ms.dtcnum_p], ".0")
                                # t_regex = re.findall(RequestResponseReg,t)

                                # wait for message sending
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][bz_ms.msname_p], aka3_ident='-')
                                Function.wait_msgsend_f(capltestcase, regex[0][bz_ms.msname_p])

                                # set BZ fault with setting the BZ field to -1
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Set BZ error for message", aka3_ident='DTC 0x' + regex[0][bz_ms.dtcnum_p] + " is qualifying (0x01)")
                                set = SubElement(testcase, 'set', aka1_title=regex[0][bz_ms.envarbz_p])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][bz_ms.envarbz_p])
                                envvar.text = "-1"
                                if (t_execute_option == "Add_waiting_msg"):
                                    # wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][bz_ms.msname_p], aka3_ident='-')
                                    Function.wait_msgsend_f(capltestcase, regex[0][bz_ms.msname_p])

                                # RequestResponse: Measuring qualification time
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait ~110% of qualification time (" + str(q_max_time) + " ms)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(q_max_time), aka1_title="wait")
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][bz_ms.dtcnum_p] + '01', aka3_ident='Positive response is returned (0x5906' + regex[0][bz_ms.htime_p])
                                Function.request_response_DTC_f(capltestcase, regex[0][bz_ms.dtcnum_p], ".{1}[f|b|9].*")

                                # //RequestResponse: Priority check. If the priority in the parameters is set to 0 no priority check will be requested. If the priority is a valid number a RequestResponse will ba added.
                                priority = int(regex[0][bz_ms.priority_p])
                                if (priority > 10):
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][bz_ms.dtcnum_p] + '01', aka3_ident='Field #8 contains DTC priority ' + regex[0][bz_ms.priority_p])
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                                    caplparam.text = "1906" + regex[0][bz_ms.dtcnum_p] + "01"
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                                    caplparam.text = "5906" + regex[0][bz_ms.dtcnum_p] + "09.{2}0" + regex[0][bz_ms.priority_p] + '.*'
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                                    caplparam.text = "Regexp"

                                # //wait for message sending
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][bz_ms.msname_p], aka3_ident='-')
                                Function.wait_msgsend_f(capltestcase, regex[0][bz_ms.msname_p])

                                # clear BZ fault with setting the CRC field to 0
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Clear BZ error for message", aka3_ident='DTC 0x' + regex[0][bz_ms.dtcnum_p] + " is healing")
                                set = SubElement(testcase, 'set', aka1_title=regex[0][bz_ms.envarbz_p])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][bz_ms.envarbz_p])
                                envvar.text = "0"
                                if (t_execute_option == "Add_waiting_msg"):
                                    # //wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][bz_ms.msname_p], aka3_ident='Message arrived')
                                    Function.wait_msgsend_f(capltestcase, regex[0][bz_ms.msname_p])
                                #
                                # # check healing time
                                # if (h_time < 50):
                                #     wait_time = 10
                                #     testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 10 ms for PDM writing ", aka3_ident='-')
                                #     wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka1_title="wait")

                                # //wait 110% of healing time
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait ~110% of healing time (" + str(int(h_max_time+10)) + "ms)(+10ms for writing PDM)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(int(h_max_time+10)), aka1_title="wait")
                                # // RequestResponse: DTC is not present
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][bz_ms.dtcnum_p] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][bz_ms.dtcnum_p] + "), DTC is not present")
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                                Function.request_response_DTC_f(capltestcase, regex[0][bz_ms.dtcnum_p], ".{1}[0|e|8].*")

                                # Wait 2000ms before run next TC
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait 2000ms before run next TC ", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(2000), aka1_title="wait")

                                # update for new template
                                # 99% healing time
                                # clear DTC
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                                Function.clearDTC_f(capltestcase)

                                # wait for 100% of qualification time
                                wait_time = q_time * 2;
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 2 times 100% of qualification time (" + str(wait_time) + "ms)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka2_title="wait")

                                # wait for message sending
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][bz_ms.msname_p], aka3_ident='-')
                                Function.wait_msgsend_f(capltestcase, regex[0][bz_ms.msname_p])

                                # set BZ fault with setting the BZ field to -1
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Set BZ error for message", aka3_ident='DTC 0x' + regex[0][bz_ms.dtcnum_p] + " is qualifying (0x01)")
                                set = SubElement(testcase, 'set', aka1_title=regex[0][bz_ms.envarbz_p])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][bz_ms.envarbz_p])
                                envvar.text = "-1"
                                if (t_execute_option == "Add_waiting_msg"):
                                    # wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][bz_ms.msname_p], aka3_ident='-')
                                    Function.wait_msgsend_f(capltestcase, regex[0][bz_ms.msname_p])
                                # RequestResponse:  qualification time
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait ~110% of qualification time (" + str(q_max_time) + " ms)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(q_max_time), aka1_title="wait")
                                # //wait for message sending
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][bz_ms.msname_p], aka3_ident='-')
                                Function.wait_msgsend_f(capltestcase, regex[0][bz_ms.msname_p])

                                # clear BZ fault with setting the CRC field to 0
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Clear BZ error for message", aka3_ident='DTC 0x' + regex[0][bz_ms.dtcnum_p] + " is healing")
                                set = SubElement(testcase, 'set', aka1_title=regex[0][bz_ms.envarbz_p])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][bz_ms.envarbz_p])
                                envvar.text = "0"
                                if (t_execute_option == "Add_waiting_msg"):
                                    # //wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][bz_ms.msname_p], aka3_ident='Message arrived')
                                    Function.wait_msgsend_f(capltestcase, regex[0][bz_ms.msname_p])
                                #
                                # # # //wait 90% of healing time
                                # if (h_time < 50):
                                #     wait_time = 10
                                #     testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 10 ms for PDM writing ", aka3_ident='-')
                                #     wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka1_title="wait")

                                # //wait 89% of healing time
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait ~89% of healing time (" + str(int(h_min_time * 89 / 100)) + "ms)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(int(h_min_time * 89 / 100)), aka1_title="wait")
                                # // RequestResponse: DTC is not present
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][bz_ms.dtcnum_p] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][bz_ms.dtcnum_p] + "), DTC is not present")
                                Function.request_response_DTC_f(capltestcase, regex[0][bz_ms.dtcnum_p], ".{1}[f|b|9].*")

                                # Wait 2000ms before run next TC
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait 2000ms before run next TC ", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(2000), aka1_title="wait")

                                # MIN TIME
                                # clear DTC
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                                Function.clearDTC_f(capltestcase)

                                # wait for 100% of qualification time
                                wait_time = q_time * 2;
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 2 times 100% of qualification time (" + str(wait_time) + "ms)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka2_title="wait")

                                # RequestResponse: DTC not present
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][bz_ms.dtcnum_p] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][bz_ms.dtcnum_p] + "), DTC not present")
                                # Function.request_response_DTC_f(capltestcase, regex[0][bz_ms.dtcnum_p], ".0")
                                if (re.findall("SAIC", t_test_module, re.IGNORECASE)):
                                    Function.request_response_DTC_f(capltestcase, regex[0][bz_ms.dtcnum_p], ".0.*")
                                else:
                                    Function.request_response_DTC_f(capltestcase, regex[0][bz_ms.dtcnum_p], ".0")
                                # t_regex = re.findall(RequestResponseReg,t)

                                # wait for message sending
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][bz_ms.msname_p], aka3_ident='-')
                                Function.wait_msgsend_f(capltestcase, regex[0][bz_ms.msname_p])

                                # set BZ fault with setting the BZ field to -1
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Set BZ error for message", aka3_ident='DTC 0x' + regex[0][bz_ms.dtcnum_p] + " is qualifying (0x01)")
                                set = SubElement(testcase, 'set', aka1_title=regex[0][bz_ms.envarbz_p])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][bz_ms.envarbz_p])
                                envvar.text = "-1"
                                if (t_execute_option == "Add_waiting_msg"):
                                    # wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][bz_ms.msname_p], aka3_ident='-')
                                    Function.wait_msgsend_f(capltestcase, regex[0][bz_ms.msname_p])

                                # RequestResponse: Measuring qualification time
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait ~89% of qualification time (" + str(q_min_time) + " ms)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(q_min_time), aka1_title="wait")
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][bz_ms.dtcnum_p] + '01', aka3_ident='Positive response is returned (0x5906' + regex[0][bz_ms.htime_p])
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                                Function.request_response_DTC_f(capltestcase, regex[0][bz_ms.dtcnum_p], ".{1}[0|e|8].*")

                                # //RequestResponse: Priority check. If the priority in the parameters is set to 0 no priority check will be requested. If the priority is a valid number a RequestResponse will ba added.
                                priority = int(regex[0][bz_ms.priority_p])
                                if (priority > 10):
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][bz_ms.dtcnum_p] + '01', aka3_ident='Field #8 contains DTC priority ' + regex[0][bz_ms.priority_p])
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                                    caplparam.text = "1906" + regex[0][bz_ms.dtcnum_p] + "01"
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                                    caplparam.text = "5906" + regex[0][bz_ms.dtcnum_p] + "09.{2}0" + regex[0][bz_ms.priority_p] + '.*'
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                                    caplparam.text = "Regexp"

                                # //wait for message sending
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][bz_ms.msname_p], aka3_ident='-')
                                Function.wait_msgsend_f(capltestcase, regex[0][bz_ms.msname_p])

                                # clear BZ fault with setting the CRC field to 0
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Clear BZ error for message", aka3_ident='DTC 0x' + regex[0][bz_ms.dtcnum_p] + " is healing")
                                set = SubElement(testcase, 'set', aka1_title=regex[0][bz_ms.envarbz_p])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][bz_ms.envarbz_p])
                                envvar.text = "0"
                                if (t_execute_option == "Add_waiting_msg"):
                                    # //wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][bz_ms.msname_p], aka3_ident='Message arrived')
                                    Function.wait_msgsend_f(capltestcase, regex[0][bz_ms.msname_p])
                            except:
                                log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))

                            # Wait 2000ms before run next TC
                        testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait 2000ms before run next TC ", aka3_ident='-')
                        wait = SubElement(testcase, 'wait', aka1_time=str(2000), aka1_title="wait")


                    elif (re.findall(DTC_check_Signal_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        if (t_measure_type == "Measuring_auto"):
                            regex = re.findall(DTC_check_Signal_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                            try:
                                q_time = int(regex[0][invalid_ms.qtime_p])
                                h_time = int(regex[0][invalid_ms.htime_p])
                                q_min_time = q_time * 90 / 100
                                q_max_time = q_time * 11 / 10
                                h_min_time = h_time * 90 / 100
                                h_max_time = h_time * 11 / 10  # 10 ms is the time for PDM writing

                                wait_time = 0
                                # clear DTC
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                                Function.clearDTC_f(capltestcase)

                                # wait for 100% of qualification time
                                wait_time = q_time * 2;
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 2 times 100% of qualification time (" + str(wait_time) + "ms)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka2_title="wait")

                                # RequestResponse: DTC not present
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][invalid_ms.dtcnum_p] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][invalid_ms.dtcnum_p] + "), DTC not present")
                                # Function.request_response_DTC_f(capltestcase, regex[0][invalid_ms.dtcnum_p], ".0")
                                if (re.findall("SAIC", t_test_module, re.IGNORECASE)):
                                    Function.request_response_DTC_f(capltestcase, regex[0][invalid_ms.dtcnum_p], ".0.*")
                                else:
                                    Function.request_response_DTC_f(capltestcase, regex[0][invalid_ms.dtcnum_p], ".0")
                                # t_regex = re.findall(RequestResponseReg,t)

                                # SaveSignalValue
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="SaveSignalValue", aka2_title="Save Signal Value", aka3_ident='-')
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name="EnvvarName", aka2_type="string")
                                caplparam.text = regex[0][invalid_ms.envarsig_p]

                                # wait for message sending
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][invalid_ms.msname_p], aka3_ident='-')
                                Function.wait_msgsend_f(capltestcase, regex[0][invalid_ms.msname_p])

                                # set envvar value to the third parameter value
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Set signal to value " + regex[0][invalid_ms.valueinv_p], aka3_ident='DTC 0x' + regex[0][invalid_ms.dtcnum_p] + " is qualifying (0x01)")
                                set = SubElement(testcase, 'set', aka1_title=regex[0][invalid_ms.envarsig_p])
                                envvar = SubElement(set, 'envvar', aka1_name=regex[0][invalid_ms.envarsig_p])
                                envvar.text = regex[0][invalid_ms.valueinv_p]
                                if (t_execute_option == "Add_waiting_msg"):
                                    # wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][invalid_ms.msname_p], aka3_ident='-')
                                    Function.wait_msgsend_f(capltestcase, regex[0][invalid_ms.msname_p])

                                # //Check if DTC number is 0 for the no error present case
                                DTC_number_length = len(regex[0][invalid_ms.dtcnum_p])
                                if (DTC_number_length != 1):
                                    # RequestResponse: Measuring qualification time
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponseTimeElapsed", aka2_title="Measuring qualification time of the 0x" + regex[0][invalid_ms.dtcnum_p] + "DTC", aka3_ident='The DTC is qualified in qualification time (+10ms for PDM writting)')
                                    Function.measuringtime_f(capltestcase, regex[0][invalid_ms.dtcnum_p], q_min_time, int(q_max_time) + 10, ".{1}[f|b|9].*")
                                    # //RequestResponse: Priority check. If the priority in the parameters is set to 0 no priority check will be requested. If the priority is a valid number a RequestResponse will ba added.
                                    priority = int(regex[0][invalid_ms.priority_p])
                                    if (priority > 10):
                                        capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][invalid_ms.dtcnum_p] + '01', aka3_ident='Field #8 contains DTC priority ' + regex[0][invalid_ms.priority_p])
                                        caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                                        caplparam.text = "1906" + regex[0][invalid_ms.dtcnum_p] + "01"
                                        caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                                        caplparam.text = "5906" + regex[0][invalid_ms.dtcnum_p] + "09.{2}0" + regex[0][invalid_ms.priority_p] + '.*'
                                        caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                                        caplparam.text = "Regexp"

                                    # clear signal fault with RestoreSignalValue
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RestoreSignalValue", aka2_title="Set signal to default value", aka3_ident='-')
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="EnvvarName", aka2_type="string")
                                    caplparam.text = regex[0][invalid_ms.envarsig_p]
                                    # envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][invalid_ms.envarsig_p])
                                    # envvar.text = "0"
                                    if (t_execute_option == "Add_waiting_msg"):
                                        # wait for message sending
                                        capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][invalid_ms.msname_p], aka3_ident='-')
                                        Function.wait_msgsend_f(capltestcase, regex[0][invalid_ms.msname_p])
                                    # RequestResponse: Measuring healing time
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponseTimeElapsed", aka2_title="Measuring healing time of the 0x" + regex[0][invalid_ms.dtcnum_p] + "DTC", aka3_ident='The DTC is qualified in healing time (+10ms for PDM writting)')
                                    Function.measuringtime_f(capltestcase, regex[0][invalid_ms.dtcnum_p], h_min_time, int(h_max_time) + 10, ".{1}[8|e|a].*")
                                else:
                                    # //wait 110% of healing time
                                    wait_time = h_time * 11 / 10 +10
                                    testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait ~110% of qualification time (" + str(int(wait_time)) + "ms)(=10ms for PDM writing)", aka3_ident='-')
                                    wait = SubElement(testcase, 'wait', aka1_time=str(int(wait_time)), aka1_title="wait")
                                    # // RequestResponse: DTC is not present
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906", aka3_ident='Positive response is returned (0x59006), DTC is not present')
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                                    Function.request_response_DTC_f(capltestcase, regex[0][invalid_ms.dtcnum_p], ".{1}[0|e|8].*")
                                    # clear signal fault with RestoreSignalValue
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RestoreSignalValue", aka2_title="Set signal to default value", aka3_ident='-')
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="EnvvarName", aka2_type="string")
                                    caplparam.text = regex[0][invalid_ms.envarsig_p]
                                    envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][invalid_ms.envarsig_p])
                                    envvar.text = "0"
                            except:
                                log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                        elif (t_measure_type == "Measuring_manual"):
                            regex = re.findall(DTC_check_Signal_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                            try:
                                q_time = int(regex[0][invalid_ms.qtime_p])
                                q_min_time = q_time * 89 / 100
                                q_max_time = q_time * 11 / 10
                                h_time = int(regex[0][invalid_ms.htime_p])
                                h_min_time = h_time * 89 / 100
                                h_max_time = h_time * 11 / 10  # 10 ms is the time for PDM writing
                                wait_time = 0
                                # MAX TIMah E
                                # clear DTC
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                                Function.clearDTC_f(capltestcase)

                                # wait for 100% of qualification time
                                wait_time = q_time * 2;
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 2 times 100% of qualification time (" + str(wait_time) + "ms)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka2_title="wait")

                                # RequestResponse: DTC not present
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][invalid_ms.dtcnum_p] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][invalid_ms.dtcnum_p] + "), DTC not present")
                                # Function.request_response_DTC_f(capltestcase, regex[0][invalid_ms.dtcnum_p], ".0")
                                if (re.findall("SAIC", t_test_module, re.IGNORECASE)):
                                    Function.request_response_DTC_f(capltestcase, regex[0][invalid_ms.dtcnum_p], ".0.*")
                                else:
                                    Function.request_response_DTC_f(capltestcase, regex[0][invalid_ms.dtcnum_p], ".0")
                                # t_regex = re.findall(RequestResponseReg,t)

                                # SaveSignalValue
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="SaveSignalValue", aka2_title="Save Signal Value", aka3_ident='-')
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name="EnvvarName", aka2_type="string")
                                caplparam.text = regex[0][invalid_ms.envarsig_p]

                                # wait for message sending
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][invalid_ms.msname_p], aka3_ident='Message arrived')
                                Function.wait_msgsend_f(capltestcase, regex[0][invalid_ms.msname_p])

                                # set envvar value to the third parameter value
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Set signal to value " + regex[0][invalid_ms.valueinv_p], aka3_ident='DTC 0x' + regex[0][invalid_ms.dtcnum_p] + " is qualifying (0x01)")
                                set = SubElement(testcase, 'set', aka1_title=regex[0][invalid_ms.envarsig_p])
                                envvar = SubElement(set, 'envvar', aka1_name=regex[0][invalid_ms.envarsig_p])
                                envvar.text = regex[0][invalid_ms.valueinv_p]
                                if (t_execute_option == "Add_waiting_msg"):
                                    # wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][invalid_ms.msname_p], aka3_ident='-')
                                    Function.wait_msgsend_f(capltestcase, regex[0][invalid_ms.msname_p])
                                # //Check if DTC number is 0 for the no error present case
                                DTC_number_length = len(regex[0][invalid_ms.dtcnum_p])
                                if (DTC_number_length != 1):
                                    # RequestResponse: Measuring qualification time
                                    testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait ~110% of qualification time (" + str(q_max_time+10) + " ms)(+10ms for writing PDM)", aka3_ident='-')
                                    wait = SubElement(testcase, 'wait', aka1_time=str(q_max_time+10), aka1_title="wait")
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][invalid_ms.dtcnum_p] + '01', aka3_ident='Positive response is returned (0x5906' + regex[0][invalid_ms.dtcnum_p])
                                    Function.request_response_DTC_f(capltestcase, regex[0][invalid_ms.dtcnum_p], ".{1}[f|b|9].*")

                                    # //RequestResponse: Priority check. If the priority in the parameters is set to 0 no priority check will be requested. If the priority is a valid number a RequestResponse will ba added.
                                    priority = int(regex[0][invalid_ms.priority_p])
                                    if (priority > 10):
                                        capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][invalid_ms.dtcnum_p] + '01', aka3_ident='Field #8 contains DTC priority ' + regex[0][invalid_ms.priority_p])
                                        caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                                        caplparam.text = "1906" + regex[0][invalid_ms.dtcnum_p] + "01"
                                        caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                                        caplparam.text = "5906" + regex[0][invalid_ms.dtcnum_p] + "09.{2}0" + regex[0][invalid_ms.priority_p] + '.*'
                                        caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                                        caplparam.text = "Regexp"

                                    # wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][invalid_ms.msname_p], aka3_ident='-')
                                    Function.wait_msgsend_f(capltestcase, regex[0][invalid_ms.msname_p])
                                    # clear signal fault with RestoreSignalValue
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RestoreSignalValue", aka2_title="Set signal to default value", aka3_ident='-')
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="EnvvarName", aka2_type="string")
                                    caplparam.text = regex[0][invalid_ms.envarsig_p]
                                    # envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][invalid_ms.envarsig_p])
                                    # envvar.text = "0"

                                    # # //wait for message sending
                                    if (t_execute_option == "Add_waiting_msg"):
                                        # wait for message sending
                                        capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][invalid_ms.msname_p], aka3_ident='-')
                                        Function.wait_msgsend_f(capltestcase, regex[0][invalid_ms.msname_p])

                                    # RequestResponse: Measuring healing time
                                    testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait ~110% of healing time (" + str(int(h_max_time)+10) + "ms)(+10ms for writing PDM)", aka3_ident='-')
                                    wait = SubElement(testcase, 'wait', aka1_time=str(int(h_max_time)+10), aka1_title="wait")
                                    # // RequestResponse: DTC is not present
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][invalid_ms.dtcnum_p] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][invalid_ms.dtcnum_p] + "), DTC is not present")
                                    Function.request_response_DTC_f(capltestcase, regex[0][invalid_ms.dtcnum_p], ".{1}[0|e|8].*")
                                    # wait 2s before run next testcase
                                    testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait 2000ms before run next TC ", aka3_ident='-')
                                    wait = SubElement(testcase, 'wait', aka1_time=str(2000), aka1_title="wait")

                                    # update for new template
                                    # check 99% qualification time
                                    # clear DTC
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                                    Function.clearDTC_f(capltestcase)

                                    # wait for 100% of qualification time
                                    wait_time = q_time * 2;
                                    testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 2 times 100% of qualification time (" + str(wait_time) + "ms)", aka3_ident='-')
                                    wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka2_title="wait")

                                    # SaveSignalValue
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="SaveSignalValue", aka2_title="Save Signal Value", aka3_ident='-')
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="EnvvarName", aka2_type="string")
                                    caplparam.text = regex[0][invalid_ms.envarsig_p]

                                    # wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][invalid_ms.msname_p], aka3_ident='Message arrived')
                                    Function.wait_msgsend_f(capltestcase, regex[0][invalid_ms.msname_p])

                                    # set envvar value to the third parameter value
                                    testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Set signal to value " + regex[0][invalid_ms.valueinv_p], aka3_ident='DTC 0x' + regex[0][invalid_ms.dtcnum_p] + " is qualifying (0x01)")
                                    set = SubElement(testcase, 'set', aka1_title=regex[0][invalid_ms.envarsig_p])
                                    envvar = SubElement(set, 'envvar', aka1_name=regex[0][invalid_ms.envarsig_p])
                                    envvar.text = regex[0][invalid_ms.valueinv_p]

                                    if (t_execute_option == "Add_waiting_msg"):
                                        # wait for message sending
                                        capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][invalid_ms.msname_p], aka3_ident='-')
                                        Function.wait_msgsend_f(capltestcase, regex[0][invalid_ms.msname_p])
                                    # RequestResponse:wait qualification time
                                    testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait ~110% of qualification time (" + str(q_max_time+10) + " ms)", aka3_ident='-')
                                    wait = SubElement(testcase, 'wait', aka1_time=str(q_max_time+10), aka1_title="wait")
                                    # wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][invalid_ms.msname_p], aka3_ident='-')
                                    Function.wait_msgsend_f(capltestcase, regex[0][invalid_ms.msname_p])
                                    # clear signal fault with RestoreSignalValue
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RestoreSignalValue", aka2_title="Set signal to default value", aka3_ident='-')
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="EnvvarName", aka2_type="string")
                                    caplparam.text = regex[0][invalid_ms.envarsig_p]
                                    # envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][invalid_ms.envarsig_p])

                                    if (t_execute_option == "Add_waiting_msg"):
                                        # wait for message sending
                                        capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][invalid_ms.msname_p], aka3_ident='-')
                                        Function.wait_msgsend_f(capltestcase, regex[0][invalid_ms.msname_p])
                                    # # //wait 89% of healing time
                                    # RequestResponse: Measuring healing time
                                    testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait ~89% of healing time (" + str(int(h_min_time * 89 / 100)+10) + "ms)(+10ms for writing PDM)", aka3_ident='-')
                                    wait = SubElement(testcase, 'wait', aka1_time=str(int(h_min_time * 99 / 100)+10), aka1_title="wait")

                                    # // RequestResponse: DTC is not present
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][invalid_ms.dtcnum_p] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][invalid_ms.dtcnum_p] + "), DTC is not present")
                                    Function.request_response_DTC_f(capltestcase, regex[0][invalid_ms.dtcnum_p], ".{1}[f|b|9].*")
                                    # wait 2s before run next testcase
                                    testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait 2000ms before run next TC ", aka3_ident='-')
                                    wait = SubElement(testcase, 'wait', aka1_time=str(2000), aka1_title="wait")




                                else:
                                    # //wait 110% of healing time
                                    testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait ~110% of qualification time (" + str(int(q_max_time)) + "ms)", aka3_ident='-')
                                    wait = SubElement(testcase, 'wait', aka1_time=str(int(q_max_time)), aka1_title="wait")
                                    # // RequestResponse: DTC is not present
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x190209", aka3_ident='Positive response is returned (0x590219), DTC is not present')
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                                    caplparam.text = "190209"
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                                    caplparam.text = "5902.{2}"
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                                    caplparam.text = "Equal"
                                    # clear signal fault with RestoreSignalValue
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RestoreSignalValue", aka2_title="Set signal to default value", aka3_ident='-')
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="EnvvarName", aka2_type="string")
                                    caplparam.text = regex[0][invalid_ms.envarsig_p]
                                    envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][invalid_ms.envarsig_p])
                                    envvar.text = "0"
                                    # wait 2s before run next testcase
                                    testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait 2000ms before run next TC ", aka3_ident='-')
                                    wait = SubElement(testcase, 'wait', aka1_time=str(2000), aka1_title="wait")

                                # MIN TIME
                                # clear DTC
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                                Function.clearDTC_f(capltestcase)

                                # wait for 100% of qualification time
                                wait_time = q_time * 2;
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 2 times 100% of qualification time (" + str(wait_time) + "ms)", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka2_title="wait")

                                # RequestResponse: DTC not present
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][invalid_ms.dtcnum_p] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][invalid_ms.dtcnum_p] + "), DTC not present")
                                # Function.request_response_DTC_f(capltestcase, regex[0][invalid_ms.dtcnum_p], ".0")
                                if (re.findall("SAIC", t_test_module, re.IGNORECASE)):
                                    Function.request_response_DTC_f(capltestcase, regex[0][invalid_ms.dtcnum_p], ".0.*")
                                else:
                                    Function.request_response_DTC_f(capltestcase, regex[0][invalid_ms.dtcnum_p], ".0")
                                # t_regex = re.findall(RequestResponseReg,t)

                                # SaveSignalValue
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="SaveSignalValue", aka2_title="Save Signal Value", aka3_ident='-')
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name="EnvvarName", aka2_type="string")
                                caplparam.text = regex[0][invalid_ms.envarsig_p]

                                # wait for message sending
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][invalid_ms.msname_p], aka3_ident='-')
                                Function.wait_msgsend_f(capltestcase, regex[0][invalid_ms.msname_p])

                                # set envvar value to the third parameter value
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Set signal to value " + regex[0][invalid_ms.valueinv_p], aka3_ident='DTC 0x' + regex[0][invalid_ms.dtcnum_p] + " is qualifying (0x01)")
                                set = SubElement(testcase, 'set', aka1_title=regex[0][invalid_ms.envarsig_p])
                                envvar = SubElement(set, 'envvar', aka1_name=regex[0][invalid_ms.envarsig_p])
                                envvar.text = regex[0][invalid_ms.valueinv_p]
                                if (t_execute_option == "Add_waiting_msg"):
                                    # wait for message sending
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][invalid_ms.msname_p], aka3_ident='-')
                                    Function.wait_msgsend_f(capltestcase, regex[0][invalid_ms.msname_p])
                                # //Check if DTC number is 0 for the no error present case
                                DTC_number_length = len(regex[0][invalid_ms.dtcnum_p])
                                if (DTC_number_length != 1):
                                    # RequestResponse: Measuring qualification time
                                    testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait ~89% of qualification time (" + str(q_min_time) + " ms)", aka3_ident='-')
                                    wait = SubElement(testcase, 'wait', aka1_time=str(q_min_time), aka1_title="wait")
                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][invalid_ms.dtcnum_p] + '01', aka3_ident='Positive response is returned (0x5906' + regex[0][invalid_ms.dtcnum_p])
                                    Function.request_response_DTC_f(capltestcase, regex[0][invalid_ms.dtcnum_p], ".{1}[0|e|8].*")

                                    # //RequestResponse: Priority check. If the priority in the parameters is set to 0 no priority check will be requested. If the priority is a valid number a RequestResponse will ba added.
                                    priority = int(regex[0][invalid_ms.priority_p])
                                    if (priority > 10):
                                        capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][invalid_ms.dtcnum_p] + '01', aka3_ident='Field #8 contains DTC priority ' + regex[0][invalid_ms.priority_p])
                                        caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                                        caplparam.text = "1906" + regex[0][invalid_ms.dtcnum_p] + "01"
                                        caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                                        caplparam.text = "5906" + regex[0][invalid_ms.dtcnum_p] + "09.{2}0" + regex[0][invalid_ms.priority_p] + '.*'
                                        caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                                        caplparam.text = "Regexp"

                                # clear signal fault with RestoreSignalValue
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RestoreSignalValue", aka2_title="Set signal to default value", aka3_ident='-')
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name="EnvvarName", aka2_type="string")
                                caplparam.text = regex[0][invalid_ms.envarsig_p]
                                # envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][invalid_ms.envarsig_p])
                                # envvar.text = "0"
                                # wait 2s before run next testcase
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait 2000ms ddsfdsfdsfs run next TC ", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(2000), aka1_title="wait")
                            except:
                                log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))

                    # todo -->  Not yet test *****************************************
                    elif (re.findall(WaitForMessage_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(WaitForMessage_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        t_split = re.split(",[\s+]?", regex[0][1])
                        if (t_split == None):
                            check_error = 1
                            catch_error = "Generate may be error, Please check Test step keyword row: " + str(i + 1) + ", step " + str(j + 1)
                            Function.checkerror_f(check_error, catch_error)
                        else:
                            try:
                                if len(t_split)== 1:

                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title=str(j + 1) + "- " + "Wait for message" + t_split[0], aka3_ident='Message arrived')
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="MessageName", aka2_type="string")
                                    caplparam.text = t_split[0]
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Timeout", aka2_type="int")
                                    caplparam.text = str(5000)
                                elif len(t_split)== 2:

                                    capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title=str(j + 1) + "- " + "Wait for message" + t_split[0], aka3_ident='Message arrived')
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="MessageName", aka2_type="string")
                                    caplparam.text = t_split[0]
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Timeout", aka2_type="int")
                                    caplparam.text = str(int(t_split[1]))
                            except:
                                if (re.findall(WaitForMessageReq, t_step_by_step_keyw_arr[i].step_contain[j])):
                                    t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                                    regex = re.findall(WaitForMessageReq, t_step_by_step_keyw_arr[i].step_contain[j])
                                    try:
                                        # //wait for message sending
                                        # capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title=str(j + 1)+"- " + "Wait for message" + regex[0][0], aka3_ident='Message arrived')
                                        caplparam = SubElement(capltestcase, 'caplparam', aka1_name="MessageName", aka2_type="string")
                                        caplparam.text = regex[0][0]
                                        caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Timeout", aka2_type="int")
                                        caplparam.text = str(int(regex[0][1]))
                                    except:
                                        log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                                else:
                                    log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                    # BK_GEN2.5_15.Aug.2021
                    # elif (re.findall(RequestResponseTimeElapsedReq, t_step_by_step_keyw_arr[i].step_contain[j])):
                    #     t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                    #     regex = re.findall(RequestResponseTimeElapsedReq, t_step_by_step_keyw_arr[i].step_contain[j])
                    #     try:
                    #         # //wait for message sending
                    #         capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponseTimeElapsed", aka2_title=str(j + 1)+"- " + "Measuring qualification time DTC "  + regex[0][0], aka3_ident='The DTC is qualified or health in  time')
                    #         caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                    #         caplparam.text =  regex[0][1]
                    #         caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                    #         caplparam.text =  regex[0][2]
                    #         caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                    #         caplparam.text =  regex[0][3]
                    #         caplparam = SubElement(capltestcase, 'caplparam', aka1_name="aTime1", aka2_type="string")
                    #         caplparam.text = str(int(regex[0][4]))
                    #         caplparam = SubElement(capltestcase, 'caplparam', aka1_name="aTime2", aka2_type="string")
                    #         caplparam.text = str(int(regex[0][5]))
                    #     except:
                    #         log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))

                    elif (re.findall(RequestResponseTimeElapsed_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        # t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(RequestResponseTimeElapsed_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        t_split = re.split(",\s+", regex[0][1])
                        if (t_split == None):
                            check_error = 1
                            catch_error = "Generate may be error, Please check Test step keyword row: " + str(i + 1) + ", step " + str(j + 1)
                            Function.checkerror_f(check_error, catch_error)
                        else:
                            try:
                                temp_split = re.split("\s+", t_split[0])
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponseTimeElapsed", aka2_title=str(j + 1)+"- " + "Measuring qualification time DTC "  + temp_split[2], aka3_ident='The DTC is qualified or health in  time')
                                for temp in t_split:
                                    temp_split = re.split("\s+", temp)
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name=temp_split[1], aka2_type=temp_split[0])
                                    caplparam.text = temp_split[2]
                            except:
                                if (re.findall(RequestResponseTimeElapsedReq, t_step_by_step_keyw_arr[i].step_contain[j])):
                                    t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                                    regex = re.findall(RequestResponseTimeElapsedReq, t_step_by_step_keyw_arr[i].step_contain[j])
                                    try:
                                        # //wait for message sending
                                        # capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponseTimeElapsed", aka2_title=str(j + 1)+"- " + "Measuring qualification time DTC "  + regex[0][0], aka3_ident='The DTC is qualified or health in  time')
                                        caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                                        caplparam.text =  regex[0][1]
                                        caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                                        caplparam.text =  regex[0][2]
                                        caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                                        caplparam.text =  regex[0][3]
                                        caplparam = SubElement(capltestcase, 'caplparam', aka1_name="aTime1", aka2_type="string")
                                        caplparam.text = str(int(regex[0][4]))
                                        caplparam = SubElement(capltestcase, 'caplparam', aka1_name="aTime2", aka2_type="string")
                                        caplparam.text = str(int(regex[0][5]))
                                    except:
                                        log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                                else:
                                    log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))

                    elif (re.findall(setenv_CRC_BZ_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        # t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(setenv_CRC_BZ_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        t_split = re.split(",\s+", regex[0][1])
                        if (t_split == None):
                            check_error = 1
                            catch_error = "Generate may be error, Please check Test step keyword row: " + str(i + 1) + ", step " + str(j + 1)
                            Function.checkerror_f(check_error, catch_error)
                        else:
                            try:
                                temp_split = re.split("\s+", t_split[0])
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="setenv_CRC_BZ", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                                for temp in t_split:
                                    temp_split = re.split("\s+", temp)
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name=temp_split[1], aka2_type=temp_split[0])
                                    caplparam.text = temp_split[2]
                            except:
                                log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                    elif (re.findall(Check_Eventmessage_failure_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        # t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(Check_Eventmessage_failure_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        t_split = re.split(",\s+", regex[0][1])
                        if (t_split == None):
                            check_error = 1
                            catch_error = "Generate may be error, Please check Test step keyword row: " + str(i + 1) + ", step " + str(j + 1)
                            Function.checkerror_f(check_error, catch_error)
                        else:
                            try:
                                temp_split = re.split("\s+", t_split[0])
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="Check_Eventmessage_failure", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                                for temp in t_split:
                                    temp_split = re.split("\s+", temp)
                                    caplparam = SubElement(capltestcase, 'caplparam', aka1_name=temp_split[1], aka2_type=temp_split[0])
                                    caplparam.text = temp_split[2]
                            except:
                                log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                    # GWM CHB073 PIT 7.27 todo -->  Not yet test *****************************************
                    # elif (re.findall(WaitForSignalValue_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                    #     regex = re.findall(WaitForSignalValue_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                    #     # //wait for message sending
                    #     capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][0] + " Signal to get the value of " + regex[0][1], aka3_ident='-')
                    #     caplparam = SubElement(capltestcase, 'caplparam', aka1_name="SignalName", aka2_type="string")
                    #     caplparam.text = regex[0][0]
                    #     caplparam = SubElement(capltestcase, 'caplparam', aka1_name="ExpectedValue", aka2_type="string")
                    #     caplparam.text = regex[0][1]
                    #     caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Timeout", aka2_type="int")
                    #     caplparam.text = "5000"

                    # todo -->  Not yet test *****************************************
                    elif (re.findall(MeasureEntryTime_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(MeasureEntryTime_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            wait_time = 0
                            n = int(regex[0][1])
                            for i in range(0, n, 20):
                                wait_time = 10
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 10 ms for PDM writing ", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka1_title="wait")
                                # // RequestResponse: DTC is not present
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title=str(j + 1)+"- " + "Read FMHC with 0x1906" + regex[0][2] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][2] + "), DTC is not present")
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                                caplparam.text = "1906" + regex[0][2] + "01"
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                                caplparam.text = "5906" + regex[0][2] + ".{1}[0|8|e].*"
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                                caplparam.text = "Regexp"
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))

                    elif (re.findall(MeasureEntryTime_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(MeasureEntryTime_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            q_time = int(regex[0][1])
                            q_min_time = q_time * 9 / 10
                            q_max_time = q_time * 11 / 10 + 50
                            # RequestResponse: Measuring qualification time
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponseTimeElapsed", aka2_title=str(j + 1)+"- " + "Measuring qualification time of the 0x" + regex[0][2] + "DTC", aka3_ident='The DTC is qualified in qualification time')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "1906" + regex[0][2] + "01"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "5906" + regex[0][2] + ".{1}[9|f].*"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "RegexpNoFailed"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="aTime1", aka2_type="string")
                            caplparam.text = str(int(q_min_time))
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="aTime2", aka2_type="string")
                            caplparam.text = str(int(q_max_time))
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                    elif (re.findall(CRCReg, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(CRCReg, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="CalculateCRCForMessage", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="MessageName", aka2_type="string")
                            caplparam.text = regex[0][0]
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="NrOfExecution", aka2_type="int")
                            caplparam.text = regex[0][1]
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))

                    elif (re.findall(Repeat_ignition_cycles_10_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(Repeat_ignition_cycles_10_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            # //wait for message sending
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="ignition_cycles_10", aka2_title=str(j + 1)+"- " + "Perform 10 ignition cycles" , aka3_ident='-')
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                    elif (re.findall(Repeat_ignition_cycles_9_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(Repeat_ignition_cycles_9_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                        # //wait for message sending
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="ignition_cycles_9", aka2_title=str(j + 1)+"- " + "Perform 9 ignition cycles" , aka3_ident='-')
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                    elif (re.findall(write_variant_ntime_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(write_variant_ntime_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            # //wait for message sending
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="write_variant_ntime", aka2_title=str(j + 1)+"- " + "Perform write variant" +regex[0][3]+ " times" , aka3_ident='-')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = str(regex[0][0])
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = str(regex[0][1])
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = regex[0][2]
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="n", aka2_type="int")
                            caplparam.text = regex[0][3]
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                    #todo --> test later
                    #========================================================================================================================
                    # =============================DTC check for event message===============================================================
                    # =======================================================================================================================
                    elif (re.findall(DTC_check_CRC_Event_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(DTC_check_CRC_Event_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            qualification_ev = int(regex[0][4])
                            healing_ev = int(regex[0][5])
                            # clear DTC
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "14ffffff"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "54"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Equal"
                            # RequestResponse: DTC not present
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][3] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][3] + "), DTC not present")
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "1906" + regex[0][3] + "01"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "5906" + regex[0][3] + ".0"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Regexp"
                            # set CRC fault with setting the CRC field to -1
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Set CRC error for message", aka3_ident='DTC 0x' + regex[0][2] + " is qualifying (0x01)")
                            set = SubElement(testcase, 'set', aka1_title=regex[0][2])
                            envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][2])
                            envvar.text = "-1"
                            #send message (qualicfication time check)
                            for i in range (qualification_ev-1):
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Transmit Message", aka3_ident='Message Transmitted')
                                # testcase.text = regex[0][0]
                                set = SubElement(testcase,"set", aka1_title=regex[0][1])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][1])
                                envvar.text = "1"
                                wait = SubElement(testcase,"wait", aka1_time=str(100), aka1_title="wait")
                                set = SubElement(testcase, "set", aka1_title=regex[0][1])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][1])
                                envvar.text = "0"
                                wait = SubElement(testcase, "wait", aka1_time=str(100), aka1_title="wait")
                            # READ DTC
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="READ DTC with 0x19 02 09", aka3_ident='No DTC received')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "190209"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "5902.{2}"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Regexp"
                            #send message (qualicfication time check)
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Transmit Message", aka3_ident='Message Transmitted')
                            # testcase.text = regex[0][0]
                            set = SubElement(testcase, "set", aka1_title=regex[0][1])
                            envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][1])
                            envvar.text = "1"
                            wait = SubElement(testcase, "wait", aka1_time=str(100), aka1_title="wait")
                            set = SubElement(testcase, "set", aka1_title=regex[0][1])
                            envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][1])
                            envvar.text = "0"
                            wait = SubElement(testcase, "wait", aka1_time=str(100), aka1_title="wait")
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="READ DTC with 0x19 02 09", aka3_ident='Positive response is Received ')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "190209"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "5902.{2}" + regex[0][3] + ".{1}[9|f]"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Regexp"
                            # RequestResponse: Check for MID
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Check for MID 0x", aka3_ident='DTC')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "1906"+ regex[0][3] + "02"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "5906" + regex[0][3] + ".{1}[9|f].*"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Regexp"

                            # clear CRC fault with setting the CRC field to 0
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Set CRC error for message", aka3_ident='DTC 0x' + regex[0][2] + " is qualifying (0x01)")
                            set = SubElement(testcase, 'set', aka1_title=regex[0][2])
                            envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][2])
                            envvar.text = "0"
                            # send message (healing time check)
                            for i in range(healing_ev):
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Transmit Message", aka3_ident='Message Transmitted')
                                # testcase.text = regex[0][0]
                                set = SubElement(testcase, "set", aka1_title=regex[0][1])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][1])
                                envvar.text = "1"
                                wait = SubElement(testcase, "wait", aka1_time=str(100), aka1_title="wait")
                                set = SubElement(testcase, "set", aka1_title=regex[0][1])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][1])
                                envvar.text = "0"
                                wait = SubElement(testcase, "wait", aka1_time=str(100), aka1_title="wait")

                            # RequestResponse: Check for healing
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Check DTC status 0x", aka3_ident='The DTC is healed ')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "1906" + regex[0][3] + "02"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "5906" + regex[0][3] + ".{1}[0|8|e].*"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Regexp"
                            # clear DTC
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "14ffffff"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "54"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Equal"
                            # READ DTC
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="READ DTC with 0x19 02 09", aka3_ident='No DTC received')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "190209"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "5902.{2}"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Regexp"
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))

                    # todo --> test later
                    # DTC check BZ for event message
                    elif (re.findall(DTC_check_BZ_Event_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(DTC_check_BZ_Event_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            qualification_ev = int(regex[0][4])
                            healing_ev = int(regex[0][5])
                            # clear DTC
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "14ffffff"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "54"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Equal"
                            # RequestResponse: DTC not present
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][3] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][3] + "), DTC not present")
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "1906" + regex[0][3] + "01"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "5906" + regex[0][3] + ".0"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Regexp"
                            # set BZ fault with setting the BZ field to -1
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Set BZ error for message", aka3_ident='DTC 0x' + regex[0][2] + " is qualifying (0x01)")
                            set = SubElement(testcase, 'set', aka1_title=regex[0][2])
                            envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][2])
                            envvar.text = "-1"
                            # send message (qualicfication time check-1)
                            for i in range(qualification_ev-1):
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Transmit Message", aka3_ident='Message Transmitted')
                                # testcase.text = regex[0][0]
                                set = SubElement(testcase, "set", aka1_title=regex[0][1])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][1])
                                envvar.text = "1"
                                wait = SubElement(testcase, "wait", aka1_time=str(100), aka1_title="wait")
                                set = SubElement(testcase, "set", aka1_title=regex[0][1])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][1])
                                envvar.text = "0"
                                wait = SubElement(testcase, "wait", aka1_time=str(100), aka1_title="wait")
                            # READ DTC
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="READ DTC with 0x19 02 09", aka3_ident='No DTC received')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "190209"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "5902.{2}"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Regexp"
                            # send message (qualicfication time check)
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Transmit Message", aka3_ident='Message Transmitted')
                            # testcase.text = regex[0][0]
                            set = SubElement(testcase, "set", aka1_title=regex[0][1])
                            envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][1])
                            envvar.text = "1"
                            wait = SubElement(testcase, "wait", aka1_time=str(100), aka1_title="wait")
                            set = SubElement(testcase, "set", aka1_title=regex[0][1])
                            envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][1])
                            envvar.text = "0"
                            wait = SubElement(testcase, "wait", aka1_time=str(100), aka1_title="wait")
                            # READ DTC
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="READ DTC with 0x19 02 09", aka3_ident='Positive response is Received ')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "190209"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "5902.{2}" + regex[0][3] + ".{1}[f|9]"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Regexp"
                            # RequestResponse: Check for MID
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Check for MID 0x", aka3_ident='DTC')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "1906" + regex[0][3] + "02"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "5906" + regex[0][3] + ".{1}[f|b|9].*"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Regexp"
                            # clear BZ fault with setting the BZ field to 0
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="clear BZ error for message", aka3_ident='DTC 0x' + regex[0][2] + " is qualifying (0x01)")
                            set = SubElement(testcase, 'set', aka1_title=regex[0][2])
                            envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][2])
                            envvar.text = "0"
                            # send message (healing time check)
                            for i in range(healing_ev):
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Transmit Message", aka3_ident='Message Transmitted')
                                # testcase.text = regex[0][0]
                                set = SubElement(testcase, "set", aka1_title=regex[0][1])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][1])
                                envvar.text = "1"
                                wait = SubElement(testcase, "wait", aka1_time=str(100), aka1_title="wait")
                                set = SubElement(testcase, "set", aka1_title=regex[0][1])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][1])
                                envvar.text = "0"
                                wait = SubElement(testcase, "wait", aka1_time=str(100), aka1_title="wait")
                            # RequestResponse: Check for healing
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Check DTC status 0x", aka3_ident='The DTC is healed ')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "1906" + regex[0][3] + "02"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "5906" + regex[0][3] + ".{1}[0|8|e].*"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Regexp"
                            # clear DTC
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "14ffffff"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "54"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Equal"
                            # READ DTC
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="READ DTC with 0x19 02 09", aka3_ident='No DTC received')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "190209"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "5902.{2}"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Regexp"
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))

                    # DTC check invalid signal  for event message
                    elif (re.findall(DTC_check_invalid_signal_Event_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(DTC_check_invalid_signal_Event_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            qualification_ev = int(regex[0][4])
                            healing_ev = int(regex[0][5])
                            # clear DTC
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "14ffffff"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "54"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Equal"
                            # RequestResponse: DTC not present
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][4] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][4] + "), DTC not present")
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "1906" + regex[0][4] + "01"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "5906" + regex[0][4] + ".0"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Regexp"
                            # SaveSignalValue
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="SaveSignalValue", aka2_title="Save Signal Value", aka3_ident='-')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="EnvvarName", aka2_type="string")
                            caplparam.text = regex[0][2]
                            # set envvar value to the third parameter value
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Set signal to value " + regex[0][3], aka3_ident='DTC 0x' + regex[0][4] + " is qualifying (0x01)")
                            set = SubElement(testcase, 'set', aka1_title=regex[0][2])
                            envvar = SubElement(set, 'envvar', aka1_name=regex[0][2])
                            envvar.text = regex[0][3]
                            # send message (qualicfication time check-1)
                            for i in range(qualification_ev-1):
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Transmit Message", aka3_ident='Message Transmitted')
                                # testcase.text = regex[0][0]
                                set = SubElement(testcase, "set", aka1_title=regex[0][1])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][1])
                                envvar.text = "1"
                                wait = SubElement(testcase, "wait", aka1_time=str(100), aka1_title="wait")
                                set = SubElement(testcase, "set", aka1_title=regex[0][1])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][1])
                                envvar.text = "0"
                                wait = SubElement(testcase, "wait", aka1_time=str(100), aka1_title="wait")
                            # READ DTC
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="READ DTC with 0x19 02 09", aka3_ident='No DTC received')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "190209"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "5902.{2}"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Regexp"
                            # send message (qualicfication time check)
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Transmit Message", aka3_ident='Message Transmitted')
                            # testcase.text = regex[0][0]
                            set = SubElement(testcase, "set", aka1_title=regex[0][1])
                            envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][1])
                            envvar.text = "1"
                            wait = SubElement(testcase, "wait", aka1_time=str(100), aka1_title="wait")
                            set = SubElement(testcase, "set", aka1_title=regex[0][1])
                            envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][1])
                            envvar.text = "0"
                            wait = SubElement(testcase, "wait", aka1_time=str(100), aka1_title="wait")
                            # READ DTC
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="READ DTC with 0x19 02 09", aka3_ident='Positive response is Received ')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "190209"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "5902.{2}" + regex[0][4] + ".{1}[f|b|9].*"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Regexp"
                            # RequestResponse: Check for MID
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Check for MID 0x", aka3_ident='DTC')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "1906" + regex[0][4] + "02"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "5906" + regex[0][4] + ".{1}[f|b|9].*"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Regexp"
                            # clear signal fault with RestoreSignalValue
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RestoreSignalValue", aka2_title="Set signal to default value", aka3_ident='-')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="EnvvarName", aka2_type="string")
                            caplparam.text = regex[0][2]
                            # send message (healing time check)
                            for i in range(healing_ev):
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Transmit Message", aka3_ident='Message Transmitted')
                                # testcase.text = regex[0][0]
                                set = SubElement(testcase, "set", aka1_title=regex[0][1])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][1])
                                envvar.text = "1"
                                wait = SubElement(testcase, "wait", aka1_time=str(100), aka1_title="wait")
                                set = SubElement(testcase, "set", aka1_title=regex[0][1])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][1])
                                envvar.text = "0"
                                wait = SubElement(testcase, "wait", aka1_time=str(100), aka1_title="wait")
                            # RequestResponse: Check for healing
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Check DTC status 0x", aka3_ident='The DTC is healed ')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "1906" + regex[0][4] + "02"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "5906" + regex[0][4] + ".{1}[0|8|e].*"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Regexp"
                            # clear DTC
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "14ffffff"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "54"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Equal"
                            # READ DTC
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="READ DTC with 0x19 02 09", aka3_ident='No DTC received')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "190209"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "5902.{2}"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Regexp"
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                    # DTC check DLC  for event message
                    elif (re.findall(DTC_check_DLC_Event_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(DTC_check_DLC_Event_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            qualification_ev = int(regex[0][5])
                            healing_ev = int(regex[0][6])
                            # clear DTC
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "14ffffff"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "54"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Equal"
                            # RequestResponse: DTC not present
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][4] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][4] + "), DTC not present")
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "1906" + regex[0][4] + "01"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "5906" + regex[0][4] + ".0"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Regexp"
                            # set "Enable for wrong DLC" to 1 and set DLC number to 7
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Enable wrong DLC for the message", aka2_ident='DTC 0x' + regex[0][4] + ' is qualifying (0x01)')
                            set = SubElement(testcase, 'set', aka1_title=regex[0][2])
                            envvar = SubElement(set, 'envvar', aka1_name=regex[0][2])
                            envvar.text = "1"
                            set = SubElement(testcase, 'set', aka1_title=regex[0][3])
                            envvar = SubElement(set, 'envvar', aka1_name=regex[0][3])
                            envvar.text = "7"
                            # send message (qualicfication time check-1)
                            for i in range(qualification_ev-1):
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Transmit Message", aka2_ident='Message Transmitted ', aka3_type= "string")
                                # testcase.text = regex[0][0]
                                set = SubElement(testcase, "set", aka1_title=regex[0][1])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][1])
                                envvar.text = "1"
                                wait = SubElement(testcase, "wait", aka1_time=str(100), aka1_title="wait")
                                set = SubElement(testcase, "set", aka1_title=regex[0][1])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][1])
                                envvar.text = "0"
                                wait = SubElement(testcase, "wait", aka1_time=str(100), aka1_title="wait")
                            # READ DTC
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="READ DTC with 0x19 02 09", aka3_ident='No DTC received')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "190209"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "5902.{2}"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Regexp"
                            # send message (qualicfication time check)
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Transmit Message", aka2_ident='Message Transmitted',aka3_name= "string")
                            # testcase.text = regex[0][0]
                            set = SubElement(testcase, "set", aka1_title=regex[0][1])
                            envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][1])
                            envvar.text = "1"
                            wait = SubElement(testcase, "wait", aka1_time=str(100), aka1_title="wait")
                            set = SubElement(testcase, "set", aka1_title=regex[0][1])
                            envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][1])
                            envvar.text = "0"
                            wait = SubElement(testcase, "wait", aka1_time=str(100), aka1_title="wait")
                            # READ DTC
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="READ DTC with 0x19 02 09", aka3_ident='Positive response is Received ')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "190209"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "5902.{2}" + regex[0][4] + ".{1}[f|b|9].*"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Regexp"
                            # RequestResponse: Check for MID
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Check for MID 0x", aka3_ident='DTC')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "1906" + regex[0][4] + "02"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "5906" + regex[0][4] + ".{1}[f|b|9].*"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Regexp"
                            # clear "Enable for wrong DLC"
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Disable wrong DLC for the message", aka2_ident='DTC 0x' + regex[0][4] + ' is healing')
                            set = SubElement(testcase, 'set', aka1_title=regex[0][2])
                            envvar = SubElement(set, 'envvar', aka1_name=regex[0][2])
                            envvar.text = "0"
                            # send message (healing time check)
                            for i in range(healing_ev):
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Transmit Message", aka3_ident='Message Transmitted')
                                # testcase.text = regex[0][0]
                                set = SubElement(testcase, "set", aka1_title=regex[0][1])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][1])
                                envvar.text = "1"
                                wait = SubElement(testcase, "wait", aka1_time=str(100), aka1_title="wait")
                                set = SubElement(testcase, "set", aka1_title=regex[0][1])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][1])
                                envvar.text = "0"
                                wait = SubElement(testcase, "wait", aka1_time=str(100), aka1_title="wait")
                            # RequestResponse: Check for healing
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Check DTC status 0x", aka3_ident='The DTC is healed ')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "1906" + regex[0][4] + "02"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "5906" + regex[0][4] + ".{1}[0|8|e].*"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Regexp"
                            # clear DTC
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "14ffffff"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "54"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Equal"
                            # READ DTC
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="READ DTC with 0x19 02 09", aka3_ident='No DTC received')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "190209"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "5902.{2}"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Regexp"
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))

                    elif (re.findall(DTC_check_Timeout_Msg_handle_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall("(\w+)[,\)]", t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            number_msg = int(regex[1])
                            q_time = int(regex[number_msg + 3])
                            q_min_time = q_time * 9 / 10
                            q_max_time = q_time * 11 / 10
                            if (q_time <= 100):
                                q_max_time = q_time * 12 / 10
                                q_min_time = q_time * 8 / 10
                            h_time = int(regex[number_msg + 4])
                            wait_time = 0
                            # clear DTC
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "14ffffff"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "54"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Equal"
                            # wait for 100% of qualification time
                            wait_time = q_time * 2;
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 2 times 100% of qualification time (" + str(wait_time) + "ms)", aka3_ident='-')
                            wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka2_title="wait")

                            # RequestResponse: DTC not present
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[number_msg + 2] + "01", aka3_ident='Positive response is returned (0x5906' + regex[2] + "), DTC not present")
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "1906" + regex[number_msg + 2] + "01"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "5906" + regex[number_msg + 2] + ".0"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Regexp"

                            # wait for message sending
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0], aka3_ident='Message arrived')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="MessageName", aka2_type="string")
                            caplparam.text = regex[0]
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Timeout", aka2_type="int")
                            caplparam.text = "5000"

                            for i in range(2, number_msg + 2):
                                # switch off cyclic sending of message with envvar set to 0
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Disable Cyclic Tx for the message", aka3_ident='DTC 0x' + regex[number_msg + 2] + " is qualifying (0x01)")
                                set = SubElement(testcase, 'set', aka1_title=regex[i])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[i])
                                envvar.text = "0"
                            # RequestResponse: Measuring qualification time
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponseTimeElapsed", aka2_title="Measuring qualification time of the 0x" + regex[2] + "DTC", aka3_ident='The DTC is qualified in qualification time')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "1906" + regex[number_msg + 2] + "01"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "5906" + regex[number_msg + 2] + ".{1}[f|b|9].*"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "RegexpNoFailed"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="aTime1", aka2_type="string")
                            caplparam.text = str(int(q_min_time))
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="aTime2", aka2_type="string")
                            caplparam.text = str(int(q_max_time))
                            # //RequestResponse: Priority check. If the priority in the parameters is set to 0 no priority check will be requested. If the priority is a valid number a RequestResponse will ba added.
                            priority = int(regex[number_msg+5])
                            if (priority > 10):
                                capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[number_msg + 2] + '01', aka3_ident='Field #8 contains DTC priority ' + regex[number_msg + 5])
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                                caplparam.text = "1906" + regex[number_msg + 2] + "01"
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                                caplparam.text = "5906" + regex[number_msg + 2] + "09.{2}0" + regex[number_msg + 5] + '.*'
                                caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                                caplparam.text = "Regexp"
                            for i in range(2, number_msg + 2):
                                # //switch on cyclic sending of message with envvar set to 1
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Enable Cyclic Tx for the message", aka3_ident='DTC 0x' + regex[number_msg + 2] + " is healing")
                                set = SubElement(testcase, 'set', aka1_title=regex[i])
                                envvar = SubElement(set, 'envvar', aka1_name="" + regex[i])
                                envvar.text = "1"
                            # //wait for message sending
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0], aka3_ident='Message arrived')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="MessageName", aka2_type="string")
                            caplparam.text = regex[0]
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Timeout", aka2_type="int")
                            caplparam.text = "5000"
                            # //wait 110% of healing time
                            wait_time = h_time * 11 / 10
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait ~110% of healing time (" + str(int(wait_time)) + "ms)", aka3_ident='-')
                            wait = SubElement(testcase, 'wait', aka1_time=str(int(wait_time)), aka1_title="wait")
                            if (h_time < 50):
                                wait_time = 10;
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 10 ms for PDM writing ", aka3_ident='-')
                                wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka1_title="wait")

                                # // RequestResponse: DTC is not present
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[number_msg + 2] + "01", aka3_ident='Positive response is returned (0x5906' + regex[number_msg + 2] + "), DTC is not present")
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "1906" + regex[number_msg + 2] + "01"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            caplparam.text = "5906" + regex[number_msg + 2] + ".{1}[0|8|e].*"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Regexp"
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))



                    # =======================================================================================================================
                    # =============================CANTP_gen_TC =============================================================================
                    # =======================================================================================================================
                    elif(re.findall(SendDiagFrame_Req,t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(SendDiagFrame_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="SendDiagFrame", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_type="int", aka2_name="messageID")
                            caplparam.text = regex[0][0]
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_type="int", aka2_name="DLC")
                            caplparam.text = regex[0][1]
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_type="string", aka2_name="frame")
                            caplparam.text = str(regex[0][2])
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_type="int", aka2_name="deltaT")
                            caplparam.text = regex[0][3]
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                    elif(re.findall(SetUseFC_Req,t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(SetUseFC_Req,t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="SetUseFC", aka2_title=str(j + 1)+"- " + t_step_by_test_step_arr[i].step_contain[j])
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="value", aka2_type="int")
                            caplparam.text = regex[0]
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title=t_step_by_test_step_arr[i].step_contain[j], aka3_ident="")
                            set = SubElement(testcase, 'set', aka2_title="EnvUseFC", aka3_ident="")
                            envvar = SubElement(set, 'envvar', aka1_name="EnvUseFC" )
                            envvar.text = regex[0]
                            wait = SubElement(testcase, 'wait', aka1_time=str(1000), aka1_title="wait")
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                    elif(re.findall(Check_Diagnosis_Trace_Req,t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        testcase = SubElement(arr_rank[main_cl.rank], 'testcase',  aka2_title=str(j + 1)+"- " + "Check Diagnosis Trace", aka3_ident="")
                        testerconfirmation = SubElement(testcase, 'testerconfirmation',  aka1_title="Check Diagnosis Trace", )
                        testerconfirmation.text = t_step_by_test_response_arr[i].step_contain[j]

                    elif (re.findall(StartPerformanceTest_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name=str(j + 1)+"- " + "StartPerformanceTest", aka2_title="Start Performance Test")
                        capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="CheckStatisticData", aka2_title="Check Statistic Data")
                    elif (re.findall(StartTimeoutTest_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(StartTimeoutTest_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name=str(j + 1)+"- " + "StartTimeoutTest", aka2_title=t_step_by_test_step_arr[i].step_contain[j])
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="timeoutpar", aka2_type="string")
                            caplparam.text = str(regex[0])
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))
                    # =======================================================================================================================


                    # =======================================================================================================================
                    # =============================FOr new template: DTC check EVENT method =================================================
                    # =======================================================================================================================
                    elif (re.findall(DTC_check_DLC_EventCount_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(DTC_check_DLC_EventCount_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            q_time = int((int(regex[0][dlc_ec.Flv_p]))/(int(regex[0][dlc_ec.Fup_p])))
                            h_time = int((int(regex[0][dlc_ec.Flv_p]))/(int(regex[0][dlc_ec.Fdown_p])))
                            # check qualification time
                            # clear DTC
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                            Function.clearDTC_f(capltestcase)
                            # wait 5000 ms
                            wait_time = 5000
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 5000ms  ", aka3_ident='-')
                            wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka1_title="wait")
                            # RequestResponse: DTC not present
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][dlc_ec.dtcnum_p] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][dlc_ec.dtcnum_p] + "), DTC not present")
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "1906" + regex[0][dlc_ec.dtcnum_p] + "01"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            if(re.findall("SAIC", t_test_module, re.IGNORECASE)):
                                caplparam.text = "5906" + regex[0][dlc_ec.dtcnum_p] + ".0.*"
                            else:
                                caplparam.text = "5906" + regex[0][dlc_ec.dtcnum_p] + ".0"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Regexp"
                            # wait for message sending
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][dlc_ec.msname_p], aka3_ident='Message arrived')
                            Function.wait_msgsend_f(capltestcase, regex[0][dlc_ec.msname_p])
                            #turn off cyclic message
                            if (regex[0][dlc_ec.mscycl] != "None") and (regex[0][dlc_ec.mscycl] != "none")and (regex[0][dlc_ec.mscycl] != ""):
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Turn off cyclic message", aka2_ident='')
                                set = SubElement(testcase, 'set', aka1_title=regex[0][dlc_ec.mscycl])
                                envvar = SubElement(set, 'envvar', aka1_name=regex[0][dlc_ec.mscycl])
                                envvar.text = "0"
                            # set "Enable for wrong DLC" to 1 and set DLC number to 0
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Enable wrong DLC for the message", aka2_ident='DTC 0x' + regex[0][dlc_ec.dtcnum_p] + ' is qualifying (0x01)')
                            set = SubElement(testcase, 'set', aka1_title=regex[0][dlc_ec.envarset_p])
                            envvar = SubElement(set, 'envvar', aka1_name=regex[0][dlc_ec.envarset_p])
                            envvar.text = "1"
                            set = SubElement(testcase, 'set', aka1_title=regex[0][dlc_ec.envardlc_p])
                            envvar = SubElement(set, 'envvar', aka1_name=regex[0][dlc_ec.envardlc_p])
                            envvar.text = "0"
                            if (q_time-1)>0 :
                                for count in range (0,q_time-1,1):
                                    testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Transmit Message:", aka3_ident='Message Transmitted')
                                    # message transmit
                                    Function.transmitmgs_f(testcase, regex[0][dlc_ec.mstrs_p])
                            # RequestResponse: Measuring qualification time with count-1
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Measuring qualification time ((DTC is not logged) :Read FMHC with 0x1906" + regex[0][dlc_ec.dtcnum_p] + '01', aka3_ident='Positive response is returned (0x5906' + regex[0][dlc_ec.dtcnum_p])
                            Function.request_response_DTC_f(capltestcase, regex[0][dlc_ec.dtcnum_p], ".{1}[0|e|8].*")
                            # transmit message
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Transmit Message:", aka3_ident='Message Transmitted')
                            Function.transmitmgs_f(testcase, regex[0][dlc_ec.mstrs_p])
                            # wait 10 ms for PDM writing
                            wait_time = 10
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 10 ms for PDM writing  ", aka3_ident='-')
                            wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka1_title="wait")
                            # RequestResponse: Measuring qualification time with manual
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Measuring qualification time ((DTC status is active): Read FMHC with 0x1906" + regex[0][dlc_ec.dtcnum_p] + '01', aka3_ident='Positive response is returned (0x5906' + regex[0][dlc_ec.dtcnum_p])
                            Function.request_response_DTC_f(capltestcase, regex[0][dlc_ec.dtcnum_p], ".{1}[f|b|9].*")

                            # "Disable for wrong DLC"
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Disable wrong DLC for the message", aka2_ident='DTC 0x' + regex[0][dlc_ec.dtcnum_p] + ' is healing')
                            set = SubElement(testcase, 'set', aka1_title=regex[0][dlc_ec.envarset_p])
                            envvar = SubElement(set, 'envvar', aka1_name=regex[0][dlc_ec.envarset_p])
                            envvar.text = "0"
                            if (h_time-1)>0 :
                                for count in range (0,h_time-1,1):
                                    testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Transmit Message:", aka3_ident='Message Transmitted')
                                    #  message transmit
                                    Function.transmitmgs_f(testcase, regex[0][dlc_ec.mstrs_p])
                            #  RequestResponse: DTC present with active state
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Measuring healing time(DTC status is active): Read FMHC with 0x1906" + regex[0][dlc_ec.dtcnum_p] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][dlc_ec.dtcnum_p] + "), DTC is not present")
                            Function.request_response_DTC_f(capltestcase, regex[0][dlc_ec.dtcnum_p], ".{1}[f|b|9].*")
                            # transmit message
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Transmit Message:", aka3_ident='Message Transmitted')
                            Function.transmitmgs_f(testcase, regex[0][dlc_ec.mstrs_p])
                            # wait 10 ms for PDM writing
                            wait_time = 10
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 10 ms for PDM writing  ", aka3_ident='-')
                            wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka1_title="wait")
                            #  RequestResponse: DTC present with active state
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Measuring healing time(DTC status is passive) :Read FMHC with 0x1906" + regex[0][dlc_ec.dtcnum_p] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][dlc_ec.dtcnum_p] + "), DTC is not present")
                            Function.request_response_DTC_f(capltestcase, regex[0][dlc_ec.dtcnum_p], ".{1}[0|e|8].*")
                            # turn on cyclic message
                            if (regex[0][dlc_ec.mscycl] != "None") and (regex[0][dlc_ec.mscycl] != "none") and (regex[0][dlc_ec.mscycl] != ""):
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Turn off cyclic message", aka2_ident='')
                                set = SubElement(testcase, 'set', aka1_title=regex[0][dlc_ec.mscycl])
                                envvar = SubElement(set, 'envvar', aka1_name=regex[0][dlc_ec.mscycl])
                                envvar.text = "1"
                            # clear DTC
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                            Function.clearDTC_f(capltestcase)
                            #	wait 2s before run next TC
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait 2000ms before run next TC ", aka3_ident='-')
                            wait = SubElement(testcase, 'wait', aka1_time=str(2020), aka1_title="wait")
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))

                    elif (re.findall(DTC_check_CRC_EventCount_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(DTC_check_CRC_EventCount_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            q_time = int((int(regex[0][crc_ec.Flv_p])) / (int(regex[0][crc_ec.Fup_p])))
                            h_time = int((int(regex[0][crc_ec.Flv_p])) / (int(regex[0][crc_ec.Fdown_p])))
                            # clear DTC
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                            Function.clearDTC_f(capltestcase)
                            # wait 5000 ms
                            wait_time = 5000
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 5000ms  ", aka3_ident='-')
                            wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka1_title="wait")
                            # RequestResponse: DTC not present
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][crc_ec.dtcnum_p] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][crc_ec.dtcnum_p] + "), DTC not present")
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "1906" + regex[0][crc_ec.dtcnum_p] + "01"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            if (re.findall("SAIC", t_test_module, re.IGNORECASE)):
                                caplparam.text = "5906" + regex[0][crc_ec.dtcnum_p] + ".0.*"
                            else:
                                caplparam.text = "5906" + regex[0][crc_ec.dtcnum_p] + ".0"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Regexp"
                            # wait for message sending
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][crc_ec.msname_p], aka3_ident='-')
                            Function.wait_msgsend_f(capltestcase, regex[0][crc_ec.msname_p])
                            # turn off cyclic message
                            if (regex[0][crc_ec.mscycl] != "None") and (regex[0][crc_ec.mscycl] != "none") and (regex[0][crc_ec.mscycl] != ""):
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Turn off cyclic message", aka2_ident='')
                                set = SubElement(testcase, 'set', aka1_title=regex[0][crc_ec.mscycl])
                                envvar = SubElement(set, 'envvar', aka1_name=regex[0][crc_ec.mscycl])
                                envvar.text = "0"
                            # set CRC fault with setting the CRC field to -1
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Set CRC error for message", aka3_ident='DTC 0x' + regex[0][crc_ec.dtcnum_p] + " is qualifying (0x01)")
                            set = SubElement(testcase, 'set', aka1_title=regex[0][crc_ec.envarcrc_p])
                            envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][crc_ec.envarcrc_p])
                            envvar.text = "-1"
                            # transmit message
                            if (q_time - 1) > 0:
                                for count in range(0, q_time - 1, 1):
                                    testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Transmit Message:", aka3_ident='Message Transmitted')
                                    # Transmit message
                                    Function.transmitmgs_f(testcase, regex[0][crc_ec.mstrs_p])

                            # RequestResponse: Measuring qualification time with count-1
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Measuring qualification time ((DTC is not logged): Read FMHC with 0x1906" + regex[0][crc_ec.dtcnum_p] + '01', aka3_ident='Positive response is returned (0x5906' + regex[0][crc_ec.dtcnum_p])
                            Function.request_response_DTC_f(capltestcase, regex[0][crc_ec.dtcnum_p], ".{1}[0|e|8].*")
                            # transmit message
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Transmit Message:", aka3_ident='Message Transmitted')
                            Function.transmitmgs_f(testcase, regex[0][crc_ec.mstrs_p])
                            # wait 10 ms for PDM writing
                            wait_time = 10
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 10 ms for PDM writing  ", aka3_ident='-')
                            wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka1_title="wait")
                            # RequestResponse: Measuring qualification time with count
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Measuring qualification time ((DTC is active): Read FMHC with 0x1906" + regex[0][crc_ec.dtcnum_p] + '01', aka3_ident='Positive response is returned (0x5906' + regex[0][crc_ec.dtcnum_p])
                            Function.request_response_DTC_f(capltestcase, regex[0][crc_ec.dtcnum_p], ".{1}[f|b|9].*")
                            # clear CRC fault with setting the CRC field to 0
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Clear CRC error for message", aka3_ident='DTC 0x' + regex[0][crc_ec.dtcnum_p] + " is healing")
                            set = SubElement(testcase, 'set', aka1_title=regex[0][crc_ec.envarcrc_p])
                            envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][crc_ec.envarcrc_p])
                            envvar.text = "0"
                            if (h_time - 1) > 0:
                                for count in range(0, h_time - 1, 1):
                                    testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Transmit Message:", aka3_ident='Message Transmitted')
                                    # Transmit message
                                    Function.transmitmgs_f(testcase, regex[0][crc_ec.mstrs_p])

                            # RequestResponse: Measuring healing time with count-1
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Measuring healing time ((DTC is active): Read FMHC with 0x1906" + regex[0][crc_ec.dtcnum_p] + '01', aka3_ident='Positive response is returned (0x5906' + regex[0][crc_ec.dtcnum_p])
                            Function.request_response_DTC_f(capltestcase, regex[0][crc_ec.dtcnum_p], ".{1}[f|b|9].*")
                            # transmit message
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Transmit Message:", aka3_ident='Message Transmitted')
                            Function.transmitmgs_f(testcase, regex[0][crc_ec.mstrs_p])
                            # wait 10 ms for PDM writing
                            wait_time = 10
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 10 ms for PDM writing  ", aka3_ident='-')
                            wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka1_title="wait")
                            # RequestResponse: Measuring healing time with count
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Measuring healing time ((DTC is not logged): Read FMHC with 0x1906" + regex[0][crc_ec.dtcnum_p] + '01', aka3_ident='Positive response is returned (0x5906' + regex[0][crc_ec.dtcnum_p])
                            Function.request_response_DTC_f(capltestcase, regex[0][crc_ec.dtcnum_p], ".{1}[0|e|8].*")
                            # turn on cyclic message
                            if (regex[0][crc_ec.mscycl] != "None") and (regex[0][crc_ec.mscycl] != "none") and (regex[0][crc_ec.mscycl] != ""):
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Turn off cyclic message", aka2_ident='')
                                set = SubElement(testcase, 'set', aka1_title=regex[0][crc_ec.mscycl])
                                envvar = SubElement(set, 'envvar', aka1_name=regex[0][crc_ec.mscycl])
                                envvar.text = "1"
                            # clear DTC
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                            Function.clearDTC_f(capltestcase)
                            #	wait 2s before run next TC
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait 2000ms before run next TC ", aka3_ident='-')
                            wait = SubElement(testcase, 'wait', aka1_time=str(2020), aka1_title="wait")
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))


                    elif (re.findall(DTC_check_BZ_EventCount_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(DTC_check_BZ_EventCount_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            q_time = int((int(regex[0][bz_ec.Flv_p])) / (int(regex[0][bz_ec.Fup_p])))
                            h_time = int((int(regex[0][bz_ec.Flv_p])) / (int(regex[0][bz_ec.Fdown_p])))
                            # clear DTC
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                            Function.clearDTC_f(capltestcase)
                            # wait 5000 ms
                            wait_time = 5000
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 5000ms  ", aka3_ident='-')
                            wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka1_title="wait")
                            # RequestResponse: DTC not present
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][bz_ec.dtcnum_p] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][bz_ec.dtcnum_p] + "), DTC not present")
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "1906" + regex[0][bz_ec.dtcnum_p] + "01"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            if (re.findall("SAIC", t_test_module, re.IGNORECASE)):
                                caplparam.text = "5906" + regex[0][bz_ec.dtcnum_p] + ".0.*"
                            else:
                                caplparam.text = "5906" + regex[0][bz_ec.dtcnum_p] + ".0"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Regexp"
                            # wait for message sending
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][bz_ec.msname_p], aka3_ident='-')
                            Function.wait_msgsend_f(capltestcase, regex[0][bz_ec.msname_p])
                            # turn off cyclic message
                            if (regex[0][bz_ec.mscycl] != "None") and (regex[0][bz_ec.mscycl] != "none") and (regex[0][bz_ec.mscycl] != ""):
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Turn off cyclic message", aka2_ident='')
                                set = SubElement(testcase, 'set', aka1_title=regex[0][bz_ec.mscycl])
                                envvar = SubElement(set, 'envvar', aka1_name=regex[0][bz_ec.mscycl])
                                envvar.text = "0"
                            # set BZ fault with setting the BZ field to -1
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Set BZ error for message", aka3_ident='DTC 0x' + regex[0][bz_ec.dtcnum_p] + " is qualifying (0x01)")
                            set = SubElement(testcase, 'set', aka1_title=regex[0][bz_ec.envarbz_p])
                            envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][bz_ec.envarbz_p])
                            envvar.text = "-1"
                            # transmit message
                            if (q_time - 1) > 0:
                                for count in range(0, q_time - 1, 1):
                                    testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Transmit Message:", aka3_ident='Message Transmitted')
                                    # Transmit message
                                    Function.transmitmgs_f(testcase, regex[0][bz_ec.mstrs_p])
                            # RequestResponse: Measuring qualification time with count-1
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Measuring qualification time ((DTC is not logged): Read FMHC with 0x1906" + regex[0][bz_ec.dtcnum_p] + '01', aka3_ident='Positive response is returned (0x5906' + regex[0][bz_ec.dtcnum_p])
                            Function.request_response_DTC_f(capltestcase, regex[0][bz_ec.dtcnum_p], ".{1}[0|e|8].*")
                            # transmit message
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Transmit Message:", aka3_ident='Message Transmitted')
                            Function.transmitmgs_f(testcase, regex[0][bz_ec.mstrs_p])
                            # wait 10 ms for PDM writing
                            wait_time = 10
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 10 ms for PDM writing  ", aka3_ident='-')
                            wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka1_title="wait")
                            # RequestResponse: Measuring qualification time with count
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Measuring qualification time ((DTC is active): Read FMHC with 0x1906" + regex[0][bz_ec.dtcnum_p] + '01', aka3_ident='Positive response is returned (0x5906' + regex[0][bz_ec.dtcnum_p])
                            Function.request_response_DTC_f(capltestcase, regex[0][bz_ec.dtcnum_p], ".{1}[f|b|9].*")
                            # clear BZ fault with setting the CRC field to 0
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Clear BZ error for message", aka3_ident='DTC 0x' + regex[0][bz_ec.dtcnum_p] + " is healing")
                            set = SubElement(testcase, 'set', aka1_title=regex[0][bz_ec.envarbz_p])
                            envvar = SubElement(set, 'envvar', aka1_name="" + regex[0][bz_ec.envarbz_p])
                            envvar.text = "0"
                            if (h_time - 1) > 0:
                                for count in range(0, h_time - 1, 1):
                                    testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Transmit Message:", aka3_ident='Message Transmitted')
                                    # Transmit message
                                    Function.transmitmgs_f(testcase, regex[0][bz_ec.mstrs_p])
                            # RequestResponse: Measuring healing time with count-1
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Measuring healing time ((DTC is active): Read FMHC with 0x1906" + regex[0][bz_ec.dtcnum_p] + '01', aka3_ident='Positive response is returned (0x5906' + regex[0][bz_ec.dtcnum_p])
                            Function.request_response_DTC_f(capltestcase, regex[0][bz_ec.dtcnum_p], ".{1}[f|b|9].*")
                            # transmit message
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Transmit Message:", aka3_ident='Message Transmitted')
                            Function.transmitmgs_f(testcase, regex[0][bz_ec.mstrs_p])
                            # wait 10 ms for PDM writing
                            wait_time = 10
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 10 ms for PDM writing  ", aka3_ident='-')
                            wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka1_title="wait")
                            # RequestResponse: Measuring healing time with count
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Measuring healing time ((DTC is not logged): Read FMHC with 0x1906" + regex[0][bz_ec.dtcnum_p] + '01', aka3_ident='Positive response is returned (0x5906' + regex[0][bz_ec.dtcnum_p])
                            Function.request_response_DTC_f(capltestcase, regex[0][bz_ec.dtcnum_p], ".{1}[0|e|8].*")
                            # turn on cyclic message
                            if (regex[0][bz_ec.mscycl] != "None") and (regex[0][bz_ec.mscycl] != "none") and (regex[0][bz_ec.mscycl] != ""):
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Turn off cyclic message", aka2_ident='')
                                set = SubElement(testcase, 'set', aka1_title=regex[0][bz_ec.mscycl])
                                envvar = SubElement(set, 'envvar', aka1_name=regex[0][bz_ec.mscycl])
                                envvar.text = "1"
                            # clear DTC
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                            Function.clearDTC_f(capltestcase)
                            #	wait 2s before run next TC
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait 2000ms before run next TC ", aka3_ident='-')
                            wait = SubElement(testcase, 'wait', aka1_time=str(2020), aka1_title="wait")
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))

                    elif (re.findall(DTC_check_Signal_EventCount_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(DTC_check_Signal_EventCount_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            q_time = int((int(regex[0][invalid_ec.Flv_p])) / (int(regex[0][invalid_ec.Fup_p])))
                            h_time = int((int(regex[0][invalid_ec.Flv_p])) / (int(regex[0][invalid_ec.Fdown_p])))
                            # clear DTC
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                            Function.clearDTC_f(capltestcase)
                            # wait 5000 ms
                            wait_time = 5000
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 5000ms  ", aka3_ident='-')
                            wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka1_title="wait")
                            # RequestResponse: DTC not present
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Read FMHC with 0x1906" + regex[0][invalid_ec.dtcnum_p] + "01", aka3_ident='Positive response is returned (0x5906' + regex[0][invalid_ec.dtcnum_p] + "), DTC not present")
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
                            caplparam.text = "1906" + regex[0][invalid_ec.dtcnum_p] + "01"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
                            if (re.findall("SAIC", t_test_module, re.IGNORECASE)):
                                caplparam.text = "5906" + regex[0][invalid_ec.dtcnum_p] + ".0.*"
                            else:
                                caplparam.text = "5906" + regex[0][invalid_ec.dtcnum_p] + ".0"
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
                            caplparam.text = "Regexp"
                            # SaveSignalValue
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="SaveSignalValue", aka2_title="Save Signal Value", aka3_ident='-')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="EnvvarName", aka2_type="string")
                            caplparam.text = regex[0][invalid_ec.envarsig_p]
                            # wait for message sending
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="WaitForMessage", aka2_title="Wait for message" + regex[0][invalid_ec.msname_p], aka3_ident='Message arrived')
                            Function.wait_msgsend_f(capltestcase,regex[0][invalid_ec.msname_p])
                            # turn off cyclic message
                            if (regex[0][invalid_ec.mscycl]!= "None") and (regex[0][invalid_ec.mscycl]!= "none") and(regex[0][invalid_ec.mscycl] != ""):
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Turn off cyclic message", aka2_ident='')
                                set = SubElement(testcase, 'set', aka1_title=regex[0][invalid_ec.mscycl])
                                envvar = SubElement(set, 'envvar', aka1_name=regex[0][invalid_ec.mscycl])
                                envvar.text = "0"
                            # set envvar value to the third parameter value
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Set signal to value " + regex[0][invalid_ec.valueinv_p], aka3_ident='DTC 0x' + regex[0][invalid_ec.dtcnum_p] + " is qualifying (0x01)")
                            set = SubElement(testcase, 'set', aka1_title=regex[0][invalid_ec.envarsig_p])
                            envvar = SubElement(set, 'envvar', aka1_name=regex[0][invalid_ec.envarsig_p])
                            envvar.text = regex[0][invalid_ec.valueinv_p]
                            # transmit message
                            if (q_time - 1) > 0:
                                for count in range(0, q_time - 1, 1):
                                    testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Transmit Message:", aka3_ident='Message Transmitted')
                                    # transmit message
                                    Function.transmitmgs_f(testcase, regex[0][invalid_ec.mstrs_p])
                                    # RequestResponse: Measuring qualification time with count-1
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Measuring qualification time ((DTC is not logged): Read FMHC with 0x1906" + regex[0][invalid_ec.dtcnum_p] + '01', aka3_ident='Positive response is returned (0x5906' + regex[0][invalid_ec.dtcnum_p])
                            Function.request_response_DTC_f(capltestcase, regex[0][invalid_ec.dtcnum_p],".{1}[0|e|8].*")
                            # transmit message
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Transmit Message:", aka3_ident='Message Transmitted')
                            Function.transmitmgs_f(testcase, regex[0][invalid_ec.mstrs_p])
                            # wait 10 ms for PDM writing
                            wait_time = 10
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 10 ms for PDM writing  ", aka3_ident='-')
                            wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka1_title="wait")
                            # RequestResponse: Measuring qualification time with count
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Measuring qualification time ((DTC is active): Read FMHC with 0x1906" + regex[0][invalid_ec.dtcnum_p] + '01', aka3_ident='Positive response is returned (0x5906' + regex[0][invalid_ec.dtcnum_p])
                            Function.request_response_DTC_f(capltestcase, regex[0][invalid_ec.dtcnum_p], ".{1}[f|b|9].*")
                            # clear signal fault with RestoreSignalValue
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RestoreSignalValue", aka2_title="Set signal to default value", aka3_ident='-')
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_name="EnvvarName", aka2_type="string")
                            caplparam.text = regex[0][invalid_ec.envarsig_p]
                            if (h_time - 1) > 0:
                                for count in range(0, h_time - 1, 1):
                                    # transmit message
                                    testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Transmit Message:", aka3_ident='Message Transmitted')
                                    Function.transmitmgs_f(testcase, regex[0][invalid_ec.mstrs_p])
                            # RequestResponse: Measuring healing time with count-1
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Measuring healing time ((DTC is active): Read FMHC with 0x1906" + regex[0][invalid_ec.dtcnum_p] + '01', aka3_ident='Positive response is returned (0x5906' + regex[0][invalid_ec.dtcnum_p])
                            Function.request_response_DTC_f(capltestcase,regex[0][invalid_ec.dtcnum_p],".{1}[f|b|9].*")
                            # transmit message
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Transmit Message:", aka3_ident='Message Transmitted')
                            Function.transmitmgs_f(testcase,regex[0][invalid_ec.mstrs_p])
                            # wait 10 ms for PDM writing
                            wait_time = 10
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka2_title="Wait 10 ms for PDM writing  ", aka3_ident='-')
                            wait = SubElement(testcase, 'wait', aka1_time=str(wait_time), aka1_title="wait")
                            # RequestResponse: Measuring healing time with count
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Measuring healing time ((DTC is not logged): Read FMHC with 0x1906" + regex[0][invalid_ec.dtcnum_p] + '01', aka3_ident='Positive response is returned (0x5906' + regex[0][invalid_ec.dtcnum_p])
                            Function.request_response_DTC_f(capltestcase,regex[0][invalid_ec.dtcnum_p],".{1}[0|e|8].*")
                            # turn on cyclic message
                            if (regex[0][invalid_ec.mscycl] != "None") and (regex[0][invalid_ec.mscycl] != "none") and (regex[0][invalid_ec.mscycl] != ""):
                                testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Turn off cyclic message", aka2_ident='')
                                set = SubElement(testcase, 'set', aka1_title=regex[0][invalid_ec.mscycl])
                                envvar = SubElement(set, 'envvar', aka1_name=regex[0][invalid_ec.mscycl])
                                envvar.text = "1"
                            # clear DTC
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="RequestResponse", aka2_title="Clear FMHC with 0x14 FF FF FF", aka3_ident='Positive response is returned (0x54)')
                            Function.clearDTC_f(capltestcase)
                            #	wait 2s before run next TC
                            testcase = SubElement(arr_rank[main_cl.rank], 'testcase', aka1_title="Wait 2000ms before run next TC ", aka3_ident='-')
                            wait = SubElement(testcase, 'wait', aka1_time=str(2020), aka1_title="wait")
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))

                    elif (re.findall(Checking_Configuration_Req, t_step_by_step_keyw_arr[i].step_contain[j])):
                        t_step_by_step_keyw_arr[i].step_contain[j] = re.sub("\s+", "", t_step_by_step_keyw_arr[i].step_contain[j])
                        regex = re.findall(Checking_Configuration_Req, t_step_by_step_keyw_arr[i].step_contain[j])
                        try:
                            capltestcase = SubElement(arr_rank[main_cl.rank], 'capltestcase', aka1_name="Checking_Configuration", aka2_title=str(j + 1) + "- " + t_step_by_test_step_arr[i].step_contain[j], aka3_ident=t_step_by_test_response_arr[i].step_contain[j])
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_type="string", aka2_name="write_VIN")
                            caplparam.text = regex[0][0]
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_type="string", aka2_name="read_VIN")
                            caplparam.text = regex[0][1]
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_type="string", aka2_name="write_Height")
                            caplparam.text = str(regex[0][2])
                            caplparam = SubElement(capltestcase, 'caplparam', aka1_type="string", aka2_name="write_BoardDistance")
                            caplparam.text = regex[0][3]
                        except:
                            log_handle.info("Error: please check parameter in test step keword, row: " + str(i + 1) + ", step " + str(j + 1))


        # if len(main_cl.contains) != 0:

        for loop in range (len(main_cl.contains)):
            hierarchy_check.parent = testmodule
            get_out_data(main_cl.contains[loop],t_data_w, t_step_by_step_keyw_arr, t_step_by_test_step_arr, t_step_by_test_response_arr, t_path_output, object_heading_arr,t_ECAN_main_node, t_SFCAN_main_node)
            global t_progress
            t_progress = t_progress + .43
            ProgressValue_obj.setValue(21+t_progress)


        # else:
        #     for loop in range(len(main_cl.contains)):
        #         if hierarchy_check.element <= len(main_cl.parent.contains):
        #             if (main_cl.parent):
        #                 return (main_cl.parent.contains[hierarchy_check.element],t_data_w, t_step_by_step_keyw_arr, t_step_by_test_step_arr, t_step_by_test_response_arr, t_path_output, object_heading_arr,t_ECAN_main_node, t_SFCAN_main_node)
        #             else:
        #                 return testmodule
        #         else:
        #             temp_grand = main_cl.parent
        #             if (temp_grand.parent):
        #                 return (temp_grand.parent.contains[hierarchy_check.parent],t_data_w, t_step_by_step_keyw_arr, t_step_by_test_step_arr, t_step_by_test_response_arr, t_path_output, object_heading_arr,t_ECAN_main_node, t_SFCAN_main_node)
        #             else:
        #                 return testmodule


    get_out_data(main_cl, t_data_w, t_step_by_step_keyw_arr, t_step_by_test_step_arr, t_step_by_test_response_arr, t_path_output, object_heading_arr, t_ECAN_main_node, t_SFCAN_main_node)
    global myglobal
    myglobal = 0
    tree = Element(hierarchy_check.parent)
    t = minidom.parseString(tostring(testmodule)).toprettyxml()  #
    tree1 = ElementTree(fromstring(t))
    tree1.write("filename.xml", encoding='utf-8', xml_declaration=True)
    ProgressValue_obj.setValue(85)

        # log_handle.info(content)
    # Check error in file log and show if have
    content=""
    with open("information_detail.log", "r") as f:
        content = f.read()
    if re.search("Error",content):
        win32api.MessageBox(0, "Generated may got an error, please find the result in log file", 'ERROR')
        os.startfile('information_detail.log')
        time.sleep(2)
        ProgressValue_obj.setValue(90)
        with open("information_detail.log", "w") as f:
            pass
    # replace some text (to avoid auto sort in element tree ==)
    else:
        with open("filename.xml", "r") as f:
            content = f.read()
            content = re.sub("aka\d+_", "", content)
            content = re.sub("_x000D_", "", content)
        t_path_output = t_path_output + r'\TC_gen.xml'
        with open(t_path_output, "w") as f:
            f.write(content)
        ProgressValue_obj.setValue(100)
        print("Success  ", ProgressValue_obj.getValue())
        cmd_command = r'"C:\Program Files\Notepad++\notepad++.exe" {}'.format(t_path_output)
        notepad_path_check = r'C:\Program Files\Notepad++\notepad++.exe'

        if (os.path.exists(notepad_path_check) == True):
            # log_handle.info(cmd_command)
            # subprocess.call(cmd_command,timeout=5)
            subprocess.Popen(cmd_command)
            # win32api.MessageBox(0, " Generate done -__-", '')
        else:
            cmd_command = r'"C:\Program Files (x86)\Notepad++\notepad++.exe" {}'.format(t_path_output)
            notepad_path_check = r'C:\Program Files (x86)\Notepad++\notepad++.exe'
            if (os.path.exists(notepad_path_check) == True):
                # win32api.MessageBox(0, " Generate done -__-", '')
                subprocess.Popen(cmd_command)
                # subprocess.call(cmd_command,timeout= 5)
            else:
                catch_error = r'Please check the notepad folder (should be "C:\Program Files\Notepad++\notepad++.exe")'
                win32api.MessageBox(0, catch_error, 'ERROR')



        # time.sleep(2)
    # with open("information_detail.log", "w") as f:
    #     f.write(content)
    # f.close()
    # END of XLM file
    # =======================================================

