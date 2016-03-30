from peewee import *
import config

class UnknownField(object):
    pass

class BaseModel(Model):
    class Meta:
        database = MySQLDatabase('imageserver', **{'host': config.db_url, 'password':
            config.db_password, 'user': config.db_user})

class Image(BaseModel):
    image_guid = CharField(primary_key=True)
    bucket = CharField(db_column='bucket_id', null=True)
    filename = CharField(null=True)
    url = CharField(db_column='url_id', null=True)
    accessability = IntegerField(null=True)
    passphrase = CharField(null=True)

    class Meta:
        db_table = 'images'

    def __repr__(self):
        return """
        guid:{0}
        \tbucket:{1}
        \tfilename:{2}
        \turl:{3}
        \taccessability:{4}
        \tpassphrase:{5}""".format(self.image_guid, self.bucket, self.filename,
                                   self.url, self.accessability,
                                   self.passphrase)

if __name__ == '__main__':
    for image in Image.select():
        print(image)