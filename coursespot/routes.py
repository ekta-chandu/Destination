from flask import render_template, redirect, url_for, flash, request
from coursespot import app, db, bcrypt,mail
from coursespot.forms import RegistrationForm, LoginForm, ContactForm, UpdateForm, RequestResetForm, ResetPasswordForm
from coursespot.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

from bs4 import BeautifulSoup
import requests

#primary site
url = "http://www.openculture.com/"
course_dict = [{},{},{},{}]  #list of 6 dictionaries
sub_url=["computer_science_free_courses","free-online-data-science-courses",
         "math_free_courses","engineering_free_courses"]
csv_files=["computerscience","datascience","math","engineering"]
#extraction of data
for i in range(len(sub_url)):
    course_no = 0
    url_new = url + sub_url[i]
    response = requests.get(url_new)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    contents = soup.find_all("ul")
    for content in contents:
        names = content.find_all("strong")
        for name in names:
            if len(name.text)>=6:
                course_link = []
                course_name = name.text
                courses = name.find_next_siblings("a")
                course_provider = name.find_parent("li").text[len(course_name)+1:]
                count =0
                for course in courses:
                    if count<=3 :
                        course_link.append(course.get('href'))
                        count +=1

                #print(course_no,course_name,course_provider,course_link)
                (course_dict[i])[course_no] = [course_name,course_provider,course_link]
                course_no += 1

            else:
                continue



comp_img=["https://www.openaccessgovernment.org/wp-content/uploads/2020/08/dreamstime_l_124110584.jpg",
"https://images.pexels.com/photos/163125/board-printed-circuit-board-computer-electronics-163125.jpeg", 
"https://images.pexels.com/photos/276452/pexels-photo-276452.jpeg",
"https://images.pexels.com/photos/943096/pexels-photo-943096.jpeg",
"https://images.pexels.com/photos/6963944/pexels-photo-6963944.jpeg",
"https://images.pexels.com/photos/4164418/pexels-photo-4164418.jpeg",
"https://images.pexels.com/photos/3861969/pexels-photo-3861969.jpeg",
"https://images.pexels.com/photos/50711/board-electronics-computer-data-processing-50711.jpeg",
"https://images.pexels.com/photos/1194713/pexels-photo-1194713.jpeg",
"https://images.pexels.com/photos/247676/pexels-photo-247676.jpeg",
"https://images.pexels.com/photos/919734/pexels-photo-919734.jpeg",
"https://images.pexels.com/photos/2777898/pexels-photo-2777898.jpeg",
"https://images.pexels.com/photos/417458/pexels-photo-417458.jpeg",
"https://images.pexels.com/photos/745708/pexels-photo-745708.jpeg",
"https://images.pexels.com/photos/1591060/pexels-photo-1591060.jpeg",
"https://images.pexels.com/photos/373543/pexels-photo-373543.jpeg",
"https://cdn.pixabay.com/photo/2018/05/08/08/44/artificial-intelligence-3382507__340.jpg",
"https://cdn.pixabay.com/photo/2016/04/04/14/12/monitor-1307227__480.jpg",
"https://cdn.pixabay.com/photo/2017/12/26/21/19/tech-3041437__340.jpg"]

data_img=["https://cdn.pixabay.com/photo/2019/08/06/22/48/artificial-intelligence-4389372__340.jpg",
"https://cdn.pixabay.com/photo/2018/03/15/16/11/background-3228704__340.jpg",
"https://cdn.pixabay.com/photo/2017/02/20/14/18/technology-2082642__340.jpg",
"https://cdn.pixabay.com/photo/2021/05/30/21/47/dots-6297146__340.jpg",
"https://cdn.pixabay.com/photo/2018/01/26/18/21/matrix-3109378__340.jpg",
"https://cdn.pixabay.com/photo/2021/11/04/06/27/artificial-intelligence-6767502__340.jpg",
"https://cdn.pixabay.com/photo/2018/12/02/10/07/web-3850917__340.jpg",
"https://cdn.pixabay.com/photo/2016/07/23/10/51/binary-1536651__340.jpg",
"https://cdn.pixabay.com/photo/2017/09/08/08/57/binary-2728117__340.jpg",
"https://cdn.pixabay.com/photo/2016/09/26/09/10/binary-1695478__340.jpg",
"https://cdn.pixabay.com/photo/2017/11/02/10/23/security-2910624__340.jpg",
"https://cdn.pixabay.com/photo/2021/08/02/21/10/chip-6517875__340.jpg",
"https://cdn.pixabay.com/photo/2020/04/30/17/52/network-5113928__340.jpg",
"https://cdn.pixabay.com/photo/2016/06/01/19/56/board-1429589__340.jpg",
"https://cdn.pixabay.com/photo/2018/10/12/12/32/security-3742114__340.jpg",
"https://cdn.pixabay.com/photo/2017/06/28/10/06/binary-2450152__340.jpg",
"https://cdn.pixabay.com/photo/2020/01/29/23/47/matrix-4804001__340.jpg",
"https://cdn.pixabay.com/photo/2020/04/22/09/38/circuits-5076888__340.png",
"https://cdn.pixabay.com/photo/2017/09/22/22/08/computer-2777254__340.jpg"]

math_img=["https://www.championtutor.com/blog/wp-content/uploads/2017/11/When-to-Get-a-Maths-Tutor-for-Your-Child.jpg",
          "https://news.schoolsdo.org/wp-content/uploads/2016/02/algebra_geometry_chalk.jpg",
          "https://i.ytimg.com/vi/uMO95_YlEKM/maxresdefault.jpg",
          "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/math-1569525694.jpg?crop=1.00xw:1.00xh;0,0&resize=1200:*",
          "https://s-i.huffpost.com/gen/1003503/images/o-BAD-AT-MATH-facebook.jpg",
          "http://www.girlsbuildstem.com/wp-content/uploads/2016/04/18336230-mathematics-doodle-Stock-Vector-mathematics-math-formula.jpg",
          "https://www.yu.edu/sites/default/files/math-515606506.jpg",
          "https://thumbs.dreamstime.com/z/mathematical-background-abstract-dark-light-green-figures-graphs-44727240.jpg",
          "https://endeavors.unc.edu/wp-content/uploads/Foundations_physics_with-logo.jpg",
          "https://thumbs.dreamstime.com/z/abstract-mathematics-4060499.jpg",
          "https://2.bp.blogspot.com/-hLUlKobMiSc/WY0RkNi7srI/AAAAAAAAEco/L8kGgVSjwpo5lFKBCVRgbExScfPIHAARwCLcBGAs/s1600/Abstract+Algebra+Review.png",
          "https://c8.alamy.com/comp/RYGW67/digital-mathematical-symbols-3d-illustration-abstract-futuristic-background-with-math-and-physics-symbols-and-mesh-network-grid-4k-science-concept-RYGW67.jpg",
          "http://academics.smcvt.edu/jellis-monaghan/AbstractAlg/dihedralpale.gif",
          "https://st2.depositphotos.com/2060305/7239/v/950/depositphotos_72399269-stock-illustration-mathematical-symbols-seamless-pattern-with.jpg",
          "https://science.ubc.ca/sites/science.ubc.ca/files/Mathematics.jpg",
          "https://d2v9y0dukr6mq2.cloudfront.net/video/thumbnail/EbyCIUQPl/videoblocks-abstract-clean-green-waving-3d-grid-or-mesh-as-dream-background-green-geometric-vibrating-environment-or-pulsating-math-background_hrxp_omzw_thumbnail-full01.png",
          "http://cdn.sci-news.com/images/enlarge6/image_7570e-Complex-Math.jpg",
          "http://images4.wikia.nocookie.net/__cb20120501125545/powerlisting/images/5/51/Mathematical_equations.jpg"
          "https://wallpaperaccess.com/full/931342.jpg"]

eng_img=["https://cdn.mos.cms.futurecdn.net/P5BDqJBgzU9FYn9yTAcM2f.jpg",
        "https://www.bolton.ac.uk/assets/Uploads/shutterstock-1213477993-2.jpg",
        "https://cdn.mos.cms.futurecdn.net/steVjWGx3vYPjMpJL2jVcV.jpg",
        "https://digitaldefynd.com/wp-content/uploads/2021/02/Best-Quality-Engineering-course-tutorial-class-certification-training-online-scaled.jpg",
        "https://www.currentschoolnews.com/wp-content/uploads/2020/03/Engineeering.png",
        "https://www.mdx.ac.uk/__data/assets/image/0021/447213/Design-Engineering.jpg",
        "https://nvshq.org/wp-content/uploads/2021/02/Aeronautical_Engineering_courses_career_jobs_salary.png",
        "https://prod-discovery.edx-cdn.org/media/programs/card_images/90f4789c-2549-4670-ade7-12cc8b590f5c-e56e4adebd27.jpg",
        "https://feutech.edu.ph/assets/features/40/Aw27R.jpg",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQZDROmY7uWh3s0-U3AKJbeNbBDkXBpoZc--Q&usqp=CAU",
        "https://i0.wp.com/www.dainikreporters.com/wp-content/uploads/2021/11/aerospace-engineers.jpeg",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSc-i0ea-DfU2cc-NrgC-c3J8DTYYlXcWdP_g&usqp=CAU",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSh_kVZAwkhuw22godoQBiQfcH5tXbqJEaalg&usqp=CAU",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRcsQi6e_0UdU9UzWggFi_V51N2YgpAjka0IA&usqp=CAU",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT0fB_xgyadaugF7TG4k-LpelFle2Fk2cqdgw&usqp=CAU",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQALfIkY1J0c674AA7B94LQJC653KB0fDLPgw&usqp=CAU",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQXmEQIKeHov25iRtUm3tjz-d2636FkcKgFig&usqp=CAU",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQIXIVZC0U24WEWwcLFCRQ15SnXH3oycdrqgA&usqp=CAU",
        "https://digitaldefynd.com/wp-content/uploads/2020/04/Best-Electrical-Engineering-course-tutorial-class-certification-training-online-scaled.jpg"]

@app.route("/")
def welcome():
    return render_template("welcome.html", title="Welcome")


@app.route("/home")
@login_required
def home():
    return render_template('home.html', home='active', title="Home")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username = form.username.data,
            email = form.email.data,
            password = hashed_pw
        )
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully. You can now login", "success")
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form, signup="active")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login unsuccessful. Please check your email and password", "danger")
    return render_template('login.html', title="Login", form=form, login="active")  


@app.route("/about")
def about():
    return render_template("about.html", title="About", about="active")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('welcome'))


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form=UpdateForm()
    if form.validate_on_submit():
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash("Information updated successfully", "success")
        return redirect(url_for('account'))
    elif request.method=="GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("account.html", title="Account", form=form, account="active")


@app.route("/contact", methods=["GET", "POST"])
@login_required
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = Message('Contact',
                  sender='destinationcoc22@gmail.com',
                  recipients=[user.email])
        msg.body = f'''
        Feedback received from {form.email.data}
        Message :
        {form.message.data}
'''
        mail.send(msg)
        flash("Message sent successfully!", "success")
    elif request.method=="GET":
        form.email.data = current_user.email
    return render_template("contact.html", form=form, title="Contact", contact="active")


# Routes for courses

@app.route("/computerscience")
@login_required
def compscience():
    return render_template('computerscience.html',course_dict_0=course_dict[0],j=0,x=len(course_dict[0]),comp_img=comp_img, title="Computer Science")


@app.route("/computerscience2")
@login_required
def compscience2():
    return render_template('computerscience2.html',course_dict_0=course_dict[0],j=0,x=len(course_dict[0]),comp_img=comp_img, title="Computer Science")


@app.route("/computerscience3")
@login_required
def compscience3():
    return render_template('computerscience3.html',course_dict_0=course_dict[0],j=0,x=len(course_dict[0]),comp_img=comp_img, title="Computer Science")


@app.route("/computerscience4")
@login_required
def compscience4():
    return render_template('computerscience4.html',course_dict_0=course_dict[0],j=0,x=len(course_dict[0]),comp_img=comp_img, title="Computer Science")


@app.route("/datascience")
@login_required
def datascience():
    return render_template("datascience.html",course_dict_1=course_dict[1],x=len(course_dict[1]),data_img=data_img, title="Data Science")

@app.route("/maths")
@login_required
def maths():
    return render_template("math.html",course_dict_2=course_dict[2],x=len(course_dict[2]),math_img=math_img, title="Maths")

@app.route("/engineering")
@login_required
def engineering():
    return render_template("engineering.html",course_dict_3=course_dict[3],x=len(course_dict[3]),eng_img=eng_img, title="Engineering")

# Meet the team
@app.route("/team")
def team():
    return render_template("team.html", title="Team")


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='destinationcoc22@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)



@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)



@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
