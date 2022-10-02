#==========================================
# Title:  Function
# Author: Nguyen Vu Huan  -  NHY2HC 
# Date:   1- Dec - 2020
#==========================================
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, fromstring, ElementTree
from xml.dom import minidom
import time
import re
import os
import win32api
import subprocess

def trim_space(text):
    trim_txt = re.sub(' ','',text)
    return trim_txt

def msgName(line):
    msgValueOfCanSignalReg = '^(.*) ([A-Z](.*)) |\('
    msgValueOfCanSignalReg2 = '( |)([A-Z].[^\(| ]+)'
    if (re.findall(msgValueOfCanSignalReg2, line)):
        regex = re.findall(msgValueOfCanSignalReg2, line)
        return regex[0][1]
    elif (re.findall(msgValueOfCanSignalReg, line)):
        regex = re.findall(msgValueOfCanSignalReg2, line)
        return regex[0][1]
    else :
        return "nem uzenet"
def SaveSignalValueReq_f(capltestcase,regex):
    caplparam = SubElement(capltestcase,'caplparam', aka1_name="EnvvarName",aka2_type="string")
    caplparam.text = regex[0]

def RestoreSignalValueReq_f(capltestcase,regex):
    caplparam = SubElement(capltestcase,'caplparam', aka1_name="EnvvarName",aka2_type="string")
    caplparam.text = regex[0]

def RequestResponseReg_f(capltestcase,regex):
    caplparam = SubElement(capltestcase,'caplparam', aka1_name="Request",aka2_type="string")
    caplparam.text = regex[0][0]
    caplparam = SubElement(capltestcase,'caplparam', aka1_name="Response", aka2_type="string")
    caplparam.text = str(regex[0][1])
    caplparam = SubElement(capltestcase,'caplparam', aka1_name="CompareMode", aka2_type="string")
    caplparam.text = regex[0][2]

def FunctionalMessageReg_f(capltestcase, regex):
    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
    caplparam.text = regex[0][0]
    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
    caplparam.text = str(regex[0][1])
    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
    caplparam.text = regex[0][2]

def FunctionalMessage_SPRB_f(capltestcase, regex):
    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
    caplparam.text = regex[0][2]

def RequestResponse_SPRB_f(capltestcase, regex):
    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
    caplparam.text = regex[0][2]
    # caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
    # caplparam.text = str(regex[0][1])
    # caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
    # caplparam.text = regex[0][2]
def RequestResponseCanMsgIdReg_f(capltestcase,regex):
    caplparam = SubElement(capltestcase,'caplparam', aka1_name="Request",aka2_type="string")
    caplparam.text = regex[0][0]
    caplparam = SubElement(capltestcase,'caplparam', aka1_name="Response", aka2_type="string")
    caplparam.text = regex[0][1]
    caplparam = SubElement(capltestcase,'caplparam', aka1_name="CompareMode", aka2_type="string")
    caplparam.text = regex[0][2]
    caplparam = SubElement(capltestcase,'caplparam', aka1_name="rxId", aka2_type="int")
    caplparam.text = regex[0][3]
    caplparam = SubElement(capltestcase,'caplparam', aka1_name="rxId", aka2_type="int")
    caplparam.text = regex[0][4]

def ResetCameraReg_f(capltestcase,regex):
    caplparam = SubElement(capltestcase, 'caplparam', aka1_type= "int",aka2_name="WaitTime")
    caplparam.text = regex[0][0]

def waitReg_f(testcase,regex):
    wait = SubElement(testcase, 'wait', aka1_time= regex[0],aka2_title="wait")

def CalcCRCReg_f(capltestcase,regex):
    caplparam = SubElement(capltestcase,'caplparam', aka1_type="string",aka2_name="MessageName")
    caplparam.text = regex[0][0]
    caplparam = SubElement(capltestcase,'caplparam', aka1_type="string", aka2_name="Sid")
    caplparam.text = regex[0][1]
    caplparam = SubElement(capltestcase,'caplparam', aka1_type="int", aka2_name="NrOfExecution")
    caplparam.text = regex[0][2]

def DiagSessionCtrlReg_f(capltestcase,regex):
    caplparam = SubElement(capltestcase,'caplparam', aka1_type="string",aka2_name="sessionName")
    caplparam.text = regex[0]

def SetVoltageReg_f(testcase,regex):
    initialize = SubElement(testcase,'initialize', aka1_title="set",aka2_wait="0")
    envvar = SubElement(initialize, 'envvar', aka1_name="Env_VoltBKValue")
    envvar.text = regex[0]
    envvar = SubElement(initialize, 'envvar', aka1_name="Env_VoltBKSet")
    envvar.text = "1"

def SetSpeedReg_f(testcase,regex):
    initialize = SubElement(testcase,'initialize', aka1_title="",aka2_wait=regex[1])
    #todo --> modify signal or not use this function
    envvar = SubElement(initialize, 'envvar', aka1_name="E_pubc_Gateway_MQB_ESP_21_ESP_v_Signal_Rv")
    envvar.text = regex[0]

def loginReg_f(capltestcase,regex):
    caplparam = SubElement(capltestcase,'caplparam', aka1_type="string",aka2_name="LoginType")
    caplparam.text = regex[0]

def Measurement_value_test_Reg_f(capltestcase,regex):
    caplparam = SubElement(capltestcase,'caplparam', aka1_type="string",aka2_name="ID")
    caplparam.text = regex[0][0]
    caplparam = SubElement(capltestcase, 'caplparam', aka1_type="int", aka2_name="def_session")
    caplparam.text = regex[0][1]
    caplparam = SubElement(capltestcase, 'caplparam', aka1_type="int", aka2_name="ext_session")
    caplparam.text = regex[0][2]
    caplparam = SubElement(capltestcase, 'caplparam', aka1_type="int", aka2_name="eol_session")
    caplparam.text = regex[0][3]
    caplparam = SubElement(capltestcase, 'caplparam', aka1_type="int", aka2_name="dev_session")
    caplparam.text = regex[0][4]
    caplparam = SubElement(capltestcase, 'caplparam', aka1_type="int", aka2_name="prog_session")
    caplparam.text = regex[0][5]
    caplparam = SubElement(capltestcase, 'caplparam', aka1_type="int", aka2_name="login_level")
    caplparam.text = regex[0][6]
    caplparam = SubElement(capltestcase, 'caplparam', aka1_type="int", aka2_name="data_length")
    caplparam.text = regex[0][7]

def Adaption_value_test_Reg_f(capltestcase,regex):
    caplparam = SubElement(capltestcase,'caplparam', aka1_type="string",aka2_name="ID")
    caplparam.text = regex[0][0]
    caplparam = SubElement(capltestcase, 'caplparam', aka1_type="int", aka2_name="def_session")
    caplparam.text = regex[0][1]
    caplparam = SubElement(capltestcase, 'caplparam', aka1_type="int", aka2_name="ext_session")
    caplparam.text = regex[0][2]
    caplparam = SubElement(capltestcase, 'caplparam', aka1_type="int", aka2_name="eol_session")
    caplparam.text = regex[0][3]
    caplparam = SubElement(capltestcase, 'caplparam', aka1_type="int", aka2_name="dev_session")
    caplparam.text = regex[0][4]
    caplparam = SubElement(capltestcase, 'caplparam', aka1_type="int", aka2_name="prog_session")
    caplparam.text = regex[0][5]
    caplparam = SubElement(capltestcase, 'caplparam', aka1_type="int", aka2_name="login_level")
    caplparam.text = regex[0][6]
    caplparam = SubElement(capltestcase, 'caplparam', aka1_type="string", aka2_name="def_value")
    caplparam.text = regex[0][8]
    caplparam = SubElement(capltestcase, 'caplparam', aka1_type="string", aka2_name="test_values")
    caplparam.text = regex[0][9]

def clearDTC_f(capltestcase):
    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
    caplparam.text = "14ffffff"
    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
    caplparam.text = "54"
    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
    caplparam.text = "Equal"

def request_response_DTC_f(capltestcase, regex, dtc_status):
    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
    caplparam.text = "1906" + regex + "01"
    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
    caplparam.text = "5906" + regex + dtc_status
    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
    caplparam.text = "Regexp"
def transmitmgs_f(testcase,regex):
    set = SubElement(testcase, "set", aka1_title=regex)
    envvar = SubElement(set, 'envvar', aka1_name="" + regex)
    envvar.text = "1"
    wait = SubElement(testcase, "wait", aka1_time=str(5), aka1_title="wait")
    set = SubElement(testcase, "set", aka1_title=regex)
    envvar = SubElement(set, 'envvar', aka1_name="" + regex)
    envvar.text = "0"
    wait = SubElement(testcase, "wait", aka1_time=str(5), aka1_title="wait")
def wait_msgsend_f(capltestcase,regex):
    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="MessageName", aka2_type="string")
    caplparam.text = regex
    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Timeout", aka2_type="int")
    caplparam.text = "5000"
def measuringtime_f(capltestcase,regex,timin,timax,dtc_status):
    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Request", aka2_type="string")
    caplparam.text = "1906" + regex + "01"
    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="Response", aka2_type="string")
    caplparam.text = "5906" + regex + dtc_status
    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="CompareMode", aka2_type="string")
    caplparam.text = "RegexpNoFailed"
    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="aTime1", aka2_type="string")
    caplparam.text = str(int(timin))
    caplparam = SubElement(capltestcase, 'caplparam', aka1_name="aTime2", aka2_type="string")
    caplparam.text = str(int(timax))

def statecheck_f (capltestcase,regex,Testresponse):
    statecheck = SubElement(capltestcase, 'statecheck', aka1_title=Testresponse, aka2_wait="-wait-")
    expected = SubElement(statecheck, 'expected')
    cansignal = SubElement(expected, 'cansignal', aka1_name=regex[0][1], aka2_bus= regex[0][2],aka3_msg= regex[0][0], aka4_node = regex[0][3])
    cansignal.text = regex[0][4]

def checkerror_f (check_error, catch_error):
    if (check_error != None):
        win32api.MessageBox(0, catch_error, 'ERROR')

def write_xml_file(parent,testmodule,filename,t_path_output):
    global myglobal
    myglobal = 0
    tree = Element(parent)
    t = minidom.parseString(tostring(testmodule)).toprettyxml()  #
    tree1 = ElementTree(fromstring(t))
    tree1.write(filename, encoding='utf-8', xml_declaration=True)
    # ProgressValue_obj.setValue(85)

    # log_handle.info(content)
    # Check error in file log and show if have
    content = ""
    with open("information_detail.log", "r") as f:
        content = f.read()
    if re.search("Error", content):
        win32api.MessageBox(0, "Generated may got an error, please find the result in log file", 'ERROR')
        os.startfile('information_detail.log')
        time.sleep(2)
        # ProgressValue_obj.setValue(90)
        with open("information_detail.log", "w") as f:
            pass
    # replace some text (to avoid auto sort in element tree ==)
    else:
        with open(filename, "r") as f:
            content = f.read()
            content = re.sub("aka\d+_", "", content)
            content = re.sub("_x000D_", "", content)
        # t_path_output = t_path_output + r'\TC_gen.xml'
        with open(t_path_output, "w") as f:
            f.write(content)
        # ProgressValue_obj.setValue(100)
        # print("Success  ", ProgressValue_obj.getValue())
        os.remove(filename)
        cmd_command = r'"C:\Program Files\Notepad++\notepad++.exe" {}'.format(t_path_output)
        notepad_path_check = r'C:\Program Files\Notepad++\notepad++.exe'
