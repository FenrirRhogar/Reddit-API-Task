import praw
import json
import pandas as pd
from prawcore import PrawcoreException
from praw.exceptions import RedditAPIException

JSON_FILE = "config.json"                                                                       # Change to your .json file name
ALLOWED_LISTING_TYPES = ['hot','new', 'rising', 'top', 'controversial']                         # All the allowed listing types


def create_reddit_object(json_file):
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)                                                                 # Loads api and credential data

        required_keys = ['client_id', 'client_secret', 'user_agent', 'username', 'password']
        if not all(key in data for key in required_keys):                                       # Checks if all required keys are present in the .json file
            missing = [key for key in required_keys if key not in data]
            raise KeyError(f"Missing required keys in config: {missing}")

        return praw.Reddit(
            client_id=data['client_id'],
            client_secret=data['client_secret'],
            user_agent=data['user_agent'],
            username=data['username'],
            password=data['password']
        )

    except FileNotFoundError:                                                                       # File not found
        print(f"Error: Config file '{json_file}' not found.")
        return None
    except json.JSONDecodeError:                                                                    # Invalid JSON format
        print(f"Error: Invalid JSON format in '{json_file}'.")
        return None
    except KeyError as e:                                                                           # Missing keys in JSON file
        print(f"Configuration error: {str(e)}")
        return None


pd.set_option('display.max_colwidth', None)                                                         # Options set to avoid cropping
pd.set_option('display.max_columns', None)                                                          # of fetched data


def fetch_posts(subreddit_name, listing_type, post_limit):
    try:
        if listing_type not in ALLOWED_LISTING_TYPES:                                               # Checks if the listing type is valid
            raise ValueError(f"Invalid listing type '{listing_type}'. Allowed allowed listing types: {ALLOWED_LISTING_TYPES}")

        reddit = create_reddit_object(JSON_FILE)                                                    # Creates our Reddit object if authentication succeeded
        if not reddit:
            return None

        subreddit = reddit.subreddit(subreddit_name)                                                # Get the subreddit object

        listing_method = getattr(subreddit, listing_type)                                           # Get subreddit's attribute based on the listing type
        posts = listing_method(limit=post_limit)                                                    # Get the posts based on the listing type and limit

        posts_data = []
        for post in posts:                                                                          # Extracts the required data from the posts
            posts_data.append({
                'Title': post.title,
                'Author': post.author,
                'Upvote Count': post.ups
            })

        return pd.DataFrame(posts_data)                                                             # Returns fetched data in a pandas DataFrame

    except ValueError as e:                                                                         # Invalid listing type
        print(f"Input error: {str(e)}")
        return None
    except PrawcoreException as e:                                                                  # Connection error
        print(f"Reddit API connection error: {str(e)}")
        return None
    except RedditAPIException as e:                                                                 # Reddit API exception
        print(f"Reddit API exception: {', '.join([err.message for err in e.items])}")
        return None
    except Exception as e:                                                                          # Unexpected error
        print(f"Unexpected error: {str(e)}")
        return None


if __name__ == "__main__":
    df = fetch_posts("cats", "new", 5)                              # Fetches 5 newest posts from the subreddit 'cats' (can be easily changed)

    if df is not None and not df.empty:                                                             # Checks if the data was fetched successfully
        print("\nSuccessfully fetched posts:")
        print(df.to_string(index=False))                                                            # Prints the fetched data
    else:
        print("Failed to fetch posts.")