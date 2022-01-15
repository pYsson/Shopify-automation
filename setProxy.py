def setProxies():
  proxies = []

  p = open('proxies.txt', 'r')
  
  while True:
    line = p.readline()
    if not line: break
    line = line.strip()
    proxy = line.split(':')
    a = "http://" + proxy[2] + ":" + proxy[3] + "@" + proxy[0] + ":" + proxy[1] + "/"
    b = "https://" + proxy[2] + ":" + proxy[3] + "@" + proxy[0] + ":" + proxy[1] + "/"
    proxy = {
      "http": a,
      "https": b
    }
    proxies.append(proxy)
    
  p.close()

  return proxies