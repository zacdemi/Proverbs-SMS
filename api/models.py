import os
from datetime import datetime

from pynamodb.attributes import UnicodeAttribute, BooleanAttribute, UTCDateTimeAttribute
from pynamodb.models import Model

class UserModel(Model):
    class Meta:
        local = False
        if local:
            table_name = 'dev-users'
            host = 'http://localhost:8000'
        else:
            table_name = 'dev-users'
            region = 'us-east-1'

    phone = UnicodeAttribute(hash_key=True, null=False)
    subscribed = BooleanAttribute(null=False, default=False)
    createdAt = UTCDateTimeAttribute(null=False, default=datetime.now())
    updatedAt = UTCDateTimeAttribute(null=False)
    confirm = UnicodeAttribute(hash_key=True, null=False)

    def save(self, conditional_operator=None, **expected_values):
        self.updatedAt = datetime.now()
        super(UserModel, self).save()

    def __iter__(self):
        for name, attr in self._get_attributes().items():
            yield name, attr.serialize(getattr(self, name))
