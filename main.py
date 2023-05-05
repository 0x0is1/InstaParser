from lib.InstaParser import *

parser = InstaParser(input("Enter username:"))

posts = parser.fetch_posts()
# print(parser.get_userDetails(posts))
# exit(0)

data = parser.get_postThumbnails(posts)
for i in data['images']:
    webbrowser.open_new_tab(i)

for i in range(1):
    posts = parser.fetch_posts(data['count'], data['max_id'])
    data = parser.get_postThumbnails(posts)
    for i in data['images']:
        webbrowser.open_new_tab(i)
    if not data['more_available']: break