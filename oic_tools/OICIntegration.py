class OICIntegration:
    """
    This class is responsible for integrating with the OIC (Oracle Integration Cloud) system.
    It handles the connection to the OIC, sending requests, and processing responses.
    """

    def __init__(self, oic_url, client_id, client_secret):
        """
        Initializes the OICIntegration class with the provided OIC URL, client ID, and client secret.

        :param oic_url: The URL of the OIC instance.
        :param client_id: The client ID for authentication.
        :param client_secret: The client secret for authentication.
        """
        self.oic_url = oic_url
        self.client_id = client_id
        self.client_secret = client_secret
