#from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from forms import AppointmentForm
from forms import PostForm
from models import UploadFile
from django.http import HttpResponse
from django.shortcuts import render
from models import CalendarEvent, Tutor, AppointmentAvailability
from datetime import datetime, timedelta, date

from datetime import datetime, timedelta

import calendar
import json
from django.shortcuts import redirect
from django.core.mail import send_mail

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def login_student(request):
    user = authenticate(username = 'student', password = 'student')
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)

#############################################
# Calendar Form
#############################################


### Displays an appointment form
def appt_form(request):
    return render(request, 'portal/index.html')

'''   
def decideTutor() :

tutors = Tutor.object.all()


return tutorName
'''

###############################################################################################################
# make_appt -
# This function calls other functions like create_appointment_slots, tutor_schedule_check, check_slot_availability.
# It also books appointment and displays it on the admin page.
# It returns the different values to the portal page depending upon the conditions in the code.
# It creates string of 15 minutes slots for provided date and tutor combination.
###############################################################################################################   
def make_appt(request):
    #Appointment Form Input Values
    login_student(request)

    full_name = ''
    email = ''
    course = ''
    date = ''
    time = ''
    tutor = ''
    message = ''
    duration = ''
           
    if 'full_name' in request.POST:
        full_name = request.POST['full_name']
        message += 'Your name: %r' % request.POST['full_name']
    else:
        message = 'Please enter your name.'         
    if 'email' in request.POST:
        email = request.POST['email']
        message += '<br></br>Your email: %r' % email
    else:
        message = 'Please enter your UNCC email.'
    if 'course' in request.POST:
        course = request.POST['course']
        message += '<br></br>Your course: %r' % course
    else:
        message = 'Please select enter a course you need help with.'
    if 'date' in request.POST:
        date = request.POST['date']
        message += '<br></br>Your date: %r' % date
    else:
        message = 'Please enter a date.'
    if 'time' in request.POST:
        time = request.POST['time']
        message += '<br></br>Your time: %r' % time
    else:
        message = 'Please enter a time.'
    if 'tutor' in request.POST:
        tutor = request.POST['tutor']
    '''
        if tutor == 'Anyone':
            tutor = decideTutor()
    '''
    if 'duration' in request.POST:
        duration = request.POST['duration']
        if duration == 'no_preference':
            duration = 'Anyone Available'
        else:
            message += '<br></br>Your tutor: %r' % duration
           
    #Converting DatePicker input to datetime format
    dateConvert = {'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06':'Jun', '07':'Jul', '08':'Aug', '09':'Sep', '10':'Oct', '11':'Nov', '12':'Dec'}
    date_list = date.split('/')
    #month = str(dateConvert[str(date_list[0])])
    month = str(date_list[0])
    day = str(date_list[1])
    year = str(date_list[2])
    date_string = month + ' ' + day + ' ' + year
    date_input = date_string + ' ' + time

    message += '<br><br> Date String: %r' % date_string
    message += '<br><br> Date Input: %r' % date_input
    try:
        #print date
        #print time 
        start = datetime.datetime.strptime(str(date + ' ' + time), '%m/%d/%Y %I:%M%p')
        end = start + timedelta(minutes=int(duration)) # Adding duration to the start time of the appointment
        #print start
        #print end
    except:
        start = None
        end = None

    tutor_emails = {'Grace': 'gchriste@uncc.edu', 'Chinmai': 'chinmai.padalkar4@gmail.com', 'David': 'dfarthing@uncc.edu'}
    
    create_appointment_slots(tutor, date)
    
    scheduleAvailability = tutor_schedule_check(tutor, date, time, duration)
    
    if scheduleAvailability == 1 :
        availability = check_slot_availability(tutor, date, time, duration)
    else :
        availability =0
    '''
    #Create empty slots for unique tutor and date combination
    availableAppointments = Appointment()
    
    availableAppointments.tutor = tutor
    availableAppointments.date = date
    availableAppointments.slots = "08:00AM,08:15AM,08:30AM,08:45AM,09:00AM,09:15AM,09:30AM,09:45AM,10:00AM,10:15AM,10:30AM,10:45AM,11:00AM,11:15AM,11:30AM,11:45AM,12:00PM,12:15PM,12:30PM,12:45PM,01:00PM,01:15PM,01:30PM,01:45PM,02:00PM,02:15PM,02:30PM,02:45PM,03:00PM,03:15PM,03:30PM,03:45PM,04:00PM,04:15PM,04:30PM,04:45PM"    
    # check availability for slot
    # if available do following else alert slot is booked choose different slot
    '''
    if (not isinstance(availability,str)) and availability == 1:
        try:
            print '########################################################################'
            event = CalendarEvent()
            event.availability = False
            title = 'Tutoring Appointment for ' + full_name + ' with ' + tutor + ' at ' + time
            #event.availability = False
            event.title = title
            event.tutor = tutor
            print title
            print tutor
            event.tutor_email = tutor_emails[tutor]
            event.student_email = email
            print email
            event.student = full_name
            print full_name
            event.course = course
            event.css_class = 'event-primary'
            event.start = start
            print start
            event.end = end
            print end
            message = str(event) + ': <br></br>' + message
            event.save()
            print '##############################################################'
            message = 'Success! Thank you for scheduling your appointment with CCI Tutors!'
            
            print 'Printing email.....'
            recipients = ['chinmai.padalkar4@gmail.com']
            send_mail('Tutoring Appointment Scheduled', 'Confirming CCI ' + title, student_email, recipients)
            print email
            if email == "":
                print 'No email provided'
            else:
                sendMail = "['" + email + "']"
                print sendMail
                #send_mail('Tutoring Appointment Scheduled', 'Confirming CCI ' + title, tutor_emails[tutor], recipients)
                # Send email to Student 
            
        except:
            message = 'Form submission failed (form submitted without all needed data to create a Calendar Event).'
        
        return redirect('/portal')

    else:
        message = 'Appointment slot not available for that day!!!'
        print message
        message = 1
        
        #return HttpResponse(message)
        if isinstance(availability,str):
            print 'in else'
            time = processTime(availability)
            print tutor, email, full_name, date, time, duration
            return render_to_response('portal/index.html', {'suggestion' : availability , 'tutor' : tutor, 'email' : email, 'course' : course, 'name': full_name, 'date' : date, 'time': time, 'duration' : duration}, context_instance = RequestContext(request) )
            
        else:
            return render_to_response('portal/index.html', {'message' : message}, context_instance = RequestContext(request) )
        #return redirect('/portal', message=message)


###############################################################################################################
# processTime -
# This function generates time from the suggestion string.
# It return time in the required format.
###############################################################################################################           
def processTime(suggestion):
    addAMPM = {'01': 'PM', '02': 'PM', '03': 'PM', '04': 'PM', '05': 'PM', '06':'PM', '07':'PM', '08':'AM', '09':'AM', '10':'AM', '11':'AM', '12':'PM'}
    time=suggestion[:5]+addAMPM[suggestion[:2]]
    return time
    
def suggestion_form(request):
        return redirect('/portal')
 
 
###############################################################################################################
# create_appointment_slots -
# This function creates slots from 8am to 5pm.
# It creates string of 15 minutes slots for provided date and tutor combination.
###############################################################################################################   
def create_appointment_slots(tutor, date):
    # Create empty slots for unique tutor and date combination
    
        #availableAppointments = Appointments()
    appointment, created = AppointmentAvailability.objects.get_or_create(tutor = str(tutor), date = str(date))
    if created:
        #print 'inside if'
        appointment.tutor = str(tutor)
        appointment.date = str(date)
        appointment.slotAvail = '08:00,08:15,08:30,08:45,09:00,09:15,09:30,09:45,10:00,10:15,10:30,10:45,11:00,11:15,11:30,11:45,12:00,12:15,12:30,12:45,01:00,01:15,01:30,01:45,02:00,02:15,02:30,02:45,03:00,03:15,03:30,03:45,04:00,04:15,04:30,04:45'
        appointment.save()
    else:
        # appointment already created
        print 'Already exists!!!'

###############################################################################################################
# tutor_schedule_check -
# It checks whether selected appointment is in tutor scheduled.
###############################################################################################################
def tutor_schedule_check(tutor, date, time, duration) :

    print '!!!!!!!!!!!!!!!!!!!!!'
    time1 = datetime.datetime.strptime(str(time), '%I:%M%p')
    print time
    time1 = str(time1).split(' ')
    timeList = time1[1].split(':')
    timeList = [int (x) for x in timeList]

    dateList = date.split('/')
    dateList = [int (x) for x in dateList]
    
    # This is appointment timing
    checkAppointmentTime = datetime.datetime(dateList[2],dateList[0],dateList[1],timeList[0],timeList[1])
    
    dateDash = str(date).split('/')
    
    dateDash = str(dateDash[2] + '-' + dateDash[0] + '-' + dateDash[1])
    print dateDash
    dateString = str(dateDash) + ' ' + str(time)
    print dateString
    format = '%Y-%m-%d %I:%M%p'
    
    makeDate = datetime.datetime.strptime(dateString, format)
    print 'makedate' 
    print  makeDate
    addedTime = makeDate + timedelta(minutes = int(duration))
    print 'addedtime'
    print addedTime
    appointmentEnd = str(addedTime).split(" ")
    
    appointmentEndTime = appointmentEnd[1].split(':')
    appointmentEndTime = [int (x) for x in appointmentEndTime]
    
    checkAppointmentEndTime = datetime.datetime(dateList[2],dateList[0],dateList[1],appointmentEndTime[0],appointmentEndTime[1])  
    
    ######
    tutorObj = Tutor.objects.get(tutor = str(tutor))
    startString = tutorObj.start
    endString = tutorObj.end
    ######
    startList = startString.split(',')
    endList = endString.split(',')
    
    toDay = datetime.date(dateList[2],dateList[0],dateList[1]).weekday()
    tutorStart = startList[toDay]
    tutorStart = datetime.datetime.strptime(tutorStart, '%I:%M%p')
    tutorEnd = endList[toDay]
    tutorEnd = datetime.datetime.strptime(tutorEnd, '%I:%M%p')
    
    print '####'
    print tutorStart
    print '$$$$'
    print tutorEnd
    tutorStart = str(tutorStart).split(' ')
    tutorStartTime = tutorStart[1].split(':')
    tutorStartTime = [int (x) for x in tutorStartTime]
    
    checkStartTime = datetime.datetime(dateList[2],dateList[0],dateList[1],tutorStartTime[0],tutorStartTime[1])
    
    tutorEnd = str(tutorEnd).split(' ')
    tutorEndTime = tutorEnd[1].split(':')
    tutorEndTime = [int (x) for x in tutorEndTime]
    
    checkEndTime = datetime.datetime(dateList[2],dateList[0],dateList[1],tutorEndTime[0],tutorEndTime[1])
    print '-------'
    print checkAppointmentTime.time()
    print checkStartTime.time()
    
    print checkAppointmentEndTime.time()   
    print checkEndTime.time()
    
    if (checkAppointmentTime.time() < checkStartTime.time()) :
        return 0
    elif (checkAppointmentEndTime.time() > checkEndTime.time()) :
        return 0
    else:
        return 1
 
###############################################################################################################
# check_slot_availability -
# It checks whether selected appointment slot is available under the selected tutor.
# In case of already booked appointment, it suggests new slot if available.
###############################################################################################################
def check_slot_availability(tutor, date, time, duration) :
    
    #AppointmentAvailability.objects.all().delete()
    appointmentAvailable = AppointmentAvailability.objects.get(tutor = str(tutor), date = str(date))
    
    listSlots = []
    listSlots = appointmentAvailable.slotAvail.split(',')
    
    dateString = str(date) + ' ' + str(time)
    print dateString
    format = '%m/%d/%Y %H:%M%p'
    
    print 'slots after get'
    print listSlots
    
    slotString = '08:00,08:15,08:30,08:45,09:00,09:15,09:30,09:45,10:00,10:15,10:30,10:45,11:00,11:15,11:30,11:45,12:00,12:15,12:30,12:45,01:00,01:15,01:30,01:45,02:00,02:15,02:30,02:45,03:00,03:15,03:30,03:45,04:00,04:15,04:30,04:45'
    slotSuggestions=slotString.split(',')
    makeDate = datetime.datetime.strptime(dateString, format)
    
    print 'makedate'
    print makeDate
    storeSlot = []
    runloop = 0
    if duration == '15':
        addedTime = makeDate + timedelta(minutes = 0)
        print 'addedtime'
        print addedTime
        printDate = str(addedTime).split(" ")[1][:5]
        runLoop = 1
        print 'printdate'
        print printDate
        storeSlot.append(printDate)
    elif duration == '30':
        addedTime = makeDate + timedelta(minutes = 0)
        printDate = str(addedTime).split(" ")[1][:5]
        storeSlot.append(printDate)
        
        addedTime = makeDate + timedelta(minutes = 15)
        printDate = str(addedTime).split(" ")[1][:5]
        storeSlot.append(printDate)
        runLoop = 2
    elif duration == '45':
        addedTime = makeDate + timedelta(minutes = 0)
        printDate = str(addedTime).split(" ")[1][:5]
        storeSlot.append(printDate)
        
        addedTime = makeDate + timedelta(minutes = 15)
        printDate = str(addedTime).split(" ")[1][:5]
        storeSlot.append(printDate)    
        
        addedTime = makeDate + timedelta(minutes = 30)
        printDate = str(addedTime).split(" ")[1][:5]
        storeSlot.append(printDate)
        runLoop = 3
    elif duration == '60':
        addedTime = makeDate + timedelta(minutes = 0)
        printDate = str(addedTime).split(" ")[1][:5]
        storeSlot.append(printDate)
        
        addedTime = makeDate + timedelta(minutes = 15)
        printDate = str(addedTime).split(" ")[1][:5]
        storeSlot.append(printDate)    
        
        addedTime = makeDate + timedelta(minutes = 30)
        printDate = str(addedTime).split(" ")[1][:5]
        storeSlot.append(printDate)
        
        addedTime = makeDate + timedelta(minutes = 45)
        printDate = str(addedTime).split(" ")[1][:5]
        storeSlot.append(printDate)
        runLoop = 4

    print '####'
    print storeSlot
    slotFlag = 0
    for i in range(0, len(storeSlot)):
        if storeSlot[i] not in listSlots:
            slotFlag = 0
            break
        else:
            slotFlag = 1
            
    if slotFlag == 1:
        for j in range(0, len(storeSlot)):
            listSlots.remove(storeSlot[j])
            #return 1
        print 'slots after deletion'
        print listSlots
        slotAvail = ','.join(listSlots)
        appointmentAvailable.slotAvail = slotAvail
        appointmentAvailable.save()
        print slotAvail
        return 1
    else:
        try:
            timeIndex=slotSuggestions.index(storeSlot[0])
        except ValueError:
            print -1
        foundIndex = 0
        for listIndex in range(timeIndex,len(slotSuggestions)):
            if slotSuggestions[listIndex] in listSlots :
                foundIndex = listSlots.index(slotSuggestions[listIndex])
                break
        
        suggestionList=[]
        foundIndex1=0
        for i in range(foundIndex,len(listSlots)) :
            foundIndex1 = i
            for j in range(foundIndex1,runLoop+foundIndex1) :
                if j < len(listSlots) :
                    suggestionList.append(listSlots[j])
                else :
                    return 0
        
            suggestionString = ','.join(suggestionList)
            if suggestionString in slotString :
                break
            else :
                return 0
        
                
        print '$%^&*(**&^%$##$%^#@#%^&*%$#@#'
        print suggestionList
        startTimeList = suggestionList[0].split(':')
        startTime = datetime.datetime(100,1,1,int(startTimeList[0]),int(startTimeList[1]),0)
        endTime = startTime + timedelta(minutes = int(duration))
        startTime=str(startTime).split(" ")[1][:5]
        endTime=str(endTime).split(" ")[1][:5]
        
        sendString = str(startTime) + ' - ' + str(endTime)
        print sendString
        return sendString
        

### Displays an tutor availability
def tutor_form(request):
    return render(request, 'portal/index.html')

###############################################################################################################
# tutor_schedule1 -
# This is extra function for storing tutor schedule in the database.
# It hardcodes the schedule for each tutor.
###############################################################################################################
def tutor_schedule1(tutorName) :
    
    if tutorName == 'Chinmai':
        tutorChin, create = Tutor.objects.get_or_create(tutor = str(tutorName))
        if create:
            tutorChin.tutor = 'Chinmai'
            tutorChin.start = '9:00AM,2:00PM,8:00AM,1:00PM,10:00AM'
            tutorChin.end = '1:00PM,5:00PM,1:00PM,5:00PM,2:00PM'
            tutorChin.save()
            return 1
        else:
            print 'Tutor exists'
            return 0
    
    if tutorName == 'David':
        tutorDavid, create = Tutor.objects.get_or_create(tutor = str(tutorName))
        if create:
            tutorDavid.tutor = 'David'
            tutorDavid.start = '8:00AM,10:00AM,12:00PM,8:00AM,2:00PM'
            tutorDavid.end = '12:00PM,2:00PM,5:00PM,12:00PM,5:00PM'
            tutorDavid.save()
            return 1
        else:
            print 'Tutor exists'
            return 0
        
    if tutorName == 'Grace':
        tutorGrace, create = Tutor.objects.get_or_create(tutor = str(tutorName))
        if create:
            tutorGrace.tutor = 'Grace'
            tutorGrace.start = '1:00PM,8:00AM,9:00AM,9:00AM,8:00AM'
            tutorGrace.end = '5:00PM,1:00PM,12:00PM,2:00PM,11:00AM'
            tutorGrace.save()
            return 1
        else:
            print 'Tutor exists'
            return 0
 
def load_courses(request) :
    print 'loading courses'
    
    return redirect('/portal')

###############################################################################################################
# tutor_schedule -
# This function loads JSON and stores schedule for tutors in the objects.
# This function needs to be called after changes in the JSON for the changes to be reflected in the objects.
###############################################################################################################
def tutor_schedule(tutor) :
    fname = 'portal/schedule.json'
    
    json_data=open(fname)

    data = json.load(json_data)
    # pprint(data)


    print data[tutor][0]["start"]
    json_data.close()

    tutorObj, create = Tutor.objects.get_or_create(tutor = str(tutor))
    if create:
        tutorObj.tutor = str(tutor)
        tutorObj.start = str(data[str(tutor)][0]["start"])
        tutorObj.end = str(data[str(tutor)][1]["end"])
        tutorObj.save()
        return 1
    else:
        print 'Tutor exists'
        tutorObj = Tutor.objects.get(tutor = str(tutor))
        tutorObj.tutor = str(tutor)
        tutorObj.start = str(data[str(tutor)][0]["start"])
        tutorObj.end = str(data[str(tutor)][1]["end"])
        tutorObj.save()
  
        return 0

###############################################################################################################
# tutor_schedule2 -
# This is extra function for storing tutor schedule in the database.
# It read from the schedule for each tutor from text file.
###############################################################################################################
def tutor_schedule2(tutor) :
    fname = 'portal/schedule.txt'
    tutorName = []
    startString = []
    endString = []
    with open(fname) as f:
        content = f.readlines()
  
        for i in range(0,len(content)):
            if content[i][0] == '[':
                tutorName.append(content[i][1:-2]) 
            elif content[i].split('-')[0] == 'START':
                startString.append(content[i][:-1].split('-')[1])
            elif content[i].split('-')[0] == 'END':
                endString.append(content[i][:-1].split('-')[1])
        
        print tutorName
        print startString
        print endString
        
        for i in range(0,len(tutorName)):
            if tutorName[i] == tutor :
                tutorObj, create = Tutor.objects.get_or_create(tutor = str(tutor))
                if create:
                    tutorObj.tutor = str(tutorName[i])
                    tutorObj.start = str(startString[i])
                    tutorObj.end = str(endString[i])
                    tutorObj.save()
                    return 1
                else:
                    print 'Tutor exists'
                    tutorObj = Tutor.objects.get(tutor = str(tutor))
                    tutorObj.tutor = str(tutorName[i])
                    tutorObj.start = str(startString[i])
                    tutorObj.end = str(endString[i])
                    tutorObj.save()
              
                    return 0
       
###############################################################################################################
# tutor_availability -
# This function creates calendar events according to tutor schedule.
# Calendar events are generated on the student login page.
###############################################################################################################
def tutor_availability(request):
    
    """if 'tutor' in request.POST:
        tutor_name = request.POST['tutor']
        message += 'Your first name: %r' % tutor_name
    else:
        message = 'Please enter your first name.' 
    print message"""
    
    now = datetime.datetime.now()
    #AppointmentAvailability.objects.all().delete()
    #CalendarEvent.objects.filter(css_class='event-success').delete()
    #CalendarEvent.objects.filter(css_class='event-primary').delete() 
    #Tutor.objects.all().delete()
    
    tutorName=request.POST['tutor']
    
    createEvent = tutor_schedule(tutorName)
    
    if createEvent == 1:
    
        tutorObject = Tutor.objects.get(tutor=str(tutorName))
        
        currMonth = str(now.month)
        currYear = str(now.year)
        today = int(now.day) 
        noOfDays= calendar.monthrange(now.year, now.month)[1]

        for currDate in range(today,noOfDays+1) :
        
            availabilityTutor = CalendarEvent()
            availabilityTutor.tutor = tutorName
            
            toDay = date(now.year,now.month,currDate).weekday()
            
            if   toDay > 4:
                continue
                
            startString = str(currMonth + '/' + str(currDate) + '/' + currYear + ' ' + str(tutorObject.start.split(',')[toDay]))
            endString = str(currMonth + '/' + str(currDate) + '/' + currYear + ' ' + str(tutorObject.end.split(',')[toDay]))
            availabilityTutor.start= datetime.datetime.strptime(startString, '%m/%d/%Y %I:%M%p')
            print availabilityTutor.start
            availabilityTutor.end= datetime.datetime.strptime(endString, '%m/%d/%Y %I:%M%p')
            print availabilityTutor.end
            availabilityTutor.css_class = 'event-success'
            title =  availabilityTutor.tutor + ' available from ' + str(availabilityTutor.start).split(' ')[1][:5] + ' to ' + str(availabilityTutor.end).split(' ')[1][:5]
            #event.availability = False
            availabilityTutor.title = title
            availabilityTutor.save()
         
        print "tutor scheduled"
     
    else:
        tutorObject = Tutor.objects.get(tutor=str(tutorName))
        
        currMonth = str(now.month)
        currYear = str(now.year)
        today = int(now.day) 
        noOfDays= calendar.monthrange(now.year, now.month)[1]
        CalendarEvent.objects.filter(tutor = tutorName,css_class='event-success').delete()
        for currDate in range(today,noOfDays+1) :
        
            availabilityTutor = CalendarEvent()
            availabilityTutor.tutor = tutorName
            
            toDay = date(now.year,now.month,currDate).weekday()
            
            if   toDay > 4:
                continue
                
            startString = str(currMonth + '/' + str(currDate) + '/' + currYear + ' ' + str(tutorObject.start.split(',')[toDay]))
            endString = str(currMonth + '/' + str(currDate) + '/' + currYear + ' ' + str(tutorObject.end.split(',')[toDay]))
            availabilityTutor.start= datetime.datetime.strptime(startString, '%m/%d/%Y %I:%M%p')
            print availabilityTutor.start
            availabilityTutor.end= datetime.datetime.strptime(endString, '%m/%d/%Y %I:%M%p')
            print availabilityTutor.end
            availabilityTutor.css_class = 'event-success'
            title =  availabilityTutor.tutor + ' available from ' + str(availabilityTutor.start).split(' ')[1][:5] + ' to ' + str(availabilityTutor.end).split(' ')[1][:5]
            #event.availability = False
            availabilityTutor.title = title
            availabilityTutor.save()
            
        print 'Tutor schedule modified'
    #print Tutor_chin.tutor,Tutor_chin.start,Tutor_chin.end
    # CalendarEvent.objects.filter(css_class='event-primary').delete()
    """
    data1=Tutor.objects.get(tutor = "Chinmai")
    print data1.tutor,data1.start,data1.end
    print data1.start.split(",")[0]
    """
    return redirect('/portal')

    
    
### Displays an tutor availability
def filtertutor_form(request):
    return render(request, 'portal/index.html')
 
def tutor_filter(request) :
    
    tutorName = '';
    message = ''

    if 'tutor' in request.POST:
        tutorName = request.POST['tutor']
        if tutorName == 'no_preference':
            tutorName = 'Anyone Available'
        else:
            message += '<br></br>Your tutor: %r' % tutorName
    else:
        message = 'Please enter a tutor.'

    for tutor in CalendarEvent.objects.all() :
        if tutor.tutor == tutorName :
            continue
        tutor.css_class = ''
        
        tutor.save()
   
    return redirect('/portal')


#############################################
# Form Test
#############################################

### Displays a search form
def search_form(request):
    return render(request, 'search_form.html')

### Function to search for whatever term the user entered via the request
def search(request):
    #Handles the GET request
    if 'q' in request.GET:
        message = 'You searched for: %r' % request.GET['q'] #Returns what the user searched for
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message) #Return an HttpResponse with the result message

#############################################
# Main Calendar View
#############################################

def portal_main_page(request):

    #if request.method == 'POST':
        # form = AppointmentForm(request.POST, request.FILES)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             course = form.cleaned_data['course']
#             date = form.cleaned_data['date']
#             comment = form.cleaned_data['comment']
# # <<<<<<< HEAD:portal/views.py
#             recipients = ['glchriste@gmail.com', 'wevie13@gmail.com']
# # =======
# #             recipients = ['wevie13@gmail.com']
# # >>>>>>> a5577930ebce31881ed307749d7fa01d02b92d19:TutoringApplication/portal/views.py
#             #Send Email with data
#             from django.core.mail import send_mail
#             send_mail('Tutoring Appointment Scheduled', comment, email, recipients)


            #return HttpResponseRedirect(reverse('portal:portal_main_page'))
            
            #return render_to_response('portal/index.html')
    #else:
        #form = AppointmentForm()
 
    #data = {'form': form}
    #return render_to_response('portal/index.html', data, context_instance=RequestContext(request))
    login_student(request)
    return HttpResponseRedirect('portal/index.html')
        # return HttpResponseRedirect(reverse('portal:portal_main_page'))

from django.views.generic import ListView, TemplateView
from models import CalendarEvent

from serializers import event_serializer
from utils import timestamp_to_datetime

import datetime

#############################################
# Converts calendar events to JSON list
#############################################

class CalendarJsonListView(ListView):

    template_name = 'django_bootstrap_calendar/calendar_events.html'
    #Returns the calendar events as a JSON
    def get_queryset(self):
        queryset = CalendarEvent.objects.filter()
        from_date = self.request.GET.get('from', False)
        to_date = self.request.GET.get('to', False)

        if from_date and to_date:
            queryset = queryset.filter(
                start__range=(
                    timestamp_to_datetime(from_date) + datetime.timedelta(-30),
                    timestamp_to_datetime(to_date)
                    )
            )
        elif from_date:
            queryset = queryset.filter(
                start__gte=timestamp_to_datetime(from_date)
            )
        elif to_date:
            queryset = queryset.filter(
                end__lte=timestamp_to_datetime(to_date)
            )

        return event_serializer(queryset)


class CalendarView(TemplateView):

    template_name = 'portal/index.html'

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super(CalendarView, self).dispatch(*args, **kwargs)
