from django import forms
from models import  AbstractNas



RAD_NAS_TYPES = (
    ('Async', 'Async'),
    ('Sync', 'Sync'),
    ('ISDN Sync', 'ISDN Sync'),
    ('ISDN Async V.120', 'ISDN Async V.120'),
    ('ISDN Async V.110', 'ISDN Async V.110'),
    ('Virtual', 'Virtual'),
    ('PIAFS', 'PIAFS'),
    ('HDLC Clear', 'HDLC Clear'),
    ('Channel', 'Channel'),
    ('X.25', 'X.25'),
    ('X.75', 'X.75'),
    ('G.3 Fax', 'G.3 Fax'),
    ('SDSL', 'SDSL - Symmetric DSL'),
    ('ADSL-CAP', 'ADSL-CAP'),
    ('ADSL-DMT', 'ADSL-DMT'),
    ('IDSL', 'IDSL'),
    ('Ethernet', 'Ethernet'),
    ('xDSL', 'xDSL'),
    ('Cable', 'Cable'),
    ('Wireless - Other', 'Wireless - Other'),
    ('IEEE 802.11', 'Wireless - IEEE 802.11'),
    ('Token-Ring', 'Token-Ring'),
    ('FDDI', 'FDDI'),
    ('Wireless - CDMA2000', 'Wireless - CDMA2000'),
    ('Wireless - UMTS', 'Wireless - UMTS'),
    ('Wireless - 1X-EV', 'Wireless - 1X-EV'),
    ('IAPP', 'IAPP'),
    ('FTTP', 'FTTP'),
    ('IEEE 802.16', 'Wireless - IEEE 802.16'),
    ('IEEE 802.20', 'Wireless - IEEE 802.20'),
    ('IEEE 802.22', 'Wireless - IEEE 802.22'),
    ('PPPoA', 'PPPoA - PPP over ATM'),
    ('PPPoEoA', 'PPPoEoA - PPP over Ethernet over ATM'),
    ('PPPoEoE', 'PPPoEoE - PPP over Ethernet over Ethernet'),
    ('PPPoEoVLAN', 'PPPoEoVLAN - PPP over Ethernet over VLAN'),
    ('PPPoEoQinQ', 'PPPoEoQinQ - PPP over Ethernet over IEEE 802.1QinQ'),
    ('xPON', 'xPON - Passive Optical Network'),
    ('Wireless - XGP', 'Wireless - XGP'),
    ('WiMAX', ' WiMAX Pre-Release 8 IWK Function'),
    ('WIMAX-WIFI-IWK', 'WIMAX-WIFI-IWK: WiMAX WIFI Interworking'),
    ('WIMAX-SFF', 'WIMAX-SFF: Signaling Forwarding Function for LTE/3GPP2'),
    ('WIMAX-HA-LMA', 'WIMAX-HA-LMA: WiMAX HA and or LMA function'),
    ('WIMAX-DHCP', 'WIMAX-DHCP: WIMAX DCHP service'),
    ('WIMAX-LBS', 'WIMAX-LBS: WiMAX location based service'),
    ('WIMAX-WVS', 'WIMAX-WVS: WiMAX voice service'),
    ('Other', 'Other'),
)

# class for add customer fields in the NAS
class NasModelForm(forms.ModelForm):

    standard_type = forms.ChoiceField(choices = RAD_NAS_TYPES,
                                      help_text = "choose one of the standard types...",
                                      initial='Other',
                                      );

    other_NAS_type = forms.CharField(help_text = "...or write a new type.",
                                     required = False,
                                     max_length=30,
                                     );

    class Meta:
        fields = '__all__'
