# Reddit API Task

A Python script to fetch posts from Reddit using PRAW (Python Reddit API Wrapper).

## Required Dependencies

1. **Install PRAW**:
    ```bash
   pip install praw
2. **Install Pandas**:
    ```bash
   pip install pandas
## Versions used

- Python 3.12.6
- PRAW 7.8.1
- pandas 2.2.3

## Setup

A `.json` file is needed in the following format to provide all the authorization data:
```json
{
    "client_id": "your_client_id",
    "client_secret": "your_secret_key",
    "user_agent": "your_app_name",
    "username": "your_username",
    "password": "your_password"
}
```

`JSON_FILE` variable in the script should be changed to the name of the created `.json` file.

## The Task
I tried to optimize the tool's functionality in order to ensure smoother and easier user's experience.
The current task's requirements where to retrieve the latest 5 posts from a given subreddit but I wanted 
to make it easier for the user to fetch data from any subreddit, with any listing type and any limit.
That's why the main method only calls `fetch_posts()` with the following parameters:
- `subreddit_name`: The name of the subreddit.
- `listing_type`: One of the allowed listing types ('hot','new', 'rising', 'top', 'controversial').
- `post_limit`: The number of the wanted posts.

## Usage
Write the desired `subreddit_name`, `listing_type` and `post_limit` as arguments in `fetch_posts()` and run the main method. All fetched data will appear in the terminal.

### Error Handling
- `Missing required keys`: The `.json` file is missing one or more required keys (`client_id`, `client_secret`, `user_agent`, `username`, `password`).
- `File not found`: Given `.json` file was not found.
- `Invalid JSON format`: The `.json` file does not contain valid JSON.
- `Invalid listing type`: The provided listing type is not one of the allowed listing types (`hot`, `new`, `rising`, `top`, `controversial`).
- `Connection error`: Issues connecting to the Reddit API.
- `Reddit API exception`: Errors returned by the Reddit API (rate limits or invalid requests).
- `Unexpected error`: Any other unforeseen errors during execution.

#### Ioannis Bouritis