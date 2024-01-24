from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django_quill.fields import QuillField

'''
# schema.sql:
# -- Represent users of the site
# CREATE TABLE IF NOT EXISTS "users" (
# 	"id" INTEGER,
# 	"email" TEXT NOT NULL UNIQUE,
#    "password_hash" TEXT NOT NULL,
# 	"firstname" TEXT NOT NULL,
# 	"lastname" TEXT NOT NULL,
# 	"bio" TEXT,
# 	"pic_url" TEXT,

# 	PRIMARY KEY("id")
# );

# -- Represent articles posted by users
# CREATE TABLE IF NOT EXISTS "articles" (
# 	"id" INTEGER,
# 	"author_id" INTEGER,
#     "title" TEXT NOT NULL,
#     "content" TEXT NOT NULL,
#     "published" NUMERIC NOT NULL DEFAULT CURRENT_TIMESTAMP,

# 	PRIMARY KEY ("id"),
# 	FOREIGN KEY ("author_id") REFERENCES "users"("id")
# );

# -- Represent topics of articles
# CREATE TABLE IF NOT EXISTS "topics" (
#     "id" INTEGER,
#     "name" TEXT NOT NULL,

#     PRIMARY KEY("id")
# );

# -- Represent association between articles and topics
# CREATE TABLE IF NOT EXISTS "articles_topics" (
#     "article_id" INTEGER,
#     "topic_id" INTEGER,

#     FOREIGN KEY ("article_id") REFERENCES "articles"("id"),
#     FOREIGN KEY ("topic_id") REFERENCES "topics"("id")
# );

# -- Represent article likes by users
# CREATE TABLE IF NOT EXISTS "likes" (
# 	"article_id" INTEGER,
# 	"user_id" INTEGER,

# 	FOREIGN KEY ("article_id") REFERENCES "articles" ("id"),
# 	FOREIGN KEY ("user_id") REFERENCES "users"("id")
# );

# -- Represent comments on articles by users
# CREATE TABLE IF NOT EXISTS "comments" (
#     "id" INTEGER,
#     "article_id" INTEGER,
#     "author_id" INTEGER,
#     "content" TEXT NOT NULL,
#     "written" NUMERIC NOT NULL DEFAULT CURRENT_TIMESTAMP,

#     PRIMARY KEY("id"),
#     FOREIGN KEY ("article_id") REFERENCES "articles" ("id"),
#     FOREIGN KEY ("author_id") REFERENCES "users"("id")
# );

# -- Represent users following other users
# CREATE TABLE IF NOT EXISTS "follows" (
# 	"user_id" INTEGER,
# 	"following_id" INTEGER,

# 	FOREIGN KEY ("user_id") REFERENCES "users"("id"),
# 	FOREIGN KEY ("following_id") REFERENCES "users"("id")
# );

# -- Represent logs for activities
# CREATE TABLE IF NOT EXISTS "activity_logs" (
#     "action_by_id" INTEGER NOT NULL,
#     "action_for_id" INTEGER,  -- user on whom action is done, eg. followed
#     "action_on_id" INTEGER,  -- post on which action is done, eg. liked
#    	"action_type" TEXT NOT NULL CHECK ("action_type" IN ('comment', 'like', 'follow', 'post')),
#     "timestamp" NUMERIC NOT NULL DEFAULT CURRENT_TIMESTAMP,

#     FOREIGN KEY ("action_by_id") REFERENCES "users"("id"),
#     FOREIGN KEY ("action_for_id") REFERENCES "users"("id"),
#     FOREIGN KEY ("action_on_id") REFERENCES "articles"("id")  -- Assuming posts table
# );
# -- Activity logs will be used for updates to users and a user activity log page
# -- eg:
# -- 	"Alex" liked your post "SQL basics"
# -- 	"Bob" followed you
# -- 	"Carey" commented on your post "SQL basics"
# -- 	"Alex" posted an article "HTML for beginners" (assuming Alex is followed by you)


# -- Create indexes to speed common searches
# CREATE INDEX IF NOT EXISTS "article_by_writer_search" ON "articles" ("author_id");
# CREATE INDEX IF NOT EXISTS "article_by_title_search" ON "articles" ("title");
# CREATE INDEX IF NOT EXISTS "articles_by_topic_search" ON "articles_topics" ("topic_id");
# CREATE INDEX IF NOT EXISTS "topics_for_articles_search" ON "articles_topics" ("article_id");
# CREATE INDEX IF NOT EXISTS "likes_for_article_search" ON "likes" ("article_id");
# CREATE INDEX IF NOT EXISTS "comments_for_article_search" ON "comments" ("article_id");
# CREATE INDEX IF NOT EXISTS "user_follows_search" ON "follows" ("user_id");
# CREATE INDEX IF NOT EXISTS "user_followers_search" ON "follows" ("following_id");
# CREATE INDEX IF NOT EXISTS "user_updates_search" ON "activity_logs" ("action_for_id");
# CREATE INDEX IF NOT EXISTS "article_updates_search" ON "activity_logs" ("action_on_id");


# -- Triggers for updating activity logs on insertions in various tables
# CREATE TRIGGER IF NOT EXISTS "article_posted"
# AFTER INSERT ON "articles"
# BEGIN
#     INSERT INTO "activity_logs" ("action_by_id", "action_on_id", "action_type")
#     VALUES (NEW."author_id", NEW."id", "post");
# END;

# CREATE TRIGGER IF NOT EXISTS "liked"
# AFTER INSERT ON "likes"
# BEGIN
#     INSERT INTO "activity_logs" ("action_by_id", "action_on_id", "action_type")
#     VALUES (NEW."user_id", NEW."article_id", "like");
# END;

# CREATE TRIGGER  IF NOT EXISTS "followed"
# AFTER INSERT ON "follows"
# BEGIN
#     INSERT INTO "activity_logs" ("action_by_id", "action_for_id", "action_type")
#     VALUES (NEW."user_id", NEW."following_id", "follow");
# END;

# CREATE TRIGGER IF NOT EXISTS "commented"
# AFTER INSERT ON "comments"
# BEGIN
#     INSERT INTO "activity_logs" ("action_by_id", "action_on_id", "action_type")
#     VALUES (NEW."author_id", NEW."article_id", "comment");
# END;


# /* Views */

# -- Get number of likes on an article (to show on a list articles pages)
# CREATE VIEW IF NOT EXISTS "article_likes_count" AS
# SELECT
#     "article_id",
#     COUNT(*) AS "likes"
# FROM
#     "likes"
# GROUP BY "article_id";

# -- Get number of comments on an article 
# CREATE VIEW IF NOT EXISTS "article_comments_count" AS
# SELECT
#     "article_id",
#     COUNT(*) AS "comments"
# FROM
#     "comments"
# GROUP BY "article_id";


# -- Details of an article
# CREATE VIEW IF NOT EXISTS "article_details" AS
# SELECT
#     "A"."id" AS "id",
#     "A"."title" AS "title",
#     "A"."content" AS "content",
#     "A"."published" AS "published",
#     "U"."firstname" || ' ' || "U"."lastname" AS "author_name",
#     "U"."pic_url" AS "author_pic_url",
#     GROUP_CONCAT("T"."name") AS "topics",
#     "L"."likes" AS "likes",
#     "C"."comments" AS "comments"
# FROM
#     "articles" AS "A"
#     JOIN "users" AS "U" ON "A"."author_id" = "U"."id"
#     JOIN "articles_topics" AS "AT" ON "A"."id" = "AT"."article_id"
#     JOIN "topics" AS "T" ON "AT"."topic_id" = "T"."id"
#     JOIN "article_likes_count" AS "L" ON "A"."id" = "L"."article_id"
#     JOIN "article_comments_count" AS "C" ON "A"."id" = "C"."article_id"
# GROUP BY "A"."id";

# -- Followers and following count of a user
# CREATE VIEW IF NOT EXISTS "follow_counts" AS
# SELECT
#     "id",
#     (SELECT COUNT(*) FROM "follows" WHERE "following_id" = "id") AS "followers",
#     (SELECT COUNT(*) FROM "follows" WHERE "user_id" = "id") AS "followings"
# FROM
#     "users";

# -- User details
# CREATE VIEW IF NOT EXISTS "user_details" AS
# SELECT
#     "users"."id" AS "id",
#     "users"."email" AS "email",
#     "users"."firstname" || ' ' || "users"."lastname" AS "name",
#     "users"."bio" AS "bio",
#     "users"."pic_url" AS "pic_url",
#     "follow_counts"."followers" AS "followers",
#     "follow_counts"."followings" AS "followings"
# FROM
#     "users"
#     JOIN "follow_counts" ON "users"."id" = "follow_counts"."id";


'''

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pictrues", blank=True, null=True)
    followings = models.ManyToManyField("self", related_name="followers", blank=True, symmetrical=False)
    # fields defined in schema but not here because they are already defined in AbstractUser:
    # email, password, firstname, lastname

    def follow(self, user):
        self.followings.add(user)

        # log follow
        ActivityLog.objects.create(
            performer=self,
            action_type="follow",
            target_user=user
        )

    def unfollow(self, user):
        self.followings.remove(user)

        # unlog associated follow
        ActivityLog.objects.filter(
            performer=self,
            action_type="follow",
            target_user=user
        ).delete()

    def get_updates(self):
        return ActivityLog.objects.filter(
            Q(target_user=self, action_type__in=['like', 'comment', 'follow'])
            |
            Q(performer__in=self.followings.all(), action_type="post")
        )

    # usage examples:
    # Create a user (email, password, firstname, lastname):
    # >>> from django.contrib.auth.models import User 
    # >>> user = User.objects.create_user(email='user@example', password='pass', firstname='first', lastname='last')
    # >>> user.save()
    # updating user (adding bio and pic_url):
    # >>> user = User.objects.get(email='user@example')
    # >>> user.bio = 'bio'
    # >>> user.pic_url = 'pic_url'
    # >>> user.save()
    # logging in:
    # >>> from django.contrib.auth import authenticate, login, logout
    # >>> user = authenticate(request, username='user@example', password='pass')
    # >>> if user is not None:
    # >>>     login(request, user)

class Topic(models.Model):
    name = models.CharField(max_length=80, unique=True, blank=False, null=False)

    def __str__(self):
        return self.name

class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    title = models.CharField(max_length=100, blank=False, null=False)
    content = QuillField()
    published_at = models.DateTimeField(auto_now_add=True)
    topics = models.ManyToManyField(Topic, related_name="articles", blank=True)
    likers = models.ManyToManyField(User, related_name="liked_articles", blank=True)

    def like(self, user):
        self.likers.add(user)

        # log like
        ActivityLog.objects.create(
            performer=user,
            action_type="like",
            target_user=self.author,
            target_article=self
        )

    def unlike(self, user):    
        self.likers.remove(user)
        
        # unlog associated like
        ActivityLog.objects.filter(
            performer=user,
            action_type="like",
            target_user=self.author,
            target_article=self
        ).delete()

    def add_comment(self, user, content):
        comment = Comment.objects.create(article=self, author=user, content=content)

        # log comment
        ActivityLog.objects.create(
            performer=user,
            action_type="comment",
            target_user=self.author,
            target_article=self
        )

        return comment
    

    def remove_comment(self, comment):
        comment_author = comment.author
        comment.delete()

        # unlog associated comment
        ActivityLog.objects.filter(
            performer=comment_author,
            action_type="comment",
            target_user=self.author,
            target_article=self
        ).delete()

    def save(self, *args, **kwargs):

        being_created = self._state.adding == True

        super().save(*args, **kwargs)

        ## activity log update
        # if article is being created, not updated
        if being_created:
            ActivityLog.objects.create(
                performer=self.author,
                action_type="post",
                target_article=self
            )

    class Meta:
        ordering = ["-published_at"]
        indexes = [
            models.Index(fields=["author"]),
            models.Index(fields=["title"])
        ]
         
    
class Comment(models.Model):
    article = models.ForeignKey("Article", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(blank=False, null=False, max_length=500)
    published_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-published_at"]


class ActivityLog(models.Model):
    ACTION_TYPES = (
        ("comment", "comment"),
        ("like", "like"),
        ("follow", "follow"),
        ("post", "post")
    )
    performer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="actions")
    timestamp = models.DateTimeField(auto_now_add=True)
    action_type = models.CharField(choices=ACTION_TYPES, max_length=max(len(x[0]) for x in ACTION_TYPES))
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    target_article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):

        # delete previous logs of same action if present, bec we want to mark only latest one
        ActivityLog.objects.filter(
            performer=self.performer,
            action_type=self.action_type,
            target_user=self.target_user,
            target_article=self.target_article
        ).delete()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.action_type == "post":
            return f"{self.performer} posted an article {self.target_article.title}"
        elif self.action_type == "like":
            return f"{self.performer} liked article '{self.target_article.title}' by {self.target_user}"
        elif self.action_type == "comment":
            return f"{self.performer} commented on {self.target_article.title} by {self.target_user}"
        elif self.action_type == "follow":
            return f"{self.performer} followed {self.target_user}"
    
    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["performer"]),
            models.Index(fields=["target_user"]),
        ]
        


# from django.db.models import Q
# user = request.user

# To get updates of current users followings posting articles:
# ActivityLog.Objects.filter(performer__in=request.user.followings.all(), action_type="post")
    
# to get updates of current user's articles getting likes
# ActivityLog.Objects.filter(action_type='like', target_article__in=user.articles.all())
    
# To get updates of current user's articles getting comments
# ActivityLog.Objects.filter(action_type='comment', target_article__in=user.articles.all())
    
# To get updates of current user getting a follow
# ActivityLog.Objects.filter(target_user=user, action_type="follow")
    
# combine query 2 and 3:
# ActivityLog.Objects.filter(action_type__in=['comment', 'like'], target_article__in=user.articles.all())
    
# combine all
# user_updates = ActivityLog.objects.filter(
#     Q(action_type='like', target_article__in=user.articles.all()) |
#     Q(performer__in=request.user.followings.all(), action_type="post") |
#     Q(action_type='comment', target_article__in=user.articles.all()) |
#     Q(target_user=user, action_type="follow")
#   )

# further refine:
#  user_updates = ActivityLog.objects.filter(
#     Q(performer__in=request.user.followings.all(), action_type="post") |
#     Q(action_type__in=['like', 'comment'], target_article__in=user.articles.all()) |
#     Q(target_user=user, action_type="follow")
#   )
    
# # further refine, final form:
# user_updates = ActivityLog.objects.filter(
#     Q(target_user=user) | Q(target_article__in=user.articles.all())
# )

# Better, best USE THIS!!!
# user_updates = ActivityLog.objects.filter(
#     Q(target_user=user, action_type__in=['like', 'comment', 'follow'])
    # | Q(perfomer__in=user.followings.all(), action_type="post")
# )
