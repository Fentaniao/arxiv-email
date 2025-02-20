# HOW TO RUN IT:
# 1. Open the .env file and input your email and password
#
# 2. Update your subscription preferences here:


import csv
import feedparser
from jinja2 import Template
from datetime import date
from pathlib import Path
from dataclasses import dataclass, field, asdict, replace

today = date.today()

# -------------------------------------
# Path Configuration
# -------------------------------------

template_dir = Path('template')


@dataclass
class Paper:
    title: any = ''
    tags: any = ''
    version: any = ''
    authors: any = ''
    authors_str: any = ''
    abstract: any = ''
    abs_link: any = ''
    html_link: any = ''
    pdf_link: any = ''


def renderer(subscription_preferences):
    # Get a list of subjects and tags from 'subj-list.csv'
    with open('subj-list.csv', 'r') as f:
        reader = csv.reader(f)
        subjects = list(reader)

    all_possible_tags = [x[0] for x in subjects]
    all_possible_subjects = [x[1] for x in subjects]

    papers_subjects = {}
    for subj in subscription_preferences:

        # Goes from math.AG -> Algebraic Geometry
        subj_index = all_possible_tags.index(subj)
        subj_title = all_possible_subjects[subj_index]

        rss_url = f"http://rss.arxiv.org/rss/{subj}"
        Feed = feedparser.parse(rss_url)
        entries = Feed.entries

        papers = []
        for entry in entries:
            paper = Paper()

            # Get the title
            paper.title = str(entry.title)

            # Get the tags
            # Get the primary tag (note that entry.tags is a list)
            # The API convention, from what I can understand, lists the primary posting as the first tag
            paper.tags = [tag.term for tag in entry.tags]

            # Get the version number
            # Strip the entry.id at 'v' to get the version number
            # new entries by convention have v1
            paper.version = entry.id.split('v')[2]

            # Get the authors
            paper.authors = entry.author.split('\n')
            paper.authors_str = ', '.join(paper.authors)

            # Get the abstract
            paper.abstract = str(entry.summary).split('Abstract: ')[1]

            # Get the link
            paper.abs_link = entry.link
            paper.html_link = entry.link.replace('abs', 'html')
            paper.pdf_link = entry.link.replace('abs', 'pdf')

            papers.append(paper)

        papers_subjects[subj_title] = papers

    # Create the body of the message (an HTML version).
    html = render_html_template(
        template_path=template_dir / "daily_feed.html",
        output_path="",
        template_data={
            "date": today.strftime("%B %d, %Y"),
            "papers_subjects": papers_subjects,
        },
    )

    return html


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def sender(html, recipient_email, sender_email, sender_password):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Daily arXiv Feed: " + str(today.strftime("%B %d, %Y"))
    msg['From'] = sender_email
    msg['To'] = recipient_email

    # Record the MIME types of both parts,text/plain and text/html.
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part2)

    # Send the message via local SMTP server.
    mail = smtplib.SMTP('smtp.gmail.com', 587)

    mail.ehlo()

    mail.starttls()

    mail.login(sender_email, sender_password)
    mail.sendmail(sender_email, recipient_email, msg.as_string())
    mail.quit()


def render_html_template(
        template_path,
        output_path,
        template_data,
):
    """
    Renders an HTML file from a Jinja2 template.
    """
    try:
        # Read and render the template
        with open(template_path, "r", encoding="utf-8") as template_file:
            template_content = template_file.read()
            j2_template = Template(template_content)
            rendered_content = j2_template.render(template_data)

        # Write the rendered content to the output file
        if output_path:
            with open(output_path, "w", encoding="utf-8") as output_file:
                output_file.write(rendered_content)

    except FileNotFoundError:
        raise RuntimeError(f"Template file {template_path} not found.")

    except Exception as e:
        raise RuntimeError(f"Error during template rendering: {e}")

    return rendered_content

######################################################

# References:
#
# https://dev.to/maxhumber/how-to-send-and-schedule-emails-with-python-dnb
#
# https://stackoverflow.com/a/26369282
#
#
