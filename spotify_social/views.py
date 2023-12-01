from django.shortcuts import render, redirect
from django.urls import reverse
from spotify_social.database import *
from spotify_social.actions import get_callback, load_user_profile


# ----------------------------------------------------------------------------
# # Shows the user the landing page. This should be the first page they see
# TODO: clean up landing page of user info
# ----------------------------------------------------------------------------
def landing_page(request):
    db = Database()
    result = db.execute("SELECT * FROM user_profile;", (), True)

    db.close()
    return render(request, "signed-out/landing_page.html", {"results": result[1]})


# ----------------------------------------------------------------------------
# displays a page for user to log in
# ----------------------------------------------------------------------------
def login_page(request):
    return render(request, "signed-out/login_page.html", {})


# ----------------------------------------------------------------------------
# displays a page for the user to create an account
# ----------------------------------------------------------------------------
def signup_page(request):
    # if username taken or password mismatch, user info stored in request.session["user_inputs"]
    if "user_inputs" in request.session:
        user_data = request.session.pop("user_inputs", {})
        inputted_user_name = user_data[0]
        inputted_fname = user_data[1]
        inputted_lname = user_data[2]
        inputted_phone = user_data[3]
        inputted_dob = user_data[4]

        return render(
            request,
            "signed-out/signup_page.html",
            {
                "username": inputted_user_name,
                "first_name": inputted_fname,
                "last_name": inputted_lname,
                "phone_number": inputted_phone,
                "dob": inputted_dob,
            },
        )

    return render(request, "signed-out/signup_page.html", {})


# ----------------------------------------------------------------------------
# displays a page to ask user to sign into spotify
# ----------------------------------------------------------------------------
def authorize_spotify(request):
    # check if user is signed in before proceeding
    if "user_id" not in request.session:
        return redirect(reverse("login_page"))

    return render(request, "signed-in/authorize.html", {})


# ----------------------------------------------------------------------------
# displays the home page of the user
# TODO: could add posts here
# ----------------------------------------------------------------------------
def user_home_page(request):
    # check if user is signed in before proceeding
    if "user_id" in request.session:
        # TODO: populate user home page by passing variables into HTML below

        get_callback(request)
        return render(request, "signed-in/home_page.html", {})

    else:
        return redirect(reverse("login_page"))


# ----------------------------------------------------------------------------
# displays the profile of the current user
# TODO: show that there are no top songs/artists if the user does not
# ----------------------------------------------------------------------------
def user_profile_page(request):
    # check if user is signed in before proceeding
    if "user_id" not in request.session:
        return redirect(reverse("login_page"))

    user_name = request.session["user_id"]
    db = Database()
    result = db.execute(
        """
        SELECT * 
        FROM user_profile
        WHERE user_name = %s;
        """,
        (user_name,),
        True,
    )

    top_artists = []
    top_tracks = []

    load_user_profile(request)

    if "top_items_user_profile" in request.session:
        top_artists = request.session["top_items_user_profile"][0]
        top_tracks = request.session["top_items_user_profile"][1]

    return render(
        request,
        "signed-in/profile_page.html",
        {"results": result[1], "top_artists": top_artists, "top_tracks": top_tracks},
    )


# ----------------------------------------------------------------------------
# display the profile editing page
# ----------------------------------------------------------------------------
def user_edit_profile_page(request):
    # check if user is signed in before proceeding
    if "user_id" not in request.session:
        return redirect(reverse("login_page"))

    return render(request, "signed-in/edit_profile_page.html", {})


# ----------------------------------------------------------------------------
# display a page of all the items related to user's search
# ----------------------------------------------------------------------------
def search_page(request):
    # check if user is signed in before proceeding
    if "user_id" not in request.session:
        return redirect(reverse("login_page"))

    if "search_results" in request.session:
        artists = request.session["search_results"][0]
        tracks = request.session["search_results"][1]
        albums = request.session["search_results"][2]

    return render(
        request,
        "search pages/search_items.html",
        {"artists": artists, "tracks": tracks, "albums": albums},
    )


# ----------------------------------------------------------------------------
# display a page of all the user profiles with user names similar to
# what the user searched
# ----------------------------------------------------------------------------
def search_profile_page(request):
    # check if user is signed in before proceeding
    if "user_id" not in request.session:
        return redirect(reverse("login_page"))

    profiles = request.session.pop("searched_profiles", {})

    return render(
        request,
        "search pages/search_profile.html",
        {"profiles": profiles},
    )


# ----------------------------------------------------------------------------
# displays the profile that the user wants to view (not his/her own)
# TODO: show that there are no top songs/artists if the user does not
# ----------------------------------------------------------------------------
def view_profile_page(request):
    # check if user is signed in before proceeding
    if "user_id" not in request.session:
        return redirect(reverse("login_page"))

    top_artists = []
    top_tracks = []
    if "selected_profile_info" in request.session:
        user_info, items = request.session["selected_profile_info"]
        top_artists, top_tracks = items[0], items[1]

    return render(
        request,
        "search pages/view_profile_page.html",
        {"results": user_info, "top_artists": top_artists, "top_tracks": top_tracks},
    )
