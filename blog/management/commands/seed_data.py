import datetime
from django.core.management.base import BaseCommand
from blog.models import Post, Comment

class Command(BaseCommand):
    help = 'Seeds the database with initial blog posts and comments'

    def handle(self, *args, **options):
        self.stdout.write('Deleting old data...')
        Post.objects.all().delete()
        Comment.objects.all().delete()

        self.stdout.write('Creating new data...')

        # Create Posts
        post1 = Post.objects.create(title='台南新化小白貓', text='這是一隻可愛的小白貓')
        post2 = Post.objects.create(title='新北板橋黑輪', text='這是新北板橋的美食')
        post3 = Post.objects.create(title='高雄左營小乖', text='這是高雄左營的小乖')

        # Create Comments
        comment_text = '檢查費用明細'
        image_url = 'https://kcsaa.org.tw/images/KCSAA/receipt/2009/2009-04-2.jpg'
        
        posts = [post1, post2, post3]
        for post in posts:
            # Text comment
            Comment.objects.create(
                post=post,
                comment_date=datetime.date(2023, 8, 9),
                comment_type='text',
                text='這是一則純文字的留言。'
            )
            # Image comment
            Comment.objects.create(
                post=post,
                comment_date=datetime.date(2023, 8, 8),
                comment_type='image',
                image_url='https://kcsaa.org.tw/images/KCSAA/receipt/2009/2009-04-2.jpg'
            )
            # Another text comment
            Comment.objects.create(
                post=post,
                comment_date=datetime.date(2023, 8, 7),
                comment_type='text',
                text='這是另一則純文字的測試留言。'
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))
