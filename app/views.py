from flask import current_app as app
from flask import render_template, abort
from app.get_data import get_data
from app.get_place import get_location, get_location_data


@app.errorhandler(404)
def page_not_found(error):
    return render_template("weather_template/404.html", title="404"), 404


@app.route("/", methods=['GET', 'POST'])
def home():
    """ This function accepts data file(.txt)
        and saves it in uploads folder.If the
        the file is not found, Error 404 pagenotfound is called
    """
    try:
        locate_place = get_location()
        # if locate_place == None:
        #     return render_template(request, "weather_template/404.html")
        weather_data = get_location_data(locate_place)
        context = get_data(weather_data)
        context.update(address=locate_place.address)
        return render_template("weather_template/index.html", context=context)

    except:
        abort(404)
