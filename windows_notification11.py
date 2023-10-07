# from plyer import notification
#
# # Notification title and message
# # title = 'My Notification'
# # message = 'This is a sample notification.'
#
# def windows_not(title,message):
#     # Send the notification
#     notification.notify(
#     title=title,
#     message=message,
#     app_name='trrrrrrrrst',  # Set your app name
#     timeout=40  # Notification display time in seconds
# )
# # #wndows_not('Anpr',"Stored date is more than 24 hours old.")



from win10toast import ToastNotifier

import six
import appdirs
import packaging.requirements



def windows_not(title, message):
    # Create a ToastNotifier
    notifier = ToastNotifier()

    # Display the notification
    notifier.show_toast(title, message, duration=10)  # duration is in seconds
#
# #windows_not('Anpr', 'Stored date is more than 24 hours old.')



