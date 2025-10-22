#!/usr/bin/env python3
"""
Reddit Upvote Bot - Daily random post upvoter
Upvotes one random post per day from specified subreddit(s)
"""

import os
import sys
import random
import json
import praw
from datetime import datetime


def load_config():
    """Load configuration from config.json or environment variables"""
    config = {
        'subreddits': [],
        'client_id': os.getenv('REDDIT_CLIENT_ID'),
        'client_secret': os.getenv('REDDIT_CLIENT_SECRET'),
        'username': os.getenv('REDDIT_USERNAME'),
        'password': os.getenv('REDDIT_PASSWORD'),
        'user_agent': os.getenv('REDDIT_USER_AGENT', 'RedditUpvoterBot/1.0'),
        'min_score': int(os.getenv('MIN_SCORE', '10'))
    }

    # Try to load subreddits from config file
    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            file_config = json.load(f)
            config['subreddits'] = file_config.get('subreddits', [])
            config['min_score'] = file_config.get('min_score', config['min_score'])

    # Override with environment variable if present
    if os.getenv('SUBREDDITS'):
        config['subreddits'] = [s.strip() for s in os.getenv('SUBREDDITS').split(',')]

    return config


def validate_config(config):
    """Validate that all required configuration is present"""
    required_fields = ['client_id', 'client_secret', 'username', 'password']
    missing_fields = [field for field in required_fields if not config.get(field)]

    if missing_fields:
        print(f"Error: Missing required configuration: {', '.join(missing_fields)}")
        return False

    if not config['subreddits']:
        print("Error: No subreddits specified. Add them to config.json or SUBREDDITS environment variable")
        return False

    return True


def get_reddit_client(config):
    """Create and return authenticated Reddit client"""
    try:
        reddit = praw.Reddit(
            client_id=config['client_id'],
            client_secret=config['client_secret'],
            username=config['username'],
            password=config['password'],
            user_agent=config['user_agent']
        )

        # Test authentication
        print(f"Authenticated as: {reddit.user.me()}")
        return reddit
    except Exception as e:
        print(f"Error authenticating with Reddit: {e}")
        return None


def get_random_post(reddit, subreddits, limit=50, min_score=10):
    """Get a random post from the specified subreddits with minimum upvotes"""
    # Pick a random subreddit from the list
    subreddit_name = random.choice(subreddits)
    print(f"Selected subreddit: r/{subreddit_name}")

    try:
        subreddit = reddit.subreddit(subreddit_name)

        # Get top posts from the last day (can change to 'hot', 'week', 'month', etc.)
        posts = list(subreddit.top(time_filter='day', limit=limit))

        # Filter posts by minimum score
        popular_posts = [post for post in posts if post.score >= min_score]

        if not popular_posts:
            print(f"No posts with {min_score}+ upvotes found in r/{subreddit_name}")
            print(f"Falling back to hot posts...")
            # Fallback to hot posts if no popular posts found
            posts = list(subreddit.hot(limit=limit))
            popular_posts = [post for post in posts if post.score >= min_score]

            if not popular_posts:
                print(f"No posts found with minimum score. Using any available post.")
                popular_posts = posts if posts else []

        if not popular_posts:
            print(f"No posts found in r/{subreddit_name}")
            return None

        # Pick a random post from popular posts
        post = random.choice(popular_posts)
        print(f"Found {len(popular_posts)} posts with {min_score}+ upvotes")
        return post
    except Exception as e:
        print(f"Error fetching posts from r/{subreddit_name}: {e}")
        return None


def upvote_post(post):
    """Upvote the given post"""
    try:
        post.upvote()
        print(f"\n✓ Successfully upvoted post:")
        print(f"  Title: {post.title}")
        print(f"  Subreddit: r/{post.subreddit.display_name}")
        print(f"  Author: u/{post.author}")
        print(f"  URL: {post.url}")
        print(f"  Score: {post.score}")
        print(f"  Posted: {datetime.fromtimestamp(post.created_utc)}")
        return True
    except Exception as e:
        print(f"Error upvoting post: {e}")
        return False


def main():
    """Main function"""
    print("=" * 60)
    print("Reddit Daily Upvoter Bot")
    print(f"Run time: {datetime.now()}")
    print("=" * 60)

    # Get number of posts to upvote (default to 1)
    try:
        post_count = int(os.getenv('POST_COUNT', '1'))
        if post_count < 1:
            post_count = 1
    except ValueError:
        post_count = 1

    print(f"Posts to upvote: {post_count}")

    # Load and validate configuration
    config = load_config()
    if not validate_config(config):
        sys.exit(1)

    print(f"\nTarget subreddits: {', '.join(config['subreddits'])}")
    print(f"Minimum post score: {config['min_score']} upvotes")

    # Authenticate with Reddit
    reddit = get_reddit_client(config)
    if not reddit:
        sys.exit(1)

    # Upvote multiple posts
    successful_upvotes = 0
    failed_upvotes = 0

    for i in range(post_count):
        print(f"\n{'='*60}")
        print(f"Processing post {i+1} of {post_count}")
        print(f"{'='*60}")

        # Get a random post
        print("\nFetching random post...")
        post = get_random_post(reddit, config['subreddits'], min_score=config['min_score'])
        if not post:
            print("Failed to fetch a post")
            failed_upvotes += 1
            continue

        # Upvote the post
        if upvote_post(post):
            successful_upvotes += 1
        else:
            failed_upvotes += 1

    # Print summary
    print(f"\n{'='*60}")
    print("Summary:")
    print(f"  Total posts processed: {post_count}")
    print(f"  Successful upvotes: {successful_upvotes}")
    print(f"  Failed upvotes: {failed_upvotes}")
    print(f"{'='*60}")

    if successful_upvotes > 0:
        print("\n✓ Task completed!")
        sys.exit(0)
    else:
        print("\n✗ All upvotes failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
