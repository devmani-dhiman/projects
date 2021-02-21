import requests
import html2text
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode

url = 'https://www.facebook.com/careers/jobs?offices[0]=Gurgaon%2C%20India&offices[1]=Bangalore%2C%20India&' \
      'offices[2]=Hyderabad%2C%20India&offices[3]=New%20Delhi%2C%20India&offices[4]=Mumbai%2C%20India'

"""def test_init_db():
    global conn
    try:
        print("[+] Connecting to DB: ", end="")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("ACCESS DENIED")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("DB does not exist")
        else:
            print(err)
        exit()
    else:
        print("OK")
    conn = sql.connect("linkedin.db")
    _cursor = conn.cursor()
    return _cursor"""


def parsing_html(_url):
    """Parsing the Html on the Job search page and Returning the soup object.

    :param _url of the main page
    :return soup object of the url given.
    """
    html_text = requests.get(_url).text
    _soup: BeautifulSoup = BeautifulSoup(html_text, "html.parser")
    return _soup


def extracting_details(_soup, _tag, _class):
    """Extracting the details from the soup object returned by the parsing_html() function.

    :param _class:
    :param _tag:
    :param _soup:
    :return The details/text inside different tags and classes.
    """
    detail_tag = str(_soup.find_all(_tag, _class))
    details = html2text.html2text(detail_tag)
    return details


def get_location(_soup, _tag, _class):
    location = list()
    _loc = extracting_details(_soup, _tag, _class).split(",")
    _n = len(_loc)
    d = 0
    while d < _n:
        location.append(_loc[d])
        d += 2
    return location


def format_location(_location):
    if len(_location) < 5:
        _location = ''.join(c for c in _location if c not in '[').strip("[").replace("[", ",")
    return _location


soup = parsing_html(url)
opportunities = extracting_details(soup, "div", "_8opg")
opportunities = int(opportunities.split(" ")[2])
print(opportunities)


def breaking_bad(_string):
    """
    To break the full description into different sections containing the information

    :param _string:
    :return dictionary containing the given points as keys and their index as the values.
    """
    break_points = ["Responsibilities", "Minimum Qualifications", "Location"]
    ind_dict = dict()
    for point in break_points:
        ind = _string.find(point)
        ind_dict[point] = ind
    return ind_dict


details_dict = dict()


def get_data():
    for a in soup.find_all(class_="_8sef"):
        job_url = "https://www.facebook.com" + a['href']
        details_list = []
        soup2 = parsing_html(job_url)
        job_id = job_url.split("/")[-2]
        title = extracting_details(soup2, "div", "_9ata")
        loc1 = get_location(soup2, "a", "_8lfp _9a80")
        if len(loc1) == 1:
            loc1 = extracting_details(soup2, "span", "_8lfp _9a80")
        location = format_location(loc1)
        description = extracting_details(soup2, "div", "_1n-_ _6hy- _94t2")
        resp_quali_combined = extracting_details(soup2, 'div', "_8mlh")
        ind_dict = breaking_bad(resp_quali_combined)
        responsibilities = resp_quali_combined[ind_dict["Responsibilities"]:ind_dict["Minimum Qualifications"]]
        qualification = resp_quali_combined[ind_dict["Minimum Qualifications"]:ind_dict["Location"]]

        details_list.append(title)
        details_list.append(location)
        details_list.append(description)
        details_list.append(responsibilities)
        details_list.append(qualification)
        details_list.append(job_url)

        details_dict[job_id] = details_list
    return details_dict


def init_db():
    global conn
    try:
        print("[+] Connecting to DB: ", end="")
        conn = mysql.connector.connect(user='******', password='******', host='******',
                                       database='******')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("ACCESS DENIED")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("DB does not exist")
        else:
            print(err)
        exit()
    else:
        print("OK")

    _cursor = conn.cursor()
    return _cursor


def create_table(_cursor):
    try:
        _cursor.execute('''CREATE TABLE facebook
            (ID                         VARCHAR(200) PRIMARY KEY     NOT NULL,
            TITLE                       TEXT    NOT NULL,
            LOCATION                    TEXT    NOT NULL,
            DESCRIPTION                 TEXT,
            RESPONSIBILITIES            TEXT,
            QUALIFICATION               TEXT,
            JOB_URL                     TEXT,
            ACTIVE                      VARCHAR(1) DEFAULT 'I');''')  # A: Active, I: Inactive

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
            _cursor.close()
            conn.close()
            exit()
    else:
        print("OK")

    _cursor.execute("SELECT id FROM facebook")
    facebook_ids = [row[0] for row in _cursor]
    return facebook_ids


def update_table(_cursor, job_dict, prejob_ids):
    if job_dict:
        ct = 0
        for key, value in job_dict.items():
            if key not in prejob_ids:
                ct += 1
                try:
                    print(f"\r[+] Writing to DB: {ct}", end="")
                    _cursor.execute(
                        "INSERT INTO facebook (id, title, location, description, responsibilities, qualification,"
                        " job_url, active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (key, job_dict[key][0], job_dict[key][1], job_dict[key][2], job_dict[key][3],
                         job_dict[key][4], job_dict[key][5], "A"))
                except mysql.connector.Error as err:
                    if err.errno != errorcode.ER_DUP_ENTRY:
                        print("\n" + str(err.msg))
                        _cursor.close()
                        conn.close()
                        exit()


def main():
    job_dict = get_data()
    _cursor = init_db()
    _cursor.execute("DROP TABLE facebook")
    prejob_ids = create_table(_cursor)
    update_table(_cursor, job_dict, prejob_ids)
    conn.commit()


if __name__ == "__main__":
    main()
