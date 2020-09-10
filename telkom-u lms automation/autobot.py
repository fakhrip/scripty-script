"""
Autobot v0.01 alpha

COPYRIGHT -> (c) 2020 by Muhammad Fakhri Putra Supriyadi.
LICENSE   -> MIT, see LICENSE for more details.
"""

from subprocess import check_output
from subprocess import call 
from bs4 import BeautifulSoup
import stdiomask
import requests
import json
import os

def hello() :
    clear()

    TEMPLATE = """
    \r===================================================================
    \r                     ___                ___                ___      
    \r                    (   )              (   )              (   )     
    \r  .---.   ___  ___   | |_       .--.    | |.-.     .--.    | |_     
    \r / .-, \ (   )(   ) (   __)    /0010\   | /   \   /    \  (   __)   
    \r(__) ; |  | |  | |   | |      |10.-.1;  |  .-. | |  .-. ;  | |      
    \r  .'`  |  | |  | |   | | ___  |0|  |1|  | |  | | | |  | |  | | ___  
    \r / .'| |  | |  | |   | |(   ) |0|  |0|  | |  | | | |  | |  | |(   ) 
    \r| /  | |  | |  | |   | | | |  |1|  |1|  | |  | | | |  | |  | | | |  
    \r; |  ; |  | |  ; '   | ' | |  |1'  |0|  | '  | | | '  | |  | ' | |  
    \r' `-'  |  ' `-'  /   ' `-' ;  ' 1`-'0/  ' `-' ;  '  `-' /  ' `-' ;  
    \r`.__.'_.   '.__.'     `.__.    `.01.'    `.__.    `.__.'    `.__.   
    \r
    \r===================================================================
    \r|   Welcome to AUTOBOT, a slightly better version of TEL-U LMS    |
    \r|               created with inner peace by f4r4w4y               |
    \r===================================================================
    """
    print(TEMPLATE, end='')

def menu() :
    TEMPLATE = """
    \r===================================================================
    \r| [1] All my courses                                              |
    \r| [2] Access course                                               |
    \r| [3] All my messages                                             |
    \r| [4] All events in this month                                    |
    \r| [5] Logout from current account                                 |
    \r| [6] Exit the app                                                |
    \r===================================================================
    """
    print(TEMPLATE, end='')

    inp = int(input('\r[+] Choose menu (1-6) = '))
    return inp

def clear():  
    _ = call('clear' if os.name =='posix' else 'cls') 

def pause() :
    input("[#] Press Enter to continue...")

def welcome(fullname, sessionCookie) :
    clear()
    
    TEMPLATE = """
    \r===================================================================
    \r Welcome, {}
    \r Current session = {}
    \r===================================================================
    """
    print(TEMPLATE.format(fullname, sessionCookie), end='')

def show(what) :
    if what == 'hello' :
        hello()
    elif what == 'menu' :
        ret_code = menu()
        return ret_code

class User :
    """
    User class for saving and generating user profiles
    and all the meta.

    Parameters
    ----------
    username : str
        Username of the user
    password : str
        Password of the user
    """
    __username = ''
    __password = ''
    __cookie = ''

    def __init__(self, username, password) :
        self.__username = username
        self.__password = password

    def getSessionCookie(self) :
        """Get session cookie based on username and password."""
        return self.__cookie

    def generateSessionCookie(self) :
        """Generate session cookie based on username and password."""
        print('[+] Logging in... (Please wait, this will take a while).')
        result = check_output([
            'node', 
            'sleepynightnight.js', 
            self.__username, 
            self.__password,
        ])

        if b'Cookie:' in result :
            result = result.split(b'Cookie: ')[1]

            try:
                resJson = json.loads(result)
                cookie = resJson['value']
                self.__cookie = cookie
                return cookie
            except ValueError:
                print('[!] Failed to decode the resulted json.')

        print('[!] Login failed, there are three possible reasons for this :')
        print('    - username and password not found,')
        print('    - you are not connected to the internet,')
        print('    - https://lms.telkomuniversity.ac.id is currently down.')

        return None

    def addCourse(self, course) :
        """
        Add course to current all courses array.

        Parameters
        ----------
        course : dict
            Course to be added

        Returns
        -------
        Boolean
            True if succeed, otherwise False
        """
        if self.__courses :
            self.__courses.append(course)
            return True
        else : 
            return False

    def printAllCourses(self) :
        """Fancy print all the courses."""
        TEMPLATE = """
        \r - Course fullname = {}
        \r   Course shortname = {}
        \r   Category = {}
        """

        print('===================================================================', end='')
        if len(self.__courses) <= 0 :
            print('[+] Sadly, you\'re not currently enrolled to any course :(')
        else :
            for data in self.__courses :
                print(TEMPLATE.format(data['fullname'], data['shortname'], data['coursecategory']))
        print('===================================================================')

    def setAllCourses(self, courses) :
        self.__courses = courses

    def getAllCourses(self) :
        return self.__courses

class Web :
    """
    Web class for saving session and all the state.

    Parameters
    ----------
    cookie : str
        Cookie of corresponding credential
    """    
    BASE_DOMAIN = 'https://lms.telkomuniversity.ac.id{}'

    GET_URL = {
        'home': '/my',
        'logout': '/login/logout.php?sesskey={apikey}',
    }

    POST_URL = {
        'events': '/lib/ajax/service.php?sesskey={apikey}&info=core_calendar_get_action_events_by_timesort',
        'courses': '/lib/ajax/service.php?sesskey={apikey}&info=core_course_get_enrolled_courses_by_timeline_classification'
    }

    POST_DATA = {
        'events': '[{\
            "index": 0,\
            "methodname": "core_calendar_get_action_events_by_timesort",\
            "args": {\
                "limitnum": 20,\
                "timesortfrom": {from},\
                "timesortto": {to},\
                "limittononsuspendedevents": true\
            }\
        }]',
        'courses': '[{\
            "index": 0,\
            "methodname": "core_course_get_enrolled_courses_by_timeline_classification",\
            "args": {\
                "offset": 0,\
                "limit": 0,\
                "classification": "all",\
                "sort": "fullname",\
                "customfieldname": "",\
                "customfieldvalue": ""\
            }\
        }]'
    }

    __session = ''
    __apikey = ''

    def __init__(self, cookie) :
        self.__session = requests.Session()
        cookie_obj = requests.cookies.create_cookie(
            domain = 'lms.telkomuniversity.ac.id',
            name   = 'MoodleSession',
            value  = cookie
        )
        self.__session.cookies.set_cookie(cookie_obj)
        
        print('[+] Parsing api key...')
        self.parseApiKey()

    def parseApiKey(self) :
        """Parse api key (or in this case session key) from homepage html."""
        res = self.__session.get(self.BASE_DOMAIN.format(self.GET_URL['home']))
        soup = BeautifulSoup(res.text, 'html.parser')
        hidden_inp = soup.find_all(attrs={"name": "sesskey"})
        if len(hidden_inp) > 0 :
            try:
                chosen_inp = hidden_inp[0]
                self.__apikey = chosen_inp.attrs['value']
            except :
                print('[!] Error parsing API key')
        
    def parseCourses(self, user) :
        """
        Parse all user courses.

        Parameters
        ----------
        user: User
            current user class object
        """
        course_url = self.POST_URL['courses'].format(apikey = self.__apikey)
        course_data = self.POST_DATA['courses']
        res = self.__session.post(self.BASE_DOMAIN.format(course_url), data = course_data)
        
        try:
            resJson = json.loads(res.text)

            result = resJson[0]
            isError = result['error']

            if not isError :
                # Filter out only important data
                data = result['data']
                courses = data['courses']
                courses = [{
                    'fullname': x['fullname'].replace('\n', ' '),
                    'shortname': x['shortname'],
                    'idnumber': x['idnumber'],
                    'viewurl': x['viewurl'],
                    'coursecategory': x['coursecategory']
                } for x in courses]

                user.setAllCourses(courses)
            else :
                print('[!] Error fetching courses data.')
        except ValueError:
            print('[!] Failed to decode the resulted json.')

def main() :
    show('hello')

    username = str(input('\r[+] Input your username = '))
    password = stdiomask.getpass(prompt='\r[+] Input your password = ', mask='●')

    currentUser = User(username, password)
    sessionCookie = currentUser.generateSessionCookie()

    if sessionCookie :
        process = Web(sessionCookie)
        
        while True :
            welcome(username, sessionCookie)

            inp = show('menu')
            if inp == 1 :
                # Parse all courses
                process.parseCourses(currentUser)
                
                if currentUser.getAllCourses() != None :
                    currentUser.printAllCourses()

            elif inp == 2 :
                # Access one of the course
                print('[+] access course')

            elif inp == 3 :
                # Parse all my messages
                print('[+] parse message')

            elif inp == 4 :
                # Parse all event in this month
                print('[+] parse events')

            elif inp == 5 :
                # Logout current account
                print('[+] logout')

            elif inp == 6 :
                # Exit the app
                print('[#] Thanks for using this app :D')
                break

            else :
                # Input is out of range (1-5)
                print('[!] Wrong input...')
            
            pause()

    else :
        # Couldn't log the user in, terminate app
        print('[!] Try running the script again, if you think you\'ve solved the problem.')

if __name__ == "__main__":
    main()