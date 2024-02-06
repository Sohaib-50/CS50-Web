from django.test import TestCase

from .helpers import get_quill
from .models import Article, User


# Create your tests here.
class TestTehreer(TestCase):

    def setUp(self):

        alex = User.objects.create_user(username='alex@foo.com', email='alex@foo.com', password='alex', first_name='Alex', last_name='Ander')
        bob = User.objects.create_user(username='bob@bar.com', email='bob@bar.com', password='bob', first_name='Bob', last_name='TheBuilder')
        carey = User.objects.create_user(username='carey@baz.com', email='carey@baz.com', password='carey', first_name='Carey', last_name='Anderson')
        self.users = {'alex': alex, 'bob': bob, 'carey': carey}

        # Create articles
        article0 = Article.objects.create(title='Article 0', content=get_quill('Article 0 content'), author=alex)
        article1 = Article.objects.create(title='Article 1', content=get_quill('Article 1 content'), author=alex)
        article2 = Article.objects.create(title='Article 2', content=get_quill('Article 2 content'), author=bob)
        article3 = Article.objects.create(title='Article 3', content=get_quill('Article 3 content'), author=carey)
        self.articles = {'article0': article0, 'article1': article1, 'article2': article2, 'article3': article3}
    
    def test_liking(self):

        self.assertEqual(self.articles['article0'].likers.count(), 0)  # check 0 likes initially
        
        # make a user, Bob like article 0
        self.articles['article0'].like(self.users['bob'])
        self.assertEqual(self.articles['article0'].likers.count(), 1)  # check 1 like
        self.assertIn(self.users['bob'], self.articles['article0'].likers.all())  # check bob is counted as liker

        # check multiple likes not being added
        self.articles['article0'].like(self.users['bob'])
        self.assertEqual(self.articles['article0'].likers.count(), 1)

        # make another user, Carey, like the same article
        self.articles['article0'].like(self.users['carey'])
        self.assertEqual(self.articles['article0'].likers.count(), 2)
        expected_likers = [self.users['bob'], self.users['carey']]
        actual_likers = list(self.articles['article0'].likers.all())
        self.assertListEqual(expected_likers, actual_likers)

        # make Bob unlike article 0
        self.articles['article0'].unlike(self.users['bob'])
        self.assertEqual(self.articles['article0'].likers.count(), 1)
        self.assertNotIn(self.users['bob'], self.articles['article0'].likers.all())
        self.assertNotIn(self.users['alex'], self.articles['article0'].likers.all())
        self.assertIn(self.users['carey'], self.articles['article0'].likers.all())


    def test_likes_activitylogging(self):

        def test_updates(user, article, performer, count):
            updates = user.get_updates()
            latest_update = updates.latest('timestamp')
            self.assertEqual(updates.filter(action_type="like").count(), count)
            self.assertEqual(latest_update.action_type, "like")
            self.assertEqual(latest_update.performer, performer)
            self.assertEqual(latest_update.target_article, article)
            self.assertEqual(latest_update.target_user, user)

        alex = self.users['alex']
        bob = self.users['bob']
        carey = self.users['carey']
        alex_article = self.articles['article0']

        self.assertEqual(alex.get_updates().count(), 0)
        
        # make Bob like article 0
        alex_article.like(bob)
        test_updates(alex, alex_article, bob, 1)

        # make Carey, like the same article
        alex_article.like(carey)
        test_updates(alex, alex_article, carey, 2)

        # check multiple likes not being added
        alex_article.like(bob)
        test_updates(alex, alex_article, bob, 2)

        # make Bob unlike article 0
        alex_article.unlike(bob)
        test_updates(alex, alex_article, carey, 1)
        

    def test_commenting(self):

        article = self.articles['article0']
        alex = self.users['alex']
        bob = self.users['bob']
        carey = self.users['carey']

        # check 0 comments initially
        self.assertEqual(article.comments.count(), 0)

        # make a comment
        comment0 = article.add_comment(alex, 'Comment 0')
        self.assertEqual(article.comments.count(), 1)
        self.assertEqual(comment0.author, alex)
        self.assertEqual(comment0.content, 'Comment 0')
        self.assertEqual(comment0.article, article)

        # make another comment
        comment1 = article.add_comment(bob, 'Comment 1')
        self.assertEqual(article.comments.count(), 2)
        self.assertEqual(comment1.author, bob)
        self.assertEqual(comment1.content, 'Comment 1')
        self.assertEqual(comment1.article, article)


        # check ordering
        comments = article.comments.all()
        self.assertEqual(comments[0], comment1)
        self.assertEqual(comments[1], comment0)

        # remove first comment
        article.remove_comment(comment0)
        self.assertEqual(article.comments.count(), 1)
        

    def test_comments_activitylogging(self):
        def test_updates(user, article, performer, count):
            updates = user.get_updates()
            latest_update = updates.latest('timestamp')
            self.assertEqual(updates.filter(action_type="comment").count(), count)  # check count of comment updates
            self.assertEqual(latest_update.action_type, "comment")  # make sure latest update is a comment
            self.assertEqual(latest_update.performer, performer)  # check latest update is by expected performer
            self.assertEqual(latest_update.target_article, article)  # check latest update is on the expected article
            self.assertEqual(latest_update.target_user, user)  # check latest update is for the expected user

        alex = self.users['alex']
        bob = self.users['bob']
        carey = self.users['carey']
        alex_article = self.articles['article0']

        # check no updates initially
        self.assertEqual(alex.get_updates().count(), 0)

        # make a comment
        comment0 = alex_article.add_comment(bob, 'Comment 0')
        test_updates(alex, alex_article, bob, 1)

        # make another comment
        comment1 = alex_article.add_comment(carey, 'Comment 1')
        test_updates(alex, alex_article, carey, 2)

        # remove first comment
        alex_article.remove_comment(comment0)
        test_updates(alex, alex_article, carey, 1)


    def test_following(self):
        
        alex = self.users['alex']
        bob = self.users['bob']
        carey = self.users['carey']

        # check 0 followers initially
        self.assertEqual(alex.followers.count(), 0)

        # make Bob follow Alex
        bob.follow(alex)
        self.assertEqual(alex.followers.count(), 1)
        self.assertIn(bob, alex.followers.all())

        # check multiple follows not being added
        bob.follow(alex)
        self.assertEqual(alex.followers.count(), 1)

        # make Carey follow Alex
        carey.follow(alex)
        self.assertEqual(alex.followers.count(), 2)
        expected_followers = [bob, carey]
        actual_followers = list(alex.followers.all())
        self.assertListEqual(expected_followers, actual_followers)

        # make Bob unfollow Alex
        bob.unfollow(alex)
        self.assertEqual(alex.followers.count(), 1)
        self.assertNotIn(bob, alex.followers.all())
        self.assertNotIn(alex, bob.followers.all())
        self.assertIn(carey, alex.followers.all())
        
        # make Carey unfollow Alex
        carey.unfollow(alex)
        self.assertEqual(alex.followers.count(), 0)
        self.assertNotIn(carey, alex.followers.all())
        self.assertNotIn(alex, carey.followers.all())
        self.assertNotIn(bob, alex.followers.all())

    
    def test_following_activitylogging(self):

        def test_updates(user, performer, count):
            updates = user.get_updates()
            latest_update = updates.latest('timestamp')
            self.assertEqual(updates.filter(action_type="follow").count(), count)
            self.assertEqual(latest_update.action_type, "follow")
            self.assertEqual(latest_update.performer, performer)
            self.assertEqual(latest_update.target_user, user)

        alex = self.users['alex']
        bob = self.users['bob']
        carey = self.users['carey']

        # check no updates initially
        self.assertEqual(alex.get_updates().count(), 0)

        # make Bob follow Alex
        bob.follow(alex)
        test_updates(alex, bob, 1)

        # make Carey follow Alex
        carey.follow(alex)
        test_updates(alex, carey, 2)
        
        # check multiple follow logs not being added
        bob.follow(alex)
        test_updates(alex, bob, 2)

        alex_updates = alex.get_updates().filter(action_type="follow")
        follow_performers = [update.performer for update in alex_updates]
        self.assertIn(bob, follow_performers)
        self.assertIn(carey, follow_performers)

        # make Bob unfollow Alex
        bob.unfollow(alex)
        test_updates(alex, carey, 1)

        # make Carey unfollow Alex
        carey.unfollow(alex)
        self.assertEqual(alex.get_updates().count(), 0)

        

