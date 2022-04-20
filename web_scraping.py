from bs4 import BeautifulSoup
import pandas as pd

### You will use extraction techniques while building a dataset of data science events listed on the site Eventbrite.

### First we will process search result webpages, and then extract information from the individual event pages.


def get_title(html):
    """Create a function that expects as input a string of HTML and retreives the title element. In doing this, you
    should make use of the BeautifulSoup library. If there is no title element, raise a ValueError.

    :type html: str
    :param html: a string of HTML to be parsed
    :return: the title element from the HTML string
    :rtype: bs4.element.Tag
    """

    soup = BeautifulSoup(html, "html.parser")
    title = soup.find_all('title')
    if len(title) == 0:
        raise ValueError
    return title[0].get_text()


def get_event_titles(html):
    """We want to get a list of the titles of the search result events. One practical way of finding the section of the
    html that has the information you want is to use the inspect functionality on your browser.

    Open the sample search results page "data/search_page.html" on Chrome or Firefox , right-click on the title of a
    search result event and select inspect. It will open a side bar with the html of the page, highlighting the section
    that contains the code for that part of the page.

    Note that the title is inside a section of type "div", and attribute "data-spec=event-card__formatted-name". We will
    use this attribute as a marker to find the title content.

    Create a function that extracts all instances of this section, with the "find_all()" method. From each of these,
    extract the title string from the first (i.e. zero indexed) element. Note that the title is in a subsection, which
    can be accessed with the ".children" attribute. From this, you can extract a string using the ".string" attribute.

    Create a list of all the event titles in the search page, by extracting the title from all the "find_all()" results.
    Note that there are two instances for each title. Remove the duplicates and return the list. Note that order matters
    and you should return a list of title strings in the order that the "find_all" method returns them, albeit with the
    duplicates removed.

    You may test your function with the sample event page 'data/event_page.html', and visualize elements of the result
    using the "prettify()" method.

    :type html: str
    :param html: a string of HTML to be parsed
    :return: list of title strings of each event
    :rtype: list(str)
    """

    soup = BeautifulSoup(html, "html.parser")
    titles = soup.find_all('div', attrs={"data-spec": "event-card__formatted-name"})
    titles = dict.fromkeys(titles).keys()
    titles = [title.text for title in titles]
    return titles


def get_event_links(html):
    """Now we want to extract the link address to the individual event pages. As before, one practical way of finding
    the section of the html that has the information you want is to use the inspect functionality on your browser.

    Open the sample search results page "data/search_page.html" on Chrome or Firefox , right-click on the title of a
    search result event and select inspect. It will open a side bar with the html of the page, highlighting the section
    that contains the code for that part of the page.

    Find the html section that has the link to the individual event pages as an attribute. Using the "find_all()"
    method, extract all instances of this section. From this, extract the link attributes (the "href") into a list.

    Note that there are duplicates which should be removed. Again, order matters here so your list of event links should
    be in the order that "find_all()" returns.

    :type html: str
    :param html: a string of HTML to be parsed
    :return: list of link strings of each event
    :rtype: list(str)
    """

    soup = BeautifulSoup(html, "html.parser")
    divs_with_a = soup.find_all('div', attrs={"class": "eds-event-card-content__primary-content"})
    links = [div.find('a')["href"] for div in divs_with_a]
    links = list(dict.fromkeys(links).keys())
    return links


def extract_event_images(html):
    """Now that we have gathered the links to the event pages, we will extract some relevant information from these
    pages for our database.

    As before, one practical way of finding the section of the html that has the information you want is to use the
    inspect functionality on your browser.

    Open the sample events page "data/event_page.html" on Chrome or Firefox and, using the inspect tool, find the
    html section that contains the link address of the main image for the event. In other words, find the "div"
    section containing the image.

    Once you have identified the relevant "div" and its class, use the "find_all()" method to retrieve the element.
    If you have done this correctly, a single element should be returned. From this element, access its picture
    section and return its content.

    If there are no relevant "div" sections, and "find_all()" returns an empty list, your function should raise a
    ValueError.

    Hint: You may load and visualize the image with the requests and IPython.display libraries, using:
      import IPython.display as Disp
      Disp.Image(requests.get(image_link).content)

    :type html: str
    :param html: a string of event page HTML to be parsed
    :return: Image link address
    :rtype: str
    """

    soup = BeautifulSoup(html, "html.parser")
    divs_with_pic = soup.find_all('div', attrs={'class': 'listing-hero'})
    if len(divs_with_pic) == 0:
        raise ValueError
    else:
      picture = divs_with_pic[0].find('picture')["content"]
      return picture


def extract_event_organizer(html):
    """We want to find the name of the listing organizer. As before, we can use the inspect functionality to find
    the relevant part of the web page, and use BeautifulSoup to "find_all()" instances of that particular element and
    class.

    Open the sample events page "data/event_page.html" on Chrome or Firefox and, using the inspect tool, find
    the html element that contains the name of the event organiser.

    Using BeautifulSoup's "find_all()" method, find the organizer's name. You will want to specify the type of element
    and the class. This should return a list with one entry. From this entry, extract the string containing the
    organizer's name, and return it.

    In retrieving the name, your function should exclude trailing space and any prefixes such as "by ".

    If there are no relevant "div" sections, and "find_all()" returns an empty list, your function should raise a
    ValueError.

    Hint: Access the string attribute. You may use the regular expression library to find the "by " substring, and you
    can access non-space characters with the "." regular expression term.

    :type html: str
    :param html: a string of event page HTML to be parsed
    :return: Organizer name
    :rtype: str
    """

    soup = BeautifulSoup(html, "html.parser")
    divs_with_org = soup.find_all('div', attrs={'class': 'listing-organizer-title'})
    if len(divs_with_org) == 0:
        raise ValueError
    else:
      org = divs_with_org[0].find('a').text.strip()[3:]
      return org


def find_event_tags(html):
    """In this function, we want to find a list of tags for a given event. As before, we can use the inspect functionality
    to find the relevant part of the web page, and use BeautifulSoup to "find_all()" instances of that particular type of
    element and the class.

    Open a sample events page (in the "data/event_pages/" directory) on Chrome or Firefox and, using the inspect tool, find
    the html element that contains the string "Tags". This can be found towards the bottom of the page. Note the element
    type and the class and use BeautifulSoup's "find_all()" method to find all matching instances. However, we are only
    interested in where the string contents of this element is equal to "Tags" (luckily the "find_all()" method has an
    string argument to help filter.)

    Assuming that you have found this element (and that you have opened a sample events page with a list of tags) you will
    notice that, in the HTML, the parent of the Tags element also contains all of the tags themselves, each within an "a"
    element. Using "find_all()" again, extract all "a" elements found within the parent of the Tags element that you found
    earlier.

    For each of these "a" elements, extract the text as a string, remove any trailing spaces and end-of-line characters,
    and return a list.

    If there are no "a" elements found (i.e. "find_all()" returns an empty list), your function should raise a ValueError.

    :type html: str
    :param html: a string of event page HTML to be parsed
    :return: Event tags
    :rtype: list(str)
    """

    soup = BeautifulSoup(html, "html.parser")
    a_tags = soup.find_all("h3", string="Tags")[0].parent.find_all("a")
    if len(a_tags) == 0:
        raise ValueError
    else:
      tags = [a_tag.text.strip() for a_tag in a_tags]
      return tags


def scrape_event_pages(event_pages):
    """In the previous functions, we have done some fairly involved web scraping. In this function, we want to bring it all
    together and automate the scraping of a number of different pages. The input to this function ("event_pages") consists
    of a list of HTML strings. For each page, we want to extract the image, the organizer, and the tags.

    First, create an empty Pandas DataFrame with columns "image", "organizer", and "tags". Next, iterate over the "event_pages"
    input and, at each iteration:
        1. Extract the link for the main image on the page
        2. Extract the name of the event organizer, stripping out trailing space and prefixes such as "by "
        3. Extract a list of tags as strings (remember that order matters!)

    After (or during) each iteration, update the DataFrame with the extracted information in the appropriate column.

    If any item is absent from an event page, then set it to be an empty string.

    :type html: list(str)
    :param html: list of event pages HTML to be parsed
    :return: Event Pages Database
    :rtype: Pandas DataFrame
    """

    df = pd.DataFrame(columns=['image', 'organizer', 'tags'])

    for event in event_pages:
        try:
            image = extract_event_images(event)
        except ValueError:
            image = ""
        
        try:
            organizer = extract_event_organizer(event)
        except ValueError:
            organizer = ""
        
        try:
            tags = find_event_tags(event)
        except ValueError:
            tags = ""

        df = df.append({'image': image, 'organizer': organizer, 'tags': tags}, ignore_index=True)
    
    return df


def create_tags_library(event_db):
    """In this function, it is a assumed that we have already completed our web scraping and have created a DataFrame like
    that returned by the "scrape_event_pages" function. That is, a Pandas DataFrame with the columns "image", "organizer",
    and "tags".

    This function takes as input a DataFrame with the above structure (i.e. three columns). It should iterate over the
    DataFrame and return an output DataFrame with two columns: "tag" and "event".

    For each row in the input DataFrame, this function should iterate over each tag, and add a row to the output DataFrame
    indexing the row of the input DataFrame that the tag maps to.

    For instance, the following input DataFrame:

    | image       | organizer      | tags                        |
    |-------------|----------------|-----------------------------|
    | www.url.com | CambridgeSpark | ["#python", "data science"] |
    | www.url.com | ARU            | ["ML", "#python"]           |

    Would result in the output DataFrame:

    | tag            | event |
    |----------------|-------|
    | "#python"      | 0     |
    | "data science" | 0     |
    | "ML"           | 1     |
    | "#python"      | 1     |


    :type event_db: Pandas DataFrame
    :param event_db: DataFrame with event information
    :return: Tags library DataFrame
    :rtype: Pandas DataFrame
    """

    df = pd.DataFrame(columns=['tag', 'event'])

    event_db = event_db.drop(columns=['image', 'organizer'], axis=1)
    event_db = event_db.explode('tags')

    df['tag'] = event_db['tags']
    df['event'] = event_db.index
    df = df.reset_index(drop=True)

    return df


def search_by_tag(tags_lib, events_db, search_tag):
    """In this final function, we take a "tags_lib" DataFrame which maps tags to their row index of events in the "events_db"
    and a "search_tag" string.

    Use the "search_tag" input to return a list of event organizers whose events contain the given tag.

    :type tags_lib: Pandas DataFrame
    :param tags_lib: tags library, with "tag" and "event" columns
    :type events_db: Pandas DataFrame
    :param events_db: events db, with "image", "organizer" and "tag" columns
    :type search_tag: str
    :param search_tag: a tag to be searched
    :return: List of event titles
    :rtype: list(str)
    """

    organizers = []
    for _, row in tags_lib.iterrows():
        if search_tag in row['tag']:
            organizers.append(events_db.iloc[int(row['event'])]['organizer'])
    return organizers
