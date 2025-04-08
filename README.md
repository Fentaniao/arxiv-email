# arxiv-email

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/tbrazel/arxiv-email/math-email.yml)

Welcome to **arxiv-email**,
a GitHub-hosted project that automates sending daily HTML-formatted emails featuring the latest arXiv publications.

This bot aggregates the newest content from arXiv and delivers it directly to your inbox.

<img width="667" alt="arxiv-email" src="https://github.com/tbrazel/arxiv-email/assets/42276623/082de276-3624-4b3e-9e87-97426b165aff">

## Installation

1. **Fork this repository:**  
   Start by creating your own copy of this repository on GitHub.

2. **Prepare Your Gmail Credentials:**  
   Ensure you have your Gmail credentials available. You may need to set up a [new app password](https://support.google.com/mail/answer/185833?hl=en-GB) if required by your Gmail account.

3. **Add Secure Credentials:**  
   In your forked repository, go to **Settings** > **Secrets and variables** > **Actions
   **. Add the following secrets and variables:

    - **Repository Secrets:**
        - `GMAIL_USER` – Your Gmail address used to send daily emails.
        - `GMAIL_PASSWORD` – The app password for that Gmail account.

    - **Repository Variables:**
      - `FREELOADERS` – The email address(es) where you will receive your arXiv subscriptions and your subscriptions subjects.

And you're good to go!

## Usage

### Configuration for `FREELOADERS`

`FREELOADERS` variable should be structured like:

```text
example0@gmail.com:primary1,secondary11,secondary12:primary2:primary3,secondary31
example1@gmail.com:quant-ph,cs.LG,cs.CV,cs.AI,cs.GR:math.AG
example2@gmail.com:math.NT
```

This will be translated into Python dictionaries by the bot like:

```python
SUBSCRIPTIONS0 = {
    "primary1": ["secondary11", "secondary12", ],
    "primary2": [],
    "primary3": ["secondary31", ],
}

SUBSCRIPTIONS1 = {
    "quant-ph": ["cs.LG", "cs.CV", "cs.AI", "cs.GR", ],
    "math.AG": [],
}

SUBSCRIPTIONS2 = {
    "math.NT": [],
}
```

And you will receive emails with the latest papers from the topics you subscribed to.

### Configuration for `subject_list.csv`

If the subjects you need aren't in `subject_list.csv` file, you can add it in `subject_list.csv` file.

Here is the complete and enhanced version of your GitHub README:

### Configuration for sending time

Emails go out at 5:00 UTC (midnight ET) by default.

You can change this in the `.github/workflows/math-email.yml` file.

## Contributing

Contributions to the project are welcome!
If you encounter issues or have suggestions for improvements, please:

- Open an issue.
- Fork the repository and submit a pull request with your proposed changes.

We appreciate your contributions to making **arxiv-email** better!

## License

This project is licensed under the GPL-3.0 license.
