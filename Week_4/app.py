from flask import Flask
from flask import render_template
from flask import request
import matplotlib.pyplot as plt


Student_data=open('data.csv','r')
n=Student_data.readline().strip('\n').split(',')
D=[]
l=[]
for j in range(len(n)):
  n[j]=n[j].strip(" ")
s=Student_data.readlines()
for line in s:
  l.append(line.strip('\n').split(","))
sd=[]
cd=[]
for elem in l:
  d={}
  for k in range(len(elem)):
    for i in range(len(n)):
      if i==0 and k==0 and elem[k].strip(" ") not in sd:
        sd.append(elem[k].strip(" "))
      if i==1 and k==1 and elem[k].strip(" ") not in cd:
        cd.append(elem[k].strip(" ")) 
      if i==k and i!=2:
        d[n[i]]=elem[k].strip(" ")
        break
      elif i==k and i==2:
        d[n[i]]=int(elem[k].strip(" "))
        break
  D.append(d)
Student_data.close()


app=Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    if request.method=="GET":
        return render_template("index.html")
    elif request.method=="POST":
      c=request.form.get("ID")
      value=request.form["id_value"]
      
      if (c is None) or value=='':
        return render_template("error.html")

      if c=="student_id" and value in sd:
        return render_template("student.html",D=D,p=value)
      
      elif c=="course_id" and value in cd:
        s=[]
        for i in D:
          if i["Course id"]==value:
            s.append(i["Marks"])
          plt.hist(s)
          plt.xlabel("Marks")
          plt.ylabel("Frequency")
          plt.savefig(f"static/pc.png")
          plt.clf()
        return render_template("course.html",D=D,p=value)
      
      else:
        return render_template("error.html")



if __name__=="__main__":
    app.run(debug=True)
