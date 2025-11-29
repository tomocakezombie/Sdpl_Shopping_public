import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Item, Shop


class ItemModelTests(TestCase):
    def test_should_buy_today_true_when_due_today_and_not_bought(self):
        today = datetime.date.today()
        item = Item(
            name="メロン",
            count=1,
            buy_date=today,
            buy=False,
        )
        self.assertTrue(item.should_buy_today())

    def test_should_buy_today_false_when_due_future(self):
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        item = Item(
            name="ブドウ",
            count=2,
            buy_date=tomorrow,
            buy=False,
        )
        self.assertFalse(item.should_buy_today())

    def test_should_buy_today_false_when_already_bought(self):
        today = datetime.date.today()
        item = Item(
            name="ミカン",
            count=3,
            buy_date=today,
            buy=True,
        )
        self.assertFalse(item.should_buy_today())


class ShoppingListViewTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            account_id="tester",
            email="tester@example.com",
            password="StrongPass123",
        )

        self.shop = Shop.objects.create(name="スーパーA", shop_site="https://example.com")

        Item.objects.create(
            name="トマト",
            count=2,
            buy_date=datetime.date.today(),
            buy=False,
            shop=self.shop,
        )
        Item.objects.create(
            name="きゅうり",
            count=3,
            buy_date=datetime.date.today(),
            buy=True,
        )

    def test_item_list_requires_login(self):
        url = reverse("shoppinglist:list")
        response = self.client.get(url)
        self.assertRedirects(
            response,
            f"{reverse('accounts:login')}?next={url}",
            fetch_redirect_response=False,
        )

    def test_item_list_shows_items_after_login(self):
        self.client.login(account_id="tester", password="StrongPass123")
        response = self.client.get(reverse("shoppinglist:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "トマト")
        self.assertContains(response, "きゅうり")

    def test_item_list_filter_buy_true(self):
        self.client.login(account_id="tester", password="StrongPass123")
        response = self.client.get(reverse("shoppinglist:list"), {"buy": "true"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "きゅうり")
        self.assertNotContains(response, "トマト")

    def test_item_list_sort_by_name_descending(self):
        self.client.login(account_id="tester", password="StrongPass123")
        response = self.client.get(reverse("shoppinglist:list"), {"sort": "-name"})

        self.assertEqual(response.status_code, 200)
        object_list = list(response.context["object_list"])
        names = [item.name for item in object_list]
        self.assertEqual(names, sorted(names, reverse=True))

    def test_toggle_buy_flips_status(self):
        self.client.login(account_id="tester", password="StrongPass123")
        item = Item.objects.first()
        url = reverse("shoppinglist:toggle_buy", kwargs={"pk": item.pk})

        response = self.client.post(url, {"buy": "True"})

        self.assertRedirects(response, reverse("shoppinglist:list"))
        item.refresh_from_db()
        self.assertTrue(item.buy)

    def test_add_item_creates_new_record(self):
        self.client.login(account_id="tester", password="StrongPass123")
        url = reverse("shoppinglist:add")
        payload = {
            "name": "ほうれん草",
            "item_url": "https://example.com/spinach",
            "count": 5,
            "buy_date": datetime.date.today().isoformat(),
            "shop": self.shop.pk,
        }

        response = self.client.post(url, payload)

        self.assertRedirects(response, reverse("shoppinglist:list"))
        self.assertTrue(Item.objects.filter(name="ほうれん草").exists())