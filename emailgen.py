# HOW TO RUN IT:
# 1. Open the .env file and input your email and password
#
# 2. Update your subscription preferences here:


import csv
import feedparser
from datetime import date
today = date.today()


def send_email(recipient_email,subscription_preferences,sender_email,sender_password):
	# Get a list of math subjects and math tags from 'subj-list.csv'
	with open('subj-list.csv','r') as f:
		reader = csv.reader(f)
		mathSubjects = list(reader)

	all_possible_tags = [x[0] for x in mathSubjects]
	all_possible_subjects = [x[1] for x in mathSubjects]

	# Generate HTML for the email
	html_top = """\
	<html>
	<head>
		<style>
			html{
				background-color: #F2F3F4;
			}
			p{
				color:#2B303A;
			}
			.colored {
				color: blue;
			}
			#body {
				font-size: 14px;
			}
			#banner{
				width:100%;
				font-size:18px;
				color: #F4F2F3;
				text-align:center;
				padding:1px;
				border-radius: 20px;
				background-color: #515c5d;
			}

			.banner_table{
				border-radius: 20px;
				text-align: center;
				color: white;
				background-size: cover;
			}

			#banner h1{
				width: 75%;
				display: inline-block;
				margin: 10px;
			}


			#body a{
				color: #0C7C59;
			}
			#subjectTitle{
				width:inherit;
				font-size:14px;
				color : #984447;
				text-align:center;
			}
			#subject{
				text-align:left;
			}

			#tag, #xlistedtag, #updated{
				display: inline;
				color: white;
				border-radius: 8px;
				padding: 2px;
				font-size: 12px;
				margin: 2px;
				padding-left: 4px;
  				padding-right: 4px;
			}

			#tag{
				background-color: #984447;
			}
			#xlistedtag{
				background-color: #a65094;
			}

			#updated{
				background-color: #575757;
			}


			.container {
			  position: relative;
			  text-align: center;
			  color: yellow;
			}

			.container h1{
			   z-index: 2;
			   position: absolute;
			   top: 50%;
				left: 50%;
				right: 50%;
				font-size: 18px;
				width: inherit;
				padding: 0;
				margin: 0;
			}

			.container img{
				z-index: 1;
				width: 100%;
				height: 100%;
				position: absolute;
				top:0;
				right:0;
				bottom:0;
				left:0;
			}


		</style>
	</head>
	<body>
		<div id="banner">
			<h1>Daily Math Feed: """ + str(today.strftime("%B %d, %Y")) + """</h1>
		</div>

		<br>
		<div id="body">
	"""
	text_top = "Daily Math Feed\n\n"

	html_bottom = """\
		</div>
	</body>
	</html>
	"""

	rss_html = ""
	rss_text = ""

	for subj in subscription_preferences:

		# Goes from math.AG -> Algebraic Geometry
		subj_index = all_possible_tags.index(subj)
		subj_title = all_possible_subjects[subj_index]


		rss_url = "http://rss.arxiv.org/rss/" + str(subj)
		Feed = feedparser.parse(rss_url)
		pointer = Feed.entries

		rss_html = rss_html + """\t<div id="subjectTitle">\n\t<h2 id="subjectTitleText">""" + str(subj) + """</h2>\n\t</div>\n\t<div id="subject">\n"""
		text_html = str(subj) + '\n'

		for entry in pointer:

			# Get the title of the paper
			papertitle = str(entry.title)

			# Get the primary tag (note that entry.tags is a list)
			# The API convention, from what I can understand, lists the primary posting as the first tag
			primarytag = entry.tags[0].term


			# Make the list of tags, and the associated html
			tags_html = ''
			for x in entry.tags:
				tag = x.term
				if tag == primarytag:
					newtag = '<div id="tag">' + str(tag) + '</div>'
				else:
					newtag = '<div id="xlistedtag">' + str(tag) + '</div>'
				
				tags_html = tags_html + newtag


			# Strip the entry.id at 'v' to get the version number
			# new entries by convention have v1
			version_number = entry.id.split('v')[2]

			version_html = ''
			if int(version_number) != 1:
				version_html = version_html + '<div id="updated">v' + str(version_number) + '</div>'



			# Get author info
			author_list = entry.author.split('\n')
			author_str = author_list[0]

			# If there are multiple authors
			if len(author_list) > 1:
				for i in range(1,len(author_list)):
					author_str = author_str + ', ' + author_list[i].lstrip()



			# Make the html for the entry
			entry_html = '\n\t\t<div id="paper"><b>Title:</b> '

			# Add the link to the title
			entry_html = entry_html + '<a id="paperTitle" href="' + str(entry.link) + '">' + papertitle + '</a>'
			
			# Add tags and version info
			entry_html = entry_html + '<br>\n\t<b> Tags: </b>' + tags_html + version_html

			# Add authors
			entry_html = entry_html + '<br>\n\t<b> Authors: </b>' + author_str

			# Add summary
			abstract = str(entry.summary).split('Abstract: ')[1]
			entry_html = entry_html	+ '<br>\n\t\t<b>Abstract: </b>' + abstract + '</div>\n<hr>'


			# Add alternative text version of email
			entry_text = str(entry.title) + '\n\t' + author_str + '\n\n\t\t' + str(entry.summary)

			rss_html = rss_html + entry_html
			rss_text = rss_text + entry_text


		rss_html = rss_html + "\t</div>\n"


	import smtplib
	from email.mime.multipart import MIMEMultipart
	from email.mime.text import MIMEText
	from email.mime.image import MIMEImage


	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Daily Math Feed: " + str(today.strftime("%B %d, %Y"))
	msg['From'] = sender_email
	msg['To'] = recipient_email

	# Create the body of the message (a plain-text and an HTML version).
	text = text_top + rss_text
	html = html_top + rss_html + html_bottom

	# print('HTML is :')
	# print(html)

	# ### Uncomment the following lines for testing:
	# testingpage = open('test.html','w')
	# testingpage.write(html)




	# Record the MIME types of both parts,text/plain and text/html.
	part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')

	# Attach parts into message container.
	# According to RFC 2046, the last part of a multipart message, in this case
	# the HTML message, is best and preferred.
	msg.attach(part1)
	msg.attach(part2)

	# Send the message via local SMTP server.
	mail = smtplib.SMTP('smtp.gmail.com', 587)

	mail.ehlo()

	mail.starttls()

	mail.login(sender_email, sender_password)
	mail.sendmail(sender_email, recipient_email, msg.as_string())
	mail.quit()

######################################################

# References:
#
# https://dev.to/maxhumber/how-to-send-and-schedule-emails-with-python-dnb
#
# https://stackoverflow.com/a/26369282
#
# 
