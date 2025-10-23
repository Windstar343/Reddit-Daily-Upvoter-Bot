<div align="center">
  <img src="DAILYUPVOTER BOTV2.png" alt="Daily Upvoter Bot" width="600">
</div>

# Reddit Daily Upvoter Bot

A GitHub Actions bot that automatically upvotes one random post per day from specified subreddit(s).

## Features

- Upvotes one random post daily from a list of subreddits
- Runs automatically via GitHub Actions (no server needed!)
- Can also run locally on Windows/Mac/Linux
- Can target single or multiple subreddits
- Randomly selects both the subreddit and the post
- Manual trigger option to upvote multiple posts at once
- Only upvotes popular posts (configurable minimum score)
- Provides detailed logging of upvoted posts

## Two Ways to Use This Bot

### Option 1: GitHub Actions (Recommended - Runs Automatically)
Fork this repo and it runs automatically in the cloud every day. **No local setup needed!**

### Option 2: Run Locally on Your Computer
Download and run the Python script manually on your Windows/Mac/Linux machine whenever you want.

---

## Setup Instructions (GitHub Actions)

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

### 3. Enable GitHub Actions

1. Go to the "Actions" tab in your repository
2. If prompted, enable GitHub Actions
3. The workflow will run daily at 6:00 AM UTC (7:00 AM CET / 8:00 AM CEST) and upvote 1 post with at least 100 upvotes

### 4. Manual Execution (Optional)

You can manually trigger the bot anytime to upvote multiple posts:

1. Go to the **Actions** tab in your repository
2. Click on **"Daily Reddit Upvote"** workflow
3. Click the **"Run workflow"** dropdown button
4. Configure your options:
   - **Number of posts to upvote**: Enter how many posts (e.g., `5` for 5 posts)
   - **Minimum upvotes a post must have**: Enter minimum score (e.g., `500` for very popular posts)
5. Click the green **"Run workflow"** button

---

## Setup Instructions (Local/Manual Use)

Want to run it on your own computer instead? Follow these steps:

### 1. Install Python

Download and install Python 3.11 or higher from [python.org](https://www.python.org/downloads/)

### 2. Download the Bot

Clone or download this repository to your computer:
```bash
git clone https://github.com/yourusername/RedditUpvoterStreakholder.git
cd RedditUpvoterStreakholder
```

### 3. Install Dependencies

Open terminal/command prompt in the project folder and run:
```bash
pip install praw
```

### 4. Create Reddit App

Follow the same steps as in **"Setup Instructions (GitHub Actions)"** section above to create a Reddit app.

### 5. Edit config.json

Open [config.json](config.json) and add your subreddits:
```json
{
  "subreddits": [
    "iphone",
    "apple",
    "Steam"
  ],
  "min_score": 100
}
```

### 6. Set Up Environment Variables

**Windows (PowerShell):**
```powershell
$env:REDDIT_CLIENT_ID="your_client_id_here"
$env:REDDIT_CLIENT_SECRET="your_client_secret_here"
$env:REDDIT_USERNAME="your_reddit_username"
$env:REDDIT_PASSWORD="your_reddit_password"
```

**Windows (Command Prompt):**
```cmd
set REDDIT_CLIENT_ID=your_client_id_here
set REDDIT_CLIENT_SECRET=your_client_secret_here
set REDDIT_USERNAME=your_reddit_username
set REDDIT_PASSWORD=your_reddit_password
```

**Mac/Linux:**
```bash
export REDDIT_CLIENT_ID="your_client_id_here"
export REDDIT_CLIENT_SECRET="your_client_secret_here"
export REDDIT_USERNAME="your_reddit_username"
export REDDIT_PASSWORD="your_reddit_password"
```

### 7. Run the Bot

**Upvote 1 post:**
```bash
python upvote_reddit.py
```

**Upvote multiple posts (e.g., 5 posts):**

Windows PowerShell:
```powershell
$env:POST_COUNT=5; python upvote_reddit.py
```

Windows Command Prompt:
```cmd
set POST_COUNT=5 && python upvote_reddit.py
```

Mac/Linux:
```bash
POST_COUNT=5 python upvote_reddit.py
```

**Change minimum upvotes threshold:**
```powershell
# Windows PowerShell - Only upvote posts with 500+ upvotes
$env:MIN_SCORE=500; python upvote_reddit.py
```

---

## Configuration

### Schedule

The bot runs automatically every day at **6:00 AM UTC** (7:00 AM CET / 8:00 AM CEST).

To change when the bot runs, edit the cron schedule in [.github/workflows/daily-upvote.yml](.github/workflows/daily-upvote.yml#L6):

```yaml
schedule:
  - cron: '0 6 * * *'  # Currently set to 6:00 AM UTC (7:00 AM CET)
```

Cron format: `minute hour day month day-of-week`
- `0 6 * * *` = 6:00 AM UTC (7:00 AM CET / 8:00 AM CEST)
- `0 0 * * *` = Midnight UTC every day
- `0 18 * * *` = 6:00 PM UTC every day

Use [crontab.guru](https://crontab.guru/) to help create cron schedules.

### Post Selection

By default, the bot:
- Fetches the **top posts from the last 24 hours**
- Filters posts to only those with **100+ upvotes** (configurable)
- Randomly selects one post from the filtered list

You can modify the selection strategy in [upvote_reddit.py](upvote_reddit.py#L84):

```python
# Change 'day' to 'week', 'month', 'year', or 'all'
posts = list(subreddit.top(time_filter='day', limit=50))

# Change minimum score threshold
min_score = 100  # Only upvote posts with 100+ upvotes
```

To change the default minimum score, edit line 46 in [.github/workflows/daily-upvote.yml](.github/workflows/daily-upvote.yml#L46):
```yaml
MIN_SCORE: ${{ github.event.inputs.min_score || '100' }}  # Change '100' to your preferred default
```

## How It Works

**Automatic Daily Mode:**
1. The GitHub Action triggers daily at 6:00 AM UTC (7:00 AM CET)
2. The script authenticates with Reddit using your credentials
3. It randomly selects one subreddit from your list
4. It fetches the top posts from the last 24 hours
5. It filters posts to those with 100+ upvotes
6. It randomly selects one post and upvotes it
7. It logs details about the upvoted post

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

This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)** - see the [LICENSE](LICENSE) file for details.

**What this means:**

✅ **You CAN:**
- Use this code for FREE for personal use
- Modify and adapt the code
- Share it with others
- Fork it on GitHub

❌ **You CANNOT:**
- **Sell this software or charge money for it**
- **Use it for commercial purposes without permission**
- **Claim this code as your own creation**
- Remove the copyright notice or license

⚠️ **Important:**
- You MUST give credit to **Windstar343** (the original author)
- Any modifications must also include attribution
- Use responsibly and follow Reddit's Terms of Service

**Need commercial use?** Contact Windstar343 for permission.

Copyright (c) 2025 Windstar343. All rights reserved.
