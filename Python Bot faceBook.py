import requests
import csv

# Replace with your own values
app_id = "671111107901676"                  //add your app id
app_secret = "f5d55***********************" //add your app secret 
user_access_token = ""                      //add your access token
group_id = "42*************"                //add your group id 

def get_group_data():
    # Get an app access token
    app_access_token = f"{app_id}|{app_secret}"

    # Get the group name and posts
    fields = "posts.limit(100){message,comments.limit(25){message,from,created_time,like_count}},name"
    url = f"https://graph.facebook.com/v12.0/{group_id}?fields={fields}&access_token={app_access_token}"
    response = requests.get(url)
    data = response.json()

    return data

def main():
    group_data = get_group_data()

    if "error" in group_data:
        print("Error:", group_data["error"]["message"])
        return

    group_name = group_data.get("name", "Unknown Group")
    posts = group_data.get("posts", {}).get("data", [])

    if not posts:
        print("No posts found in the group.")
        return

    scraped_data = []

    for post in posts:
        post_text = post.get("message", "")
        comments = post.get("comments", {}).get("data", [])
        num_comments = len(comments)
        num_likes = post.get("like_count", 0)
        username = post.get("from", {}).get("name", "")

        data_entry = {
            "Post Text": post_text,
            "Number of Comments": num_comments,
            "Number of Likes": num_likes,
            "Username": username
        }

        scraped_data.append(data_entry)

        for comment in comments:
            comment_text = comment.get("message", "")
            comment_username = comment.get("from", {}).get("name", "")
            comment_entry = {
                "Comment": comment_text,
                "Username": comment_username
            }
            scraped_data.append(comment_entry)

    csv_file = f"{group_name}_data.csv"

    with open(csv_file, "w", newline="", encoding="utf-8") as file:
        fieldnames = scraped_data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(scraped_data)

if __name__ == "__main__":
    main()
