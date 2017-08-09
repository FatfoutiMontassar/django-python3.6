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
    LIKED = 'L'
    LOVED = 'O'
    WISHED = 'W'
    NOTIFICATION_TYPES = (
        (LIKED, 'Liked'),
        (LOVED, 'Loved'),
        (WISHED, 'Wished'),
        )

    _LIKED_TEMPLATE = '<a href="/messenger/{0}/">{1}</a> liked your product: <a href="/shop/product_details/{2}/">{3}</a>'  # noqa: E501
    _LOVED_TEMPLATE = '<a href="/messenger/{0}/">{1}</a> loved your product: <a href="/shop/product_details/{2}/">{3}</a>'  # noqa: E501
    _WISHED_TEMPLATE = '<a href="/messenger/{0}/">{1}</a> wished your product: <a href="/shop/product_details/{2}/">{3}</a>'  # noqa: E501

    from_user = models.ForeignKey(User, related_name='+')
    to_user = models.ForeignKey(User, related_name='+')
    date = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(max_length=1,choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    product = models.ForeignKey('shop.Product', null=True,related_name="related_product")

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ('-date',)

    def __str__(self):
        if self.notification_type == self.LIKED:
            return self._LIKED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.username),
                self.product.pk,
                escape(self.get_summary(self.product.name))
                )
        elif self.notification_type == self.LOVED:
            return self._LOVED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.username),
                self.product.pk,
                escape(self.get_summary(self.product.name))
                )
        elif self.notification_type == self.WISHED:
            return self._WISHED_TEMPLATE.format(
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
