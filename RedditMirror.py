import praw, datetime, os, base64, requests, json
#Login to reddit
reddit = praw.Reddit(user_agent="Post scraper (by /u/jershxl)", client_id="CLIENT_ID", client_secret="CLIENT_SECRET", username="USERNAME", password="PASSWORD")
#Create the index html file
f = open("index.html","w+")
css = open("main.css", "w+")
css.write("html * { font-family: 'Roboto', sans-serif; }")
css.close()
posts = [ ]
titles = [ ]
#Set the date and print title
today = datetime.date.today()
#CSS Shit
f.write("<head><link href=\"https://fonts.googleapis.com/css?family=Roboto\" rel=\"stylesheet\"><link href=\"main.css\" rel=\"stylesheet\"></head>")
f.write("<center>AskReddit Mirror</center>")
f.write("Last updated on: " + str(today) + "<br>")

i = 0
for submission in reddit.subreddit('askreddit').hot(limit=10):
    try:
        #Make the individual pages
        posts.append(open(str(i)+".html","w+"))
        titles.append(submission.title)
        posts[i].write("<head><link href=\"https://fonts.googleapis.com/css?family=Roboto\" rel=\"stylesheet\"><link href=\"..\main.css\" rel=\"stylesheet\"></head>")
        print("Writing title...")
        posts[i].write("<h1>" + submission.title + "</h1>")
    except UnicodeEncodeError:
        print("Unicode Error (ignore)")
    submission.comments.replace_more(limit=0)
    for comment in submission.comments:
        try:
            print("Writing comment...")
            posts[i].write(">>" + comment.body + "<br>")
        except UnicodeEncodeError:
            print("Unicode Error (ignore)")
        for scomment in comment.replies:
            try:
                print("Writing child comment...")
                posts[i].write("<ul>")
                posts[i].write("<li>" + scomment.body + "</li>")
                posts[i].write("</ul>")
            except UnicodeEncodeError:
                print("Unicode Error (ignore)")
    posts[i].close()
    i += 1

   
i = 0
for post in posts:
    f.write("<a href=\"" + str(i) + ".html\"><h1>" + titles[i] + "</h1></a><br>")
    i += 1

f.write("<center>Created by @jershxl</center>")

f.close()
#Credit goes to Martin Monperrus @ SO for this method
def push_to_github(filename, repo, branch, token):
    url="https://api.github.com/repos/"+repo+"/contents/"+filename

    base64content=base64.b64encode(open(filename,"rb").read())

    data = requests.get(url+'?ref='+branch, headers = {"Authorization": "token "+token}).json()
    sha = data['sha']

    if base64content.decode('utf-8')+"\n" != data['content']:
        message = json.dumps({"message":"update",
                            "branch": branch,
                            "content": base64content.decode("utf-8") ,
                            "sha": sha
                            })

        resp=requests.put(url, data = message, headers = {"Content-Type": "application/json", "Authorization": "token "+token})

        print(resp)
    else:
        print("nothing to update")

token = "GITHUB_TOKEN"
filename="index.html"
repo = "GITHUB_USER/GITHUB_REPO"
branch="GITHUB_BRANCH"

print("Pushing index file...")
push_to_github(filename, repo, branch, token)

filename = "main.css"
print("Pushing CSS file...")
push_to_github(filename, repo, branch, token)

i = 0
print("Pushing posts...")
for post in posts:
    print("Pushing post " + str(i) + "...")
    push_to_github(str(i)+".html", repo, branch, token)
    i += 1
print("DONE :D")