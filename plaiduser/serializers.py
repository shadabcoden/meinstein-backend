from rest_framework import serializers
from plaiduser.models import MeAccounts, MeUserdetail


class MeAccountsSerializer(serializers.ModelSerializer):
	users = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
	class Meta:
		model = MeAccounts
		fields = ('account_id', 'username', 'email', 'contact_number', 'active', 'updated', 'users')
		#depth = 1

	# call other class serialiser inorder to save data in those model as well	
	# def create(self, validated_data):
	# 	return MeAccounts(**validated_data)

class MeUserdetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = MeUserdetail
		fields = ('user_id', 'first_name', 'last_name', 'zipcode', 'city', 'state', 'country', 'updated', 'account')