import os
import json

file_path_following = os.environ["INFO_DIR"] + "/connections/followers_and_following/following.json"
file_path_followers = os.environ["INFO_DIR"] + "/connections/followers_and_following/followers_1.json"
file_path_pending = os.environ["INFO_DIR"] + "/connections/followers_and_following/follow_requests_you've_received.json"

def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def find_following(data):
    following = []
    following_raw = data["relationships_following"]
    for i in range(0, len(following_raw)):
        following.append(following_raw[i]['string_list_data'][0]['value'])
    return following

def find_followers(data):
    followers = []
    for i in range(0, len(data)):
        followers.append(data[i]['string_list_data'][0]['value'])
    return followers

def find_difference(following, followers, pending):
    following_set = set(following)
    followers_set = set(followers)
    pending_set = set(pending)
    difference_following_followers = following_set.difference(followers_set) # I follow, no follow back
    difference_following_pending = difference_following_followers.difference(pending_set) # No follow, no pending
    return difference_following_pending

def save_difference(difference):
    with open("difference.txt", "w") as file:
        file.write("Users who I follow but do not follow me back and have not accepted my follow request:\n\n")
        for user in difference:
            file.write(user + "\n")

def find_pending_requests(data):
    pending_requests = []
    pending = data["relationships_follow_requests_received"]
    for i in range(0, len(pending)):
        pending_requests.append(pending[i]['string_list_data'][0]['value'])
    return pending_requests

if __name__ == "__main__":
    data_following = load_data(file_path_following)
    following = find_following(data_following)
    data_followers = load_data(file_path_followers)
    followers = find_followers(data_followers)
    data_pending = load_data(file_path_pending)
    pending = find_pending_requests(data_pending)
    diff = find_difference(following, followers, pending)
    save_difference(diff)
    

    