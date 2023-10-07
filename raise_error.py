import win32evtlog
import win32evtlogutil
import win32con


def application_error(message):
    # Log the exception to the Windows Event Log
    log_type = 'Anpr'  # You can change this to 'Security', 'System', etc.
    event_id = 870  # You can choose a unique event ID
    event_category = 0  # The category of the event (0 for none)
    description = "An exception occurred during the request to the remote service."
    event_strings = [f"Exception occurred: {message}",description]

    # # Additional information for the event

    # task_category = 1  # You can choose an appropriate task category

    # Open the event log for writing
    h_log = win32evtlog.OpenEventLog(None, log_type)

    # Print parameters for debugging
    print(
        f"log_type: {log_type}, event_id: {event_id}, event_category: {event_category}, event_strings: {event_strings}")

    # Report the event
    win32evtlog.ReportEvent(
        h_log,
        win32evtlog.EVENTLOG_ERROR_TYPE,
        event_category,
        event_id,
        None,
        event_strings,
        None,

    )

    # Close the event log
    win32evtlog.CloseEventLog(h_log)
    return message