import ultrasonic
import pisetup
import time
from picture import capture
import pi_email

class MailMan:
    def __init__(self):
        self.poll_time = 2
        self.normal_distance = 0
        self.difference = 5
        self.gpio_button = None
        self.gpio_trigger = None
        self.gpio_echo = None
        self.opened = False
        self.was_opened = False
        self.opened_at = 0
        self.last_opened = 0
        self.opened_for = 0

    def setup(self):
        self.gpio_trigger, self.gpio_echo, self.gpio_button = pisetup.setup_pi(16, 18, 12)
        self.normal_distance = pisetup.set_distance(self.gpio_button, self.gpio_trigger, self.gpio_echo)

    def check_mail(self):
        current_dist = ultrasonic.measure_distance(self.gpio_trigger, self.gpio_echo)
        if abs(current_dist - self.difference) > self.normal_distance:
            if self.opened:
                self.last_opened = self.opened_at
                self.opened_for = time.time() - self.last_opened
                print("Mailbox has been open for {}s".format(self.opened_for))
            else:
                self.opened = True
                self.opened_at = time.time()
                print("Mailbox opened!")
                time.sleep(1)
                paths = capture(1)
                pi_email.send_mail(paths)
                # if self.opened_at - 30 >= self.last_opened :
                #     # If opened in last 30 seconds figure out what we do
                self.last_opened = self.opened_at
            self.was_opened = True
        else:
            if self.was_opened:
                print("Mailbox now closed after being opened for {:2}s".format(self.opened_for))
                self.opened_for = 0
                self.was_opened = False
            self.opened = False
            self.opened_at = 0
        print("\n---------------------------------------------------\n")
            
    def mail_loop(self):
        print("Mail checker starting up!")
        while True:
            try:
                self.check_mail()
                time.sleep(self.poll_time)
            except KeyboardInterrupt:
                print("Mail checker stopped by user!")
                GPIO.cleanup()
                return 0
            
if __name__ == "__main__":
    mailman = MailMan()
    mailman.setup()
    mailman.mail_loop()