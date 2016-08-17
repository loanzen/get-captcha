# get-captcha

  Get Captcha text from the image using real intelligence, not artificial intelligence.

  It's a lightweight api client for 2captcha APIs


## how to install

```bash
   $ pip install -e git+git@github.com:loanzen/get-captcha.git#egg=captcha
```


## how to use

### submit captcha

```python

   from captcha import CaptchaClient

   c = CaptchaClient(`<your 2captcha api key>`)

   c.submit_captcha(`<path of the captcha image>`)

```


### get solved captcha

```python

   c.get_solved_captcha(`<api key>`, `<captcha id received from submit captcha request>`)

```


## TODO

- Add the other method of submitting captcha, i.e. with-b64encode image