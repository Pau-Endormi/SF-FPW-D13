import datetime
import pytz

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from celery import shared_task

from models import Post


@shared_task
def weekly_notify_subscribers():  # task
    weekly_articles = list()

    # Getting the first and last day of the last week
    current_date = datetime.datetime.now()
    start_of_last_week = current_date - datetime.timedelta(days=7 + current_date.weekday(),
                                                           hours=current_date.hour,
                                                           minutes=current_date.minute,
                                                           seconds=current_date.second,)
    end_of_last_week = start_of_last_week + datetime.timedelta(days=7) - datetime.timedelta(seconds=1)

    print('The current date:', current_date)
    print('The first day of last week:', start_of_last_week)
    print('The last day of last week:', end_of_last_week)

    start_of_last_week = start_of_last_week.replace(tzinfo=pytz.UTC)
    end_of_last_week = end_of_last_week.replace(tzinfo=pytz.UTC)

    # Getting published posts of the last week
    posts = Post.objects.all()
    for post in posts:
        if start_of_last_week <= post.timeCreation <= end_of_last_week:
            weekly_articles.append(post)
            print(post, post.timeCreation)

    if weekly_articles:
        # Getting categories from all posts
        categories_obj = set()

        for post in weekly_articles:
            post_categories = post.postcategory_set.all()
            print(post_categories)
            for obj in post_categories:
                categories_obj.add(obj.category)

        print(categories_obj)

        # Getting subscribers from each category
        for category in categories_obj:
            subscribers = category.subscribers.all()
            print(subscribers)
            for subscriber in subscribers:
                message = f'Еженедельная рассылка статей из категроии «{category.name}», список:'
                message = ' '.join([f'Здравствуй, «{subscriber.username}».', message])

                # Send data to subscriber of the current category
                html_content = render_to_string(
                    'subscription_weekly.html',
                    {
                        'message': message,
                        'weekly_articles': weekly_articles,
                    }
                )
                msg = EmailMultiAlternatives(
                    subject=f'{category.name}',
                    body=message,
                    from_email='',
                    to=[subscriber.email, ],  # emails
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                print("send-----------------*")
