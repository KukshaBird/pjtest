# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Sum
from django.views.generic import ListView, DetailView, UpdateView
from datetime import datetime, timedelta

# Forms
from .forms import UserFilterForm

# Models
from .models import User


class UserListView(ListView):
    model = User
    paginate_by = 50
    template_name = 'user_list.html'

    def get_queryset(self):
        queryset = User.objects.annotate(total_clicks=Sum('statistic__clicks'),
                                         total_page_views=Sum('statistic__page_views')).order_by('id')
        return queryset


# UpdateView need for resolve 405 status error problem.
class UserDetailView(DetailView, UpdateView):
    template_name = 'user_detail.html'
    model = User
    # we don't need to DELETE method yet.
    http_method_names = ['get', 'post', 'head', 'options', 'trace']
    fields = ['first_name']

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        # Default form data: 7 last days.
        default_form = {'to_date': datetime.today(), 'from_date': datetime.today() - timedelta(days=7)}
        context['form'] = UserFilterForm(default_form)
        if self.request.method == 'POST':
            f = UserFilterForm(self.request.POST)
            if f.is_valid():
                data = f.cleaned_data
                dates = []  # type: list
                clicks = []
                views = []
                dif = data['to_date'] - data['from_date']
                # create datetime range (list)
                days_range = [data['to_date'] - timedelta(days=x) for x in range(dif.days)]
                for day in days_range[::-1]:
                    total_c = (self.object.statistic.select_related('clicks').filter(date=str(day))
                        .aggregate(Sum('clicks'))['clicks__sum'])
                    total_v = (self.object.statistic.select_related('page_views').filter(date=str(day))
                        .aggregate(Sum('page_views'))['page_views__sum'])
                    clicks.append(total_c) if total_c != None else clicks.append(0)
                    views.append(total_v) if total_v != None else views.append(0)
                    dates.append("/".join([str(day.day), str(day.month)]))
                context['data'] = list(map(lambda d, c, v: (d, c, v), dates, clicks, views))  # make zip
                # set latest form data
                context['form'] = UserFilterForm({'to_date': data['to_date'], 'from_date': data['from_date']})
                return context
            else:
                return context
        else:
            return context
