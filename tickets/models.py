# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


def validate_fer_email(address):
    if re.match(".*@fer\.hr", address) is None:
        raise ValidationError(
            _('Unesite valjanu FER e-mail adresu, oblika "@fer.hr".')
            )


class Student(models.Model):
    code = models.CharField('jmbag', max_length=30, unique=True)
    first_name = models.CharField('ime', max_length=30, blank=True)
    last_name = models.CharField('prezime', max_length=30, blank=True)
    email = models.EmailField('e-mail', max_length=75, blank=True, validators=[validate_fer_email, ])

    @property
    def ticket_or_none(self):
        try:
            return self.ticket
        except ObjectDoesNotExist:
            return None

    class Meta:
        ordering = ['code']
        verbose_name = 'brucoš'
        verbose_name_plural = 'brucoši'

    def __unicode__(self):
        return u'%s %s %s' % (self.first_name, self.last_name, self.code)


class Ticket(models.Model):
    number = models.CharField('br. karte', max_length=30, unique=True)
    student = models.OneToOneField(Student, related_name='ticket')
    creation_time = models.DateTimeField('vrijeme prodaje', auto_now_add=True)

    class Meta:
        ordering = ['-creation_time']
        verbose_name = 'karta'
        verbose_name_plural = 'karte'

    def __unicode__(self):
        return u'Karta za %s' % unicode(self.student)


@receiver(pre_save, sender=Ticket)
def exam_gen_id(sender, instance, **kwargs):
    if instance.number:    # ako je update
        return
    qs = Ticket.objects.all().order_by('-number')
    if qs.exists():
        max_num = qs[0].number
        num = int(max_num.split('B')[1]) + 1
    else:
        num = 1
    instance.number = 'B%03d' % num
