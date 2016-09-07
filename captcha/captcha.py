from retrying import retry
import requests


def retry_if_not_ready(exception):
    """
    Return True if we should retry
    in this case when it's an E-114, False otherwise
    """
    return isinstance(exception, CaptchaException) and exception.code == 'CAPCHA_NOT_READY'


class CaptchaException(Exception):

    def __init__(self, code, message):
        super(CaptchaException, self).__init__(message)
        self.code = code


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
            raise CaptchaException(response, '')
        elif response.startswith('OK'):
            return response.split('|')[1]
        else:
            return CaptchaException(None, 'Unexpected Response')

    def submit_captcha_b64(self, captcha_b64):
        """
            submit a captcha image to be broken. Below is the example in the 2captcha API doc
            <form method="post" action="http://2captcha.com/in.php">
                <input type="hidden" name="method" value="base64">
                Your key:
                <input type="text" name="key" value="YOUR_APIKEY">
                The CAPTCHA file body in base64 format:
                <textarea name="body">BASE64_FILE</textarea>
                <input type="submit" value="download and get the ID">
            </form>

            @param captcha_b64: base64 encoded captcha image
            @type captcha_b64: str (base64 encoded)
        """
        
        data = {'key': self.api_key, 'method': 'base64', 'body': captcha_b64}

        res = requests.post(url='http://2captcha.com/in.php', data=data)
        if res.status_code >= 400:
            raise Exception("Error {}: {}".format(res.status_code, res.content))

        response = res.content
        if response.startswith('ERROR'):
            raise CaptchaException(response, '')
        elif response.startswith('OK'):
            return response.split('|')[1]
        else:
            return CaptchaException(None, 'Unexpected Response')

    @retry(retry_on_exception=retry_if_not_ready,
           wait_fixed=2000,
           stop_max_delay=60000)
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
            raise CaptchaException(response, '')
        elif response.startswith('OK'):
            return response.split('|')[1]
        else:
            return CaptchaException(None, 'Unexpected Response')

if __name__ == '__main__':
    import time
    client = CaptchaClient('82868d30e4365251d3345d809cbef7cb')
    captcha_id = client.submit_captcha('/Users/surya/loanzen/zenscraper/test.png')

    """captcha_id = client.submit_captcha_b64('iVBORw0KGgoAAAANSUhEUgAAAKAAAAAuCAYAAAC'
                                       'vdRKFAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAMk0l'
                                       'EQVR4nO2deXBUVRaHv96X7AkhbFEIMaCRyKIguA0'
                                       'WiKMwCiXu4igWWuqIywiKlAoDzig6LgiDzKA4jIj'
                                       'jgOKCRjYRJLIFiIAsQjAQspLupJPu1/v80Wbp193'
                                       'kpft1Gmb6q0oV7/Lufb+qnD7n3HPP6yi8Xq+XOHF'
                                       'ihDLWAuL8fxM3wDgxJW6AcWJK3ADjxJS4AcaJKXE'
                                       'DjBNT4gYYJ6bEDTBOTIkbYJyYEjfAODFFHWsBcTo'
                                       'HjyDgrKvDIwh4rFaUej2G3NxYy5JmgC6zmZNvvYW'
                                       'luBhnTQ1uqxV9dja5b7yBIScn2hrPORxOF6dqTNS'
                                       'YG6itb6S+0UpDkw27w4nH48Xj9WLUa0k06MlMS6Z'
                                       'Pj0x6d89Eo1ZFTVPlsmUceeSRluu0UaMoWLMmas+'
                                       'TiiQDPDZzJhWLF/uNWffvp+Ldd8mZMycqwsQ8M3s'
                                       'ThRtKAXjh6RHcfGNeh+avWXuU5+ZuBmDUNeczb9Z'
                                       'IWfUVHyxl0+6DHDx+impTPR1t8dBrNYwoyOO3Iy7'
                                       'hguxusmoDUBmNftdum032Z4SDpBzQ63IFHXdWV8s'
                                       'q5kzMeOJyMjMMALy6YAflFRbJc01mgXlvbwcgOUn'
                                       'Ls49fLru+b4t/YlPxT1TVddz4AASHkw079zNt/nL'
                                       'e+WQ9dodTVn1Kvd7v2iMIsq4fLpIMUJOeHnTcWVc'
                                       'nq5gzkZyk48VnrgSgyerk+T9vkTz3L2/+gLneDsC'
                                       '0PwwjPc0guz6jTivLOl4vfLV1Ly8tXY3b7ZFlTQC'
                                       'lyAN6rFbZ1o4ESSFYnZYWdNxlMskqpj1GXNaTW2/'
                                       'uz78/PUhxSRXvr9jHvbdffMY5Gzb/wjcbj/vmD+3'
                                       'Jjdf1jYo2g97fADNSEsntlUVmWjLJCQYS9DoMei0'
                                       'qpRK3x0OjVaDa1MDxihoOlJbj8fi7zb1Hylj21RZ'
                                       '+P/ZqWfSdrR5QkgGeDR6wmccfupSiHeWcKLfw9j+'
                                       'KuWJoT3Jzgn9AGix2Xnr9BwASjBqe/+OIqOkyiDz'
                                       'gtZfmc9f1V0ia22gT+GLLblZu2I7T5W4ZX7N1DxN'
                                       'GXkZyQuQeW2XwX8N9lnhASSFYHcIAXTEwQINezZw'
                                       'ZV6FSKXC5PMyY8x0uV/BQ9dqCHZyu8yXbUx8cQlb'
                                       'XhOjpEhmgze6QPDfRoOf20cN5fvIElEpFy7jD6WL'
                                       '7/qOy6DuTB3SZzVh27qRm5UqqPvgA08aNnWag50w'
                                       'O2JaC/K7cf+cAAI4cM7FgSXHAPVt3lPPZ1z8DMLg'
                                       'gi4k39Y+qJqM+fANsZkBuNiOHXOQ3VlZ1OiJdzQT'
                                       'LAU/On8/ua67h+6wsikeM4MAdd3DwvvsoGTOGoux'
                                       'sfpk7F69Hvjw0qC4pN4XKAb12e8xyiSn3DqT/Bb4'
                                       'Pxvsr9rFnX+uO3Gp18qd5WwHQ61S8ME1aKIwEo17'
                                       'nd20TOm6AAAP6ZvtdV9fVh62pLWIP6HU6OfrUUzQ'
                                       'UFRFs2+62WDg+axaHH3pIlueH1CXlplAeEGLnBdV'
                                       'qJXOeuxqtVoXXCzPnfodN8JWL3ly8i8rqJgAevn8'
                                       'Q5/VKjroevVbjd20Ls4yiUvr/SlQqeU5LxXVAqVQ'
                                       'uXUr9FukVh44SUQ4IsckDm+nbO5VHJw8CoLyikXn'
                                       'zt7G7pIqPVx8E4OL+XbhrYn6naAkIwWF6wGOn/Gu'
                                       'r3dJTwtbUFrEHbEadkUH3KVPot2QJ/ZYsIfPWWwP'
                                       'uqVq+XBYNQZ8v5SaV0YhCo8HrDPxUx8oDNnPPbRf'
                                       'zXdFJdu6p5JMvj/Dt9yfwen0e8sVnrvRL6qOJQRy'
                                       'CHR03wFqzhbXb9vmNDczrHYmsFsQ5IECfuXPpNXU'
                                       'qSm3rh6fbPfew3+WidtWqlrHGvXtl0RBUl9QbQ+6'
                                       'EO7kWGIzZz15JgtEXAk1mX076wN0F9O2d2mkaDOI'
                                       'Q3EEPWFZ1mhcW/4dGW2tOnXdedwbkZp9hlnQUSiW'
                                       'o/M+au9x0k5/xtR1viyOKJ16Su2HUqak4q6oCxmP'
                                       'tAQG6ZyUy+e4C3lq8C4DUFB2T7y7oVA3iQrRVggF'
                                       'aBTv7j51k855DbNl7yK8YnZGSyPRJ42TVqDIacVt'
                                       'ajzBDbSC13fzPoqN5aiLZADXp6QQ7vo5lDtiMTXD'
                                       'x6ZojLdfmejsrPz/EbeMv7DQNRp1/CLba7XxVtBe'
                                       'b4MBmb/2xNAnUmBuoMVn8vF1bcnp25ck7byAjJVF'
                                       'WjUq93t8AQxhWZxatpXvAEKUY51kQgufN30bZyQY'
                                       'maXy73X86G3h1wQ4K8rtyYV5Gp2hQKhVo1KqWkwy'
                                       'Px8s7q9Z3eJ0eXdJ4cPy19OoaeuMXLgG1QLs9+H2'
                                       'deGwnOQcMVYqJtQd8ffQqkr6pYpImmaJsFUNmXYZ'
                                       'CAS6Xh6df2EhjU3i70XAQ74TD4VStielvr+Dhl9+'
                                       'j8IeSgDPiSBAbVijPFrBhcbtDdkRFinQPeBadhrw'
                                       '+unWH9pnRjrnejlarYvnz4+jbO5UH7i7g78tKKK9'
                                       'oZNYr38ve+xcKg05HfaM8fXanak38beU61m3fx/R'
                                       'J4+iSmhTxmuJaYCjPFqxk4xEEVInypgTQkRwwVEd'
                                       'MJxpgs+E9sXYCAI89uw5z0UkApk4Z0rLrfei+Qez'
                                       'aW0VxSRXrNv3Cqi8OM2FsxxpYw0HsAa+4JI9u6Sk'
                                       'Y9DoMWg0GvRaDzvejUatQq5TYHS4sNoFTNSaOlFWy'
                                       '+/Bxv4aEIycqmbnoY+Y9dgdJxsiaEgJCaygPeDYaY'
                                       'EgPGOUcsK23azY8gFVfHGbzr8Y3uCCLO29pPUNVKh'
                                       'W8NPNqJt6/Gkujg3nztzHkkizOz5anqBsK8WnIDSM'
                                       'Gkp/Tq0NrWAU7ywu38sWW3S1jlafNLFuzhYdvGR2R'
                                       'PqVocxHKAwY7NXFbrWiC3Bspkg1QoQyeLkYjQQ1ldM'
                                       '1UVDXy6gJfh7Nep2LWr42qbcnqmsAzU4fx3NzNCHY302'
                                       'dt4l+LxqJWR+9FQPF5sFUInuS3t8YDN40k0ahnxTdF'
                                       'LeMbdx1g8u9+g04bvhlI3VyE8oDRQLIBCidOREVAW8QhN'
                                       'hRzXivCZvMlxQ/fP4hePYLnRzeM7st3RScp3FDKoZ/rWLR0D'
                                       '48+MFhe0W0Qh2DBHn5b/cRrh7F224+crm8EwOlyc6C0nEH9eoe9'
                                       'ZsB7ISFCsEKt9hWt3a2pQLRqgZLcgUcQqPn446D/p+veXTYxT6yd0K'
                                       '7xffnNUbZuLwfggpy0ds96n338ctJSfZ/opR/+yP6DtfKIDYI4B'
                                       'FvDaMlqRqVScrGoM6ai1hz2etCx8kpnlWICDNAjCNQVFmLZuZPG'
                                       'PXuo/ugjdo8ciVBaGnSBhILOO3Gob7C3hF6FAmY+Nbzds96UZB3TH'
                                       'xsGgNvtZeZLm3E63WecEy5yhOC2JBlFZZMIe/MC6oBneDOus96'
                                       'iCwjBR6dN49SiRZIX6BqkeyJaLHx3d8vLRRPG5lGQ31XSvDHX9qFwQ'
                                       'ykbt5RxvKye9z7cx5RJl8iuT84QDFBjavC7Fnddd5RzwgPWrl4teXLa'
                                       'qFEkDx0qq6BQHD1uZuXnhwDISDfw2JQhHZo/44nLSUr0/QLf+6CEiqp'
                                       'G2TXKGYJNDU3sOugfdbp3iay5QmoOCKAQNSl0Sg7oMptxVFRImqjv04'
                                       'd+opfVo8lfF+7A7fadCjz96FCSk3TtzPCnS4aRpx/1fVgEu5uX39wmu'
                                       '0a5QrDd4eSVZZ/javNapkGnpf/5PSLSpxSdV5/JqzkqK/2uxQYpF/4h'
                                       'WKn0JVftvFmdMXYseQsXBnRNRJMFr0RWAwMYd30u466P3vehiDtihDC'
                                       '6on/8+QSLP1nPiWr/Av/oYQMi7o6WWoiuKyzE09TkN6bNyoro2aHwM0'
                                       'B1cjIXrVhB+YIFWA8dwmO14nW5UKemYsjNJXn4cDInTCBpcPRKGecy4'
                                       'pfTpbRkWaw2SstrOHC8nK0lhymrDHwJKSMlkTuuGx6xvoBNiMgDCmVl'
                                       'mNau5diMGf7zDAYSBw6M+PnBCNiEZI4fT+b48VF52P86ep1/Dlh6qpp'
                                       'FK9ehVCnxuD04XG4EuwOLTaChyUatyUJTO2E6IyWR2Q/eEvEGBAI9oG'
                                       'n9er7PysJtteIN0RkD0H3y5KCNq3IQ/3o2GRH3BJotVr7+oSTs9S7s3'
                                       'YMn77yBzDR5XqoSb0K8Tme7He3G/Hz6zJ4ty/ODETdAGZGjHUuhgPyc'
                                       'Xoy7ajDD8uXNV0O9mBRKSObEieQtXBiVJoRm4gYoI+IQLAW1SkmPzDT'
                                       '69swiP6cXg/r1lr0TuuVZqanosrNRGo0o9XpURiNKg6H133o9mi5d0Pfp'
                                       'Q/qYMZ3y3Y+K+B8rlJdGm0B1XQNmSxM2hxO7w4nX6/W9qadSotGoMWg1J'
                                       'CUYSE9OjJqxnSv8F+dSq/gtNDGfAAAAAElFTkSuQmCC')"""
    print "captcha_id: ", captcha_id
    time.sleep(2)

    try:
        captcha = client.get_solved_captcha(captcha_id)
        print "captcha: ", captcha
    except CaptchaException as e:
        print "e.code", e.code