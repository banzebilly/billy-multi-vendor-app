from django.db import models
from datetime import time, date, datetime
from account.models import UserAccount, UserProfile
from account.utils import send_notification

class Vendor(models.Model):
    user = models.OneToOneField(UserAccount, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vendor_name} (ID: {self.id})"

    def is_open(self):
        """
        Checks if the vendor is currently open based on opening hours.
        """
        today = date.today().isoweekday()  # Get current weekday as an integer
        now = datetime.now().time()  # Get current time

        current_opening_hours = OpeningHour.objects.filter(vendor=self, day=today, is_closed=False)

        for opening_hour in current_opening_hours:
            start_time = datetime.strptime(opening_hour.from_hour, "%I:%M %p").time()
            end_time = datetime.strptime(opening_hour.to_hour, "%I:%M %p").time()
            
            if start_time <= now <= end_time:  # Direct time comparison
                return True  # Vendor is open

        return False  # Vendor is closed

    def save(self, *args, **kwargs):
        """
        Overrides the save method to send notifications when the vendor's approval status changes.
        If a vendor is newly approved, sends a congratulatory email.
        If a vendor's approval is revoked, sends a notification email.
        The save function is triggered when an admin updates the vendor's approval status in the admin panel.
        *args and **kwargs are used to handle any number of arguments passed to this method.
        """
        if self.pk:  # Check if this is an update (not a new object)
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:  # Trigger only when approval status changes
                mail_template = "account/email/admin_approval_email.html"
                mail_subject = (
                    "Congratulations! Your restaurant has been approved."
                    if self.is_approved
                    else "We’re sorry, but you are not eligible to publish your food menu on our marketplace."
                )
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
                    'to_email': self.user.email,
                }
                send_notification(mail_subject, mail_template, context)

        super().save(*args, **kwargs)  # Call the parent class's save method

DAYS = [
    (1, "Monday"),
    (2, "Tuesday"),
    (3, "Wednesday"),
    (4, "Thursday"),
    (5, "Friday"),
    (6, "Saturday"),
    (7, "Sunday"),
]

HOUR_OF_DAY_24 = [
    (time(h, m).strftime('%I:%M %p'), time(h, m).strftime('%I:%M %p')) 
    for h in range(0, 24) for m in (0, 30)
]

class OpeningHour(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    to_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('day', '-from_hour')
        unique_together = ('vendor', 'day', 'from_hour', 'to_hour')

    def __str__(self):
        return self.get_day_display()

   