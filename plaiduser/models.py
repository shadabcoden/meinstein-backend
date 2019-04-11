from django.db import models
from django.utils import timezone

class MeAccounts(models.Model):
    account_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    updated = models.DateField(auto_now_add=True)

    def __str__(self):
        return "account_id = " + str(self.account_id) + " username = " + self.username + " email = " + self.email + " contact_number = " + self.contact_number

    class Meta:
    	ordering = ('updated',)
    	managed = False
    	db_table = 'me_accounts'


class MePlaidIncome(models.Model):
    income_id = models.AutoField(primary_key=True)
    streams = models.IntegerField(blank=True, null=True)
    last_year_income = models.IntegerField(blank=True, null=True)
    last_year_income_pre_tax = models.IntegerField(blank=True, null=True)
    projected_income = models.IntegerField(blank=True, null=True)
    projected_income_pre_tax = models.IntegerField(blank=True, null=True)
    plaid_useritem = models.ForeignKey('MePlaidUserItem', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'me_plaid_income'


class MePlaidIncomeStream(models.Model):
    stream_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    monthly_income = models.IntegerField(blank=True, null=True)
    days = models.IntegerField(blank=True, null=True)
    confidence = models.FloatField(blank=True, null=True)
    income = models.ForeignKey(MePlaidIncome, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'me_plaid_income_stream'


class MePlaidItemAccountsNumber(models.Model):
    number_id = models.AutoField(primary_key=True)
    number_type = models.CharField(max_length=45, blank=True, null=True)
    account = models.CharField(max_length=100)
    plaid_account = models.ForeignKey('MePlaidUserItemAccounts', on_delete=models.CASCADE)
    routing = models.CharField(max_length=45, blank=True, null=True)
    wire_routing = models.CharField(max_length=45, blank=True, null=True)
    institution = models.CharField(max_length=45, blank=True, null=True)
    branch = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'me_plaid_item_accounts_number'


class MePlaidUserBalanceDetail(models.Model):
    balance_id = models.AutoField(primary_key=True)
    plaid_account = models.ForeignKey('MePlaidUserItemAccounts', on_delete=models.CASCADE)
    balance = models.IntegerField()
    temporal_type = models.CharField(max_length=200)
    fetched_date = models.DateField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'me_plaid_user_balance_detail'
        unique_together = (('plaid_account', 'temporal_type'),)


class MePlaidUserIdentity(models.Model):
    user_identity_id = models.AutoField(primary_key=True)
    plaid_item = models.ForeignKey('MePlaidUserItem', on_delete=models.CASCADE)
    names = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'me_plaid_user_identity'


class MePlaidUserItem(models.Model):
    user_item_id = models.AutoField(primary_key=True)
    item_id = models.CharField(max_length=45)
    item_name = models.CharField(max_length=100)
    accesstoken = models.CharField(max_length=200)
    user = models.ForeignKey('MeUserdetail', on_delete=models.CASCADE)
    linked_date = models.DateField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'me_plaid_user_item'
        unique_together = (('item_id', 'user'),)


class MePlaidUserItemAccounts(models.Model):
    account_id = models.CharField(primary_key=True, max_length=200)
    name = models.CharField(max_length=200, blank=True, null=True)
    mask = models.CharField(max_length=45, blank=True, null=True)
    accounts_type = models.CharField(max_length=45, blank=True, null=True)
    subtype = models.CharField(max_length=45, blank=True, null=True)
    official_name = models.CharField(max_length=200, blank=True, null=True)
    available_balance = models.IntegerField(blank=True, null=True)
    iso_currency_code = models.CharField(max_length=45, blank=True, null=True)
    user_item = models.ForeignKey(MePlaidUserItem, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'me_plaid_user_item_accounts'
        unique_together = (('account_id', 'user_item'),)


class MePlaidUserTransactionDetails(models.Model):
    transaction_detail_id = models.AutoField(primary_key=True)
    plaid_account = models.ForeignKey(MePlaidUserItemAccounts, on_delete=models.CASCADE)
    frequency = models.IntegerField()
    category = models.CharField(max_length=200)
    temporal_type = models.CharField(max_length=200)
    fetched_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'me_plaid_user_transaction_details'
        unique_together = (('plaid_account', 'category', 'temporal_type'),)


class MeUserdetail(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=45)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    updated = models.DateField(auto_now_add=True)
    account = models.ForeignKey(MeAccounts, related_name='users' ,on_delete=models.CASCADE)

    def __str__(self):
        return "user_id = " + str(self.user_id) + " first_name = " + self.first_name + " zipcode = " + self.zipcode + " city = " + self.city + " country = " + self.country

    class Meta:
        managed = False
        db_table = 'me_userdetail'


class PlaidIdentityAddress(models.Model):
    address_id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    street = models.CharField(max_length=200, blank=True, null=True)
    zipcode = models.CharField(max_length=45)
    is_primary = models.IntegerField(blank=True, null=True)
    plaid_user_item = models.ForeignKey(MePlaidUserIdentity, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'plaid_identity_address'


class PlaidIdentityEmail(models.Model):
    email_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=200)
    is_primary = models.IntegerField(blank=True, null=True)
    plaid_user_item = models.ForeignKey(MePlaidUserIdentity, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'plaid_identity_email'


class PlaidIdentityPhone(models.Model):
    phone_id = models.AutoField(primary_key=True)
    phone_type = models.CharField(max_length=45, blank=True, null=True)
    number = models.CharField(max_length=45, blank=True, null=True)
    is_primary = models.IntegerField(blank=True, null=True)
    plaid_identity = models.ForeignKey(MePlaidUserIdentity, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'plaid_identity_phone'