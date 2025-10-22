<div align="center">
  <img src="DAILYUPVOTER BOTV2.png" alt="Daily Upvoter Bot" width="600">
</div>

# Reddit Daily Upvoter Bot

A GitHub Actions bot that automatically upvotes one random post per day from specified subreddit(s).

## Features

- Upvotes one random post daily from a list of subreddits
- Runs automatically via GitHub Actions
- Can target single or multiple subreddits
- Randomly selects both the subreddit and the post
- Manual trigger option to upvote multiple posts at once
- Provides detailed logging of upvoted posts

## Setup Instructions

### 1. Create a Reddit Application

1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Fill in the form:
   - **name**: Reddit Upvoter Bot (or any name you prefer)
   - **App type**: Select "script"
   - **description**: (optional)
   - **about url**: (optional)
   - **redirect uri**: http://localhost:8080 (required but not used)
4. Click "Create app"
5. Note down your:
   - **client_id** (under the app name)
   - **client_secret** (labeled as "secret")

### 2. Configure GitHub Repository

1. Fork or push this repository to your GitHub account

2. Go to your repository Settings > Secrets and variables > Actions

3. Add the following secrets (click "New repository secret" for each):
   - `REDDIT_CLIENT_ID`: Your Reddit app client ID
   - `REDDIT_CLIENT_SECRET`: Your Reddit app client secret
   - `REDDIT_USERNAME`: Your Reddit username
   - `REDDIT_PASSWORD`: Your Reddit password
   - `SUBREDDITS`: Comma-separated list of subreddits (e.g., `programming,python,technology`)

### 3. Configure Subreddits

You can configure subreddits in two ways:

**Option 1: GitHub Secrets (Recommended for GitHub Actions)**
- Add to `SUBREDDITS` secret as comma-separated values
- Example: `programming,python,technology,machinelearning`

**Option 2: config.json (For local testing)**
- Edit [config.json](config.json) and add your subreddits and minimum score:
```json
{
  "subreddits": [
    "programming",
    "python",
    "technology"
  ],
  "min_score": 10
}
```

### 4. Enable GitHub Actions

1. Go to the "Actions" tab in your repository
2. If prompted, enable GitHub Actions
3. The workflow will run daily at 10:00 AM UTC (configurable in [.github/workflows/daily-upvote.yml](.github/workflows/daily-upvote.yml))

### 5. Manual Execution

You can manually trigger the bot and specify how many posts to upvote:

1. Go to the **Actions** tab in your repository
2. Click on **"Daily Reddit Upvote"** workflow
3. Click the **"Run workflow"** dropdown button
4. Configure your options:
   - **Number of posts to upvote**: Enter how many posts (e.g., `2` for 2 posts, default is `1`)
   - **Minimum upvotes a post must have**: Enter minimum score (e.g., `50` for posts with 50+ upvotes, default is `10`)
5. Click the green **"Run workflow"** button

When manually triggered:
- **Default**: Upvotes 1 post with at least 10 upvotes
- **Custom**: Specify both post count and minimum score
- Posts are selected from the **top posts of the day** that meet your criteria
- Each post is randomly selected from your subreddit list
- The bot will provide a summary showing successful and failed upvotes

## Local Testing

To test the bot locally:

1. Install Python 3.11 or higher

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables:
```bash
# On Linux/Mac
export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_CLIENT_SECRET="your_client_secret"
export REDDIT_USERNAME="your_username"
export REDDIT_PASSWORD="your_password"
export SUBREDDITS="programming,python"

# On Windows (Command Prompt)
set REDDIT_CLIENT_ID=your_client_id
set REDDIT_CLIENT_SECRET=your_client_secret
set REDDIT_USERNAME=your_username
set REDDIT_PASSWORD=your_password
set SUBREDDITS=programming,python

# On Windows (PowerShell)
$env:REDDIT_CLIENT_ID="your_client_id"
$env:REDDIT_CLIENT_SECRET="your_client_secret"
$env:REDDIT_USERNAME="your_username"
$env:REDDIT_PASSWORD="your_password"
$env:SUBREDDITS="programming,python"
```

4. Run the script:
```bash
# Upvote 1 post (default)
python upvote_reddit.py

# Upvote multiple posts (e.g., 5 posts)
# On Linux/Mac:
POST_COUNT=5 python upvote_reddit.py

# On Windows (Command Prompt):
set POST_COUNT=5 && python upvote_reddit.py

# On Windows (PowerShell):
$env:POST_COUNT=5; python upvote_reddit.py
```

## Configuration

### Schedule

To change when the bot runs, edit the cron schedule in [.github/workflows/daily-upvote.yml](.github/workflows/daily-upvote.yml#L5):

```yaml
schedule:
  - cron: '0 10 * * *'  # Runs at 10:00 AM UTC daily
```

Cron format: `minute hour day month day-of-week`
- `0 10 * * *` = 10:00 AM UTC every day
- `0 0 * * *` = Midnight UTC every day
- `0 18 * * *` = 6:00 PM UTC every day

Use [crontab.guru](https://crontab.guru/) to help create cron schedules.

### Post Selection

By default, the bot:
- Fetches the **top posts from the last 24 hours**
- Filters posts to only those with **10+ upvotes** (configurable)
- Randomly selects one post from the filtered list

You can modify the selection strategy in [upvote_reddit.py](upvote_reddit.py#L84):

```python
# Change 'day' to 'week', 'month', 'year', or 'all'
posts = list(subreddit.top(time_filter='day', limit=50))

# Change minimum score threshold
min_score = 10  # Only upvote posts with 10+ upvotes
```

To change the default minimum score globally, set the `MIN_SCORE` environment variable or add it to your GitHub secrets.

## How It Works

**Automatic Daily Mode:**
1. The GitHub Action triggers daily at the scheduled time
2. The script authenticates with Reddit using your credentials
3. It randomly selects one subreddit from your list
4. It fetches the hot posts from that subreddit
5. It randomly selects one post and upvotes it
6. It logs details about the upvoted post

**Manual Mode:**
1. You trigger the workflow from GitHub Actions
2. You specify how many posts to upvote (1-N)
3. For each post, the bot randomly selects a subreddit and post
4. All upvotes are processed and a summary is displayed

## Security Notes

- Never commit your Reddit credentials to the repository
- Use GitHub Secrets to store sensitive information
- The bot only performs upvotes, no other actions
- Consider using a dedicated Reddit account for bot activities

## Troubleshooting

**Authentication Failed**
- Double-check your Reddit credentials in GitHub Secrets
- Ensure your Reddit account doesn't have 2FA enabled, or use an app-specific password
- Verify your Reddit app client_id and client_secret are correct

**No Posts Found**
- Check that the subreddit names are spelled correctly
- Ensure the subreddits are public and have recent posts
- Try different subreddits

**Workflow Not Running**
- Check that GitHub Actions is enabled in your repository settings
- Ensure the workflow file is in the correct location: `.github/workflows/`
- Check the Actions tab for any error messages

## License

This project is provided as-is for educational purposes. Use responsibly and in accordance with Reddit's Terms of Service and API rules.
