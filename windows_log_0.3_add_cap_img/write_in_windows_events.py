import win32evtlog
import win32evtlogutil
import win32con
from datetime import datetime,timedelta

def event_viewer_log(event_id,event_strings,description):
    # Log the exception to the Windows Event Log
    log_type = 'iParkRightAnpr'  # You can change this to 'Security', 'System', etc.
    # event_id = 1005  # You can choose a unique event ID
    event_category = 0  # The category of the event (0 for none)
    # description = "Please restart your device . New Data Not Comming."
    # event_strings = [f"Exception occurred: {message}",description]

    # # Additional information for the event

    # task_category = 1  # You can choose an appropriate task category

    # Open the event log for writing
    h_log = win32evtlog.OpenEventLog(None, log_type)

    # Print parameters for debugging
    #print(f"log_type: {log_type}, event_id: {event_id}, event_category: {event_category}, event_strings: {event_strings}")

    win32evtlog.ReportEvent(h_log,win32evtlog.EVENTLOG_ERROR_TYPE,event_category,event_id,None,event_strings,None,)
    win32evtlog.CloseEventLog(h_log)


    return True



def starting_event_TEST():

    # Define your event source and log name
    #event_source = "iParkRight"
    event_log = "iParkRightAnpr"

    # Open the event log for writing
    handle = win32evtlog.OpenEventLog(None, event_log)

    # Define the event category, event ID, and event message
    event_category = 0
    event_id = 1001  # Unique event ID
    event_message = f"ANPR Services Started Successfully - {datetime.now()} "

    # Write an information event
    win32evtlog.ReportEvent(handle, win32evtlog.EVENTLOG_INFORMATION_TYPE, event_category, event_id, None,
                            (event_message,),None)

    # Close the event log handle
    win32evtlog.CloseEventLog(handle)
    return False


