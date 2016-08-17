import requests


class CaptchaClient(object):

    def __init__(self, api_key):
        self.api_key = api_key

    def submit_captcha(self, captcha_path):
        """
            submit a captcha image to be broken. Below is the example in the 2captcha API doc
            <form method="post" action="http://2captcha.com/in.php" enctype="multipart/form-data">
                <input type="hidden" name="method" value="post">
                 Your key:
                 <input type="text" name="key" value="82868d30e4365251d3345d809cbef7cb">
                 The CAPTCHA file:
                 <input type="file" name="file">
                 <input type="submit" value="download and get the ID">
            </form>

            @param captcha_path: path to the captcha image
            @type captcha_path: str
        """
        data = {'key': self.api_key}
        files = {'file': open(captcha_path, 'rb')}

        res = requests.post(url='http://2captcha.com/in.php', data=data, files=files)
        if res.status_code >= 400:
            raise Exception("Error {}: {}".format(res.status_code, res.content))

        response = res.content
        if response.startswith('ERROR'):
            raise Exception(response)
        elif response.startswith('OK'):
            return response.split('|')[1]
        else:
            return Exception('Unexpected Response')

    def get_solved_captcha(self, captcha_id):
        """
            Use GET request of the following configuration:
            http://2captcha.com/res.php?key=YOUR_APIKEY&action=get&id=CAPCHA_ID
            YOUR_APIKEY - stands for you key 32 symbols length.
            CAPTCHA_ID - stands for the ID of the previously uploaded CAPTCHA

          @param: captcha_id: id of the captcha returned from submit_captcha request
          @type: captcha_id: str
        """
        params = {'key': self.api_key, 'action': 'get', 'id': captcha_id}

        res = requests.get(url='http://2captcha.com/res.php', params=params)
        if res.status_code >= 400:
            raise Exception("Error {}: {}".format(res.status_code, res.content))

        response = res.content
        if response.startswith('ERROR') or response == 'CAPCHA_NOT_READY':
            raise Exception(response)
        elif response.startswith('OK'):
            return response.split('|')[1]
        else:
            return Exception('Unexpected Response')

if __name__ == '__main__':
    import time
    client = CaptchaClient('82868d30e4365251d3345d809cbef7cb')
    captcha_id = client.submit_captcha('/Users/surya/Downloads/api_spec.png')
    print "captcha_id: ", captcha_id
    time.sleep(10)
    captcha = client.get_solved_captcha(captcha_id)
    print "captcha: ", captcha