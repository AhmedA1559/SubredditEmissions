import statistics
from math import sqrt
from typing import Tuple

import praw
from tqdm import tqdm

from utils.util import num_bytes_from_url, get_total_sub


class Client:
    def __init__(self, client_id, client_secret):
        self._reddit = praw.Reddit(client_id=client_id, client_secret=client_secret,
                                   user_agent="Ether 19.0")

    def get_subreddit_emissions(self, subreddit_name, posts=None, trends=False) -> Tuple:
        subreddit = self._reddit.subreddit(subreddit_name)

        sub_all_total = get_total_sub(subreddit_name)

        sub_list = self._generate_random_list(subreddit, sub_all_total, posts, trends)

        return self._stat_calc(sub_list, sub_all_total)

    def _generate_random_list(self, subreddit, total_sub, posts, trends):
        generated_list = []

        if not trends and (random_test := subreddit.random()):  # subreddit has random submissions
            generated_list.append(random_test.score * num_bytes_from_url(random_test.url))

            # clamp between 30 and 250 (minus 1 to account for previous random)
            for _ in tqdm(range(int(max(min(total_sub * .05, 250), 30)) - 1 if posts is None else posts)):
                sub = subreddit.random()
                generated_list.append(sub.score * num_bytes_from_url(sub.url))
        else:  # use random trends
            generated_list = subreddit.random_rising()

        return generated_list

    def _stat_calc(self, sub_list, sub_total):
        mean = statistics.mean(sub_list)
        stdev = statistics.stdev(sub_list, xbar=mean) if len(sub_list) > 1 else 0

        return(mean * sub_total * (28 / 1_000_000_000),
              stdev * sub_total * (28 / 1_000_000_000) / sqrt(len(sub_list)))