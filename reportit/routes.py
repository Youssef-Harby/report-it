from functools import wraps
import json
from flask import abort, render_template, request, url_for, flash, redirect
from flask_login import login_required, login_user, current_user, logout_user
from reportit import app, session, bcrypt
import folium
from folium import plugins
import geopandas
import leafmap.kepler as leafmap
from reportit.models import User,Categories,Utility,Pollution,Disaster,Road,Fire
from reportit.newForm import RegistrationForm, LoginForm, UpdateAccountForm

ACCESS = {
    'guest': 0,
    'user': 1,
    'waterORG': 2,
    'gasORG': 3,
    'utilityORG': 4,
    'admin': 666,
}

myReports = [
    {
        'author': 'Youssef Harby',
        'problem': 'Pipeline Break',
        'description': 'Description Test 1',
        'date_reported': '11-03-2022',
        'status': True

    },
    {
        'author': 'Khalid',
        'problem': 'Noise Pollution',
        'description': 'Description Test 2',
        'date_reported': '10-03-2022',
        'status': False

    }
]


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
    return render_template('index.html', title='Home')

# @app.route('/')
# def home():
#     return render_template('home.html')


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
        return redirect(url_for('myreports'))
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


@app.route('/myaccount',methods=['GET', 'POST'])
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
    elif request.method =='GET':
        form.fname.data = current_user.f_Name
        form.lname.data = current_user.l_Name
        form.email.data = current_user.email
        form.nationalid.data = current_user.national_id
        form.phonenumber.data = current_user.phone_num
    reports = session.query(User).get(current_user.id).reports
    numreports = len(reports)
    return render_template('myaccount.html', title='My Account', numreports=numreports, form=form)


@app.route('/myreports')
@login_required
def myreports():
    reports = session.query(User).get(current_user.id).reports
    reportsIDs=[]
    for i in reports:
       obj = {
           "id":i.id,
           "lat": i.lat,
           "lon": i.lon,
           "solved": i.solved
       }
       reportsIDs.append(obj)
    data = json.dumps(reportsIDs)
    return render_template('myreports.html', reports=reports, title='My Reports',data=data)


@app.route('/tools')
@login_required
@requires_access_level(ACCESS['waterORG'])
def tools():
    return render_template('tools.html', title='Tools')
    
@app.route('/analysis1')
@login_required
@requires_access_level(ACCESS['waterORG'])
def analysis1():
    from threading import Timer
    from reportit.analysis.sjoina import sJoinA
    gdf = sJoinA('SELECT * FROM public.utility')
    admin_poly = geopandas.read_file("Data/Facilities/Admin3Poly.gpkg", layer='All-Admin-Area-Egypt').to_crs("EPSG:3857") #Polygon
    m = leafmap.Map()
    config = "reportit/analysis/config2.json"
    m.add_gdf(gdf, layer_name="layer1")
    m.add_gdf(admin_poly, layer_name="layer2", config=config)
    # m.to_html("reportit/templates/mymap.html")
    return m._repr_html_()

@app.route('/report')
@login_required
def report():
    return render_template('report.html')


@app.route('/folium')
def foliumMap():
    from reportit.postgis import df_utility
    # print(df.info())
    geometry = geopandas.points_from_xy(df_utility.lon, df_utility.lat)
    geo_df = geopandas.GeoDataFrame(
        df_utility[['id', 'description', 'lat', 'lon', 'timestamp']], geometry=geometry)
    print(geo_df.head())
    # Create a geometry list from the GeoDataFrame
    geo_df_list = [[point.xy[1][0], point.xy[0][0]]
                   for point in geo_df.geometry]
    # print(geo_df_list)

    start_coords = (30.0444, 31.2357)
    folium_map = folium.Map(location=start_coords, zoom_start=6)
    plugins.HeatMap(geo_df_list).add_to(folium_map)
    # return df.keys()
    return folium_map._repr_html_()


@app.route('/leafmap')
def leafmapTest():
    from reportit.postgis import df_utility
    m = leafmap.Map(center=[30.0444, 31.2357], zoom=6,
                    height=600, widescreen=False)
    geometry = geopandas.points_from_xy(df_utility.lon, df_utility.lat)
    geo_df = geopandas.GeoDataFrame(
        df_utility[['id', 'description', 'lat', 'lon']], geometry=geometry)
    print(geo_df.head())
    m.add_gdf(geo_df, layer_name="Points",
              fill_colors=["red", "green", "blue"])
    # m.to_html(outfile='./reportit/templates/leafmap.html')
    return m._repr_html_()


@app.route('/submission')
def submission():
    return render_template('submission.html')

    
@app.route('/reportm')
@login_required
def reportm():
    return render_template('reportm.html')

@app.route('/jsontest', methods=['POST'])
@login_required
def jsontestpost():
    data = request.get_json()
    # print(data)
    session.add(Utility(1, float(data['lat']), float(data['lng']), int(3), data['Description'], False, current_user.id))
    # session.add(Utility(1, data["Sub Problem"], float(data["lat"]), float(data["lng"]), int(data["rating"]), data['Description'],data["image"], False, int(current_user.id)))
    session.commit()
    return url_for('submission')