from django.test import TestCase, Client
from LegacySite.models import Card
from django.urls import reverse

# Create your tests here.

class MyTest(TestCase):
    # Django's test run with an empty database. We can populate it with
    # data by using a fixture. You can create the fixture by running:
    #    mkdir LegacySite/fixtures
    #    python manage.py dumpdata LegacySite > LegacySite/fixtures/testdata.json
    # You can read more about fixtures here:
    #    https://docs.djangoproject.com/en/4.0/topics/testing/tools/#fixture-loading
    fixtures = ["testdata.json"]

    # Assuming that your database had at least one Card in it, this
    # test should pass.
    #def test_get_card(self):
    #    allcards = Card.objects.all()
     #   self.assertNotEqual(len(allcards), 0)

    def test1_XSS(self):
        c = Client()
        resp = c.get("/buy/?director=<script>alert()</script>")
        #print(resp.content)
        #self.assertNotIn(b"NYU", resp.content)
        self.assertNotContains(resp, "<script>alert()</script>")
        #self.assertContains(resp, '<script>alert()</script>', html=True)

    def test2_gift_a_card(self):
        c = Client()
        c.login(username='john', password='john')
        resp = c.get("/gift/", {'username':'attacker', 'amount':30})
        #print(resp.content)
        self.assertNotContains(resp, "Card given to attacker")

    def test3_obtaining_salted_password(self):
        c = Client()
        c.login(username='john', password='john')
        #files = {'card_data': open('part1/attack.gftcrd','rb')}
        #print(files)
        #values = {'card_supplied': True}

        with open('part1/attack3.gftcrd', 'rb') as fp:
            resp = c.post("/use/", {'card_supplied': True, 'card_data': fp})

        #print(resp.content)
        self.assertNotContains(resp, "000000000000000000000000000078d2$18821d89de11ab18488fdc0a01f1ddf4d290e198b0f80cd4974fc031dc2615a3")

    def test4_exploiting_another_attack(self):
        c = Client()
        c.login(username='john', password='john')
        with open('part1/attack4.gft', 'rb') as fp:
            resp = c.post("/use/", {'card_supplied': True, 'card_data': fp, 'card_fname': 'name;echo hello;'})
        #print(resp.content)
        
        
        

