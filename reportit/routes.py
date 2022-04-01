import os
from functools import wraps
import json
import secrets
from PIL import Image
from flask import abort, jsonify, render_template, request, url_for, flash, redirect
from flask_login import login_required, login_user, current_user, logout_user
from matplotlib.pyplot import title
from reportit import app, session, bcrypt,mail
import geopandas
import leafmap.kepler as leafmap
from reportit.models import User, Categories, Utility, Pollution, Disaster, Road, Fire
from reportit.newForm import RegistrationForm, LoginForm, ReportFo, UpdateAccountForm,ResetPasswordForm, RequestResetForm
from werkzeug.datastructures import ImmutableMultiDict
import concurrent.futures
from flask_mail import Message

all_classes = ["Utility", "Pollution", "Road", "Disaster", "Fire"]

Utility_List = ["Water", "Gas", "Sewage", "Electric", "Telecom"]
Poullution_List = ["Pollution", "Noise Pollution", "Air Pollution",
                   "Industrial Pollution", "Soil Pollution", "Water Pollution"]
Road_List = ["Road", "Accidents", "Lamps", "Hales", "Barriers"]
Disasters_List = ["Disasters", "Earthquakes",
                  "Floods", "Landslides", "Torrnados"]

new_list = [Utility_List, Poullution_List, Road_List, Disasters_List]


def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('You do not have access to that page. Sorry!', 'danger')
                return redirect(url_for('login'))
            elif not current_user.access:
                return redirect(url_for('login'))
            elif not current_user.allowed(access_level):
                flash('You do not have access to that page. Sorry!', 'danger')
                return redirect(url_for('home'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@app.route('/')
def home():
    return render_template('home.html', title='Home')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(form.fname.data, form.lname.data, form.email.data,
                    form.nationalid.data, form.phonenumber.data, hashed_password)
        session.add(user)
        session.commit()
        flash(f'Account created for {form.fname.data}!', 'success')
        return redirect(url_for('myreports', curr_cat=1))
    return render_template('register.html', title='Register', form=form)
    # 29912345678912
    # 01212345678911
    # 4EpGrxWT4uErY8i


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(User).filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/myaccount', methods=['GET', 'POST'])
@login_required
def myaccount():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.f_Name = form.fname.data
        current_user.l_Name = form.lname.data
        current_user.email = form.email.data
        current_user.national_id = form.nationalid.data
        current_user.phone_num = form.phonenumber.data
        session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('myaccount'))
    elif request.method == 'GET':
        form.fname.data = current_user.f_Name
        form.lname.data = current_user.l_Name
        form.email.data = current_user.email
        form.nationalid.data = current_user.national_id
        form.phonenumber.data = current_user.phone_num
    reports = session.query(User).get(current_user.id).reports
    numreports = len(reports)
    return render_template('myaccount.html', title='My Account', numreports=numreports, form=form)


@app.route('/myreports/<int:curr_cat>')
@login_required
def myreports(curr_cat):
    if curr_cat == 1:
        reports = session.query(User).get(current_user.id).reports
    elif curr_cat == 2:
        reports = session.query(User).get(current_user.id).reports_Pollution
    elif curr_cat == 3:
        reports = session.query(User).get(current_user.id).reports_Road
    elif curr_cat == 4:
        reports = session.query(User).get(current_user.id).reports_Disaster
    reportsIDs = []
    for i in reports:
        obj = {
            "id": i.id,
            "lat": i.lat,
            "lon": i.lon,
            "solved": i.solved
        }
        reportsIDs.append(obj)
    data = json.dumps(reportsIDs)
    return render_template('myreports.html', reports=reports, title='My Reports', data=data)

@app.route('/myanalysis/<int:accessuser_access>')
@login_required
# @requires_access_level(2 or 3 or 4 or 5)
def myanalysis(accessuser_access):
    if current_user.access == accessuser_access or current_user.is_admin():
        return render_template('myanalysis.html', title='My Analysis',curr_ana=accessuser_access)
    else:
        abort(404, description="Resource not found")


@app.route('/analysis1/<int:accessuser_access>')
@login_required
# @requires_access_level(2 or 3 or 4 or 5)
def analysis1(accessuser_access):
    if current_user.access == accessuser_access or current_user.is_admin():
        from reportit.analysis.sjoina import sJoinA
        from reportit.postgis import current_qry_url
        current_qry = current_qry_url(accessuser_access)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            f1 = executor.submit(sJoinA, current_qry)
            gdf = f1.result()
        # gdf = sJoinA(current_qry)
        admin_poly = geopandas.read_file(
            "Data/Facilities/Admin3Poly.gpkg", layer='All-Admin-Area-Egypt').to_crs("EPSG:3857")  # Polygon
        m = leafmap.Map()
        config = "reportit/analysis/kepler-configs/sj/config-sj-try10-label.json"
        m.add_gdf(gdf, layer_name="Final Result")
        m.add_gdf(admin_poly, layer_name="Admin Area", config=config)
        # m.to_html("reportit/templates/mymap.html")
        return m._repr_html_()
    else:
        abort(404, description="Resource not found")


@app.route('/analysis2/<int:accessuser_access>')
@login_required
# @requires_access_level(2 or 3 or 4 or 5)
def analysis2(accessuser_access):
    if current_user.access == accessuser_access or current_user.is_admin():
        from reportit.analysis.countinpoly import countPinPoly
        from reportit.postgis import current_qry_url,postGIS_GDF
        current_qry = current_qry_url(accessuser_access)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            f1 = executor.submit(countPinPoly, current_qry)
            gdf = f1.result()
        Problem_gdf = postGIS_GDF(current_qry)
        Problem_gdf['timestamp'] = Problem_gdf['timestamp'].astype(str)
        m = leafmap.Map(center=[30.0444, 31.2357], zoom=6)
        config = "reportit/analysis/kepler-configs/count/config-count-try6.json"
        m.add_gdf(Problem_gdf, layer_name="Final Result")
        m.add_gdf(gdf, layer_name="Admin Area", config=config)
        # m.add_gdf(admin_poly, layer_name="layer2")
        # m.to_html("reportit/templates/mymap.html")
        return m._repr_html_()
    else:
        abort(404, description="Resource not found")

@app.route('/analysis3/<int:accessuser_access>')
@login_required
# @requires_access_level(2 or 3 or 4 or 5)
def analysis3(accessuser_access):
    if current_user.access == accessuser_access or current_user.is_admin():
        from reportit.analysis.timeseriesA import timeSeriesA
        from reportit.postgis import current_qry_url,postGIS_GDF
        current_qry = current_qry_url(accessuser_access)
        # with concurrent.futures.ThreadPoolExecutor() as executor:
            # f1 = executor.submit(timeSeriesA, current_qry)
        m6 = timeSeriesA(current_qry)
        m6.save('reportit/templates/analysis3.html')
            # f1.result()
        # return m6._repr_html_()
        return render_template('analysis3.html')
    else:
        abort(404, description="Resource not found")

@app.route('/analysis4/<int:accessuser_access>')
@login_required
@requires_access_level(7)
def analysis4(accessuser_access):
    if current_user.access == accessuser_access or current_user.is_admin():
        from reportit.analysis.area_interpolation_h3 import area_interpolation_h3
        with concurrent.futures.ThreadPoolExecutor() as executor:
            f1 = executor.submit(area_interpolation_h3)
        gdf = f1.result()
        m = leafmap.Map()
        config = "reportit/analysis/kepler-configs/interpolationhex/config-try1.json"
        m.add_gdf(gdf,layer_name="Final Result", config=config)
        return m._repr_html_()
    else:
        abort(404, description="Resource not found")


def mkdir_p(path):
    if not os.path.exists(path):
        os.makedirs(path)


def save_img(form_img, cat_path, sub_cat):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_img.filename)
    img_fn = random_hex + file_ext
    upload_path = os.path.join(
        app.root_path, 'static/reports_imgs', cat_path, sub_cat)
    mkdir_p(upload_path)
    img_path = os.path.join(
        app.root_path, 'static/reports_imgs', cat_path, sub_cat, img_fn)
    output_size = (1024, 1024)
    i = Image.open(form_img)
    i.thumbnail(output_size)
    i.save(img_path)
    return img_fn


@app.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    from reportit.analysis.bestroutetofac import bestrouteFac
    if request.method == 'GET':
        return render_template('report.html')
    if request.method == 'POST':
        file = request.files['file']
        data = dict(request.form)
        pic_file = save_img(file, data["Problem"], data["Sub Problem"])
        try: 
            bestrouteFac(data['long'],data['lat'])
        except:
            print("no route")
        for cat in session.query(Categories).all():
            if data["Problem"] == cat.cat_name:
                cat_id_forIns = cat.id
        for classname1 in Utility_List:
            if data["Problem"] == classname1:
                session.add(Utility(cat_id_forIns, data["Sub Problem"], float(data['lat']), float(
                    data['long']), int(data['rating']), data['Description'], False, pic_file, current_user.id))
        for classname2 in Poullution_List:
            if data["Problem"] == classname2:
                session.add(Pollution(cat_id_forIns, data["Sub Problem"], float(data['lat']), float(
                    data['long']), int(data['rating']), data['Description'], False, pic_file, current_user.id))
        for classname3 in Road_List:
            if data["Problem"] == classname3:
                session.add(Road(cat_id_forIns, data["Sub Problem"], float(data['lat']), float(
                    data['long']), int(data['rating']), data['Description'], False, pic_file, current_user.id))
        for classname4 in Disasters_List:
            if data["Problem"] == classname4:
                session.add(Disaster(cat_id_forIns, data["Sub Problem"], float(data['lat']), float(
                    data['long']), int(data['rating']), data['Description'], False, pic_file, current_user.id))
        session.commit()
        return redirect(url_for('submission'))
        # return url_for('submission')
    else:
        abort(404, description="Resource not found")


@app.route('/dash')
def notdash():
    import plotly
    import plotly.express as px
    from reportit.postgis import df_utility
    df_utility['timestamp'] = df_utility['timestamp'].astype(str)

    # df = pd.DataFrame({
    #   'Fruit': ['Apples', 'Oranges', 'Bananas', 'Apples', 'Oranges',
    #   'Bananas'],
    #   'Amount': [4, 1, 2, 2, 4, 5],
    #   'City': ['SF', 'SF', 'SF', 'Montreal', 'Montreal', 'Montreal']})
    fig = px.scatter_mapbox(df_utility, lat="lat", lon="lon", color="effect", size="effect",
                            color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10,
                            mapbox_style="carto-positron")
    # fig = px.bar(df_utility, x='Fruit', y='Amount', color='City', barmode='group')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('notdash.html', graphJSON=graphJSON)


@app.route('/problemstimeline/<int:accessuser_access>')
# @requires_access_level(2 or 3 or 4 or 5)
def problemstimeline(accessuser_access):
    if current_user.access == accessuser_access or current_user.is_admin():
        from reportit.postgis import readpostpandas,current_qry_url
        current_qry = current_qry_url(accessuser_access)
        df_current = readpostpandas(current_qry)
        config = "reportit/analysis/kepler-configs/display/config-display-try3.json"
        m = leafmap.Map(center=[30.0444, 31.2357], zoom=6)
        df_current['timestamp'] = df_current['timestamp'].astype(str)
        m.add_gdf(df_current, layer_name="Problems",config=config)
        # m.to_html(outfile='./reportit/templates/leafmap.html')
        return m._repr_html_()
    else:
        abort(404, description="Resource not found")


@app.route('/submission')
def submission():
    return render_template('submission.html')


@app.route('/reportm', methods=['GET', 'POST'])
@login_required
def reportm():
    from reportit.analysis.bestroutetofac import bestrouteFac
    if request.method == 'GET':
        return render_template('reportm.html')
    if request.method == 'POST':
        file = request.files['file']
        data = dict(request.form)
        pic_file = save_img(file, data["Problem"], data["Sub Problem"])
        try: 
            bestrouteFac(data['long'],data['lat'])
        except:
            print("no route")
        for cat in session.query(Categories).all():
            if data["Problem"] == cat.cat_name:
                cat_id_forIns = cat.id
        for classname1 in Utility_List:
            if data["Problem"] == classname1:
                session.add(Utility(cat_id_forIns, data["Sub Problem"], float(data['lat']), float(
                    data['long']), int(data['rating']), data['Description'], False, pic_file, current_user.id))
        for classname2 in Poullution_List:
            if data["Problem"] == classname2:
                session.add(Pollution(cat_id_forIns, data["Sub Problem"], float(data['lat']), float(
                    data['long']), int(data['rating']), data['Description'], False, pic_file, current_user.id))
        for classname3 in Road_List:
            if data["Problem"] == classname3:
                session.add(Road(cat_id_forIns, data["Sub Problem"], float(data['lat']), float(
                    data['long']), int(data['rating']), data['Description'], False, pic_file, current_user.id))
        for classname4 in Disasters_List:
            if data["Problem"] == classname4:
                session.add(Disaster(cat_id_forIns, data["Sub Problem"], float(data['lat']), float(
                    data['long']), int(data['rating']), data['Description'], False, pic_file, current_user.id))
        session.commit()
        return redirect(url_for('submission'))
        # return url_for('submission')
    else:
        abort(404, description="Resource not found")

@app.errorhandler(404)
def page404(e):
    return render_template('404.html'), 404

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@mail.georeportit.me',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = session.query(User).filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('an email was sent with resetting info','info')
        return redirect(url_for('login'))

    return render_template('Password_reset.html',title='Reset password',form=form)


@app.route("/reset_password/<token>", methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user= User.verify_reset_token(token)
    if user is None:
        flash('invalid or expired token','warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
        form.password.data).decode('utf-8')
        user.password=hashed_password
        session.commit()
        flash(f'Password was changed !', 'success')
        return redirect(url_for('login'))

    return render_template('reset_token.html',title='Reset password',form=form )

