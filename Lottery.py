import random
import os
import sys
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


class Lottery:

    def __init__(self):
        self.COMMASPACE = ', '
        self.a_list = []

    def main_numbers(self, gen, lim):
        print(f"\nGenerated numbers set #{gen+1}")
        while len(self.a_list) < 5:
            a = random.randrange(1, lim)
            if a not in self.a_list:
                self.a_list.append(a)

        self.a_list.sort()
        print(self.a_list)

        return self.a_list

    def extra_ball(self, extra_lim, str_pr):
        b = random.randrange(1, extra_lim)
        print("%s Ball = %s" % (str_pr, b))

        return b

    def email_results(self, title):

        sender = input("\nWhat email address would you like to use as a Sender?\n ")
        g_pwd = input("Please enter the Sender's e-mail password here: ")
        recipient = input("Which Recipient's e-mail(s) would you like to use? ")
        recipients = [f'{recipient}']

        outer = MIMEMultipart()
        outer['Subject'] = title
        outer['To'] = self.COMMASPACE.join(recipients)
        outer['From'] = sender
        outer.preamble = 'You will not see this in a MIME-aware mail sender.\n'

        file_path = input("Please enter the path to the text file with the selected numbers: \n")
        attachments = [file_path]

        for file in attachments:
            try:
                with open(file, 'rb') as fp:
                    msg = MIMEBase('application', 'octet-stream')
                    msg.set_payload(fp.read())
                encoders.encode_base64(msg)
                msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
                outer.attach(msg)

            except IOError:
                print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
                raise

        composed = outer.as_string()

        # The entire email setup is for the GMail sender account

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as s:
                s.ehlo()
                s.starttls()
                s.ehlo()
                s.login(sender, g_pwd)
                s.sendmail(sender, recipients, composed)
                s.close()

            print("Email sent!")

        except IOError:
            print("Unable to send the email. Error: ", sys.exc_info()[0])
            raise


def main():
    print("Welcome to the numbers generator for the lottery program!")
    while True:

        lottery_type = input("\nWhat type of the lottery would you like to generate the tickets for\n"
                             "([p]ower ball, [m]ega millions or [q]uit? ")

        if lottery_type[0].lower() == 'q':
            print("Thanks for using this program. Goodbye!")
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

        f = open("generated_lottery_numbers.txt", "w+")

        quantity = input("How many tickets to generate? ")
        try:
            quantity = int(quantity)

        except ValueError as msg:
            print("Please start over because of", msg)
            continue

        title_string = "Generating %d sets of numbers for the %s tickets \r\n" % (quantity, title)
        print()
        print(title_string)
        f.write(title_string)

        list_of_lists = []

        for z in range(quantity):
            my_generated_list = Lottery()
            generated_list = my_generated_list.main_numbers(z, limit_main)
            extra_ball = my_generated_list.extra_ball(extra_limit, string_print)
            ball_string = f'{z+1}. {string_print} Ball = {extra_ball}'
            list_of_lists.append(generated_list)
            list_of_lists.append(ball_string)

        for item in list_of_lists:
            f.write("%s\n" % item)

        f.close()

        send_email = input("\nWould you like to send the generated numbers by email (y / n)? ")

        if send_email[0].lower() == 'y':
            email = Lottery()
            email.email_results(title)

        else:
            print('OK. As you wish, the email will not be sent.\n'
                  'You may retrieve the generated numbers from the console or by opening the test_file.txt.\n'
                  'However, please make sure you do that before running the numbers generator program again. \n'
                  'Otherwise, the numbers will be overwritten\n')


if __name__ == '__main__':
    main()
