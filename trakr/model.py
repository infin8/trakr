# -*- coding: utf-8 -*-
#db.clicks.create_index('campaign')
from collections import defaultdict
from database import db, ObjectId
from datetime import datetime

def _campaign_summary(id=None):
    spec = {'campaign':{'$exists':True}}
    exclude =  {'_id':False, 'campaign':True, 'leads':True}
    
    if id: spec['id'] = id
    
    return generate_summary(db.clicks.find(spec, exclude))

def generate_summary(clicks):
    campaigns = defaultdict(lambda: defaultdict(int))
    for click in clicks:
        id = click['campaign']
        campaign = campaigns.get(id) or get_campaign(id)
        campaign['clicks'] += 1
        campaign['leads'] += click.get('leads', 0)
        
        campaigns[id] = campaign
    
    return campaigns.values()

def get_campaign(id=''):
    spec = {'id':id}
    exclude =  {'_id':False}
    
    campaign = db.campaigns.find_one(spec, exclude) if id else None
    
    if campaign: return campaign
    
    campaign = dict(
        id = id,
        name = '',
        payout = 0,
        error = 0,
        clicks = 0,
        leads = 0,
        cpc = 0,
    )
    
    return save_campaign(campaign)

def save_campaign(campaign):
    #todo: sanitize data
    db.campaigns.update({
        'id': campaign['id'],
    }, {
        '$set': campaign
    }, upsert=True)
    
    return campaign
    
def record_click(query={}, ip='', useragent=''):
    query['land_time'] = datetime.utcnow()
    query['ip'] = ip
    query['ua'] = useragent
    
    return str(db.clicks.save(query))

def record_clickthrough(cid, url=''):
    db.clicks.update(
            {'_id': ObjectId(cid), 
            'outbound':{'$exists': False},
            'click_time':{'$exists': False}}, 
            {'$set':{
                'outbound': url,
                'click_time': datetime.utcnow()
            }},
        )

def record_lead(cid):
    try:
        db.clicks.update({'_id':ObjectId(cid)}, {'$set': {'leads': 1}})
        return True
    except:
        return False

def finalize(result, campaign):
    cpc = float(campaign['cpc'])
    payout = float(campaign['payout'])
    error = float(campaign['error'])
    
    result['id'] = campaign['id']
    result['cpc'] = cpc
    result['payout'] = payout
    result['error'] = error * 100
    result['clicks'] *= (1 + error)
    result['revenue'] = result['leads'] * payout
    result['epc'] = result['revenue'] / result['clicks']
    result['spend'] = result['clicks'] * cpc
    result['profit'] = result['revenue'] - result['spend']
    result['conversion'] = result['leads'] / result['clicks'] * 100
    result['roi'] = result['profit'] / result['spend'] \
        if result['spend'] > 0 else 0
    
    return result

def campaign_summary(campaign_id=None, groupby=None, error=0, fr=0, to=0):
    reduce = """
        function(obj,result){
            result.clicks++;
            if(obj.leads){
                result.leads += obj.leads;
            }
        }
    """
    
    exclude = { 'campaign': 1 }
    condition = {'click_time': {'$gte': datetime.fromtimestamp(fr), 
                                '$lte': datetime.fromtimestamp(to)}}
    
    if groupby:
        exclude[groupby] = 1
    
    if campaign_id:
        condition['campaign'] = str(campaign_id)

    results = generate_results(db.clicks.group(exclude, condition=condition,
                         reduce=reduce, initial={'clicks' : 0,'leads': 0}))
    
    return sorted(results, key=lambda x: x['profit'], reverse=True)

def generate_results(clicks):
    campaigns = {}
    
    for click in clicks:
        id = click['campaign']
        campaign = campaigns.get(id) or get_campaign(id)
        
        yield finalize(click, campaign)
        
        campaigns[id] = campaign