import datetime

from django import forms
from django.db.models.constants import LOOKUP_SEP
from url_filter.backends.django import DjangoFilterBackend
from url_filter.filters import Filter
from url_filter.filtersets import ModelFilterSet

from . import models


class BetterDjangoFilterBackend(DjangoFilterBackend):

    def prepare_spec(self, spec):
        if spec.lookup == "exact":
            return LOOKUP_SEP.join(spec.components)
        else:
            return '{}{}{}'.format(
                LOOKUP_SEP.join(spec.components),
                LOOKUP_SEP,
                spec.lookup,
            )

    def prepare_value(self, spec):
        if spec.lookup == "lte" and isinstance(spec.value, datetime.date):
            value = spec.value
            value = datetime.datetime(year=value.year, month=value.month,
                                      day=value.day, hour=0, minute=0, second=0)
            value = value + datetime.timedelta(days=1, microseconds=-1)
        else:
            value = spec.value

        return value

    def filter(self):
        include = {self.prepare_spec(i): self.prepare_value(i) for i in
                   self.includes}
        exclude = {self.prepare_spec(i): self.prepare_value(i) for i in
                   self.excludes}

        qs = self.queryset

        for k, v in include.items():
            try:
                qs = getattr(qs, k)(v)
            except AttributeError:
                qs = qs.filter(**{k: v})
        for k, v in exclude.items():
            try:
                qs = getattr(qs, k)(v, exclude=True)
            except AttributeError:
                qs = qs.exclude(**{k: v})

        return qs

    def bind(self, specs):
        self.specs = specs


def get_form_field_for_type(ftype):
    type_map = {
        "text": forms.CharField(),
        "date": forms.DateField(),
        "daterange": forms.DateField(),
        "duration": forms.DurationField(),
        "boolean": forms.BooleanField(required=False),
        "select": forms.ChoiceField(),
    }
    return type_map.get(ftype, forms.CharField())


def create_rel_filterset(model_name):
    model = getattr(models, model_name)
    name = model.__name__ + "FilterSet"
    Meta = type('Meta', (object,),
                {"model": model, "fields": [model._meta.pk.name]})
    rel_filterset = type(name, (ModelFilterSet,), {"Meta": Meta})
    return rel_filterset


def create_filterset(model, definition, name=None):
    if name is None:
        name = model.__name__ + "FilterSet"
    Meta = type('Meta', (object,),
                {"model": model, "fields": []})

    attrs = {}
    for f in definition:
        if f.get("type") == "daterange":
            f['lookups'] = ["gte", "lte"]

        if f.get("rel") and not f.get("method"):
            try:
                filter = globals()[f["rel"] + "FilterSet"]()
            except KeyError:
                filter_class = create_rel_filterset(f["rel"])
                filter = filter_class()
        else:
            ftype = f.get("type", "text")
            form_field = get_form_field_for_type(ftype)
            if f.get("options"):
                form_field._set_choices(f.get("options"))
            source = f.get("source", f["name"])
            lookups = f.get("lookups", ["exact"])
            default_lookup = f.get("default_lookup", lookups[0])
            filter = Filter(source=source, form_field=form_field,
                            lookups=lookups, default_lookup=default_lookup)

        attrs[f["name"]] = filter

    attrs["Meta"] = Meta
    attrs["definition"] = definition
    attrs["filter_backend_class"] = BetterDjangoFilterBackend

    return type(name, (ModelFilterSet,), attrs)


####
class NewsArticleFilterSet(ModelFilterSet):

    class Meta:
        model = models.NewsArticle
        fields = ["tstamp", "url", "title", "brief", "body", "source", "date",
            "company", "tag",]

class TagFilterSet(ModelFilterSet):

    class Meta:
        model = models.Tag
        fields = ["name",]

class CompanyFilterSet(ModelFilterSet):
        
    class Meta:
        model = models.Company
        fields= ["name",]


####


NewsArticleFilterSet = create_filterset(
    models.NewsArticle,
    [
        {"name": "id", "lookups":["in","range"], "default_lookup":"in", "method":"true"},
        {"name": "tstamp", "type":"daterange", "method":"true"},                
        {"name": "url", "lookups":["icontains"], "method":"true"},
        {"name": "title", "lookups":["icontains"], "method":"true"},
        {"name": "brief", "lookups":["icontains"], "method":"true"},
        {"name": "body", "lookups":["icontains"], "method":"true"},
        {"name": "source", "type":"select", "method":"true",
            "lookups":["exact"],
            "options":
                [
                    ["spacedotcom", "Space.com"],
                    ["spacenews", "SpaceNews.com"]
                ]
            },
        {"name": "company", "lookups":["exact","in"], "method":"true"},
        {"name": "tag", "lookups":["exact","in"], "method":"true"},
    ]
)

#***************************************************************************************
#    Based on the work...
#
#    Title: 911 / Call For Service Analytics
#    Author: Clinton Dreisbach
#    Date: 20th January 2018
#    Availability: https://github.com/cndreisbach/call-for-service
#    License: GNU Public License 3.0
#
#**************************************************************************************/
