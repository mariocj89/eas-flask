"""Client to interact with the Facebook API"""
import requests
import logging

_FB_API_URL = "https://graph.facebook.com/v3.0"
LOG = logging.getLogger(__name__)


def _json_or_fail(response):
    """Extracts the JSON of a successful response or raise"""
    try:
        response.raise_for_status()
        return response.json()
    except (requests.exceptions.HTTPError, KeyError):
        logging.info(f"Unexpected error response {response.text}",
                     exc_info=True)
        raise


def get_extended_user_token(user_token, app_id, app_secret):
    """Given an user token, returns a server side, long-lived user token"""
    response = requests.get(
        _FB_API_URL + "/oauth/access_token",
        dict(grant_type="fb_exchange_token",
             client_id=app_id,
             client_secret=app_secret,
             fb_exchange_token=user_token)
    )
    return _json_or_fail(response)["access_token"]


def get_page_token(user_token, page_id):
    """Retrieves a token to interact with a given page

    With an user token (long-lived) and a page id, searches all pages
    and returns the token of the passed in page
    """
    response = requests.get(
        _FB_API_URL + "/me/accounts",
        dict(access_token=user_token)
    )
    for page in _json_or_fail(response)["data"]:
        if page["id"] == page_id:
            return page["access_token"]

    # TODO: raise an structured response
    raise Exception(f"{page_id} not reachable by user")

# TEST: https://graph.facebook.com/v3.0/me/accounts?access_token=EAACEdEose0cBAG2ciFx62OgoNMFB1HQqXKcL7VrOMUMBPz2YB5YV7AXq3JjbxakoaFCz9ftAk4rsANO9CjHKkFb2clyXpB3ZAWNqkBHMZC35qt0WZBX65Yw4jjObdmhcT57R0XX8m18pJqyoanEEDMHwCeteniDyVjsbHZCcEGpkygNYxf8bNwt4vLpGZA2PREy4XTyZB5AwZDZD&fields=id%2C%20global_brand_page_name%2C%20access_token&format=json&method=get&pretty=0&suppress_http_code=1
# RESULT: {"data":[{"id":"351073355302481","global_brand_page_name":"PyCon Charlas","access_token":"EAACEdEose0cBAFKwGkQLeUOJFq7BTcvYOMAZAScEYxIOe4d8q9Mpzh0rzaw3iqgcUyEJDbZB0eQZBzVmhwiCnp3KY1UxnjFBEztKF8oZAKsxB1ZApNUz9qnyCZB4Rsuj2ucnHgfsbkmNcAreYjvAzC1IiR64oc9EYNTToUpXi0lLTQke6H5ecng4KUvV9hfhqq5Xtnv9ICEAZDZD"},{"id":"254267391304775","global_brand_page_name":"EtCaterva","access_token":"EAACEdEose0cBABASC7r9BxN1wPWxv2hpB289sPvRdZA9UwFQjuIfVvIYMukBRGvFeZBoQPXLPIYdtCxXuRycEptK8YxlZBvfFjoXoX8jLID8pzzIFK4NPrWmZC9cxLbnygcaGFa1wfaP2yabDmgfOZANZBNomL6y5WWl0cZBEGR1McD9vHb9TeHKQw3npvFcXcZD"},{"id":"202874843092116","global_brand_page_name":"EchaloASuerte","access_token":"EAACEdEose0cBAP7GZCNWsTHC3SIvVdpBarlDL5f0abkDqtGqxjKYasTmHPYfgFCPorlEHn4qmZA7ON5mv2qg3M9lVtIC8kK79DuowELRGvoqWv8nqTttsyfjGSaglT5C69ZB3gGpUAJVNKA89VNTmfJESsBWgrkjUQSCvebqgPGZARZAKWhUsCmt2CEJWYAoZD"}],"paging":{"cursors":{"before":"MzUxMDczMzU1MzAyNDgx","after":"MjAyODc0ODQzMDkyMTE2"}}}


def get_owner(user_token, object_id):
    """Extracts the owner of an object

    Given an user token and an object id, returns the id who owns the object
    This can be used to retrieve who is the owner of a picture for example,
    which is useful to retrieve
    """
    response = requests.get(f"{_FB_API_URL}/{object_id}?fields=from",
                            dict(access_token=user_token))
    return _json_or_fail(response)["from"]["id"]

# TEST: https://graph.facebook.com/v3.0/1240733105972946/?access_token=EAACEdEose0cBAP7GZCNWsTHC3SIvVdpBarlDL5f0abkDqtGqxjKYasTmHPYfgFCPorlEHn4qmZA7ON5mv2qg3M9lVtIC8kK79DuowELRGvoqWv8nqTttsyfjGSaglT5C69ZB3gGpUAJVNKA89VNTmfJESsBWgrkjUQSCvebqgPGZARZAKWhUsCmt2CEJWYAoZD&debug=all&fields=from%2Calbum&format=json&method=get&pretty=0&suppress_http_code=1
# RESPONSE: {"from":{"name":"EchaloASuerte","id":"202874843092116"},"album":{"created_time":"2016-05-30T19:43:12+0000","name":"Website","id":"1240732559306334"},"id":"1240733105972946","__debug__":{}}

def get_likes(owner_token, object_id):
    """Extracts like objects from an object_id

    Given the token of the owner of an object and the id of it, returns
    all likes of the object as dictionaries with "id" and "name"
    """
    response = requests.get(f"{_FB_API_URL}/{object_id}/likes",
                            dict(access_token=owner_token))
    # TODO: Handle Pagination
    return _json_or_fail(response)["data"]

# TEST: https://graph.facebook.com/v3.0/1240733105972946/likes/?access_token=EAACEdEose0cBAP7GZCNWsTHC3SIvVdpBarlDL5f0abkDqtGqxjKYasTmHPYfgFCPorlEHn4qmZA7ON5mv2qg3M9lVtIC8kK79DuowELRGvoqWv8nqTttsyfjGSaglT5C69ZB3gGpUAJVNKA89VNTmfJESsBWgrkjUQSCvebqgPGZARZAKWhUsCmt2CEJWYAoZD&debug=all&format=json&method=get&pretty=0&suppress_http_code=1
# RESPONSE: {"data":[{"id":"10202845410880288","name":"David Naranjo"},{"id":"202874843092116","name":"EchaloASuerte"}],"paging":{"cursors":{"before":"QVFIUktlUWtzV0I3YzZAoS2lkcjIzRy0wRG1nU2hrVTNMdUJZAdDMzQzFEUVNYMXpvQ0t4RkRHYjdYZAVVXdHRJaW5LV2kZD","after":"QVFIUkpudjN6Qks2QWoyNnFBdktyc2FsVS0xZATZArOF9jQWptWXk5bnBOWEFhencwaVdWR24tVTZAfWmFhVEtxbUMzYkdVR3ZAndmVQOEEyVS1taUhrS2djSDN3"}},"__debug__":{}}


logging.basicConfig(level="INFO")
token = "EAADZAqWaRKwcBAHqqsoAqYsma1Wi6S9jj6ZAZC3j9wLZBTe6iMzcZC1PsQHU0Ub7pzyHYUWMZCUoErmm6UXgj4gw7EFZCaPJrPjofnVHXu7lWMz16ZCuZB0Bk8HtRRPcZCWRyTpCrkkDO7S9lPkygPAlkk5P9acov7sYoZD"
object_id = "1240733105972946"
extended_token = get_extended_user_token(app_id="239321593490183", app_secret="b5a4825f014a7daf894ae8ce38fd7ce9", user_token=token)
owner_page_id = get_owner(extended_token, object_id)
page_token = get_page_token(extended_token, owner_page_id)
likes = get_likes(page_token, object_id)

