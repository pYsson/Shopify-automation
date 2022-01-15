import requests
import webhook
from discord_webhook import DiscordWebhook, DiscordEmbed
from playsound import playsound
import json
import pprint
import urllib3
from colorama import init, Fore, Back, Style
import time
from bs4 import BeautifulSoup as soup
import random
from urllib import parse
from termcolor import colored
import sys

# headers
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"}

global pf

def profile_extract(p):
  global pf
  
  path = 'profile/' + str(p)
  with open(path, 'r') as f:
    pf = json.load(f)
    email = pf['email']
    fname = pf['fname']
    lname = pf['lname']
    add1 = pf['add1']
    add2 = pf['add2']
    city = pf['city']
    province = pf['province']
    postal_code = pf['postal_code']
    phone = pf['phone']
    country = pf['country']
    cardholder = pf['card']['cardholder']
    card_number = pf['card']['card_number']
    exp_m = pf['card']['exp_m']
    exp_y = pf['card']['exp_y']
    cvv = pf['card']['cvv']

def carting(index, session, site, variant, proxy):
    cart_url = "https://" + site + "/cart/add.js?quantity=1&id=" + str(variant)
    r = session.get(cart_url, verify=False)
    print("Task [" + index + "] \tAdding to Cart")
    return r
  
def fill_customer_info(index, session, checkout_url):
  payload = {
    "utf8": u"\u2713",
    "_method": "patch",
    "authenticity_token": "",
    "previous_step": "contact_information",
    "step": "shipping_method",
    "checkout[email_or_phone]": pf['email'],
    "checkout[buyer_accepts_marketing]": "0",
    "checkout[shipping_address][first_name]": pf['fname'],
    "checkout[shipping_address][last_name]": pf['lname'],
    "checkout[shipping_address][company]": "",
    "checkout[shipping_address][address1]": pf['add1'],
    "checkout[shipping_address][address2]": pf['add2'],
    "checkout[shipping_address][city]": pf['city'],
    "checkout[shipping_address][country]": pf['country'],
    "checkout[shipping_address][province]": pf['province'],
    "checkout[shipping_address][zip]": pf['postal_code'],
    "checkout[shipping_address][phone]": pf['phone'],
    "checkout[remember_me]": "0",
    "checkout[client_details][browser_width]": str(random.randint(1000, 2000)),
    "checkout[client_details][browser_height]": str(random.randint(1000, 2000)),
    "checkout[client_details][browser_tz]": "420",
    "checkout[client_details][color_depth]": "30",
    "checkout[client_details][javascript_enabled]": "1",
    "button": ""
  }
  print("Task [" + index + "] \tSubmitting Info")

  return session.post(checkout_url, data=payload, allow_redirects=True, headers=headers)  

def submit_shipping(index, session, checkout_url, shipping_option):
  payload = {
    "utf8": u'\u2713',
    "_method": "patch",
    "previous_step": "shipping_method",
    "step": "payment_method",
    "checkout[shipping_rate][id]": shipping_option,
    "g-recaptcha-repsonse": "",
    "button": ""
  }
  print("Task [" + index + "] \tSubmitting Shipping")

  return session.post(checkout_url, data=payload, allow_redirects=True)

def preload_payment(session):
  link = "https://deposit.us.shopifycs.com/sessions"
  
  payload = {
    "credit_card": {
      "number": pf['card']['cardholder'],
      "name": pf['card']['card_number'],
      "month": pf['card']['exp_m'],
      "year": pf['card']['exp_y'],
      "verification_value": pf['card']['cvv']
    }
  }
  r = session.post(link, json=payload, verify=False)

  return json.loads(r.text)["id"]

def submit_payment(index, session, checkout_url, payment_token, payment_gateway, authenticity_token):
  payload = {
    "utf8": u'\u2713',
    "_method": "patch",
    "previous_step": "payment_method",
    "step": "",
    "s": payment_token,
    "authenticity_token": authenticity_token,
    "checkout[payment_gateway]": payment_gateway,
    "checkout[different_billing_address]": "false",
    'checkout[credit_card][vault]': 'false',
    "complete": "1",
    "checkout[client_details][browser_width]": '979',
    "checkout[client_details][browser_height]": '631',
    "checkout[client_details][javascript_enabled]": "1",
    "g-recaptcha-repsonse": "",
    "button": ""
  }
  print("Task [" + index + "] \tSubmitting Payment")
  r = session.post(checkout_url, data=payload, verify=False, allow_redirects=True)
  return r

def startTask(numOfTask, site, variant, proxy, p):
  profile_extract(p)
  time.sleep(3)
  
  global index
  index = str(numOfTask)
  session = requests.session()
  session.proxies = proxy
  urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

  response = carting(index, session, site, variant, proxy)
  
  # product in cart now
  checkout_link = "https://" + site + "/checkout"
  response = session.get(checkout_link, verify=False)
  
  queue_time = 1
  while True:
      checkout_url = response.url
      if 'stock_problems' in response.url:
          print("Task [" + index + "] \tOut of Stock")
          time.sleep(3)
      elif 'queue' in response.url:
          eTime = ""
          bs = soup(response.text, "html.parser")
          eTime = bs.find('p', {"id":"estimatedWaitTime"})
          eTime = eTime.get_text()
          eTime = eTime.strip()
          print(colored("Task [" + index + "] \tIn Queue [" + str(eTime) + "]", "white"))
          time.sleep(1)
          queue_time += 1
      else:
          print(colored("Task [" + index + "] \tPassed Queue", "blue"))
          info_response = fill_customer_info(index, session, checkout_url)
          response = session.get(info_response.url, verify=False)
          break
  
  while True:
    try:
      sr_url = checkout_url + "?previous_step=contact_information&step=shipping_method"
      res = session.get(sr_url, verify=False)
      bs = soup(res.text, "html.parser")
      shipping_rate = bs.find('div', {"class":"radio-wrapper"})['data-shipping-method']
      shipping_rate = parse.quote(shipping_rate)
      shipping_rate = str(shipping_rate)
      shipping_response = submit_shipping(index, session, checkout_url, shipping_rate)
      break
    except:
      print(colored("Task [" + index + "] \tRetreiving Shipping", 'red'))
      time.sleep(2)
  payment_token = preload_payment(session)
  
  url = checkout_url + "?step=payment_method"
  res = session.get(url, verify=False)
  
  bs = soup(res.text, "html.parser")
  
  authenticity_token = bs.find('input', {"name":"authenticity_token"})['value']
  
  radio_input = bs.find('input', {"name": "checkout[payment_gateway]"})
  
  payment_gateway = radio_input["value"]

  while True:
    try:
      payment_response = submit_payment(index, session, checkout_url, payment_token, payment_gateway, authenticity_token)
    
      print("Task [" + index + "] \tChecking Order")
    
      order_url = payment_response.url
      order_url = order_url.replace("checkouts", "orders")
      order_url = order_url.replace("/processing", "")
      
      result = session.get(payment_response.url, verify=False)
      
      bs = soup(result.text, "html.parser")
      prdt_name = bs.find('span', {"class": "product__description__name order-summary__emphasis"})
      prdt_name = prdt_name.get_text()
      
      prdt_size = bs.find('span', {"class": "product__description__variant order-summary__small-text"})
      prdt_size = prdt_size.get_text()
      
      imgLink = bs.find('img', {"class": "product-thumbnail__image"})
      imgLink = imgLink["src"]
      imgLink = "https:" + imgLink

      price_t = bs.find('span', {"class": "order-summary__emphasis total-recap__final-price skeleton-while-loading"})
      price_t = price_t.get_text()

      orderNumber = bs.find('span', {"class": "os-order-number"})
      orderNumber = orderNumber.get_text()
      orderNumber = orderNumber.replace("Order", "")
      orderNumber = orderNumber.replace(" ", "")  
      
      print(colored("Task [" + index + "] \tCheckout Successful", 'green'))
      playsound('sound/success.wav')

      webhook.main(site, result, imgLink, prdt_name, price_t, prdt_size, pf['email'])
      break
    except:
      bs = soup(result.text, "html.parser")
      prdt_name = bs.find('span', {"class": "product__description__name order-summary__emphasis"})
      prdt_name = prdt_name.get_text()
      
      prdt_size = bs.find('span', {"class": "product__description__variant order-summary__small-text"})
      prdt_size = prdt_size.get_text()
      
      imgLink = bs.find('img', {"class": "product-thumbnail__image"})
      imgLink = imgLink["src"]
      imgLink = "https:" + imgLink
      
      price_t = bs.find('span', {"class": "order-summary__emphasis total-recap__final-price skeleton-while-loading"})
      price_t = price_t.get_text()
      
      print(colored("Task [" + index + "] \tRetreiving Payment", 'red'))
      time.sleep(3)