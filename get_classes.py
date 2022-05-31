from bs4 import BeautifulSoup
import requests as re

base = "https://courses.illinois.edu"
class_page = re.get(f'{base}/schedule/DEFAULT/DEFAULT')

soup = BeautifulSoup(class_page.content, 'html.parser')

table = soup.find('table', {'id':'term-dt'}).find_all('tr')
classes = []
courses = {}
temp = []
for row in table[1:]:
    temp = []
    children = row.findChildren('td')
    classes.append(children)
    courses_c = re.get(f"{base}{children[1].a['href']}").content
    s  = BeautifulSoup(courses_c, 'html.parser')
    course_table = s.find('table', {'id':'default-dt'}).find_all('tr')
    
    for course in course_table[1:]:
        course_children = course.findChildren('td')
        temp.append([c.text.strip() for c in course_children])
    courses[f'{children[0].text.strip()}'] = temp
    print(f'{children[0].text.strip()}- {children[1].text.strip()}')

with open('classes.py', 'w',"utf-8") as f:
    f.write('classes = [\n')
    for _class in classes:
        f.write(f'("{_class[0].text.strip()}", "{_class[1].text.strip()}"),\n')
    f.write("]\n\n")

    f.write("courses = {\n")
    for (key, value) in courses.items():
        f.write(f'"{key}": [')
        for v in value:
            f.write(f'"{v[0]}:- {v[1]}", ')
        f.write(f"],\n")
    f.write('}\n')
