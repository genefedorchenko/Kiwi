import os
import unittest

from tcms.issuetracker.types import Bugzilla
from tcms.testcases.models import BugSystem
from tcms.tests import LoggedInTestCase


@unittest.skipUnless(os.getenv('TEST_BUGTRACKER_INTEGRATION'),
                     'Bug tracker integration testing not enabled')
class TestBugzillaIntegration(LoggedInTestCase):
    existing_bug_url = 'http://bugzilla.example.bg/bugzilla/show_bug.cgi?id=1'

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        bug_system = BugSystem.objects.create(  # nosec:B106:hardcoded_password_funcarg
            name='Dockerized Bugzilla',
            tracker_type='Bugzilla',
            api_url='http://bugzilla.example.bg/bugzilla/xmlrpc.cgi',
            api_username='admin@bugzilla.bugs',
            api_password='password',
        )
        cls.integration = Bugzilla(bug_system)

    def test_details(self):
        result = self.integration.details(self.existing_bug_url)

        # Bugzilla doesn't support OpenGraph and ATM we don't provide
        # additional integration here
        self.assertEqual('undefined', result)
