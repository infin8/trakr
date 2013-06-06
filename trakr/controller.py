import bottle, static, auth, json
from database import db, ObjectId
from datetime import datetime
from collections import defaultdict

@bottle.route('/lp')
def lander(*args, **kwargs):
    bottle.response.content_type = 'application/javascript'
    
    cid = bottle.request.cookies.cid
    
    if not cid:
        query = dict(bottle.request.query)
        query['land_time'] = datetime.utcnow()
        query['ip'] = get_addr()
        query['ua'] = bottle.request.environ.get('HTTP_USER_AGENT')
        
        cid = str(db.clicks.save(query))
        bottle.response.set_cookie('cid', cid)

    return 'var cid="%s";' % cid

@bottle.route('/ct')
def clickthrough(*args, **kwargs):
    bottle.response.content_type = 'application/javascript'
    
    cid = bottle.request.query.cid or bottle.request.cookies.cid
    
    url = bottle.request.query.url
    if bottle.request.query.url.endswith('='): url += cid
    
    yield 'document.location.replace("%s");' % url
    
    if cid:
        db.clicks.update(
            {'_id': ObjectId(cid), 
            'outbound':{'$exists': False},
            'click_time':{'$exists': False}}, 
            {'$set':{
                'outbound': bottle.request.query.url,
                'click_time': datetime.utcnow()
            }},
        )

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
    
    spec = {'campaign':{'$exists':True}}
    d = defaultdict(lambda: defaultdict(int))
    
    for row in db.clicks.find(spec):
        d[row['campaign']]['id'] = row['campaign']
        d[row['campaign']]['name'] = row.get('name', '')
        d[row['campaign']]['clicks'] += 1
        d[row['campaign']]['leads'] += row.get('leads', 0)
    
    return json.dumps(d.values())

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