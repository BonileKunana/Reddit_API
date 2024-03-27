-This is a makeshift Reddit API

It has the following functionality:
+ A user is able to create posts as well as update and delete those posts, using post id.
+ A user is able to upvote (like) or downvote (dislike) those posts, using post id.
+ A user is able to comment on posts, using post id.
+ a user is able to view all the comments for a post
+ A user is able to upvote or downvote comments, using comment id.
+ A user is able to query all the posts that they have upvoted or downvoted, using their username
+ A user is able to see all the posts created by a specific user by using their username.
+ A user is able to view any post showing you all the comments for that post as well as how many people upvoted or downvoted the post.

  
How to run the API:
1. Run the Reddit_API file (server)
2. Run the Test_Reddit_API file (client)
3.  *Please note it important to run the server before you run the client*
   
 The results will be shown on both the client side and server side:
+ The test file was designed in such a way that it first test for positive test cases(for examle, query a post that exists or delete a post that exist)
+ And then it tests for negetive test cases (for example comment on /like a post that does not exist)
