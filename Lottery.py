import random
import os
import sys
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

COMMASPACE = ', '
''' The following FILEPATH is the path to the file with the generated lottery numbers.
    It is important to provide the fully qualified path with the double-backslashes separating directories
    For example: FILEPATH = "C:\\Users\\<userName>\\PythonDirectory\\test_file.txt"
'''
FILEPATH = "C:\\Users\\<userName>\\PycharmProjects\\PyForDev\\External\\test_file.txt"


def main_numbers(gen, lim):
    """ Generating the 5-numbers sequences for the main body
        of the lottery ticket
    """

    a_list = []                             # Creating an empty list
    print(f"\nGenerated numbers {gen+1}")   # Printing line with the round number
    while len(a_list) < 5:                  # While loop controlling the number of elements in the list
        a = random.randrange(1, lim)        # Generating a random number in range from 1 to 69
        if a not in a_list:                 # Checking if the generated number exists already in the list
            a_list.append(a)                # If the number is not in the list, append it to the list

    a_list.sort()                           # Sort the 5-numbers list
    print(a_list)                           # Print the sorted list

    return a_list                           # Returning the sorted list to the main() function


def power_ball(extra_lim, str_pr):
    """ Generating a Power Ball or Mega Millions Extra number """
    p = random.randrange(1, extra_lim)      # Generate a random number in range from 1 to extra limit set by the lottery
    print("%s Ball = %s" % (str_pr, p))     # Printing the power ball value
    return p                                # Returning the extra ball to the main() function


def email_results(title):
    """ Sending email with the results"""
    # Asking the user whether or not s/he wants to send an email with the list of generated numbers
    email_choice = input("Would you like to send an email with the picked numbers? (y/n) ")
    if email_choice[0].lower() == 'y':      # In case the user choose "y"/"Y"/"Yes"/"yes", proceed to sending email
        sender = input("\nWhat Sender's email account would you like to use? ")
        g_password = input("Please enter the Sender's e-mail password here: ")
        # Could be multiple emails separated with comma
        recipient = input("Which Recipient e-mail(s) would you like to use? ")
        recipients = [f'{recipient}']       # Creating a list of email recipients

        # Create the enclosing (outer) message
        outer = MIMEMultipart()
        outer['Subject'] = title
        outer['To'] = COMMASPACE.join(recipients)
        outer['From'] = sender
        outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

        # List of attachments

        attachments = [f'{FILEPATH}']  # Providing the path to the text file containing the currently generated numbers

        # Add the attachments to the message
        for file in attachments:
            try:
                with open(file, 'rb') as fp:
                    msg = MIMEBase('application', "octet-stream")
                    msg.set_payload(fp.read())
                encoders.encode_base64(msg)
                msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
                outer.attach(msg)
            except IOError:
                print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
                raise

        composed = outer.as_string()

        # Send the email
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as s:
                s.ehlo()
                s.starttls()
                s.ehlo()
                s.login(sender, g_password)
                s.sendmail(sender, recipients, composed)
                s.close()
            print("Email sent!")
        except IOError:
            print("Unable to send the email. Error: ", sys.exc_info()[0])
            raise
    else:           # If the user choose not to send the email
        print("An email will not be sent")


def main():
    """ The main code """

    while True:             # Infinite loop. Will run until the user types 'q' as a choice
        lottery_type = input("""\nWhat type of the lottery would you like to generate tickets for
                             ([p]ower ball, [m]ega millions or [q]uit? """)
        # If the user enters a letter 'q' or a word starting with 'q' regardless of the case
        if lottery_type[0].lower() == 'q': 
            print("Goodbye!")
            break       # The program ends
        
        # If the user enters a letter 'p' or a word starting with this letter regardless of the case
        elif lottery_type[0].lower() == 'p':
            # Setting up important variables
            limit_main = 70     # Quantity of the main choices for the Power Ball ((from 1 to 69)+ 1) = 70
            extra_limit = 27    # Quantity of Power Ball choices ((from 1 to 26) + 1)   
            string_print = 'Power'
            title = 'Power Ball'

        # If the user enters a letter 'm' or a word starting with this letter regardless of the case
        elif lottery_type[0].lower() == 'm':
            # Setting up important variables
            limit_main = 71     # Quantity of the main choices for the Mega Millions ((from 1 to 70)+ 1) = 71
            extra_limit = 26    # Quantity of Mega Ball choices ((from 1 to 25) + 1)
            string_print = 'Mega'
            title = 'Mega Millions'

        else:
            print("You entered invalid value: '%s'. Please try again" % lottery_type)
            continue

        f = open("test_file.txt", "w+")                         # Open the file for writing
        quantity = input("How many tickets to generate? ")      # Getting the number of tickets to generate
        try:
            quantity = int(quantity)                            # Converting the answer into the integer

        except ValueError as msg:                               # Error handling
            print("Please start over because of", msg)
            continue

        title_string = 'Generating %d tickets for %s\r\n' % (quantity, title)
        print()
        print(title_string)
        f.write(title_string)

        list_of_lists = []              # Setting an empty list for collecting the generated numbers
        for z in range(quantity):       # Run a loop with up to asked number of tickets
            generated_list = main_numbers(z, limit_main)            # Call function to generate the main numbers
            extra_ball = power_ball(extra_limit, string_print)      # Call function to generate the Power Ball
            ball_string = f'{z+1}. {string_print} Ball = {extra_ball}'      # Constructing an appropriate string
            list_of_lists.append(generated_list)        # Printing the constructed string
            list_of_lists.append(ball_string)           # Appending the constructed string

        for item in list_of_lists:
            f.write("%s\n" % item)          # Writing to the file the generated list of numbers

        f.close()                           # Closing the file

        email_results(title)


if __name__ == '__main__':
    main()
