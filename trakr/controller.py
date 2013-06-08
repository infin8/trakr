import bottle, static, auth, json, model

@bottle.route('/lp')
def lander(*args, **kwargs):
    bottle.response.content_type = 'application/javascript'
    
    cid = bottle.request.cookies.cid
    
    if not cid:
        cid = model.record_click(
            dict(bottle.request.params),
            useragent = bottle.request.environ.get('HTTP_USER_AGENT'),
            ip = get_addr()
        )

        bottle.response.set_cookie('cid', cid)

    return 'var cid="%s";' % cid

@bottle.route('/ct')
def clickthrough(*args, **kwargs):
    bottle.response.content_type = 'application/javascript'
    
    cid = bottle.request.params.get('cid') or bottle.request.cookies.cid
    
    url = bottle.request.params.get('url')
    if url.endswith('='): url += cid
    
    yield 'document.location.replace("%s");' % url
    
    if cid: model.record_clickthrough(cid, bottle.request.query.url)
        

@bottle.route('/dashboard', apply=[auth.authenticated])
def dashboard(user=None, *args, **kwargs):
    url = bottle.url('/rest', method='campaign_summary', payout=2.05,
                      cpc=.035)
    return static.dashboard % {'url': url}

@bottle.get('/login')
def login_form(*args, **kwargs):
    return auth.login_form

@bottle.post('/login')
def login_post(*args, **kwargs):
    if auth.login():
        bottle.redirect('/dashboard')
        
    bottle.redirect('/login')

@bottle.route('/rest', apply=[auth.authenticated])
def rest(user=None, payout=0, cpc=0, *args, **kwargs): 
    bottle.response.content_type = 'application/json'
    summary = model.campaign_summary()
    return json.dumps(summary)

@bottle.route('/pb', method=['GET','POST'])
def postback():
    yield ''
    
    subid = bottle.request.params.get('subid','')
    cid = subid[:24]
    
    if len(cid) == 24: model.record_lead(cid)

@bottle.route('/save_campaign', method=['GET','POST'])
def save_campaign():
    yield ''
    
    model.save_campaign(dict(bottle.request.params))


@bottle.route('/js')
def js():
    bottle.response.content_type = 'application/javascript'
    
    lp = bottle.urljoin(bottle.request.url, bottle.url('/lp'))
    ct = bottle.urljoin(bottle.request.url, bottle.url('/ct'))
    
    return static.trackingjs % {'lp':lp, 'ct':ct}

def get_addr(*args, **kwargs):
    addr = bottle.request.environ.get('HTTP_X_FORWARDED_FOR')

    if addr:
        return addr.split(',')[-1].strip()

    return bottle.request.environ.get('REMOTE_ADDR')
    
if __name__ == '__main__':
    bottle.run(host='localhost', port=8101, debug=True, reloader=True)