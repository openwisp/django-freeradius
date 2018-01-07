import swapper
from django.utils import timezone
from rest_framework import serializers

RadiusPostAuth = swapper.load_model("django_freeradius", "RadiusPostAuth")
RadiusAccounting = swapper.load_model("django_freeradius", "RadiusAccounting")


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
        fields = '__all__'


STATUS_TYPE_CHOICES = (
    ('Start', 'Start'),
    ('Interim-Update', 'Interim-Update'),
    ('Stop', 'Stop'),
    ('Accounting-On', 'Accounting-On (ignored)'),
    ('Accounting-Off', 'Accounting-Off (ignored)')
)


class RadiusAccountingSerializer(serializers.ModelSerializer):
    framed_ip_address = serializers.IPAddressField(required=False, allow_blank=True)
    session_time = serializers.IntegerField(required=False, default=0)
    stop_time = serializers.DateTimeField(required=False)
    update_time = serializers.DateTimeField(required=False)
    input_octets = serializers.IntegerField(required=False, default=0)
    output_octets = serializers.IntegerField(required=False, default=0)
    # this is needed otherwise serialize will ignore status_type from accounting packet
    # as it's not a model field
    status_type = serializers.ChoiceField(write_only=True, choices=STATUS_TYPE_CHOICES)

    def validate(self, data):
        """
        We need to set some timestamps according to the accounting packet type
        * update_time: set everytime a Interim-Update / Stop packet is received
        * stop_time: set everytime a Stop packet is received
        * session_time: calculated if not present in the accounting packet
        :param data: accounting packet
        :return: Dict accounting packet
        """
        time = timezone.now()
        status_type = data.pop('status_type')
        if status_type == 'Interim-Update':
            data['update_time'] = time
        if status_type == 'Stop':
            data['update_time'] = time
            data['stop_time'] = time
        return data

    class Meta:
        model = RadiusAccounting
        fields = '__all__'
