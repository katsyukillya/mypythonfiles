import random
import os
import sys
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

COMMASPACE = ', '


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

    return a_list


def power_ball(extra_lim, str_pr):
    """ Generating a Power Ball number """
    p = random.randrange(1, extra_lim)      # Generate a random number in range from 1 to extra limit set by the lottery
    print("%s Ball = %s" % (str_pr, p))     # Printing the power ball value
    return p


def email_results(g_password, title):
    """ Sending email with the results"""

    sender = 'ikatsyuk@gmail.com'

    recipients = ['illya_katsyuk@msn.com']

    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = title
#    outer['Subject'] = 'Generated winning numbers'
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    # List of attachments
    attachments = ['C:\\Users\\IllyaK\\PycharmProjects\\PyForDev\\External\\test_file.txt']

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


def main():
    """ The main code """

    while True:
        lottery_type = input("""\nWhat type of the lottery would you like to generate tickets for
                             ([p]ower ball, [m]ega millions or [q]uit? """)
        if lottery_type[0].lower() == 'q':
            print("Goodbye!")
            break

        elif lottery_type[0].lower() == 'p':
            limit_main = 70
            extra_limit = 27
            string_print = 'Power'
            title = 'Power Ball'

        elif lottery_type[0].lower() == 'm':
            limit_main = 71
            extra_limit = 26
            string_print = 'Mega'
            title = 'Mega Millions'

        else:
            print("You entered invalid value: '%s'. Please try again" % lottery_type)
            continue

        f = open("test_file.txt", "w+")
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

        list_of_lists = []
        for z in range(quantity):       # Run a loop with up to asked number of tickets
            generated_list = main_numbers(z, limit_main)            # Call function to generate the main numbers
            extra_ball = power_ball(extra_limit, string_print)      # Call function to generate the Power Ball
            ball_string = f'{z+1}. extra ball = {extra_ball}'
            list_of_lists.append(generated_list)
            list_of_lists.append(ball_string)

        for item in list_of_lists:
            f.write("%s\n" % item)

        f.close()

        g_password = input("please enter the Gmail password here: ")

        email_results(g_password, title)


if __name__ == '__main__':
    main()
