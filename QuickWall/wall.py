import requests
from re import sub

from QuickWall.logger import Logger


logger = Logger('Wall')


class Wall:
    """
    Class to do tasks like downloading the wallpaper.

    URL list has 4 entries:

    desc: Description of the image
    name: Name of the user who uploaded the image
    dw_link: Download link of the image
    unique_id: ID to save the image
    """
    def __init__(
                self,
                photo_id,
                random=None,
                search=None
            ):
        self.s_term = None
        self._acces_key = sub(r'\n|"', '', requests.get("https://deepjyoti30server.herokuapp.com/key").text)
        self._URL = "https://api.unsplash.com/photos/"
        self._URL_list = []
        self.random = random
        self.search = search
        self.id = photo_id
        self._build_URL()

    def _build_URL(self):
        """Build the URL based on the passed args."""

        self.params = {
                    'client_id': self._acces_key,
                    'per_page' : 30, 
                    }

        if self.id:
            logger.info("Adding ID to URL")
            self._URL += self.id
            return

        if self.random:
            logger.info("Adding random to URL")
            self._URL += "random/"
            self.params['count'] = self.params.pop('per_page')
        if self.search:
            logger.info("Adding search term [{}] to URL".format(self.search))
            self.params.update({'query': self.search})

    def _add_to_list(self, entity):
        """
        Extract the data from the passed entity and add it to
        the list.
        """

        desc = entity['description']
        if desc is None:
            desc = entity['alt_description']

        if desc is None:
            desc = "Wallpaper"

        name = entity['user']['name']
        dw_link = entity['links']['download']
        unique_id = entity['id']

        self._URL_list.append({
                                'dw_link': dw_link,
                                'unique_id': unique_id,
                                'desc': desc,
                                'name': name
                              })

    def _get_paper(self):
        """
        Get a list of wallpaper using the access key.

        Return a iterable list of direct download URL's.
        """
        response = requests.get(self._URL, params=self.params)

        if response.status_code != 200:
            logger.critical("ERROR: {}".format(response.reason))

        json_data = response.json()

        if type(json_data) == dict:
            self._add_to_list(json_data)
        else:
            for i in json_data:
                self._add_to_list(i)

    def get_list(self):
        self._get_paper()
        return self._URL_list
