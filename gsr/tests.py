from datetime import datetime, timedelta
from django.test import TestCase

from gsr.models import Shop

class DatedModelUtils:
    """Helpers for DatedModelTests"""

    # TODO: use custom subclass instead of Shop?

    @staticmethod
    def make_new() -> Shop:
        return Shop(
            name="Shop",
            description="Shop desc",
            opening_hours="Opening hours",
            location="TODO",
        )

    PAST = datetime(2000, 1, 1)

    @staticmethod
    def make_old() -> Shop:
        # Create initial model
        model = DatedModelUtils.make_new()
        model.save()

        # Set time updated to the past
        model.date_updated = DatedModelUtils.PAST
        model.save()

        return model

    @staticmethod
    def trigger_update(model: Shop):
        model.name = model.name + " changed"
        model.save()

class DatedModelTests(TestCase):
    """Tests for DatedModel, using Shop as an example implementation"""

    def test_new_date_added(self):
        """Test that date added is set for a new object"""

        model = DatedModelUtils.make_new()
        model.save()
        self.assertLessEqual(
            datetime.now() - model.date_added,
            timedelta(minutes=5)
        )

    def test_new_date_updated(self):
        """Test that date updated is set for a new object"""

        model = DatedModelUtils.make_new()
        model.save()
        self.assertLessEqual(datetime.now().day - model.date_updated.day, 1)

    def test_old_date_writeable(self):
        """Test that date updated is set for an old object with changes"""

        model = DatedModelUtils.make_old()
        self.assertEqual(DatedModelUtils.PAST, model.date_updated)

    def test_old_date_updated(self):
        """Test that date updated is set for an old object with changes"""

        model = DatedModelUtils.make_old()
        DatedModelUtils.trigger_update(model)
        self.assertLessEqual(
            datetime.now() - model.date_added,
            timedelta(minutes=5)
        )
    
    # TODO: test non-dated fields
