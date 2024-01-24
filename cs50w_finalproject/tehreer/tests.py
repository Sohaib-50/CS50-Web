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


    def test_likes_activitylogs(self):

        def test_updates(user, article, performer, count):
            updates = user.get_updates().distinct()
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

        # remove first comment
        article.remove_comment(comment0)
        self.assertEqual(article.comments.count(), 1)
        
        

