import django
import pytest

import mock
from tinycontent.models import TinyContent

# Django 1.5 doesn't have CaptureQueriesContext, and adding support
# for checking query counts is irritating, so let's just skip those
# tests.
SKIP_CACHE_TESTS = django.VERSION < (1, 6)

if not SKIP_CACHE_TESTS:
    from django.db import DEFAULT_DB_ALIAS, connections
    from django.test.utils import CaptureQueriesContext


class FakeCache:
    def __init__(self):
        self.items = {}

    def get(self, key):
        return self.items.get(key, None)

    def set(self, key, value):
        self.items[key] = value

    def delete(self, key):
        del self.items[key]


if not SKIP_CACHE_TESTS:
    class QueryCounter(CaptureQueriesContext):
        def __init__(self):
            conn = connections[DEFAULT_DB_ALIAS]
            super().__init__(conn)

        def num_queries(self):
            return len(self)


@pytest.mark.django_db
def test_cache_hit_on_second_time(simple_content):
    if SKIP_CACHE_TESTS:
        return

    with mock.patch('tinycontent.models.cache', FakeCache()):
        with QueryCounter() as q:
            obj = TinyContent.get_content_by_name(simple_content.name)
            assert obj == simple_content
            assert q.num_queries() == 1

        with QueryCounter() as q:
            obj = TinyContent.get_content_by_name(simple_content.name)
            assert obj == simple_content
            assert q.num_queries() == 0


@pytest.mark.django_db
def test_cache_invalidated_by_delete(simple_content):
    if SKIP_CACHE_TESTS:
        return

    with mock.patch('tinycontent.models.cache', FakeCache()):
        with QueryCounter() as q:
            obj = TinyContent.get_content_by_name(simple_content.name)
            assert obj == simple_content
            assert q.num_queries() == 1

        with QueryCounter() as q:
            simple_content.delete()
            assert q.num_queries() == 1

        with QueryCounter() as q:
            with pytest.raises(TinyContent.DoesNotExist):
                obj = TinyContent.get_content_by_name(simple_content.name)
            assert q.num_queries() == 1


@pytest.mark.django_db
def test_cache_invalidated_by_save(simple_content):
    if SKIP_CACHE_TESTS:
        return

    with mock.patch('tinycontent.models.cache', FakeCache()):
        with QueryCounter() as q:
            obj = TinyContent.get_content_by_name(simple_content.name)
            assert obj == simple_content
            assert q.num_queries() == 1

        with QueryCounter() as q:
            simple_content.content = 'hello'
            simple_content.save()
            q.num_queries() == 1

        with QueryCounter() as q:
            obj = TinyContent.get_content_by_name(simple_content.name)
            assert obj.name == simple_content.name
            assert obj.content == 'hello'
            assert q.num_queries() == 1

        with QueryCounter() as q:
            obj = TinyContent.get_content_by_name(simple_content.name)
            assert obj.name == simple_content.name
            assert obj.content == 'hello'
            assert q.num_queries() == 0
