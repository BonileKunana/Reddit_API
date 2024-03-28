from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
jwt = JWTManager(app)

# Username and password
users = {'test_user': 'password'}

# Data structures to store posts, comments, and user information
posts = []
comments = {}

@app.route('/login',methods=['POST'])
def login():
    """
    Authenticate users and generate JWT token upon successful login.
    """
    username = request.json.get('username')
    password = request.json.get('password')
    print(username)
    print(password)
    if username in users and users[username] == password:
        access_token = create_access_token(identity=username)
        return 'success', 200
    return 'Invalid username or password', 404

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

    # Perform input validation here
    # Example: Ensure 'title', 'content', and 'author' fields are present
    if 'title' not in data or 'content' not in data or 'author' not in data:
        return jsonify({'message': 'Missing required fields'}), 400

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


@app.route('/post/<int:post_id>/vote', methods=['POST'])
def upvote_or_downvote_post(post_id):
    """
    This method upvote or downvote a post

    Args:
      post_id(str): identifier for each post

    Returns:
        str: feedback(success/not found)
    """
    data = request.json
    vote = data.get('vote')  # 'up' or 'down'
    for post in posts:
        if post['id'] == post_id:
            if vote == 'up':
                post['upvotes'] += 1
            elif vote == 'down':
                post['downvotes'] += 1
            return 'success', 200
    return 'not found', 404

@app.route('/post/<int:post_id>/comment', methods=['POST'])
def comment_on_post(post_id):
    """
    This method add comment to a post

    Args:
      post_id(str): identifier for each post

    Returns:
        str: feedback(success/not found)    
    """
    data = request.json
    comment_id = 1
    comment = {
        'id': comment_id,
        'author': data['author'],
        'content': data['content'],
        'upvotes': 0,
        'downvotes': 0
    }
    for post in posts:
        if post['id'] == post_id:
            post['comments'].append(comment)
            return 'success', 200
    return 'not found', 404

@app.route('/comment/<int:comment_id>/vote=[]', methods=['POST'])
def upvote_or_downvote_comment(comment_id):
    """
    This method upvote or downvote a comment

    Args:
      comment_id(str): identifier for each comment

    Returns:
        str: feedback(success/not found)
    """

    data = request.json
    vote = data.get('vote')  # 'up' or 'down'
    for post in posts:
        for comment in post['comments']:
            if comment['id'] == comment_id:
                if vote == 'up':
                    comment['upvotes'] += 1
                elif vote == 'down':
                    comment['downvotes'] += 1
                return 'success', 200
    return 'not found', 404

@app.route('/post/<int:post_id>/postview', methods=['GET'])
def view_any_post(post_id):
    """
    This method view any post along with upvotes/downvotes counts 

    Args:
      post_id(str): identifier for each post

    Returns:
       tuple/ str: post with (upvotes/downvotes)/feedback(not found)  

    """
    post = next((post for post in posts if post['id'] == post_id), None)
    if post:
        post_comments = post['comments']
        total_upvotes = sum(comment['upvotes'] for comment in post_comments)
        total_downvotes = sum(comment['downvotes'] for comment in post_comments)
        return jsonify({
            'post': post,
            'comments': post_comments,
            'upvotes': total_upvotes,
            'downvotes': total_downvotes
        })
    return 'not found', 404

@app.route('/user/<username>/posts', methods=['GET'])
def get_user_posts(username):
    """
    This method query all posts created by a specific user
    
     Args:
      username(str): name of a user

    Returns:
        str: array containing all the post for a specific user 
    """
    user_posts = [post for post in posts if post['author'] == username]
    #print(user_posts)
    if(len(user_posts)>0):
        return jsonify(user_posts)
    return 'not found', 404

@app.route('/user/<username>/votes', methods=['GET'])
def get_voted_posts_by_user(username):
    """
    
    This method query all posts upvoted or downvoted by a specific user
    
    Args:
      username(str): name of a user

    Returns:
        []/str: array of all posts upvoted or downvoted by a specific user/  feedback(not found) 
    
    """
    test_user = 'test_user'
    user_votes = [post for post in posts if username in post.get('upvoted_by', test_user) or username in post.get('downvoted_by', test_user)]
    if(len(user_votes)>0):
        return jsonify(user_votes)
    return 'not found', 404

@app.route('/post/<int:post_id>/comments', methods=['GET'])
def get_post_comments(post_id):
    """
    This method view all comments for a post 
   
     Args:
      post_id(str): identifier for each post

    Returns:
        str: comments for a post / feedback(success/not found)

    """
    for post in posts:
        if post['id'] == post_id:
            return jsonify(post['comments'])
    return 'not found', 404

@app.route('/post/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    This method delete a post

     Args:
      post_id(str): identifier for each post

    Returns:
        str: feedback(success/not found)
    """
    for post in posts:
        if post['id'] == post_id:
            posts.remove(post)
            return 'success'
    return 'not found', 404


if __name__ == '__main__':
    print(" * Server is listening!")
    app.run(debug=True)
