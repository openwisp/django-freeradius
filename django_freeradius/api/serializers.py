import swapper
from rest_framework import serializers

RadiusPostAuth = swapper.load_model("django_freeradius", "RadiusPostAuth")


class RadiusPostAuthSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False, allow_blank=True)
    called_station_id = serializers.CharField(required=False, allow_blank=True)
    calling_station_id = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        # do not save correct passwords in clear text
        if data['reply'] == 'Access-Accept':
            data['password'] = ''
        return data

    class Meta:
        model = RadiusPostAuth
        fields = ['username', 'password', 'reply',
                  'called_station_id',
                  'calling_station_id']
