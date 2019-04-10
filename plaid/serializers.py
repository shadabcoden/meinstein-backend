from rest_framework import serializers
from plaid.models import MeAccounts, MeUserdetail


class MeAccountsSerializer(serializers.ModelSerializer):
	users = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
	class Meta:
		model = MeAccounts
		fields = ('account_id', 'username', 'email', 'contact_number', 'active', 'updated', 'users')


class MeUserdetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = MeUserdetail
		fields = ('user_id', 'first_name', 'last_name', 'zipcode', 'city', 'state', 'country', 'updated', 'account')