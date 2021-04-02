from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User,Instructor,Student,Course,Assignment,Submission    
from uuid import UUID
import simplejson as json
from . import design_tool
# Create your views here.
def home(request):
    return render(request, "main/home.html")

def servomotor(request):
    return render(request, "main/servomotor.html")

def test(request):
    Gs, mag_comp, phase_comp, omega_comp, mag, phase, omega = design_tool.control()
    if request.method == "POST":
        return render(request, "main/test.html", {
                
                "omega": omega,
                "ph": phase,
                "mag": mag,
                "name": 'Servo Motor',
                "numerator": "3",
                "denominator": "3 +1",
                "mag_comp": mag_comp,
                "ph_comp": phase_comp,
                "omega_comp":omega_comp
            })
    return render(request, "main/test.html", {
                
                "omega": omega,
                "ph": phase,
                "mag": mag,
                "name": 'Servo Motor',
                "numerator": "3",
                "denominator": "3s^2 +1"
            })

def register(request):
    try: # Check if already logged in and have an account
        user = User.objects.get(username=request.user)
        return HttpResponseRedirect(reverse("home"))
    except :
        if request.method == "POST":
            username = request.POST.get("username")
            first=request.POST.get("first")
            last=request.POST.get("last")
            major= request.POST.get("major")
            email = request.POST.get("email")
            code=request.POST.get("code")
            agree=request.POST.get("agree")
            password = request.POST.get("password")
            confirmation = request.POST.get("confirmation")
            # Attempt to create new user
            # If the user is an instructor
            if request.POST.get("instructor"):
                # Ensure all fields are filled correctly
                if not password or not email or not username or not first or not last:
                    return render(request, "main/register.html", {
                        "instMSG": "Make sure all fields are filled."
                    })
                # Ensure password matches confirmation
                if password != confirmation:
                    return render(request, "main/register.html", {
                        "instMSG": "Passwords must match."
                    })
                # Ensure that the user agrees to all terms and privacy policy
                if not request.POST.get("agree")=="on":
                    return render(request, "main/register.html", {
                        "instMSG": "You need to agree on the terms in order to sign up."
                    })
                try:
                    user = User.objects.create_user(username, email, password,status="i",first_name=first,last_name=last)
                    user.save()
                    instructor=Instructor.objects.create(credentials=user,major=major)
                    instructor.save()
                except IntegrityError:
                    return render(request, "main/register.html", {
                        "instMSG": "Username already taken."
                    })
            # If the user is a student
            elif request.POST.get("student"):
                # Ensure all fields are filled correctly
                if not password or not email or not username or not first or not last:
                    return render(request, "main/register.html", {
                        "studMSG": "Make sure all fields are filled."
                    })
                # Ensure password matches confirmation
                if password != confirmation:
                    return render(request, "main/register.html", {
                        "studMSG": "Passwords must match."
                    })
                # Ensure that the user agrees to all terms and privacy policy
                if not request.POST.get("agree")=="on":
                    return render(request, "main/register.html", {
                        "studMSG": "You need to agree on the terms in order to sign up."
                   })  
                try: # Creating New User
                    try : # Check if the Course Code is valid.
                        temp = UUID(code,version=4)
                    except:
                        return render(request, "main/register.html", {
                        "studMSG": "Make sure that your course code is valid."
                    })
                    course=Course.objects.get(code=code)
                    user = User.objects.create_user(username, email, password,status="s",first_name=first,last_name=last)
                    user.save()
                    student=Student.objects.create(credentials=user,courses=course,major=major)
                    student.save()
                except IntegrityError:
                    return render(request, "main/register.html", {
                        "studMSG": "Username already taken."
                    })
                if not code:
                    return render(request, "main/register.html", {
                        "studMSG": "Make sure to enter your course code correctly."
                    })
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "main/register.html")
def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "main/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "main/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))

def student(request):
    try:
        assignments=[]
        student=Student.objects.get(credentials=request.user)
        for something in student.courses.assignments.filter():
            for sub in Submission.objects.filter(student=student):
                print(something)
            assignments.append(something)
        return render(request,"main/student.html",{
            "student":student,
            "assignments": assignments
        })
    except:
        return HttpResponseRedirect(reverse("home")) 

def instructor(request):
    try:    
        instructor= Instructor.objects.get(credentials=request.user)
    except:
        return HttpResponseRedirect(reverse("home"))
    courses=[]
    assignments=[]
    simulators=[]
    courseAssignments=[] #Assignment in each course 
    courseAssignment={} #course:assignment pairs
    assignmentSubmissions=[] #Submissions in each assignment
    assignmentSubmission={} #Assignment:submissions pairs
    course=Course.objects.filter(instructor=request.user)
    assignment=Assignment.objects.filter(instructor=request.user)
    for something in course:
        courses.append(something.name)
        for assign in something.assignments.all():
            courseAssignments.append(assign.subject)
            for submission in Submission.objects.filter(assignment=assign):
                assignmentSubmissions.append(submission)
            assignmentSubmission[f"{something.name}:{assign.subject}"]=assignmentSubmissions[:]
            assignmentSubmissions.clear()
        courseAssignment[something.name]=courseAssignments[:]
        courseAssignments.clear()
    for something in assignment:
        assignments.append(something)    
    for choice in Assignment.simulator_choices:
        simulators.append(choice[0])
    if request.POST:
        if request.POST.get("sim"):
            # Reminder: Check if there are missing fields
            sim = request.POST.get("sim")
            course = request.POST.get("course")
            desc = request.POST.get("desc")
            due = request.POST.get("due")
            subject = request.POST.get("assignmentSubject")
            assign=Assignment.objects.create(subject=subject,dueDate=due,simulator=sim,describtion=desc,score=5,instructor=request.user.username) #Scoere Adjust
            assign.save()
            course=Course.objects.get(name=course)
            course.assignments.add(assign)
            return HttpResponseRedirect(reverse("instructor"))
        if request.POST.get("courseName"):
        # Reminder: Check if there are missing fields
            courseName = request.POST.get("courseName")
            course=Course.objects.create(name=courseName,instructor=request.user)
            course.save
            return HttpResponseRedirect(reverse("instructor"))
    else:
        print(assignmentSubmission)
        return render(request,"main/instructor.html",{
            "instructor":instructor,
            "assignments": assignments,
            "simulators": simulators,
            "courseAssignment":courseAssignment,
            "courses":courses,
            "assignmentSubmission":assignmentSubmission,
        }) 


def cruise(request):
    v = [15.0, 14.517994703951095, 14.990900693284932, 15.448906990430494, 15.893289393001073, 16.32514885061716, 16.745443289989346, 17.15501235913015, 17.554596926348335, 17.944854629518034, 18.32637241196884, 18.699676731958508, 19.065241951262685, 19.42349728475093, 19.774832601677062, 20.119603302370187, 20.4581344463261, 20.790724272620878, 21.117647193377714, 21.43915637904837, 21.755485995613334, 22.0668531476201, 22.37345957312496, 22.675493128155296, 22.97312909151734, 23.266531316309294, 23.555853249335666, 23.84123883631197, 24.122823328394755, 24.40073400283375, 24.675090808656993, 24.946006946406506, 25.21358939061125, 25.477939360873883, 25.73915274886799, 25.99732050465424, 26.252528988091846, 26.504860288871456, 26.754392518261742, 27.001200075797467, 27.24535389326923, 27.486921658938925, 27.72596802281114, 27.962554785996637, 28.196741074763118, 28.428583501776206, 28.658136314391232, 28.882010732068178, 29.09926917837794, 29.310402907860517, 29.515419573035103, 29.7144806004295, 29.907690973776678, 30.095168627665032, 30.27702221367454, 30.453358643081774, 30.62428097890266, 30.789889401596323, 30.950281170051472, 31.10555124823723, 31.255791294629137, 31.401091168658464, 31.54153835141748, 31.67721830436581, 31.80821452483026, 31.934608683307502, 32.056480724017845, 32.173908967434556, 32.28697020207979, 32.39573977151399, 32.500291654643284, 32.600698541081115, 32.6970319006869, 32.78936204936937, 32.877758209922504, 32.96228856818084, 33.04302032750444, 33.12001975714846, 33.193352239530746, 33.26308231057252, 33.32927370296353, 33.39198938414369, 33.45129159191787, 33.50724186124898, 33.55990106121566, 33.60932943392812, 33.655586607990735, 33.69873162750894, 33.73882297442078, 33.77591859064857, 33.81007589833055, 33.84135181873918, 33.8698027898146, 33.89548478242802, 33.91845331542986, 33.93876346954857, 33.95646990019717, 33.971626849241986, 33.9842881557839, 33.99450726599956, 34.002337242086504, 34.00783077035343, 34.01104016849476, 34.01201739208538, 34.01081404033023, 34.007481361100616, 34.00207025528797, 33.994631280503405, 33.98521465415077, 33.97387025589852, 33.96064762957526, 33.94559598451236, 33.928764196355665, 33.91020080736804, 33.88995402624309, 33.86807172744976, 33.84460145012699, 33.81959039654657, 33.79308543016251, 33.76513307326371, 33.735779504247255, 33.705070554528795, 33.673051705106076, 33.63976808279163, 33.6052644561304, 33.569585231017484, 33.53277444603165, 33.494875767499515, 33.45593248430555, 33.41598750246291, 33.375083339460005, 33.33326211839758, 33.29056556193145, 33.2470349860355, 33.20271129359989, 33.15763496787952, 33.111846065807654, 33.065384211189524, 33.018288587791105, 32.97059793233827, 32.92235052744104, 32.87358419445859, 32.82433628631979, 32.77464368031495, 32.72454277087352, 32.67406946234352, 32.62325916178779, 32.572146771812214, 32.5207666834413, 32.469152769056485, 32.41733837541187, 32.36535631674298, 32.31323886798313, 32.26101775810241, 32.208724163584, 32.15638870205233, 32.10404142606736, 32.051711817099225, 31.999428779697062, 31.947220635865563, 31.89511511966269, 31.84313937203147, 31.791319935878445, 31.739682751411117, 31.68825315174621, 31.637055858800053, 31.586114979472214, 31.535454002132642, 31.485095793422435, 31.435062595377463, 31.385376022883943, 31.336057061473916, 31.2871260654686, 31.23860275647641, 31.19050622225225, 31.142854915923603, 31.095666655588733, 31.048958624291146, 31.002747370374166, 30.95704880821848, 30.91187821936503, 30.8672502540247, 30.823178932975637, 30.77967764984833, 30.736759173797772, 30.694435652561314, 30.652718615900298, 30.611618979422417, 30.571147048781555, 30.531312524250783, 30.4921245056637, 30.453591497718577, 30.41572141563916, 30.378521591185308, 30.34199877900608, 30.306159163327266, 30.271008364964832, 30.23655144865518, 30.20279293069263, 30.169736786864092, 30.137386460670278, 30.105744871822704, 30.074814425004952, 30.04459701888662, 30.01509405537788, 29.986306449112337, 29.958234637145654, 29.930878588857034, 29.904237816040688, 29.878311383174097, 29.853097917849645, 29.828595621356495, 29.80480227939905, 29.781715272938648, 29.759331589144995, 29.737647832443926, 29.71666023564805, 29.696364671157113, 29.676756662214874, 29.657831394209467, 29.639583726004457, 29.622008201287926, 29.605099059927195, 29.58885024931702, 29.573255435709324, 29.558308015512882, 29.54400112655165, 29.530327659270668, 29.517280267878956, 29.504851381419048, 29.493033214753176, 29.481817779456595, 29.47119689460874, 29.461162197473463, 29.45170515405992, 29.44281706955606, 29.43448909862707, 29.42671225557166, 29.419477424329205, 29.412775368331584, 29.406596740193464, 29.400932091235646, 29.39577188083622, 29.391106485604695, 29.386926208374817, 29.38322128701202, 29.379981903031894, 29.37719819002641, 29.374860241895163, 29.372958120878923, 29.371481865393505, 29.37042149766205, 29.369767031144274, 29.369508477761496, 29.369635854916627, 29.370139192308535, 29.37100853854056, 29.372233967523147, 29.373805584670947, 29.37571353289489, 29.37794799838993, 29.38049921621972, 29.383357475699132, 29.386513125576307, 29.389956579015763, 29.39367831838446, 29.39766889984271, 29.40191895774224, 29.406419208833615, 29.4111604562855, 29.41613359351843, 29.4213296078557, 29.42673958399424, 29.432354707298426, 29.438166266919808, 29.44416565874588, 29.45034438818102, 29.45669407276297, 29.463206444617974, 29.469873352758075, 29.476686765223917, 29.483638771076414, 29.490721582240884, 29.49792753520698, 29.505249092588027, 29.512678844543178, 29.52020951006601, 29.527833938142923, 29.535545108784994, 29.54333613393667, 29.55120025826482, 29.55913085983162, 29.567121450654636, 29.57516567715761, 29.583257320515266, 29.591390296895423, 29.59955865760193, 29.607756589121383, 29.615978413077148, 29.624218586093708, 29.632471699574474, 29.640732479396267, 29.64899578552338, 29.657256611544295, 29.665510084134002, 29.673751462444734, 29.681976137428062, 29.69017963109105, 29.698357595689235, 29.706505812859096, 29.714620192692674, 29.722696772756784, 29.730731717059502, 29.738721314966224, 29.74666198006779, 29.75455024900294, 29.762382780237466, 29.770156352802196, 29.777867864992096, 29.78551433302849, 29.79309288968657, 29.800600782890093, 29.808035374275413, 29.815394137726482, 29.822674657882963, 29.82987462862303, 29.836991851522807, 29.844024234293922, 29.850969789201088, 29.85782663146114, 29.864592977625136, 29.87126714394509, 29.877847544726755, 29.884332690669876, 29.89072118719737, 29.897011732774693, 29.903203117220716, 29.909294220011425, 29.9152840085776, 29.921171536597676, 29.92695594228689, 29.932636446683954, 29.938212351936134, 29.943683039583895, 29.949047968846106, 29.954306674906686, 29.959458767203742, 29.964503927721957, 29.969441909289262, 29.974272533878498, 29.978995690914893, 29.98361133559021, 29.98811948718426, 29.992520227394458, 29.996813698674217, 30.001000102580786, 30.005079698133194, 30.009052800180875, 30.012919777783658, 30.01668105260359, 30.020337097309245, 30.02388843399291, 30.02733563260129, 30.03067930938013, 30.033920125333214, 30.037058784696217, 30.040096033425836, 30.043032657704497, 30.045869482461192, 30.048607369908662, 30.05124721809733, 30.05378995948632, 30.056236559531843, 30.058588015293275, 30.060845354057186, 30.06300963197957, 30.065081932746544, 30.067063366253745, 30.068955067304643, 30.070758194327947, 30.072473928114313, 30.074103470572535, 30.075648043505343, 30.077108887405036, 30.07848726026898, 30.079784436435112, 30.08100170543773, 30.082140370883348, 30.083201749346998, 30.08418716928891, 30.085097969991658, 30.0859355005178, 30.086701118688143, 30.08739619008053, 30.088022087049293, 30.08858018776531, 30.089071875276698, 30.089498536590114, 30.089861561772643, 30.09016234307434, 30.090402274071163, 30.09058274882856, 30.090705161085367, 30.090770903458182, 30.09078136666598, 30.090737938774968, 30.090642004463657, 30.090494944307846, 30.090298134085735, 30.090052944102716, 30.089760738536004, 30.089422874798842, 30.089040702924166, 30.088615564967636, 30.088148794429898, 30.087641715697814, 30.08709564350471, 30.086511882409283, 30.08589172629311, 30.08523645787659, 30.084547348253096, 30.083825656441185, 30.08307262895464, 30.082289499390292, 30.081477488033187, 30.080637801479156, 30.07977163227435, 30.07888015857176, 30.07796454380431, 30.077025936374415, 30.076065469359797, 30.075084260235222, 30.0740834106101, 30.07306400598156, 30.072027115502895, 30.070973791767013, 30.06990507060479, 30.06882197089799, 30.067725494406535, 30.066616625609903, 30.065496331562397, 30.06436556176198, 30.063225248032538, 30.062076304419186, 30.060919627096517, 30.05975609428935, 30.058586566205935, 30.05741188498314, 30.05623287464356, 30.055050341064145, 30.053865071956164, 30.052677836856223, 30.05148938712808, 30.050300455974966, 30.04911175846225, 30.047923991550043, 30.04673783413562, 30.045553947105297, 30.04437297339558, 30.04319553806328, 30.042022248364365, 30.040853693841267, 30.03969044641843, 30.038533060505774, 30.037382073109946, 30.03623800395294, 30.035101355597984, 30.033972613582392, 30.0328522465571, 30.03174070643267, 30.0306384285316, 30.02954583174649, 30.0284633187041, 30.027391275934814, 30.026330074047465, 30.025280067909154, 30.024241596829913, 30.023214984751974, 30.02220054044339, 30.021198557695808, 30.020209315526213, 30.01923307838233, 30.018270096351586, 30.017320605373307, 30.016384827454097, 30.015462970886, 30.01455523046741, 30.01366178772647, 30.01278281114674, 30.011918456394973, 30.011068866550843, 30.01023417233836, 30.009414492358882, 30.008609933325456, 30.007820590298415, 30.00704654692196, 30.006287875661638, 30.0055446380425, 30.00481688488786, 30.00410465655832, 30.00340798319118, 30.00272688493982, 30.00206137221308, 30.001411445914417, 30.00077709768073, 30.000158310120703, 29.999555057052554, 29.99896730374105, 29.998395007133656, 29.99783811609571, 29.997296571644547, 29.996770307182327, 29.99625924872764, 29.995763315145627, 29.99528241837662, 29.994816463663103, 29.99436534977504, 29.99392896923329, 29.993507208531224, 29.99309994835426, 29.99270706379739, 29.99232842458056, 29.991963895261794, 29.991613335448047, 29.991276600003715, 29.99095353925665, 29.990643999201758, 29.990347821702, 29.990064844686795, 29.989794902347764, 29.98953782533176, 29.989293440931128, 29.98906157327119, 29.98884204349485, 29.98863466994431, 29.988439268339913, 29.988255651955967, 29.98808363179362, 29.987923016750724, 29.98777361378861, 29.98763522809586, 29.98750766324896, 29.98739072136984, 29.987284203280325, 29.987187908653418, 29.98710163616147, 29.98702518362117, 29.986958348135378, 29.986900926231804, 29.986852713998516, 29.986813507216247, 29.986783101487575, 29.986761292362903, 29.986747875463298, 29.986742646600163, 29.986745401891774, 29.986755937876648, 29.986774051623833, 29.98679954084005, 29.986832203973744, 29.986871840316077, 29.986918250098817, 29.98697123458922, 29.98703059618187, 29.98709613848752, 29.98716766641897, 29.98724498627395, 29.987327905815132, 29.987416234347183, 29.987509782790994, 29.987608363755015, 29.98771179160383, 29.987819882523883, 29.98793245458652, 29.98804932780824, 29.988170324208326, 29.98829526786375, 29.988423984961532, 29.988556303848462, 29.988692055078303, 29.988831071456474, 29.988973188082248, 29.989118242388543, 29.989266074179277, 29.98941652566442, 29.98956944149265, 29.989724668781808, 29.98988205714705, 29.99004145872684, 29.99020272820677, 29.99036572284127, 29.9905303024732, 29.990696329551476, 29.990863669146645, 29.991032188964525, 29.991201759357942, 29.991372253336582, 29.99154354657502, 29.991715517418985, 29.991888046889834, 29.99206101868735, 29.99223431919092, 29.992407837458995, 29.99258146522706, 29.992755096904045, 29.9929286295672, 29.993101962955585, 29.993274999462084, 29.993447644124082, 29.993619804612802, 29.99379139122134, 29.993962316851466, 29.9941324969992, 29.994301849739212, 29.99447029570811, 29.9946377580866, 29.99480416258062, 29.994969437401434, 29.99513351324476, 29.995296323268953, 29.995457803072263, 29.995617890669248, 29.995776526466354, 29.99593365323666, 29.996089216093893, 29.996243162465724, 29.996395442066333, 29.99654600686835, 29.996694811074132, 29.996841811086508, 29.996986965478875, 29.997130234964853, 29.99727158236738, 29.997410972587375, 29.99754837257193, 29.997683751282157, 29.997817079660567, 29.997948330598202, 29.998077478901365, 29.998204501258098, 29.998329376204396, 29.99845208409015, 29.99857260704493, 29.998690928943542, 29.998807035371417, 29.998920913589917, 29.99903255250145, 29.99914194261457, 29.99924907600898, 29.999353946300456, 29.999456548605814, 29.999556879507843, 29.999654937020242, 29.999750720552623, 29.999844230875567, 29.999935470085763, 30.000024441571224, 30.000111149976647, 30.00019560116888, 30.000277802202568, 30.00035776128594, 30.00043548774678, 30.000510991998624, 30.00058428550713, 30.00065538075671, 30.0007242912174, 30.000791031311934, 30.000855616383173, 30.000918062661746, 30.00097838723401, 30.001036608010303, 30.00109274369353, 30.00114681374805, 30.001198838368936, 30.001248838451534, 30.001296835561412, 30.00134285190466, 30.00138691029855, 30.00142903414261, 30.001469247390038, 30.001507574519568, 30.001544040507667, 30.001578670801212, 30.001611491290525, 30.001642528282847, 30.00167180847625, 30.00169935893395, 30.001725207059074, 30.001749380569848, 30.001771907475245, 30.001792816051047, 30.001812134816404, 30.00182989251077, 30.00184611807135, 30.00186084061099, 30.0018740893965, 30.001885893827446, 30.00189628341539, 30.001905287763627, 30.001912936547313, 30.001919259494123, 30.00192428636531, 30.001928046937252, 30.00193057098345, 30.001931886447924, 30.001932027291755, 30.001931019957844, 30.001928895070186, 30.001925681802277, 30.00192140966416, 30.001916107909153, 30.001909805705075, 30.001902532060747, 30.001894315831557, 30.001885185700257, 30.001875170166308, 30.00186429753298, 30.001852595895784, 30.00184009313103, 30.001826816884876, 30.001812794562774, 30.001798053319366, 30.001782620048694, 30.001766521374925, 30.00174978364336, 30.001732432911936, 30.001714494943016, 30.001695995195647, 30.001676958818134, 30.001657410641013, 30.001637375170382, 30.00161687658159, 30.001595938713297, 30.00157458506185, 30.001552838776032, 30.001530722652166, 30.001508259129476, 30.00148547028587, 30.001462377833988, 30.00143900311757, 30.001415367108155, 30.00139149040205, 30.001367393217645, 30.001343095392972, 30.001318616383593, 30.001293975260715, 30.00126919070965, 30.001244281028463, 30.00121926412696, 30.001194157525873, 30.001168978356326, 30.00114374335953, 30.001118468886737, 30.001093170899406, 30.001067864969606, 30.001042566280613, 30.001017289627782, 30.000992049419562, 30.000966859678744, 30.000941734043927, 30.000916685771106, 30.000891727735542, 30.000866872433715, 30.00084213198553, 30.00081751813663, 30.000793042260916, 30.0007687153632, 30.000744548082007, 30.000720550692552, 30.000696733109816, 30.00067310489178, 30.000649675242798, 30.000626453017073, 30.000603446722263, 30.000580664523206, 30.000558114245734, 30.00053580338063, 30.000513739087623, 30.000491928199555, 30.00047037722656, 30.000449092360377, 30.00042807947873, 30.000407344149792, 30.000386891636683, 30.00036672690209, 30.000346854612904, 30.000327279144926, 30.000308004587662, 30.00028903474909, 30.000270373160557, 30.000252023081657, 30.000233987505172, 30.000216269162056, 30.000198870526404, 30.000181793820516, 30.000165041019905, 30.0001486138584, 30.00013251383319, 30.000116742209944, 30.000101300027904, 30.000086188104984, 30.00007140704289, 30.000056957232225, 30.000042838857574, 30.00002905190263, 30.000015596155258, 30.000002471212582, 29.99998967648603, 29.9999772112064, 29.999965074428832, 29.99995326503787, 29.999941781752376, 29.999930623130517, 29.99991978757465, 29.999909273336225, 29.999899078520627, 29.999889201091992, 29.999879638877957, 29.999870389574447, 29.99986145075031, 29.99985281985202, 29.99984449420824, 29.9998364710344, 29.999828747437224, 29.99982132041914, 29.999814186882748, 29.99980734363514, 29.999800787392218, 29.999794514782938, 29.999788522353505, 29.999782806571517, 29.999777363830027, 29.999772190451573, 29.99976728269214, 29.999762636745054, 29.99975824874482, 29.999754114770894, 29.999750230851408, 29.999746592966805, 29.99974319705343, 29.999740039007047, 29.999737114686297, 29.9997344199161, 29.99973195049096, 29.99972970217824, 29.999727670721335, 29.999725851842815, 29.999724241247485, 29.999722836556913, 29.99972162891628, 29.999720618820255, 29.999719797569227, 29.9997191645184, 29.999718712997698, 29.999718439426474, 29.999718339238612, 29.999718408286594, 29.99971864201299, 29.999719036837487, 29.99971958714601, 29.999720290617073, 29.999721140417606, 29.999722134134288, 29.999723268532392, 29.999724537700605, 29.999725938022266, 29.999727465180314, 29.999729115120896, 29.99973088374634, 29.99973276701587, 29.999734760915363, 29.99973686146908, 29.999739064737817, 29.999741366821358, 29.999743763859456, 29.999746252033248, 29.99974882756637, 29.99975148672621, 29.999754225824958, 29.999757041220658, 29.99975992931822, 29.999762886570387, 29.99976590947857, 29.999768994593737, 29.99977213851719, 29.999775337901287, 29.99977858945017, 29.99978188992037, 29.99978523612143, 29.999788624916434, 29.99979205322253, 29.99979551801139, 29.9997990163096, 29.999802545199056, 29.999806101817278, 29.999809683357725, 29.999813287070022, 29.999816910260154, 29.999820550290682, 29.999824204580822, 29.9998278706066, 29.999831545900854, 29.999835228053293, 29.99983891471047, 29.999842603575754, 29.99984629240924, 29.999849979027655, 29.999853661304215, 29.99985733716844, 29.999861004605993, 29.9998646616584, 29.99986830642287, 29.999871937051935, 29.99987555175321, 29.999879148789024, 29.999882726476095, 29.999886283185113, 29.99988981734039, 29.99989332741939, 29.999896811952315, 29.99990026952165, 29.999903698761642, 29.999907098357856, 29.999910467046597, 29.999913803614426, 29.999917106897577, 29.999920375781407, 29.99992360919981, 29.999926806134614, 29.999929965614978, 29.999933086716776, 29.99993616856196, 29.999939210317915, 29.999942211196796, 29.999945170454883, 29.999948087391875, 29.999950961350244, 29.999953791714525, 29.99995657791059, 29.999959319405015, 29.99996201570429, 29.999964666354145, 29.999967270938814, 29.999969829080325, 29.999972340437743, 29.999974804706465, 29.99997722161744, 29.999979590936466, 29.999981912463447, 29.99998418603164, 29.999986411506892, 29.999988588786938, 29.999990717800614, 29.99999279850715, 29.99999483089539, 29.999996814983078, 29.999998750816097, 30.00000063846776, 30.000002478038034, 30.000004269652834, 30.0000060134633, 30.000007709645025, 30.000009358397403, 30.00001095994283, 30.000012514526073, 30.000014022413485, 30.00001548389235, 30.000016899270165, 30.00001826887396, 30.00001959304959, 30.000020872161077, 30.000022106589913, 30.00002329510005, 30.00002444194152, 30.000025544636483, 30.000026604563008, 30.000027621880577, 30.000028597157936, 30.000029530849798, 30.000030423463972, 30.000031274336877, 30.000032085620617, 30.000032857321454, 30.00003359014675, 30.000034285546704, 30.000034942758248, 30.000035562773647, 30.000036145231235, 30.00003669188542, 30.000037202947908, 30.000037679133143, 30.00003812160969, 30.000038529568975, 30.00003890469672, 30.000039247732623, 30.000039558299264, 30.000039838203676, 30.0000400872523, 30.00004030603424, 30.000040495539803, 30.000040656282003]
    return render(request,"main/cruise.html",{
        "speed_samples": v,
    })
def adaptive(request):
    return render(request,"main/adaptive.html")