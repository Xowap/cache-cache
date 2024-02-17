from flask import Flask, make_response, redirect, render_template, request, url_for

from .etag import *

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def etag_demo():
    """This view displays a simple template that informs the user about the
    current ETag value and a random string. This allows to demonstrate how
    ETag works (cache gets refreshed when ETag changes) and to test if caching
    works (if the cache works, the random string shouldn't change)."""

    if request.method == "POST":
        new_etag = generate_random_string()
        set_etag(new_etag)
        return redirect(url_for("etag_demo"))

    current_etag = get_or_set_etag()

    if current_etag == extract_etag(request.headers.get("If-None-Match", "")):
        response = make_response("", 304)
    else:
        response = make_response(
            render_template(
                "etag.html",
                etag=current_etag,
                random_string=generate_random_string(),
            )
        )

    # We put s-maxage=0 instead of no-cache because somehow this incites
    # caching proxy better to store the request into cache
    response.headers["Cache-Control"] = "public, must-revalidate, s-maxage=0"
    response.headers["ETag"] = f'W/"{current_etag}"'

    return response


if __name__ == "__main__":
    app.run(debug=True)
