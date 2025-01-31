# Python Standard Library
import os

# Third-Party Libraries
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

# Local
import helpers
import crud 
from .. import profile_bp






# Set constant variables
MAP_API_KEY = os.environ.get("MAP_API_KEY")
DATABASE_PG = os.environ.get("DATABASE_PG")

####################################################################
# 
# PROFILE - START
#
####################################################################
@profile_bp.route("/profile/start", methods=["GET", "POST"])
@helpers.login_required
def game__profile_start():

    if request.method == "POST":

        return helpers.apology("wrong page", 403)
    
    else:

        if session.get("from_root"):

            session.pop("from_root")  

            try:
                session["profile_package_main"]
                session["profile_package_geo"]
                session["profile_package_fifty"]
            except:
                session["profile_package_main"] = crud.get_dash_main(DATABASE_PG, session["user_id"])
                # session["profile_package_geo"] = session["geo_package_dash_header"] = game_geo.get_geo_package_dash_header(db_pg, session["user_id"]) 
                session["profile_package_fifty"] = session["fifty_package_dash_header"] = crud.get_fifty_package_dash_header(DATABASE_PG, session["user_id"]) 
            
            return redirect("/profile/dash")
        
        else:

            return helpers.apology("wrong page", 403)


####################################################################
# 
# PROFILE - DASHBOARD
#
####################################################################
@profile_bp.route("/profile/dash", methods=["GET", "POST"])
@helpers.login_required
def game__profile_dash():

    if request.method == "POST":

        page = session["current_page"] = request.form.get("page")
        goto = session["current_goto"] = request.form.get("goto")
        nav = session["current_nav"] = request.form.get("nav")
        bttn = session["current_bttn"] = request.form.get("bttn")

        if (page == "dash_main"):

            username = request.form.get("username")
            country = request.form.get("country")
            pass_old = request.form.get("pass_old")
            pass_new = request.form.get("pass_new")
            pass_again = request.form.get("pass_again")

            session.pop("profile_message_username", None)
            session.pop("profile_message_country", None)
            session.pop("profile_message_password", None)

            if (bttn == "profile_username"): 

                if username:
                    results = crud.get_dash_main_updated_username(DATABASE_PG,
                                                                        username, 
                                                                        session["user_id"])
                    
                    if results == 1:
                        session["profile_message_username"] = "Username changed"
                        session["username"] = username

                else:
                    session["profile_message_username"] = "Username not changed"

            if (bttn == "profile_country"): 

                if country:
                    results = crud.get_dash_main_updated_country(DATABASE_PG, 
                                                                            country, 
                                                                            session["user_id"])
                    
                    if results == 1:
                        session["profile_message_country"] = "Country changed"
                
                else:
                    session["profile_message_country"] = "Country not changed"
            
            if (bttn == "profile_hash"): 

                if pass_old:

                    user = crud.get_user_info(DATABASE_PG, session["username"])

                    if len(user) < 1 or not check_password_hash(user["hash"], pass_old):
                        session["profile_message_password"] = "Wrong password"

                    if pass_new == pass_again:
                        new_password = generate_password_hash(pass_again)
                        try:
                            crud.get_dash_main_updated_hash(DATABASE_PG, new_password, session["user_id"])
                            session["profile_message_password"] = "New password saved"
                        except (ValueError, RuntimeError):
                            session["profile_message_password"] = "New password not saved"
                    else:
                        session["profile_message_password"] = "New password did not match"

                else:
                    session["profile_message_password"] = "New password not saved"
            
            return redirect("/dash")

        else:

            return redirect("/")
    
    else:

        try:
            main = session["profile_package_main"]
            header_geofinder = None # session["profile_package_geo"]
            header_fifty = session["profile_package_fifty"]
        except:
            return redirect("/")
        
        try:
            profile_message_username = session["profile_message_username"]
        except:
            profile_message_username = None
        
        try:
            profile_message_country = session["profile_message_country"]
        except:
            profile_message_country = None
        
        try:
            profile_message_password = session["profile_message_password"]
        except:
            profile_message_password = None

        return render_template("profile.html", 
                               map_api_key=MAP_API_KEY,
                               main=main,
                               header_geofinder=header_geofinder,
                               header_fifty=header_fifty,
                               profile_message_username=profile_message_username,
                               profile_message_country=profile_message_country,
                               profile_message_password=profile_message_password)
