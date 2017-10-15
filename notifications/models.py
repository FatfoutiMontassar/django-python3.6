from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape
import shop

# Create your models here.

@python_2_unicode_compatible
class Notification(models.Model):
    
    NORMAL      = 'normal'
    SMILE       = 'smile'
    LOVE        = 'love'
    WISH        = 'wish'

    LIKE        = 'like'
    DISLIKE     = 'dislike'

    CHOICES = (
        (NORMAL, NORMAL),
        (SMILE, SMILE),
        (LOVE, LOVE),
        (WISH, WISH),
        (LIKE, LIKE),
        (DISLIKE, DISLIKE),
    )

    _NORMAL_TEMPLATE  = '<a href="/messenger/{0}/">{1}</a> reacted to your product: <a href="/shop/product_details/{2}/">{3}</a>'  # noqa: E501
    _SMILE_TEMPLATE   = '<a href="/messenger/{0}/">{1}</a> reacted to your product: <a href="/shop/product_details/{2}/">{3}</a>'  # noqa: E501
    _LOVE_TEMPLATE    = '<a href="/messenger/{0}/">{1}</a> reacted to your product: <a href="/shop/product_details/{2}/">{3}</a>'  # noqa: E501
    _WISH_TEMPLATE    = '<a href="/messenger/{0}/">{1}</a> reacted to your product: <a href="/shop/product_details/{2}/">{3}</a>'  # noqa: E501


    _LIKE_TEMPLATE    = "none" 
    _DISLIKE_TEMPLATE = "none"

    from_user         = models.ForeignKey(User, related_name='+')
    to_user           = models.ForeignKey(User, related_name='+')
    date              = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(max_length=1,choices=CHOICES)
    is_read           = models.BooleanField(default=False)
    product           = models.ForeignKey('shop.Product', null=True,related_name="related_product")

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ('-date',)

    def __str__(self):
        if self.notification_type == self.NORMAL:
            return self._NORMAL_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.username),
                self.product.pk,
                escape(self.get_summary(self.product.name))
                )
        elif self.notification_type == self.SMILE:
            return self._SMILE_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.username),
                self.product.pk,
                escape(self.get_summary(self.product.name))
                )
        elif self.notification_type == self.LOVE:
            return self._LOVE_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.username),
                self.product.pk,
                escape(self.get_summary(self.product.name))
                )
        elif self.notification_type == self.WISH:
            return self._WISH_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.username),
                self.product.pk,
                escape(self.get_summary(self.product.name))
                )
        else:
            return 'Ooops! Something went wrong.'

    def get_summary(self, value):
        summary_size = 50
        if len(value) > summary_size:
            return '{0}...'.format(value[:summary_size])

        else:
            return value
