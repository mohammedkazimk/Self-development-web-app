from django.shortcuts import render, redirect
from django.utils.timezone import now as time
from datetime import datetime,timedelta
from django.core.paginator import Paginator
from itertools import groupby
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
from operator import attrgetter
from django.db.models import Sum,Q
from .models import *

# Create your views here.
# @login_required(login_url='/login/')
def home(request):
    return render(request, 'home.html')
# @login_required(login_url='/login/')
def namaz(request):
    NamazReason_obj = NamazReason.objects.order_by('-status__date')
    paginator = Paginator(NamazReason_obj, 20)  # Show 10 entries per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'namaz.html', {'page_obj': page_obj})

# @login_required(login_url='/login/')
def new_namaz_entry(request):
    obj = NamazStatus.objects.get(date=time().date()) if NamazStatus.objects.filter(date=time().date()).exists() else None
    obj_reason = NamazReason.objects.get(status=obj) if obj and NamazReason.objects.filter(status=obj).exists() else None
    if request.method == 'POST':
        date = request.POST.get('date')
        fajar_sunnat = request.POST.get('fajar_sunnat')
        fajar_farz   = request.POST.get('fajar_farz')
        zuhar_farz   = request.POST.get('zuhar_farz')
        zuhar_sunnat = request.POST.get('zuhar_sunnat')
        asar         = request.POST.get('asar')
        maghrib_farz   = request.POST.get('maghrib_farz')
        maghrib_sunnat = request.POST.get('maghrib_sunnat')
        isha_farz   = request.POST.get('isha_farz')
        isha_sunnat = request.POST.get('isha_sunnat')
        witr        = request.POST.get('witr')
        temp_list = [fajar_sunnat, fajar_farz, zuhar_farz, zuhar_sunnat, asar, maghrib_farz, maghrib_sunnat, isha_farz, isha_sunnat, witr]
        percentage = temp_list.count("on_time") * 10 + temp_list.count("in_home") * 3 + temp_list.count("late") * 8 + temp_list.count("not_prayed") * 0
        if obj:
            previous_percentage_obj = NamazStatus.objects.order_by('-date')[1]
        else:
            previous_percentage_obj = NamazStatus.objects.order_by('-date').first()
        previous_percentage = previous_percentage_obj.percentage if previous_percentage_obj else 0.0
        if previous_percentage == percentage or previous_percentage == 0:
            growth = 2
        elif previous_percentage < percentage:
            growth = 1
        else:
            growth = 3

        if obj:
            namaz_status = obj
            namaz_status.fajar_sunnat = fajar_sunnat
            namaz_status.fajar_farz   = fajar_farz
            namaz_status.zuhar_farz   = zuhar_farz
            namaz_status.zuhar_sunnat = zuhar_sunnat
            namaz_status.asar         = asar
            namaz_status.maghrib_farz   = maghrib_farz
            namaz_status.maghrib_sunnat = maghrib_sunnat
            namaz_status.isha_farz   = isha_farz
            namaz_status.isha_sunnat = isha_sunnat
            namaz_status.witr        = witr
            namaz_status.percentage  = percentage
            namaz_status.growth      = growth
            namaz_status.save()

            namaz_reason = NamazReason.objects.get(status=namaz_status)

            namaz_reason.fajar_sunnat_reason = request.POST.get('fajar_sunnat_reason')
            namaz_reason.fajar_farz_reason   = request.POST.get('fajar_farz_reason')
            namaz_reason.zuhar_farz_reason   = request.POST.get('zuhar_farz_reason')
            namaz_reason.zuhar_sunnat_reason = request.POST.get('zuhar_sunnat_reason')
            namaz_reason.asar_reason         = request.POST.get('asar_reason')
            namaz_reason.maghrib_farz_reason = request.POST.get('maghrib_farz_reason')
            namaz_reason.maghrib_sunnat_reason = request.POST.get('maghrib_sunnat_reason')
            namaz_reason.isha_farz_reason    = request.POST.get('isha_farz_reason')
            namaz_reason.isha_sunnat_reason  = request.POST.get('isha_sunnat_reason')
            namaz_reason.witr_reason         = request.POST.get('witr_reason')

            namaz_reason.save()
        else:
            namaz_status = NamazStatus(
                date=date,
                fajar_sunnat=fajar_sunnat,
                fajar_farz=fajar_farz,
                zuhar_farz=zuhar_farz,
                zuhar_sunnat=zuhar_sunnat,
                asar=asar,
                maghrib_farz=maghrib_farz,
                maghrib_sunnat=maghrib_sunnat,
                isha_farz=isha_farz,
                isha_sunnat=isha_sunnat,
                witr=witr,
                percentage=percentage,
                growth=growth
            )
            namaz_status.save()

            fajar_sunnat_reason = request.POST.get('fajar_sunnat_reason')
            fajar_farz_reason   = request.POST.get('fajar_farz_reason')
            zuhar_farz_reason   = request.POST.get('zuhar_farz_reason')
            zuhar_sunnat_reason = request.POST.get('zuhar_sunnat_reason')
            asar_reason         = request.POST.get('asar_reason')
            maghrib_farz_reason = request.POST.get('maghrib_farz_reason')
            maghrib_sunnat_reason = request.POST.get('maghrib_sunnat_reason')
            isha_farz_reason    = request.POST.get('isha_farz_reason')
            isha_sunnat_reason  = request.POST.get('isha_sunnat_reason')
            witr_reason         = request.POST.get('witr_reason')

            namaz_reason = NamazReason(
                status=namaz_status,
                fajar_sunnat_reason=fajar_sunnat_reason,
                fajar_farz_reason=fajar_farz_reason,
                zuhar_farz_reason=zuhar_farz_reason,
                zuhar_sunnat_reason=zuhar_sunnat_reason,
                asar_reason=asar_reason,
                maghrib_farz_reason=maghrib_farz_reason,
                maghrib_sunnat_reason=maghrib_sunnat_reason,
                isha_farz_reason=isha_farz_reason,
                isha_sunnat_reason=isha_sunnat_reason,
                witr_reason=witr_reason
            )
            namaz_reason.save()
        return redirect('namaz')
    return render(request, 'new_namaz_entry.html',context={'obj': obj, 'obj_reason': obj_reason})


def get_para_and_ruku(current_cumulative_ruku, ruku_para_map):
    previous_end = 0
    current_cumulative_ruku = current_cumulative_ruku % 558
    for para, rukus_in_para, cumulative_end in sorted(ruku_para_map):
        if current_cumulative_ruku <= cumulative_end:
            current_para = para
            current_ruku = current_cumulative_ruku - previous_end
            return current_para, current_ruku,rukus_in_para

        previous_end = cumulative_end

    return None, None

# @login_required(login_url='/login/')
def quran_daily(request):
    ruku_para_map = {
        (1,16,16),
        (2,16,32),
        (3,17,49),
        (4,14,63),
        (5,17,80),
        (6,14,94),
        (7,19,113),
        (8,17,130),
        (9,18,148),
        (10,17,165),
        (11,16,181),
        (12,16,197),
        (13,19,216),
        (14,22,238),
        (15,21,259),
        (16,17,276),
        (17,17,293),
        (18,17,310),
        (19,19,329),
        (20,16,345),
        (21,19,364),
        (22,18,382),
        (23,17,399),
        (24,19,418),
        (25,20,438),
        (26,18,456),
        (27,20,476),
        (28,20,496),
        (29,22,518),
        (30,39,557),
    }
    current_cumulative_ruku = DailyQuranReading.objects.order_by('-date','-id').first().total_rukus if DailyQuranReading.objects.exists() else 0
    current_para, current_ruku, total_ruku = get_para_and_ruku(current_cumulative_ruku, ruku_para_map)
    ruku_percent = int((current_ruku / total_ruku) * 100)
    completed_para = current_para - 1
    total_paras = 30

    remaining_ruku = total_ruku - current_ruku
    remaining_para = (total_paras - current_para) + 1

    ruku_percent = int((current_ruku / total_ruku) * 100)
    quran_completed = current_cumulative_ruku // 558
    li = list()
    for i in range(1, quran_completed + 1):
        range_end = i * 558
        range_start_gt = (i - 1) * 558
        
        start_obj = DailyQuranReading.objects.filter(total_rukus__gt=range_start_gt).order_by('date', 'id').first()
        start_date = start_obj.date if start_obj else "N/A"
        
        end_obj = DailyQuranReading.objects.filter(total_rukus__gte=range_end).order_by('date', 'id').first()
        end_date = end_obj.date if end_obj else "N/A"
        
        li.append({
            'start_date': start_date,
            'end_date': end_date,
            'status': 'Completed',
            'sno': i
        })

    # In Progress Entry
    start_threshold = quran_completed * 558
    start_obj = DailyQuranReading.objects.filter(total_rukus__gt=start_threshold).order_by('date', 'id').first()
    
    if start_obj:
        in_progress_start = start_obj.date
    elif quran_completed > 0 and li:
        in_progress_start = li[-1]['end_date']
    elif quran_completed == 0:
        first_obj = DailyQuranReading.objects.order_by('date', 'id').first()
        in_progress_start = first_obj.date if first_obj else "N/A"
    else:
        in_progress_start = "N/A"

    li.append({
        'start_date': in_progress_start,
        'end_date': None,
        'status': 'In Progress',
        'sno': quran_completed + 1
    })

    # Pagination
    page_obj = DailyQuranReading.objects.order_by('-date','-start_time')[:6]

    context = {
        'current_para': current_para,
        'current_ruku': current_ruku,
        'total_ruku': total_ruku,
        'ruku_percent': ruku_percent,
        'completed_para': completed_para,
        'completed_ruku': current_ruku,
        'total_paras': total_paras,
        'para_percent': int(((current_cumulative_ruku % 558) / 558) * 100),
        'total_ruku_list': range(1, total_ruku + 1),
        'remaining_ruku': remaining_ruku,
        'remaining_para': remaining_para,
        'completed_ruku_overall': current_cumulative_ruku % 558,
        'remaining_ruku_overall': 558 - (current_cumulative_ruku % 558),
        'records': page_obj,
        'quran_completed': quran_completed,
        'quran_completion_list': li,
        'today': time().date(),
    }
    return render(request, 'quran_daily.html',context=context)


# @login_required(login_url='/login/')
def quran_daily_entry(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        ruku = request.POST.get('ruku')
        pages = request.POST.get('pages')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        fmt = '%H:%M'
        start_time_obj = datetime.strptime(start_time, fmt)
        end_time_obj = datetime.strptime(end_time, fmt)
        if end_time_obj < start_time_obj:
            end_time_obj += timedelta(days=1)
        total_time = end_time_obj - start_time_obj
        speed = round( float(pages) / ((total_time.seconds // 60) / 60))
        points = float(pages) * 10 + int(ruku) * 5 + (total_time.seconds // 60)
        previous_points_obj = DailyQuranReading.objects.order_by('-date','-id').first()
        previous_points = previous_points_obj.points if previous_points_obj else 0.0
        if previous_points == points or previous_points == 0.0:
            growth = 2
        elif previous_points < points:
            growth = 1
        else:
            growth = 3
        previous_total_rukus = previous_points_obj.total_rukus if previous_points_obj else 0
        total_rukus = previous_total_rukus + int(ruku)
        daily_quran_reading = DailyQuranReading(
            date=date,
            ruku=ruku,
            pages=pages,
            start_time=start_time,
            end_time=end_time,
            total_time=total_time,
            speed=speed,
            points=points,
            growth=growth,
            total_rukus=total_rukus
        )
        daily_quran_reading.save()
        return redirect('quran_daily')
    return render(request, 'quran_daily_entry.html')

# @login_required(login_url='/login/')
def sleep_track_home(request):
    obj = sleep_track.objects.order_by('-date','-id')
    grouped = []
    for date,items in groupby(obj, key=attrgetter('date')):
        lst = list(items)
        grouped.append({
            'date':date,
            'entries': lst,
            'count': len(lst)
        })
    page_number = request.GET.get('page')
    pagination = Paginator(grouped,20)
    page_obj = pagination.get_page(page_number)
    context = {
        'records': page_obj,
        'group': grouped,
    }
    return render(request,"sleep_track_home.html",context=context)


# @login_required(login_url='/login/')
def sleep_track_entry(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        sleep_time = request.POST.get('sleep_time')
        wakeup_time = request.POST.get('wake_time')
        sleep_time_obj = datetime.strptime(sleep_time, '%H:%M')
        wakeup_time_obj = datetime.strptime(wakeup_time, '%H:%M')
        if wakeup_time_obj < sleep_time_obj:
            wakeup_time_obj += timedelta(days=1)
        duration = wakeup_time_obj - sleep_time_obj
        sleep_entry = sleep_track(
            date=date,
            sleep_time=sleep_time,
            wakeup_time=wakeup_time,
            duration=duration
        )
        sleep_entry.save()
        return redirect('/sleep-tracking/')
    return render(request, 'sleep_track_entry.html')

def college_studies_home(request):
    # Pagination
    obj = college_studies.objects.order_by('-id','-date')
    page_obj = Paginator(obj,7)
    page_num = request.GET.get('page')
    page_obj = page_obj.get_page(page_num)
    entry_count = obj.count()
    ml = college_studies.objects.filter(subject = "machine learning").aggregate(total_duration=Sum('duration'))
    r = college_studies.objects.filter(subject = "r programming").aggregate(total_duration=Sum('duration'))
    cc = college_studies.objects.filter(subject = "cloud computing").aggregate(total_duration=Sum('duration'))
    st = college_studies.objects.filter(subject = "software testing").aggregate(total_duration=Sum('duration'))
    ml = ml['total_duration']
    r = r['total_duration']
    cc = cc['total_duration']
    st = st['total_duration']
    ml = int(ml.total_seconds()) // 3600 if ml else 0
    r = int(r.total_seconds()) // 3600 if r else 0
    cc = int(cc.total_seconds()) // 3600 if cc else 0
    st = int(st.total_seconds()) // 3600 if st else 0
    overall = (ml + r + cc + st)
    ml_perc = (ml / 150) * 100
    r_prec = (r / 135) * 100
    cc_prec = (cc / 60) * 100
    st_prec = (st / 30) * 100
    overall_prec = ((ml_perc + r_prec + cc_prec + st_prec) / 375) * 100
    context = {
        'ml':ml,
        'r': r,
        'cc':cc,
        'st':st,
        'overall':overall,
        'overall_prec': overall_prec,
        'ml_prec': ml_perc,
        'r_prec':r_prec,
        'cc_prec':cc_prec,
        'st_prec':st_prec,
        'page_obj':page_obj,
        'count':entry_count
    }
    return render(request,"college_studies.html",context=context)

# @login_required(login_url='/login/')
def college_studies_entry(request):
    if request.method == "POST":
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        start_time_obj = datetime.strptime(start_time,"%H:%M")
        end_time_obj = datetime.strptime(end_time,"%H:%M")
        if end_time_obj < start_time_obj:
            end_time_obj += timedelta(days=1)
        duration = end_time_obj - start_time_obj
        subject = request.POST.get('subject')
        note = request.POST.get('note')
        study_entry = college_studies(
            date = date,
            start_time = start_time,
            end_time = end_time,
            duration = duration,
            subject = subject,
            note = note
        )
        study_entry.save()
        return redirect("/college-studies/")
    return render(request,"college_studies_entry.html")

# @login_required(login_url='/login/')
def generate_pdf(request):
    get = request.GET.get
    from_date = get('from_date')
    to_date = get('to_date')
    include_namaz = get('namaz') == 'on'
    include_quran = get('quran') == 'on'
    include_sleep = get('sleep') == 'on'

    show_report = bool(from_date and to_date and (include_namaz or include_quran or include_sleep))
    namaz_entries = []
    quran_entries = []
    sleep_entries = []

    if show_report:
        try:
            fd = datetime.strptime(from_date, '%Y-%m-%d').date()
            td = datetime.strptime(to_date, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            show_report = False
        else:
            if include_namaz:
                namaz_entries = list(
                    NamazReason.objects.filter(
                        status__date__gte=fd,
                        status__date__lte=td
                    ).select_related('status').order_by('status__date')
                )
            if include_quran:
                quran_entries = list(
                    DailyQuranReading.objects.filter(
                        date__gte=fd,
                        date__lte=td
                    ).order_by('date')
                )
            if include_sleep:
                sleep_entries = list(
                    sleep_track.objects.filter(
                        date__gte=fd,
                        date__lte=td
                    ).order_by('date')
                )

    report_from_date = None
    report_to_date = None
    if show_report and from_date and to_date:
        try:
            report_from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            report_to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
        except ValueError:
            pass
    context = {
        'from_date': from_date,
        'to_date': to_date,
        'report_from_date': report_from_date,
        'report_to_date': report_to_date,
        'include_namaz': include_namaz,
        'include_quran': include_quran,
        'include_sleep': include_sleep,
        'show_report': show_report,
        'namaz_entries': namaz_entries,
        'quran_entries': quran_entries,
        'sleep_entries': sleep_entries,
    }
    return render(request, 'generate_pdf.html', context)


# @login_required(login_url='/login/')
def notes(request):
    query = request.GET.get('q')
    page_obj = college_studies.objects.order_by('-id','-date')
    if query:
        page_obj = college_studies.objects.filter(Q(note__icontains = query) | Q(date__icontains = query)).order_by('-id','-date')
    # Pagination
    page_obj = Paginator(page_obj,20)
    page_number = request.GET.get('page')
    page_obj = page_obj.get_page(page_number)
    return render(request,"notes.html",context={'page_obj':page_obj})

def login_function(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request,'login.html',context={'error_message': 'Invalid username or password'})
    return render(request, 'login.html',context={'error_message': None})

def logout_function(request):
    logout(request)
    return redirect('/')