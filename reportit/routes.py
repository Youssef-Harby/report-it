from functools import wraps
from flask import abort, render_template, request, url_for, flash, redirect
from flask_login import login_required, login_user, current_user, logout_user
from reportit import app, session, bcrypt
import folium
from folium import plugins
import geopandas
import leafmap.kepler as leafmap
from reportit.models import User,Categories,Utility,Pollution,Disaster,Road,Fire
from reportit.newForm import RegistrationForm, LoginForm

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
    return render_template('index.html')

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


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='My Account')


@app.route('/myreports')
@login_required
def myreports():
    return render_template('myreports.html', reports=myReports, title='My Reports')


@app.route('/tools')
@login_required
@requires_access_level(ACCESS['waterORG'])
def tools():
    return render_template('tools.html', title='Tools')
    

@app.route('/postgis1')
@login_required
@requires_access_level(ACCESS['waterORG'])
def postgis1():
    con = leafmap.connect_postgis(database="gis", host="192.168.1.104", user="docker", password="docker")
    sql = 'SELECT * FROM public.utility'
    gdf = leafmap.read_postgis(sql, con, geom_col='geometry')
    m = leafmap.Map()
    m.add_gdf_from_postgis(sql, con,geom_col='geometry', layer_name="UTIL")
    print("GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG")
    m.to_html(outfile='reportit/templates/postgis1.html')
    return render_template('postgis1.html')

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
    # session.add(User(data["First Name"], data["Last Name"], data["Email"], data["National Id"], data["phone"]))
    # session.commit()
    session.add(Utility(1, float(data['lat']), float(data['lng']), int(
        data["Intensity Range"]), data['Description'], False, current_user.id))
    session.commit()
    return url_for('submission')