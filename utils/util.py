import requests

# Returns amount of bytes url has (presumably image)
# Returns 1 as fallback
def num_bytes_from_url(image_url) -> int:
    if not image_url:
        return 1

    try:
        return int(requests.head(image_url).headers['Content-Length'])
    except:
        return 1

def get_total_sub(subreddit_name) -> int:
    return int(requests.get(f"https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit_name}&metadata=true&size=0").json()['metadata']['total_results'])