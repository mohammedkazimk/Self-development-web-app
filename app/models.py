from django.db import models

# Create your models here.

STATUS_CHOICES = [
    ("on_time", "On Time"),
    ("late", "Late"),
    ("in_home", "In Home"),
    ("prayed", "Prayed"),
    ("not_prayed", "Not Prayed"),
    ("not_marked","Not Marked"),
]

class NamazStatus(models.Model):
    date = models.DateField(unique=True)

    # Fajar
    fajar_sunnat = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True, blank=True)
    fajar_farz   = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True, blank=True)

    # Zuhar
    zuhar_farz   = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True, blank=True)
    zuhar_sunnat = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True, blank=True)

    # Asar
    asar = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True, blank=True)

    # Maghrib
    maghrib_farz   = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True, blank=True)
    maghrib_sunnat = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True, blank=True)
    # Isha
    isha_farz   = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True, blank=True)
    isha_sunnat = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True, blank=True)

    # Witr
    witr = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True, blank=True)

    # Percentage
    percentage = models.FloatField(default=0.0)

    # Growth
    growth = models.IntegerField(default=0)

    def __str__(self):
        return f"Status - {self.date}"


class NamazReason(models.Model):
    status = models.OneToOneField(NamazStatus, on_delete=models.CASCADE, related_name="reasons")

    # Fajar
    fajar_sunnat_reason = models.TextField(blank=True, null=True)
    fajar_farz_reason   = models.TextField(blank=True, null=True)

    # Zuhar
    zuhar_farz_reason   = models.TextField(blank=True, null=True)
    zuhar_sunnat_reason = models.TextField(blank=True, null=True)

    # Asar
    asar_reason = models.TextField(blank=True, null=True)

    # Maghrib
    maghrib_farz_reason   = models.TextField(blank=True, null=True)
    maghrib_sunnat_reason = models.TextField(blank=True, null=True)

    # Isha
    isha_farz_reason   = models.TextField(blank=True, null=True)
    isha_sunnat_reason = models.TextField(blank=True, null=True)

    # Witr
    witr_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reasons - {self.status.date}"

class DailyQuranReading(models.Model):

    GROWTH_CHOICES = (
        (1, 'Up'),
        (2, 'Neutral'),
        (3, 'Down'),
    )

    date = models.DateField()

    ruku = models.PositiveIntegerField(default=0)
    pages = models.FloatField(null=True, blank=True)
    total_rukus = models.PositiveIntegerField(default=0)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    total_time = models.DurationField(null=True, blank=True)

    speed = models.FloatField(default=0.0)   # pages per hour
    points = models.PositiveIntegerField(default=0)

    growth = models.PositiveSmallIntegerField(
        choices=GROWTH_CHOICES,
        default=1
    )

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def duration_display(self):
        if not self.total_time:
            return None

        seconds = int(self.total_time.total_seconds())
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60

        if hours > 0:
            return f"{hours} Hr {minutes} Min"
        return f"{minutes} Min"


    class Meta:
        ordering = ['-date']

class sleep_track(models.Model):
    date = models.DateField()
    sleep_time = models.TimeField()
    wakeup_time = models.TimeField()
    duration = models.DurationField(null=True,blank=True)

    @property
    def duration_display(self):
        if not self.duration:
            return None

        seconds = int(self.duration.total_seconds())
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60

        if hours > 0:
            if minutes > 0:
                return f"{hours}hr {minutes}min"
            else:
                return f"{hours}hr"
        return f"{minutes}min"

    class Meta:
        ordering = ['-date']


class college_studies(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration = models.DurationField()
    subject = models.CharField(max_length=30,choices=[("machine learning","Machine Learning"),("r programming","R Programming"),("cloud computing","Cloud Computing"),("software testing","Software Testing")],null=True,blank=True)
    note = models.TextField()

    @property
    def duration_display(self):
        if not self.duration:
            return None

        seconds = int(self.duration.total_seconds())
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60

        if hours > 0:
            if minutes > 0:
                return f"{hours}hr {minutes}min"
            else:
                return f"{hours}hr"
        return f"{minutes}min"

    class Meta:
        ordering = ['-date']