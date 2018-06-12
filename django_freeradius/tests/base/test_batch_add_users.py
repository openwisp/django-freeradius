class BaseTestCSVUpload(object):
    def test_generate_username_from_email(self):
        reader = [['', 'cleartext$password', 'rohith@openwisp.com', 'Rohith', 'ASRK']]
        batch = self.radius_batch_model.objects.create()
        batch.add(reader)
        self.assertEqual(self.radius_batch_model.objects.all().count(), 1)
        self.assertEqual(batch.users.all().count(), 1)
        user = batch.users.first()
        self.assertEqual(user.username, 'rohith')
        self.assertEqual(user.email, 'rohith@openwisp.com')
        self.assertEqual(user.first_name, 'Rohith')
        self.assertEqual(user.last_name, 'ASRK')

    def test_generate_username_when_repeat(self):
        hashed_password = "pbkdf2_sha256$100000$x3DUBnOFwraV$PU2dZZq1FcuBjagxVLPhhFvpicLn18fFCN5xiLsxATc="
        cleartext_password = "cleartext$password"
        reader = [['rohith', cleartext_password, 'rohith@openwisp.com', 'Rohith', 'ASRK'],
                  ['rohith', hashed_password, 'rohith@openwisp.com', '', '']]
        batch = self.radius_batch_model.objects.create()
        batch.add(reader)
        self.assertEqual(self.radius_batch_model.objects.all().count(), 1)
        self.assertEqual(batch.users.all().count(), 2)
        user = batch.users.all()[1]
        self.assertEqual(user.username, 'rohith1')
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')

    def test_generate_password(self):
        reader = [['rohith', '', 'rohith@openwisp.com', '', '']]
        batch = self.radius_batch_model.objects.create()
        batch.add(reader)
        self.assertEqual(self.radius_batch_model.objects.all().count(), 1)
        self.assertEqual(batch.users.all().count(), 1)
        user = batch.users.first()
        self.assertIsNotNone(user.password)

    def test_cleartext_password_storage(self):
        cleartext_password = 'cleartext$password'
        reader = [['rohith', cleartext_password, 'rohith@openwisp.com', 'Rohith', 'ASRK']]
        batch = self.radius_batch_model.objects.create()
        batch.add(reader)
        self.assertEqual(self.radius_batch_model.objects.all().count(), 1)
        self.assertEqual(batch.users.all().count(), 1)
        user = batch.users.first()
        self.assertNotEqual(cleartext_password, user.password)

    def test_hashed_password_storage(self):
        hashed_password = "pbkdf2_sha256$100000$x3DUBnOFwraV$PU2dZZq1FcuBjagxVLPhhFvpicLn18fFCN5xiLsxATc="
        reader = [['rohith', hashed_password, 'rohith@openwisp.com', 'Rohith', 'ASRK']]
        batch = self.radius_batch_model.objects.create()
        batch.add(reader)
        self.assertEqual(self.radius_batch_model.objects.all().count(), 1)
        self.assertEqual(batch.users.all().count(), 1)
        user = batch.users.first()
        self.assertEqual(hashed_password, user.password)
