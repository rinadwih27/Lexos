from flask import session, render_template, Blueprint

from lexos.helpers import constants as constants
from lexos.managers import utility, session_manager as session_manager
from lexos.models.stats_model import StatsModel
from lexos.views.base_view import detect_active_docs

# this is a flask blue print
# it helps us to manage groups of views
# see here for more detail:
# http://exploreflask.com/en/latest/blueprints.html
# http://flask.pocoo.org/docs/0.12/blueprints/
stats_blueprint = Blueprint('statistics', __name__)


# Tells Flask to load this function when someone is at '/statsgenerator'
@stats_blueprint.route("/statistics", methods=["GET"])
def statistics():
    """Handles the functionality on the Statistics page.

    :return: a response object (often a render_template call) to flask and
    eventually to the browser.
    """
    # Detect the number of active documents.
    num_active_docs = detect_active_docs()
    file_manager = utility.load_file_manager()
    labels = file_manager.get_active_labels_with_id()

    # "GET" request occurs when the page is first loaded.
    if 'analyoption' not in session:
        session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
    if 'statisticoption' not in session:
        session['statisticoption'] = {'segmentlist': list(
            map(str,
                list(file_manager.files.keys())))}  # default is all on
    return render_template(
        'statistics.html',
        labels=labels,
        itm="statistics",
        numActiveDocs=num_active_docs

    )


@stats_blueprint.route("/statsFile", methods=["POST"])
def stats_file():
    session_manager.cache_analysis_option()
    session_manager.cache_statistic_option()
    return StatsModel().get_file_info()


@stats_blueprint.route("/statsBoxPlot", methods=["POST"])
def stats_box_plot():
    session_manager.cache_analysis_option()
    session_manager.cache_statistic_option()
    return StatsModel().get_box_plot()
