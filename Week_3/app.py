import sys
import matplotlib.pyplot as plt
from jinja2 import Template

Student_data=open('data.csv','r')
n=Student_data.readline().strip('\n').split(',')
D=[]
l=[]
for j in range(len(n)):
  n[j]=n[j].strip(" ")
s=Student_data.readlines()
for line in s:
  l.append(line.strip('\n').split(","))
for elem in l:
  d={}
  for k in range(len(elem)):
    for i in range(len(n)):
      if i==k and i!=2:
        d[n[i]]=elem[k].strip(" ")
        break
      elif i==k and i==2:
        d[n[i]]=int(elem[k].strip(" "))
        break
  D.append(d)
Student_data.close()


TEMPLATE ="""
<!DOCTYPE html>
<html >
<head>
    <meta charset="UTF-8">
    <title>Student Data</title>
</head>
<body>
    <div>
        <h1>Student Details </h1>
        <table border="1"  >
        <thead>
          <tr >
              <th >Student id</th>
              <th >Course id</th>
              <th>Marks</th>   
          </tr>
        </thead>
        <tbody>
        <ul>
          <tr>
          {% for data in D %}
            {% if data["Student id"]== p %}
            <tr>
              <td>{{ data["Student id"] }}</td>
              <td>{{ data["Course id"] }}</td>
              <td>{{ data["Marks"] }}</td> 
            
            </tr>
            {% endif %}
          {% endfor %}
          </tr>
        </ul>
        </tbody>
        <tfoot >
          <tr>
          {% set points = [0] -%}
          {% for single_item in D -%}
          {% if single_item["Student id"]==p and points.append(points.pop()+ single_item["Marks"]) -%}{% endif %}
          {% endfor %}
              <td colspan="2" style="text-align:center">Total Marks</td>
              <td>{{ points[0] }}</td>
          </tr>
        </tfoot>
        </table>
    </div>
</body>
</html>
"""

TEMPLATE1 ="""
<!DOCTYPE html>
<html >
<head>
    <meta charset="UTF-8">
    <title>Course Data</title>
</head>
<body>
    <div>
        <h1>Course Details </h1>
        <table border="1"  >
        <thead>
          <tr >
              <th >Average Marks</th>
              <th >Maximum Marks</th>   
          </tr>
        </thead>
        <tbody>
        <ul>
          <tr>
            {% set points = [0] -%}
            {% for single_item in D -%}
            {% if single_item["Course id"]==p and points.append(points.pop()+ single_item["Marks"]) -%}{% endif %}
            {% endfor %}
            {% set point2 = [] -%}
            {% for single_item in D -%}
            {% if single_item["Course id"]==p and point2.append(single_item["Marks"]) -%}
            {% endif %}
            {% endfor %}
              <td>{{ points[0]/ point2|length}}</td>
              <td>{{point2|max}}</td>
          </tr>
        </ul>
        </tbody>
        </table>
    </div>
    <div>
        <img src={{c}}>
    </div>

</body>
</html>
"""

TEMPLATE2="""
<!DOCTYPE html>
<html >
<head>
    <meta charset="UTF-8">
    <title>Something Went Wrong</title>
</head>
<body>
<div>
  <h1>Wrong Inputs</h1>
</div>
<div>
  <p>Something went wrong</p>
</div>

</body>
</html>

"""

def main():
  flag=False
  if sys.argv[1]=='-s':
      for i in D:
        if i["Student id"]==sys.argv[2]: 
            f=sys.argv[2]
            template=Template(TEMPLATE)
            content = template.render(D=D,p=f)
            my_file=open('output.html','w')
            my_file.write(content)
            my_file.close()
            flag=True
      if flag==False:
        template=Template(TEMPLATE2)
        content = template.render(D=D)
        my_file=open('output.html','w')
        my_file.write(content)
        my_file.close()
  elif sys.argv[1]=='-c':
    s=[]
    for i in D:
        if i["Course id"]==sys.argv[2]:
          if i["Course id"]==sys.argv[2]:
            s.append(i["Marks"])
          plt.hist(s,color='#2077AE')
          plt.xlabel("Marks")
          plt.ylabel("Frequency")
          plt.savefig("my_plot.png")
          f=sys.argv[2]
          template=Template(TEMPLATE1)
          content = template.render(D=D,p=f,c="my_plot.png")
          my_file=open('output.html','w')
          my_file.write(content)
          my_file.close()
          flag=True
    if flag==False:
      template=Template(TEMPLATE2)
      content = template.render(D=D)
      my_file=open('output.html','w')
      my_file.write(content)
      my_file.close()
  else:
    template=Template(TEMPLATE2)
    content = template.render(D=D)
    my_file=open('output.html','w')
    my_file.write(content)
    my_file.close()


if __name__=="__main__":
    main()

