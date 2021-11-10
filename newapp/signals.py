from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post


@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    # Getting categories of post
    categories_obj = set()

    post_categories = instance.postcategory_set.all()
    print(post_categories)
    for obj in post_categories:
        categories_obj.add(obj.category)

    # Getting emails from each category
    for category in categories_obj:
        subscribers = category.subscribers.all()
        print(category, subscribers)
        for subscriber in subscribers:
            if created:
                message = f'Новая статья в твоём любимом разделе «{category.name}»!'
            else:
                message = f'Обновлена статья в твоём любимом разделе «{category.name}»!'
            message = ' '.join([f'Здравствуй, «{subscriber.username}».', message])

            # Send data to subscriber of the current category
            html_content = render_to_string(
                'subscription.html',
                {
                    'post': instance,
                    'message': message,
                }
            )
            msg = EmailMultiAlternatives(
                subject=f'{instance.title}',
                body=message,
                from_email='',
                to=[subscriber.email, ],  # emails
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            print('send msg --------------')
