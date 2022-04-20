from bs4 import BeautifulSoup
from web_scraping import *


search_page = open("data/search_page.html", "r")
f = open("data/event_page.html", "r")
f1 = open("data/event_1.html", "r")
f2 = open("data/event_2.html", "r")

events = [f, f1, f2]
events = [str(BeautifulSoup(event.read(), 'html.parser')) for event in events]
search_page = str(BeautifulSoup(search_page.read(), 'html.parser'))


print("Testing get_title(html) function")
print("Expected: ONLINE DATA SCIENCE MEETUP Tickets, Tue, Dec 15, 2020 at 3:00 PM | Eventbrite")
print("Actual:", get_title(events[0]))

print()

print("Testing get_event_titles(html) function")
print("Expected: All the event titles from 'search_page.html'")
print("Actual:", get_event_titles(search_page))

print()

print("Testing get_event_links(html) function")
print("Expected: All the event links from 'search_page.html'")
print("Actual:", get_event_links(search_page))

print()

print("Testing extract_event_images(html) function")
print("Expexted: Image link address of 'event_page.html'")
print("Actual:", extract_event_images(events[0]))

print()

print("Testing extract_event_organizer(html) function")
print("Expected: Wholesale Banking Advanced Analytics - ING Bank")
print("Actual:", extract_event_organizer(events[0]))

print()

print("Testing find_event_tags(html) function")
print("Expected: ['Online Events', 'Online Seminars', 'Online Science & Tech Seminars']")
print("Actual:", find_event_tags(events[0]))

print()

print("Testing scrape_event_pages(event_pages) function")
print("Expected output: Dataframe containing [image link, organizer, tags]")
print(scrape_event_pages(events))

print()

print("Testing create_tags_library(event_db) function")
print("Expected output: Dataframe containing [tag, event corresponding to row in event_db]")
print(create_tags_library(scrape_event_pages(events)))

print()

print("Testing search_by_tag(tags_lib, events_db, search_tag) function")
print("Expected output: List of organizers with same event tag")
print(search_by_tag(create_tags_library(scrape_event_pages(events)), scrape_event_pages(events), "Online Seminars"))

print()
print()
print("All functions executed successfully!")

