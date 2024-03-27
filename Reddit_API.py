from flask import Flask, request, jsonify


app = Flask(__name__)

# Data structures to store posts, comments, and user information
posts = []
comments = {}
users = {}

@app.route('/post', methods=['POST'])
def create_post():
    """
    This method creates a new post

    Args:
        none

    Returns:
        str: success 
    """
    data = request.json
    post_id = len(posts) + 1
    post = {
        'id': post_id,
        'title': data['title'],
        'content': data['content'],
        'author': data['author'],
        'upvotes': 0,
        'downvotes': 0,
        'comments': []
    }
    posts.append(post)
    return 'success'

@app.route('/post/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """
    This method updates post

    Args:
        post_id(str): identifier for each post

    Returns:
        str: feedback(success/not found)

    """
    data = request.json
    for post in posts:
        if post['id'] == post_id:
            post['title'] = data['title']
            post['content'] = data['content']
            return 'success',200
    return 'not found', 404

